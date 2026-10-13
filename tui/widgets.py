"""
tui/widgets.py - Minimal curses widget toolkit for the Upwind TUI.

Provides: safe drawing helpers, text wrapping, a scrollable TextView,
Menu lists, stepper/text NumInputs, a FormScreen base for calculators,
and a ChecklistScreen. Zero dependencies beyond the standard library.
"""

import curses
import locale
import textwrap

# ---------------------------------------------------------------------------
# Unicode handling with ASCII fallback for non-UTF-8 terminals
# ---------------------------------------------------------------------------
try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    pass

USE_UNICODE = (locale.getpreferredencoding(False) or "").upper().replace("-", "") == "UTF8"

_ASCII_MAP = str.maketrans({
    "─": "-", "│": "|", "┌": "+", "┐": "+", "└": "+", "┘": "+",
    "═": "=", "║": "|", "╔": "+", "╗": "+", "╚": "+", "╝": "+",
    "├": "+", "┤": "+", "┬": "+", "┴": "+", "┼": "+",
    "┄": ":", "┈": ":", "·": ".", "•": "*",
    "█": "#", "▓": "%", "▒": "+", "░": ".",
    "▲": "^", "▼": "v", "◄": "<", "►": ">", "→": "->", "←": "<-",
    "↑": "^", "↓": "v", "➔": "->",
    "✓": "v", "✗": "x", "⚠": "!!", "●": "o", "○": "o", "°": " deg",
})


def u(s):
    """Translate a unicode-art string to ASCII when the locale demands it."""
    return s if USE_UNICODE else s.translate(_ASCII_MAP)


# ---------------------------------------------------------------------------
# Low-level drawing helpers
# ---------------------------------------------------------------------------
def put(scr, y, x, text, attr=0):
    """addstr that never crashes on edge overruns."""
    try:
        scr.addstr(y, x, text, attr)
    except curses.error:
        pass


def clip(s, w):
    return s if len(s) <= w else s[:max(0, w)]


def wrap_text(text, width):
    """Wrap a multi-paragraph string into single lines."""
    out = []
    for para in text.split("\n"):
        para = para.rstrip()
        if not para:
            out.append("")
            continue
        out.extend(textwrap.wrap(para, width))
    return out


def seg(text, style=None):
    """One styled run of text inside a line."""
    return (text, style)


def is_seg(x):
    """True if x is a single (text, style) segment rather than a whole line."""
    return isinstance(x, tuple) and len(x) == 2 and isinstance(x[0], str)


def _resolve(style, theme, default_attr):
    if style is None:
        return default_attr
    if callable(style):
        return style(theme)
    if isinstance(style, int):
        return style
    return theme.attr(style)


def norm_line(line, theme, default_attr):
    """
    Normalize one line into [(text, attr_int)].

    Accepts every shape the views produce:
      "plain text"                                  -> one run
      ("text", style)                               -> one styled run
      [("a", "green"), ("b", "amber")]              -> several runs
      ["plain", ("styled", "red")]                  -> mixed runs
      [[("nested", "red")]]                         -> flattened
    """
    if isinstance(line, str):
        return [(line, default_attr)]
    if is_seg(line):
        return [(line[0], _resolve(line[1], theme, default_attr))]
    out = []
    for item in line:
        if isinstance(item, str):
            out.append((item, default_attr))
        elif is_seg(item):
            out.append((item[0], _resolve(item[1], theme, default_attr)))
        elif isinstance(item, (list, tuple)):
            out.extend(norm_line(item, theme, default_attr))
        elif item is not None:
            out.append((str(item), default_attr))
    return out


def draw_lines(scr, y, x, w, lines, theme, default_attr=0):
    """Draw styled lines; returns the row just past the block."""
    for i, line in enumerate(lines):
        if y + i >= curses.LINES:
            break
        cx = x
        for text, a in norm_line(line, theme, default_attr):
            if cx - x >= w:
                break
            text = clip(text, w - (cx - x))
            put(scr, y + i, cx, text, a)
            cx += len(text)
    return y + len(lines)


