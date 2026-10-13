"""
tui/diagrams.py - The five Upwind charts rebuilt as Unicode/ASCII terminal art.
Charts are generated programmatically (grids, meters, plots) so they stay
faithful to the data behind the original Tkinter canvases.
"""

import math
from tui.widgets import Screen, seg, draw_lines, draw_box, wrap_text, u, bar

# ---------------------------------------------------------------------------
# Scrollable pre-styled art screen
# ---------------------------------------------------------------------------
class ArtScreen(Screen):
    def __init__(self, app, title, lines):
        super().__init__(app)
        self.title = title
        self.lines = lines
        self.offset = 0

    def draw(self, scr, x, y, w, h):
        theme = self.app.theme
        visible = h - 2
        self.offset = max(0, min(self.offset, max(0, len(self.lines) - visible)))
        draw_box(scr, x + 1, y, w - 2, h - 1, theme.attr("muted"))
        put = _put
        put(scr, y, x + 3, " " + self.title + " ", theme.attr("card_title", bold=True))
        draw_lines(scr, y + 1, x + 2, w - 4, self.lines[self.offset:self.offset + visible],
                   theme, theme.attr("card"))
        put(scr, y + h - 2, x + 3, " ↑/↓ scroll · Esc back", theme.attr("muted"))

    def key(self, ch):
        import curses
        if ch in (curses.KEY_UP, ord("k")):
            self.offset -= 1
        elif ch in (curses.KEY_DOWN, ord("j")):
            self.offset += 1
        elif ch in (curses.KEY_PPAGE,):
            self.offset -= 10
        elif ch in (curses.KEY_NPAGE,):
            self.offset += 10
        elif ch == curses.KEY_HOME:
            self.offset = 0
        elif ch == curses.KEY_END:
            self.offset = 10 ** 9
        else:
            return False
        return True


from tui.widgets import put as _put


# ---------------------------------------------------------------------------
# 1. Airspace profile chart
# ---------------------------------------------------------------------------
def airspace_lines():
    GW, GH = 62, 16
    grid = [[seg(" ", "muted") for _ in range(GW)] for _ in range(GH)]

    def fill(r0, r1, c0, c1, ch, style):
        for r in range(r0, r1 + 1):
            for c in range(max(0, c0), min(GW, c1 + 1)):
                grid[r][c] = seg(ch, style)

    def label(r, c, text, style):
        for i, chx in enumerate(text):
            if 0 <= c + i < GW and 0 <= r < GH:
                grid[r][c + i] = seg(chx, style)

    fill(0, GH - 2, 0, GW - 1, u("·"), "as_e")                       # Class E
    fill(13, 14, 0, 12, u("░"), "as_g")                              # G 700'
    fill(12, 14, 27, 61, u("░"), "as_g")                             # G 1200'
    fill(1, 2, 0, GW - 1, u("█"), "as_a")                            # Class A
    fill(4, 6, 9, 31, u("▓"), "as_b")                                # B tiers
    fill(7, 9, 13, 27, u("▓"), "as_b")
    fill(10, 14, 16, 24, u("▓"), "as_b")
    fill(8, 10, 34, 40, u("▒"), "as_c")                              # C tiers
    fill(11, 14, 36, 39, u("▒"), "as_c")
    fill(10, 14, 45, 52, u("▓"), "as_d")                             # D

    label(1, 12, "CLASS A (IFR ONLY - 18,000' MSL to FL600)", "white")
    label(5, 16, "CLASS B", "white")
    label(9, 34, "CLASS C", "white")
    label(12, 45, "CLASS D", "white")
    label(13, 3, "CLASS G", "text_dark")
    label(13, 50, "CLASS G", "text_dark")

    ruler = {1: "FL600", 2: "18,000'", 3: "14,500'", 12: "1,200' AGL",
             13: "700' AGL", 15: "SFC"}
    lines = []
    for r in range(GH):
        row = [seg(f"{ruler.get(r, ''):>10} ", "muted")]
        row.extend(grid[r])
        lines.append(row)
    lines.append([seg(f"{'':>10} " + u("═" * GW), "white")])
    lines.append("")
    lines.append([seg(" LEGEND: ", "white"), seg("█ Class A", "as_a"), seg("  ▓ Class B", "as_b"),
                  seg("  ▒ Class C", "as_c"), seg("  ▓ Class D", "as_d"),
                  seg("  · Class E", "as_e"), seg("  ░ Class G", "as_g")])
    lines.append([seg(" AGL: Above Ground Level | MSL: Mean Sea Level | *Diagram Not to Exact Scale", "muted")])
    return lines


