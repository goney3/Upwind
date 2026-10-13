"""
tui/theme.py - curses color system.

Maps the Upwind hex palette (config.py / Discord-style dark theme) onto the
best available terminal color mode: 256-color cube, 16-color ANSI, or mono.
"""

import curses

# ---------------------------------------------------------------------------
# Semantic palette (fg, bg). bg None => terminal default.
# ---------------------------------------------------------------------------
PALETTE = {
    "root":        ("#e6e6e6", "#18191c"),
    "header":      ("#ffffff", "#202225"),
    "muted_hdr":   ("#b9bbbe", "#202225"),
    "badge":       ("#3ba55d", "#292b2f"),
    "side":        ("#b9bbbe", "#202225"),
    "side_hdr":    ("#8e9297", "#202225"),
    "side_hover":  ("#ffffff", "#292b2f"),
    "side_sel":    ("#ffffff", "#5865f2"),
    "cta":         ("#ffffff", "#5865f2"),
    "card":        ("#dcddde", "#36393f"),
    "card_title":  ("#ffffff", "#36393f"),
    "card_dark":   ("#dcddde", "#292b2f"),
    "footer":      ("#8e9297", "#202225"),
    "input":       ("#ffffff", "#292b2f"),
    "input_sel":   ("#ffffff", "#5865f2"),
    "muted":       ("#b9bbbe", None),
    "accent":      ("#5865f2", None),
    "green":       ("#3ba55d", None),
    "amber":       ("#faa61a", None),
    "red":         ("#ed4245", None),
    "blue":        ("#00b0f4", None),
    "white":       ("#ffffff", None),
    "text_dark":   ("#000000", None),
    # Airspace chart fills (fg color painted with block glyphs)
    "as_a":        ("#a92a34", None),
    "as_e":        ("#2a623d", None),
    "as_g":        ("#98c09f", None),
    "as_b":        ("#6c82c3", None),
    "as_c":        ("#b06ca6", None),
    "as_d":        ("#4fa5c4", None),
}

# xterm 6x6x6 cube channel levels and grayscale ramp start
_CUBE = (0, 95, 135, 175, 215, 255)
_ANSI16 = [
    (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0),
    (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
    (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0),
    (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255),
]


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _xterm256_index(rgb):
    """Nearest index in the fixed xterm 256-color palette."""
    r, g, b = rgb
    best, best_d = None, None
    for ri in range(6):
        for gi in range(6):
            for bi in range(6):
                d = ((r - _CUBE[ri]) ** 2 + (g - _CUBE[gi]) ** 2 +
                     (b - _CUBE[bi]) ** 2)
                if best_d is None or d < best_d:
                    best_d, best = d, 16 + 36 * ri + 6 * gi + bi
    # grayscale ramp 232..255 (levels 8, 18, ... 238)
    lum = (r + g + b) / 3.0
    for i in range(24):
        lv = 8 + 10 * i
        d = (r - lv) ** 2 + (g - lv) ** 2 + (b - lv) ** 2
        if d < best_d:
            best_d, best = d, 232 + i
    return best


def _ansi16_index(rgb):
    best, best_d = 7, None
    for idx, c in enumerate(_ANSI16):
        d = sum((a - b) ** 2 for a, b in zip(rgb, c))
        if best_d is None or d < best_d:
            best_d, best = d, idx
    return best


class Theme:
    """Allocates and caches curses color pairs on demand."""

    def __init__(self):
        self.mode = "mono"          # 'mono' | 'ansi16' | 'xterm256'
        self._pair_ids = {}
        self._next_pair = 1
        self._attr_cache = {}

    def setup(self):
        curses.start_color()
        try:
            curses.use_default_colors()
            default_bg = -1
        except curses.error:
            default_bg = curses.COLOR_BLACK
        ncols = curses.COLORS
        if ncols >= 256:
            self.mode = "xterm256"
        elif ncols >= 8:
            self.mode = "ansi16"
        else:
            self.mode = "mono"
        self.default_bg = default_bg

    def _pair(self, fg_hex, bg_hex):
        key = (fg_hex, bg_hex)
        if key in self._pair_ids:
            return self._pair_ids[key]
        if self.mode == "mono":
            pid = 0
        else:
            fg_rgb, bg_rgb = hex_rgb(fg_hex), hex_rgb(bg_hex) if bg_hex else None
            if self.mode == "xterm256":
                fg = _xterm256_index(fg_rgb)
                bg = self.default_bg if bg_rgb is None else _xterm256_index(bg_rgb)
            else:
                fg = _ansi16_index(fg_rgb)
                bg = self.default_bg if bg_rgb is None else _ansi16_index(bg_rgb)
            pid = self._next_pair
            self._next_pair += 1
            try:
                curses.init_pair(pid, fg, bg)
            except curses.error:
                pid = 0
        self._pair_ids[key] = pid
        return pid

    def attr(self, name, bold=False, dim=False, reverse=False):
        """curses attribute for a semantic palette name."""
        key = (name, bold, dim, reverse)
        if key in self._attr_cache:
            return self._attr_cache[key]
        fg_hex, bg_hex = PALETTE.get(name, ("#ffffff", None))
        a = curses.color_pair(self._pair(fg_hex, bg_hex))
        if bold:
            a |= curses.A_BOLD
        if dim:
            a |= curses.A_DIM
        if reverse:
            a |= curses.A_REVERSE
        self._attr_cache[key] = a
        return a