def draw_box(scr, x, y, w, h, attr, title=None):
    """Draw a box outline; title sits on the top border."""
    if w < 2 or h < 2:
        return
    top = u("┌") + u("─" * (w - 2)) + u("┐")
    put(scr, y, x, top, attr)
    if title:
        put(scr, y, x + 2, " " + clip(title, w - 4) + " ", attr | curses.A_BOLD)
    for r in range(y + 1, y + h - 1):
        put(scr, r, x, u("│"), attr)
        put(scr, r, x + w - 1, u("│"), attr)
    put(scr, y + h - 1, x, u("└") + u("─" * (w - 2)) + u("┘"), attr)


def bar(value, lo, hi, width, filled=None, empty=None):
    """Horizontal meter made of block glyphs."""
    filled = filled or u("█")
    empty = empty or u("·")
    frac = 0.0 if hi == lo else (value - lo) / (hi - lo)
    frac = min(1.0, max(0.0, frac))
    n = int(round(frac * width))
    return filled * n + empty * (width - n)


def progress_bar(pct, width):
    n = int(round(pct / 100.0 * width))
    return u("█" * n) + u("░" * (width - n))


# ---------------------------------------------------------------------------
# Screen base class
# ---------------------------------------------------------------------------
class Screen:
    """A content-pane view. The app owns focus/global keys."""

    def __init__(self, app):
        self.app = app
        self.cursor = None  # (y, x) absolute terminal coords, or None

    def on_enter(self):
        pass

    def draw(self, scr, x, y, w, h):
        raise NotImplementedError

    def key(self, ch):
        """Handle a key; return True if consumed."""
        return False


# ---------------------------------------------------------------------------
# Scrollable text view
# ---------------------------------------------------------------------------
class TextView(Screen):
    def __init__(self, app, title, subtitle="", body=""):
        super().__init__(app)
        self.title = title
        self.subtitle = subtitle
        self.body = body
        self.offset = 0

    def set_content(self, title, body, subtitle=None):
        self.title = title
        self.body = body
        if subtitle is not None:
            self.subtitle = subtitle
        self.offset = 0

    def _lines(self, w):
        lines = []
        inner = w - 6
        lines.append(seg("STUDY MODULE", lambda t: t.attr("accent", bold=True)))
        lines.append(seg(self.title, lambda t: t.attr("card_title", bold=True)))
        lines.append("")
        for ln in wrap_text(self.body, inner):
            lines.append(ln)
        return lines

    def draw(self, scr, x, y, w, h):
        theme = self.app.theme
        card_h = h - 2
        draw_box(scr, x + 1, y, w - 2, card_h, theme.attr("muted"))
        # card background fill
        bg = theme.attr("card")
        for r in range(y + 1, y + card_h - 1):
            put(scr, r, x + 2, " " * (w - 4), bg)
        lines = self._lines(w - 4)
        visible = card_h - 2
        self.offset = max(0, min(self.offset, max(0, len(lines) - visible)))
        draw_lines(scr, y + 1, x + 3, w - 6, lines[self.offset:self.offset + visible],
                   self.app.theme, self.app.theme.attr("card"))
        # scrollbar
        if len(lines) > visible:
            sb_h = visible - 2
            thumb = max(1, int(visible / len(lines) * sb_h))
            pos = int(self.offset / (len(lines) - visible) * (sb_h - thumb)) if sb_h > thumb else 0
            col = x + w - 3
            for i in range(sb_h):
                ch = u("█") if pos <= i < pos + thumb else u("│")
                put(scr, y + 1 + i, col, ch, self.app.theme.attr("muted"))
        self._hint(scr, y + card_h - 1, x + 2, w)

    def _hint(self, scr, r, x, w):
        put(scr, r, x, u(" ↑/↓ PgUp/PgDn scroll · Esc back"), self.app.theme.attr("muted"))

    def key(self, ch):
        h = self.app.content_height()
        if ch in (curses.KEY_UP, ord("k")):
            self.offset -= 1
        elif ch in (curses.KEY_DOWN, ord("j")):
            self.offset += 1
        elif ch in (curses.KEY_PPAGE,):
            self.offset -= max(1, h - 4)
        elif ch in (curses.KEY_NPAGE,):
            self.offset += max(1, h - 4)
        elif ch == curses.KEY_HOME:
            self.offset = 0
        elif ch == curses.KEY_END:
            self.offset = 10 ** 9
        else:
            return False
        return True