# ---------------------------------------------------------------------------
# 2. Traffic pattern & spin trap
# ---------------------------------------------------------------------------
def traffic_lines():
    d, s = u("┄"), u("┊")
    L = []
    L.append([seg(" WIND: 10 kts", "accent", )])
    L.append([seg(" " + u("◄") + u("─" * 8), "accent")])
    L.append([seg(" " + u("│"), "accent")])
    L.append([seg("   ┌" + d * 30 + "┐", "green")])
    L.append([seg("   " + s + "  UPWIND LEG" + " " * 17 + s, "green")])
    L.append([seg(u("   " + s + "  (enter 45 deg to downwind)       " + s + "  ╱ 45° ENTRY"), "blue")])
    L.append([seg("   " + s + u("  ╲") + " " * 25 + s, "green")])
    L.append([seg("   " + s + "  CROSSWIND" + " " * 18 + s, "green")])
    L.append([seg("   " + s + " " * 30 + s, "green")])
    L.append([seg("   " + s + "  DOWNWIND (500' AGL UL)" + " " * 5 + s, "green")])
    L.append([seg("   └" + d * 30 + "┘", "green")])
    L.append([seg("        ▲ BASE LEG (reduce power)", "green")])
    L.append([seg("   FINAL APPROACH " + u("➔") + " LAND INTO WIND", "green")])
    L.append([seg("   ┌════════════════════════════════════════════════════════════════════════┐", "muted")])
    L.append([seg("   ║ 09 - - - - - - - - - - - - - - - - - - - - - - - - - - 27  ║  RUNWAY", "white")])
    L.append([seg("   └════════════════════════════════════════════════════════════════════════┘", "muted")])
    L.append("")
    warn = ("⚠ DEADLY SKIDDING TURN TRAP: Overshooting centerline -> pilot pushes inside "
            "rudder instead of banking -> inside wing stalls -> SNAP ROLL & SPIN!")
    for ln in wrap_text(warn, 70):
        L.append([seg(" " + ln, "red", )])
    return L


# ---------------------------------------------------------------------------
# 3. 2-stroke vs 4-stroke gauge panels (meters instead of dials)
# ---------------------------------------------------------------------------
def _gauge(name, val_txt, frac, lo_txt, hi_txt, style):
    return [seg(f" {name:<10}", "white"), seg(f"{val_txt:>10}", style),
            seg("  [" + bar(frac * 100, 0, 100, 18) + "]", style)]


def engine_lines():
    L = []
    L.append([seg(" ┌──── TWO-STROKE ENGINE ENVELOPE ─────┐ ┌──── FOUR-STROKE (HALF-VW) ────┐", "muted")])
    L.append([seg(" │", "muted"), seg(" EGT 1,150 degF cruise", "green"), seg("            │ │", "muted"),
              seg(" OIL PRESS 35 PSI cruise", "green"), seg("        │", "muted")])
    L.append([seg(" │", "muted"), seg(" [" + bar(70, 0, 100, 18) + "]", "green"), seg("          │ │", "muted"),
              seg(" [" + bar(58, 0, 100, 18) + "]", "green"), seg("         │", "muted")])
    L.append([seg(" │  max 1,220 degF (lean burn meltdown)", "red"), seg("       │ │", "muted"),
              seg("  min 20 PSI (<15 PSI = KILL ENGINE)", "red"), seg("      │", "muted")])
    L.append([seg(" │", "muted"), seg(" CHT 300 degF normal", "green"), seg("              │ │", "muted"),
              seg(" OIL TEMP 185 degF optimal", "green"), seg("        │", "muted")])
    L.append([seg(" │", "muted"), seg(" [" + bar(55, 0, 100, 18) + "]", "green"), seg("          │ │", "muted"),
              seg(" [" + bar(62, 0, 100, 18) + "]", "green"), seg("         │", "muted")])
    L.append([seg(" │  min 250 degF warmup / max 400 overh", "amber"), seg("      │ │", "muted"),
              seg("  min 160 burnoff / max 220 redline", "amber"), seg("      │", "muted")])
    L.append([seg(" └─────────────────────────────────────┘ └────────────────────────────────┘", "muted")])
    L.append([seg(" !! Premix fuel carries lubrication! Idling on a steep descent starves bearings.", "amber")])
    L.append([seg(" v Sump oil pump protects on descent. Requires 0.006\" cold valve lash checks.", "green")])
    L.append("")
    L.append([seg(" CRITICAL WEIGHT & OPERATING COMPARISON:", "white")])
    L.append([seg("  Two-strokes (Rotax 447): ~60 lbs installed | Thirsty, low endurance,", "muted")])
    L.append([seg("  requires premix oil & throttle blipping.", "muted")])
    L.append([seg("  Four-strokes (Half-VW / V-Twin): ~82-92 lbs installed | Clean fuel burn,", "muted")])
    L.append([seg("  oil pressure protection, high torque, but eats 25+ lbs of airframe budget!", "muted")])
    return L