# ---------------------------------------------------------------------------
# Menu (sidebar and content menus)
# ---------------------------------------------------------------------------
class Menu:
    """
    items: list of tuples:
      ("section", label)          non-selectable header
      ("item", label, callback)   selectable
      ("cta", label, callback)    highlighted action
    """

    def __init__(self, items):
        self.items = items
        self.sel = self._first_selectable(1)

    def _first_selectable(self, start=0):
        for i in range(start, len(self.items)):
            if self.items[i][0] in ("item", "cta"):
                return i
        return 0

    def _move(self, delta):
        i = self.sel
        n = len(self.items)
        for _ in range(n):
            i = (i + delta) % n
            if self.items[i][0] in ("item", "cta"):
                self.sel = i
                return

    def activate(self):
        item = self.items[self.sel]
        if item[0] in ("item", "cta"):
            item[2]()
            return True
        return False

    def key(self, ch):
        if ch in (curses.KEY_UP, ord("k")):
            self._move(-1)
        elif ch in (curses.KEY_DOWN, ord("j")):
            self._move(1)
        elif ch in (curses.KEY_PPAGE,):
            for _ in range(8):
                self._move(-1)
        elif ch in (curses.KEY_NPAGE,):
            for _ in range(8):
                self._move(1)
        elif ch == curses.KEY_HOME:
            self.sel = self._first_selectable()
        elif ch == curses.KEY_END:
            self.sel = self._first_selectable(len(self.items) - 1)
            self._move(0)
            for _ in range(len(self.items)):
                j = (self.sel + 1) % len(self.items)
                if self.items[j][0] in ("item", "cta"):
                    self.sel = j
                else:
                    break
        elif ch in (curses.KEY_ENTER, 10, 13, curses.KEY_RIGHT):
            return self.activate()
        else:
            return False
        return True

    def draw(self, scr, x, y, w, h, theme, focused):
        """Draw with simple scrolling to fit h rows."""
        # scroll window so selection is visible
        top = 0
        if self.sel >= h:
            top = self.sel - h // 2
        visible = self.items[top:top + h]
        for i, item in enumerate(visible):
            r = y + i
            kind = item[0]
            label = item[1]
            if kind == "section":
                put(scr, r, x, clip(" " + label.upper(), w), theme.attr("side_hdr", bold=True))
            elif kind == "cta":
                a = theme.attr("cta", bold=True) if focused else theme.attr("cta")
                put(scr, r, x, clip(label, w), a)
            else:
                is_sel = (top + i == self.sel)
                if is_sel and focused:
                    a = theme.attr("side_sel", bold=True)
                    put(scr, r, x, " " * w, a)
                    put(scr, r, x, clip(" " + label, w), a)
                elif is_sel:
                    put(scr, r, x, clip(" " + label, w), theme.attr("side_hover", bold=True))
                else:
                    put(scr, r, x, clip(" " + label, w), theme.attr("side"))


# ---------------------------------------------------------------------------
# Numeric stepper / typed input
# ---------------------------------------------------------------------------
class NumInput:
    def __init__(self, label, lo, hi, step, value, fmt="{}"):
        self.label = label
        self.lo, self.hi, self.step = lo, hi, step
        self.value = float(value)
        self.fmt = fmt
        self.editing = False
        self.buffer = ""

    def clamp(self, v):
        return max(self.lo, min(self.hi, v))

    def adjust(self, delta):
        self.editing = False
        self.value = self.clamp(round(self.value + delta * self.step, 6))

    def display_value(self):
        v = self.value
        if self.step >= 1 and float(v).is_integer():
            return self.fmt.format(int(v))
        return self.fmt.format(v)

    def render(self, selected):
        val = self.buffer if self.editing else self.display_value()
        box = "[ " + val + " ]" if not selected else "[" + val + "]"
        return self.label, box

    def key(self, ch):
        """Handle a printable key while selected. Returns True if consumed."""
        if ch == curses.KEY_LEFT:
            self.adjust(-1)
            return True
        if ch == curses.KEY_RIGHT:
            self.adjust(1)
            return True
        if ch == curses.KEY_PPAGE:
            self.adjust(-10)
            return True
        if ch == curses.KEY_NPAGE:
            self.adjust(10)
            return True
        if 32 <= ch < 127 and (ch == 45 or ch == 46 or 48 <= ch <= 57):
            # start / continue typing a literal number
            if not self.editing:
                self.editing = True
                self.buffer = ""
            if len(self.buffer) < 8:
                self.buffer += chr(ch)
            return True
        if ch in (curses.KEY_BACKSPACE, 127, 8):
            if self.editing:
                self.buffer = self.buffer[:-1]
                if not self.buffer:
                    self.editing = False
            return True
        if ch in (curses.KEY_ENTER, 10, 13):
            if self.editing:
                try:
                    self.value = self.clamp(float(self.buffer))
                except ValueError:
                    pass
                self.editing = False
                self.buffer = ""
            return True
        return False

    @property
    def changed(self):
        return not self.editing


# ---------------------------------------------------------------------------
# Form screen for calculator tools
# ---------------------------------------------------------------------------
class FormScreen(Screen):
    """Subclasses define inputs + compute(); results/viz refresh live."""

    title = ""
    description = ""

    def __init__(self, app):
        super().__init__(app)
        self.inputs = []
        self.sel = 0
        self.build()

    def build(self):
        raise NotImplementedError

    def compute(self):
        """Return (status_lines, result_lines, viz_lines). Lines may be styled."""
        return [], [], []

    def draw(self, scr, x, y, w, h):
        theme = self.app.theme
        card_h = min(h - 2, 6 + 2 * len(self.inputs) + 2)
        draw_box(scr, x + 1, y, w - 2, card_h, theme.attr("border", ) if False else theme.attr("muted"))
        r = y + 1
        put(scr, r, x + 3, clip(self.title, w - 6), theme.attr("card_title", bold=True))
        r += 1
        for ln in wrap_text(self.description, w - 6)[:2]:
            put(scr, r, x + 3, clip(ln, w - 6), theme.attr("muted"))
            r += 1
        r += 1
        label_w = min(30, max(len(i.label) for i in self.inputs) + 2) if self.inputs else 20
        self.cursor = None
        for idx, inp in enumerate(self.inputs):
            selected = idx == self.sel
            label, box = inp.render(selected)
            a = theme.attr("input_sel") if selected else theme.attr("input")
            put(scr, r, x + 3, clip(label, label_w), theme.attr("white", bold=True))
            put(scr, r, x + 3 + label_w, box, a)
            if selected and isinstance(inp, NumInput) and inp.editing:
                self.cursor = (r, x + 3 + label_w + 1 + len(inp.buffer))
            r += 1
        put(scr, r, x + 3, "←/→ adjust · type number + Enter · ↑/↓ field · Esc back",
            theme.attr("muted"))

        status, results, viz = self.compute()
        r2 = y + card_h + 1
        if status:
            r2 = draw_lines(scr, r2, x + 3, w - 6, status, theme, theme.attr("white")) + 1
        if results:
            box_h = min(len(results) + 2, max(4, y + h - r2 - (len(viz) + 2 if viz else 0)))
            draw_box(scr, x + 1, r2, w - 2, box_h, theme.attr("accent"))
            r2 = draw_lines(scr, r2 + 1, x + 3, w - 6, results[:box_h - 2], theme, theme.attr("card"))
            r2 += 2
        if viz:
            draw_lines(scr, r2, x + 1, w - 2, viz, theme, theme.attr("card"))

    def key(self, ch):
        if ch in (curses.KEY_UP, ord("k")) and not self._editing():
            self.sel = (self.sel - 1) % len(self.inputs)
            return True
        if ch in (curses.KEY_DOWN, ord("j")) and not self._editing():
            self.sel = (self.sel + 1) % len(self.inputs)
            return True
        if self.inputs:
            consumed = self.inputs[self.sel].key(ch)
            return consumed
        return False

    def _editing(self):
        inp = self.inputs[self.sel] if self.inputs else None
        return isinstance(inp, NumInput) and inp.editing