# ---------------------------------------------------------------------------
# 4. Carb icing probability matrix (point-in-polygon on the FAA zones)
# ---------------------------------------------------------------------------
_HIGH = [(30.3, 43.75), (78.1, 43.75), (84.5, 87.5), (35.5, 87.5)]
_MOD = [(40.6, 62.5), (71.6, 62.5), (75.5, 87.5), (44.5, 87.5)]


def _in_poly(pt, poly):
    x, y = pt
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def carb_icing_lines():
    L = []
    for rh in range(100, -1, -10):
        row = [seg(f" {rh:>3}% ", "muted")]
        for oat in range(20, 105, 5):
            if _in_poly((oat, rh), _HIGH):
                row.append(seg(u("█"), "red"))
            elif _in_poly((oat, rh), _MOD):
                row.append(seg(u("▒"), "amber"))
            else:
                row.append(seg(u("·"), "muted"))
        L.append(row)
    L.append([seg("      " + "".join(f"{t % 100:<3d}" if t < 100 else f"{t:<3d}"
                                     for t in range(20, 105, 5)), "muted")])
    L.append([seg("      OUTSIDE AIR TEMPERATURE (degF)", "white")])
    L.append([seg("      RELATIVE HUMIDITY runs 0-100% up the vertical axis", "muted")])
    L.append("")
    L.append([seg(" " + u("█") + " CRITICAL: ICING AT GLIDE / LOW POWER", "red")])
    L.append([seg(" " + u("▒") + " MODERATE RISK ZONE", "amber")])
    L.append([seg(" !! PRECAUTION: Venturi pressure drop drops temperature up to 40 degF!", "amber")])
    L.append([seg("    Apply carb heat before descending in humid air.", "amber")])
    return L


# ---------------------------------------------------------------------------
# 5. Bank angle vs load factor curve
# ---------------------------------------------------------------------------
def load_factor_lines():
    PW, PH = 60, 14
    grid = [[seg(" ", "muted") for _ in range(PW)] for _ in range(PH)]
    for c in range(int(60 / 75 * PW), PW):
        for r in range(PH):
            grid[r][c] = seg(u("░"), "red")
    for deg in range(0, 76):
        g = 1.0 / math.cos(math.radians(deg))
        if g <= 4.0:
            c = int(round(deg / 75 * (PW - 1)))
            r = PH - 1 - int(round((g - 1) / 3 * (PH - 1)))
            grid[r][c] = seg(u("●"), "accent")
    lines = []
    for r in range(PH):
        g_val = 1 + (PH - 1 - r) / (PH - 1) * 3
        row = [seg(f" {g_val:>4.1f}G ", "muted")]
        row.extend(grid[r])
        lines.append(row)
    lines.append([seg("       " + "".join(f"{d:<7d}" for d in range(0, 76, 15)), "muted")])
    lines.append([seg("       BANK ANGLE (DEGREES)          " + u("░") + " = DANGER ZONE (>60 deg)", "white")])
    lines.append("")
    lines.append([seg("  30 deg: 1.15 G  +7%  stall speed", "green")])
    lines.append([seg("  45 deg: 1.41 G  +19% stall speed", "amber")])
    lines.append([seg("  60 deg: 2.00 G  +41% stall speed", "red")])
    lines.append([seg("  70 deg: 2.92 G  +71% stall speed", "red")])
    lines.append("")
    for ln in wrap_text("!! STALL SPEED FORMULA: Vs(banked) = Vs(level) x sqrt(Load Factor). "
                        "At 60 deg bank, a 24-knot stall speed spikes to 34 knots! Never execute "
                        "steep turns when slow on base or final.", 70):
        lines.append([seg(" " + ln, "amber")])
    return lines


# ---------------------------------------------------------------------------
# Registry used by the app
# ---------------------------------------------------------------------------
def build_diagram_screens(app):
    return {
        "Airspace Visual Chart": lambda: ArtScreen(app, "U.S. Airspace Classes at a Glance", airspace_lines()),
        "Traffic Pattern & Spin Trap": lambda: ArtScreen(app, "Traffic Pattern & Spin Trap", traffic_lines()),
        "2-Stroke vs 4-Stroke Gauges": lambda: ArtScreen(app, "2-Stroke vs 4-Stroke Engine Gauges", engine_lines()),
        "Carb Icing Probability Matrix": lambda: ArtScreen(app, "Carb Icing Probability Matrix", carb_icing_lines()),
        "Bank Angle & G-Load Chart": lambda: ArtScreen(app, "Bank Angle & Load Factor (G-Load)", load_factor_lines()),
    }