# ---------------------------------------------------------------------------
# Checklist screen
# ---------------------------------------------------------------------------
class ChecklistScreen(Screen):
    def __init__(self, app, title, description, sections):
        super().__init__(app)
        self.title = title
        self.description = description
        self.sections = sections  # [(phase_title, [items])]
        self.checked = set()
        self.flat = [it for _, items in sections for it in items]
        self.sel = 0
        self.offset = 0

    def _rows(self):
        rows = []  # (kind, text, item_or_None)
        for phase, items in self.sections:
            rows.append(("section", phase, None))
            for it in items:
                rows.append(("item", it, it))
        return rows

    def draw(self, scr, x, y, w, h):
        theme = self.app.theme
        total = len(self.flat)
        done = len(self.checked)
        pct = int(done / total * 100) if total else 0
        card_h = h - 2
        draw_box(scr, x + 1, y, w - 2, card_h, theme.attr("muted"))
        r = y + 1
        put(scr, r, x + 3, clip(self.title, w - 6), theme.attr("card_title", bold=True))
        r += 1
        color = "green" if pct == 100 else "amber"
        put(scr, r, x + 3, f"Progress: {done} / {total} ({pct}%)", theme.attr(color, bold=True))
        put(scr, r, x + 3 + 24, progress_bar(pct, min(20, w - 30)), theme.attr(color))
        r += 2
        rows = self._rows()
        visible = card_h - (r - y) - 2
        self.offset = max(0, min(self.offset, max(0, len(rows) - visible)))
        if self.sel < self.offset:
            self.offset = self.sel
        elif self.sel >= self.offset + visible:
            self.offset = self.sel - visible + 1
        for i, (kind, text, item) in enumerate(rows[self.offset:self.offset + visible]):
            rr = r + i
            if kind == "section":
                put(scr, rr, x + 3, clip(text.upper(), w - 6), theme.attr("accent", bold=True))
            else:
                is_sel = (self.offset + i) == self.sel
                mark = u("[✓]") if item in self.checked else u("[ ]")
                a = theme.attr("green" if item in self.checked else "card")
                if is_sel:
                    put(scr, rr, x + 3, " " * (w - 6), theme.attr("side_sel"))
                    put(scr, rr, x + 3, mark + " " + clip(text, w - 12),
                        theme.attr("side_sel", bold=True))
                else:
                    put(scr, rr, x + 3, mark, a)
                    put(scr, rr, x + 3 + 5, clip(text, w - 12), a)
        put(scr, y + card_h - 1, x + 3,
            "↑/↓ move · Space toggle · x reset all · Esc back", theme.attr("muted"))

    def key(self, ch):
        rows = self._rows()
        if ch in (curses.KEY_UP, ord("k")):
            self.sel = max(0, self.sel - 1)
            while self.sel < len(rows) and rows[self.sel][0] == "section" and self.sel > 0:
                self.sel -= 1
        elif ch in (curses.KEY_DOWN, ord("j")):
            self.sel = min(len(rows) - 1, self.sel + 1)
            while self.sel < len(rows) - 1 and rows[self.sel][0] == "section":
                self.sel += 1
        elif ch == ord(" ") or ch in (curses.KEY_ENTER, 10, 13):
            if 0 <= self.sel < len(rows) and rows[self.sel][0] == "item":
                it = rows[self.sel][2]
                if it in self.checked:
                    self.checked.discard(it)
                else:
                    self.checked.add(it)
        elif ch == ord("x"):
            self.checked.clear()
        else:
            return False
        return True
