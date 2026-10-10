"""
views/diagrams.py - Canvas-drawn aeronautical charts and diagrams.
"""

import tkinter as tk
import math
import config

def draw_airspace_chart(canvas, c_w=750, c_h=520):
    canvas.delete("all")
    y_fl600, y_180, y_145 = 45, 75, 110
    y_b_sh1, y_b_sh2, y_1200, y_700, y_sfc = 200, 290, 360, 390, 440

    canvas.create_rectangle(0, y_fl600, c_w, y_180, fill=config.AIRSPACE_COLORS["class_a"], outline="")
    canvas.create_rectangle(0, y_180, c_w, y_sfc, fill=config.AIRSPACE_COLORS["class_e_main"], outline="")

    canvas.create_polygon(
        0, y_sfc, 160, y_sfc, 160, y_700, 320, y_700, 320, y_sfc,
        480, y_sfc, 480, y_1200, c_w, y_1200, c_w, y_sfc,
        fill=config.AIRSPACE_COLORS["class_g"], outline=""
    )
    canvas.create_line(0, y_sfc, c_w, y_sfc, width=2)

    def _cyl(xc, yt, yb, rad, dark, light):
        canvas.create_rectangle(xc - rad, yt, xc + rad, yb, fill=dark, outline="")
        canvas.create_rectangle(xc - rad / 2, yt, xc + rad / 2, yb, fill=light, outline="")
        canvas.create_oval(xc - rad, yt - 6, xc + rad, yt + 6, fill=dark, outline="#333333")
        canvas.create_oval(xc - rad + 4, yt - 4, xc + rad - 4, yt + 4, fill=light, outline="")

    _cyl(240, y_145, y_b_sh1, 85, config.AIRSPACE_COLORS["class_b_dark"], config.AIRSPACE_COLORS["class_b_light"])
    _cyl(240, y_b_sh1, y_b_sh2, 58, config.AIRSPACE_COLORS["class_b_dark"], config.AIRSPACE_COLORS["class_b_light"])
    _cyl(240, y_b_sh2, y_sfc, 30, config.AIRSPACE_COLORS["class_b_dark"], config.AIRSPACE_COLORS["class_b_light"])

    _cyl(420, 260, 320, 50, config.AIRSPACE_COLORS["class_c_dark"], config.AIRSPACE_COLORS["class_c_light"])
    _cyl(420, 320, y_sfc, 30, config.AIRSPACE_COLORS["class_c_dark"], config.AIRSPACE_COLORS["class_c_light"])

    _cyl(580, 290, y_sfc, 38, config.AIRSPACE_COLORS["class_d_dark"], config.AIRSPACE_COLORS["class_d_light"])

    canvas.create_text(375, y_fl600 + 15, text="CLASS A (IFR ONLY - 18,000' MSL to FL600)", font=("Helvetica", 11, "bold"), fill="#ffffff")
    canvas.create_text(240, y_145 + 30, text="CLASS B", font=("Helvetica", 11, "bold"), fill="#ffffff")
    canvas.create_text(420, 290, text="CLASS C", font=("Helvetica", 10, "bold"), fill="#ffffff")
    canvas.create_text(580, 320, text="CLASS D", font=("Helvetica", 10, "bold"), fill="#ffffff")
    canvas.create_text(370, y_700 + 15, text="CLASS G", font=("Helvetica", 10, "bold"), fill="#000000")
    canvas.create_text(530, y_1200 + 15, text="CLASS G", font=("Helvetica", 10, "bold"), fill="#000000")

    canvas.create_text(30, y_fl600 + 15, text="FL 600\n18,000'", font=("Helvetica", 8, "bold"), fill="#ffffff", anchor="w")
    canvas.create_text(30, y_145, text="14,500' MSL", font=("Helvetica", 8, "bold"), fill="#ffffff", anchor="w")
    canvas.create_text(150, y_700 - 8, text="700' AGL", font=("Helvetica", 8, "bold"), fill="#000000", anchor="e")
    canvas.create_text(470, y_1200 - 8, text="1,200' AGL", font=("Helvetica", 8, "bold"), fill="#000000", anchor="e")
    canvas.create_text(40, 480, text="AGL: Above Ground Level   |   MSL: Mean Sea Level   |   *Diagram Not to Exact Scale", font=("Helvetica", 9), fill="#333333", anchor="w")

def draw_traffic_pattern(canvas, c_w=760, c_h=480):
    canvas.delete("all")
    canvas.create_rectangle(0, 0, c_w, c_h, fill="#23272a", outline="")

    rwy_x1, rwy_y1, rwy_x2, rwy_y2 = 260, 225, 520, 255
    canvas.create_rectangle(rwy_x1, rwy_y1, rwy_x2, rwy_y2, fill="#40444b", outline="#ffffff", width=1)
    for x in range(rwy_x1 + 15, rwy_x2 - 15, 30):
        canvas.create_line(x, 240, x + 15, 240, fill="#ffffff", width=2)
    canvas.create_text(rwy_x2 - 25, 240, text="27", font=("Helvetica", 11, "bold"), fill="#ffffff")
    canvas.create_text(rwy_x1 + 25, 240, text="09", font=("Helvetica", 11, "bold"), fill="#ffffff")

    canvas.create_line(150, 40, 70, 40, arrow=tk.LAST, width=3, fill=config.ACCENT_COLOR)
    canvas.create_text(110, 25, text="WIND: 10 KTS", font=("Helvetica", 10, "bold"), fill=config.ACCENT_COLOR)

    pts = [(520, 240), (140, 240), (140, 350), (620, 350), (620, 240), (520, 240)]
    canvas.create_line(pts, fill=config.ACCENT_GREEN, width=3, dash=(6, 3), joinstyle=tk.ROUND)

    canvas.create_text(350, 370, text="DOWNWIND LEG (500' AGL Ultralight / 1,000' GA) ➔", font=("Helvetica", 9, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(650, 290, text="BASE LEG\n(Reduce Power)", font=("Helvetica", 9, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(190, 205, text="FINAL APPROACH ➔\n(Land Into Wind)", font=("Helvetica", 9, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(120, 290, text="CROSSWIND", font=("Helvetica", 9, "bold"), fill=config.ACCENT_GREEN)

    canvas.create_line(460, 440, 390, 350, arrow=tk.LAST, width=3, fill="#00b0f4")
    canvas.create_text(470, 420, text="45° Standard Entry", font=("Helvetica", 9, "bold"), fill="#00b0f4")

    canvas.create_line(620, 350, 670, 280, 600, 220, 520, 240, fill=config.ACCENT_RED, width=3, dash=(4, 4), arrow=tk.LAST)
    canvas.create_text(580, 160, text="⚠️ DEADLY SKIDDING TURN TRAP:\nOvershooting centerline ➔ Pilot pushes inside rudder\ninstead of banking ➔ Inside wing stalls ➔ SNAP ROLL & SPIN!",
                       font=("Helvetica", 9, "bold"), fill=config.ACCENT_RED, justify="center")

def draw_engine_gauges_comparative(canvas, c_w=760, c_h=480):
    """Visualizes both 2-Stroke and 4-Stroke instrument clusters side-by-side."""
    canvas.delete("all")
    canvas.create_rectangle(0, 0, c_w, c_h, fill="#1e2124", outline="")

    # 2-STROKE PANEL
    canvas.create_rectangle(20, 20, 365, 340, fill="#25282c", outline=config.BORDER_COLOR, width=2)
    canvas.create_text(192, 40, text="TWO-STROKE ENGINE ENVELOPE", font=("Helvetica", 11, "bold"), fill="#00b0f4")

    # EGT Dial
    canvas.create_oval(50, 65, 180, 195, fill="#2f3136", outline="#ffffff", width=2)
    canvas.create_text(115, 95, text="EGT", font=("Helvetica", 10, "bold"), fill="#ffffff")
    canvas.create_text(115, 125, text="1,150°F", font=("Helvetica", 14, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(115, 150, text="CRUISE", font=("Helvetica", 8, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(115, 215, text="Max 1,220°F\n(Lean burn meltdown)", font=("Helvetica", 8), fill=config.ACCENT_RED, justify="center")

    # CHT Dial
    canvas.create_oval(205, 65, 335, 195, fill="#2f3136", outline="#ffffff", width=2)
    canvas.create_text(270, 95, text="CHT", font=("Helvetica", 10, "bold"), fill="#ffffff")
    canvas.create_text(270, 125, text="300°F", font=("Helvetica", 14, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(270, 150, text="NORMAL", font=("Helvetica", 8, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(270, 215, text="Min 250°F Warmup\nMax 400°F Overheat", font=("Helvetica", 8), fill=config.ACCENT_AMBER, justify="center")

    canvas.create_text(192, 290, text="⚠️ Premix fuel carries lubrication!\nIdling on steep descent starves bearings.",
                       font=("Helvetica", 9, "bold"), fill=config.ACCENT_AMBER, justify="center")

    # 4-STROKE PANEL (HALF-VW & V-TWINS)
    canvas.create_rectangle(395, 20, 740, 340, fill="#25282c", outline=config.BORDER_COLOR, width=2)
    canvas.create_text(567, 40, text="FOUR-STROKE ENVELOPE (HALF-VW)", font=("Helvetica", 11, "bold"), fill=config.ACCENT_GREEN)

    # Oil Pressure Dial
    canvas.create_oval(425, 65, 555, 195, fill="#2f3136", outline="#ffffff", width=2)
    canvas.create_text(490, 95, text="OIL PRESS", font=("Helvetica", 9, "bold"), fill="#ffffff")
    canvas.create_text(490, 125, text="35 PSI", font=("Helvetica", 14, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(490, 150, text="CRUISE", font=("Helvetica", 8, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(490, 215, text="Min 20 PSI\n(<15 PSI = Kill Engine)", font=("Helvetica", 8), fill=config.ACCENT_RED, justify="center")

    # Oil Temp Dial
    canvas.create_oval(580, 65, 710, 195, fill="#2f3136", outline="#ffffff", width=2)
    canvas.create_text(645, 95, text="OIL TEMP", font=("Helvetica", 9, "bold"), fill="#ffffff")
    canvas.create_text(645, 125, text="185°F", font=("Helvetica", 14, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(645, 150, text="OPTIMAL", font=("Helvetica", 8, "bold"), fill=config.ACCENT_GREEN)
    canvas.create_text(645, 215, text="Min 160°F Burnoff\nMax 220°F Redline", font=("Helvetica", 8), fill=config.ACCENT_AMBER, justify="center")

    canvas.create_text(567, 290, text="✓ Sump oil pump protects on descent.\nRequires 0.006\" cold valve lash checks.",
                       font=("Helvetica", 9, "bold"), fill=config.ACCENT_GREEN, justify="center")

    # Bottom Banner
    canvas.create_rectangle(20, 360, 740, 455, fill="#292b2f", outline=config.BORDER_COLOR)
    canvas.create_text(380, 385, text="CRITICAL WEIGHT & OPERATING COMPARISON:", font=("Helvetica", 10, "bold"), fill="#ffffff")
    canvas.create_text(380, 420, text="Two-strokes (Rotax 447): ~60 lbs installed | Thirsty, low endurance, requires premix oil & throttle blipping.\nFour-strokes (Half-VW / V-Twin): ~82–92 lbs installed | Clean fuel burn, oil pressure protection, high torque, but eats 25+ lbs of airframe budget!",
                       font=("Helvetica", 9), fill=config.TEXT_MUTED, justify="center")

def draw_carb_icing_matrix(canvas, c_w=760, c_h=440):
    canvas.delete("all")
    ox, oy = 80, 380
    gw, gh = 620, 320

    # High Risk Zone
    canvas.create_polygon(
        ox + 80, oy - 140, ox + 450, oy - 140, ox + 500, oy - 280, ox + 120, oy - 280,
        fill="#a92a34", outline=""
    )
    # Moderate Risk Zone
    canvas.create_polygon(
        ox + 160, oy - 200, ox + 400, oy - 200, ox + 430, oy - 280, ox + 190, oy - 280,
        fill="#faa61a", outline=""
    )

    canvas.create_line(ox, oy, ox + gw, oy, width=2, fill="#ffffff")
    canvas.create_line(ox, oy, ox, oy - gh, width=2, fill="#ffffff")

    for t in range(20, 110, 10):
        x = ox + (t - 20) * (gw / 80.0)
        canvas.create_line(x, oy, x, oy + 5, fill="#8e9297")
        canvas.create_text(x, oy + 16, text=f"{t}°", font=("Helvetica", 8), fill="#8e9297")
    canvas.create_text(ox + gw / 2, oy + 35, text="OUTSIDE AIR TEMPERATURE (°F)", font=("Helvetica", 9, "bold"), fill="#ffffff")

    for rh in range(0, 110, 20):
        y = oy - rh * (gh / 100.0)
        canvas.create_line(ox - 5, y, ox, y, fill="#8e9297")
        canvas.create_text(ox - 24, y, text=f"{rh}%", font=("Helvetica", 8), fill="#8e9297")
    canvas.create_text(ox - 45, oy - gh / 2, text="RELATIVE\nHUMIDITY", font=("Helvetica", 8, "bold"), fill="#ffffff")

    canvas.create_text(ox + 310, oy - 230, text="CRITICAL: ICING AT GLIDE / LOW POWER", font=("Helvetica", 9, "bold"), fill="#ffffff")
    canvas.create_text(ox + 300, oy - 260, text="SEVERE ICING AT CRUISE", font=("Helvetica", 9, "bold"), fill="#202225")

    canvas.create_rectangle(60, 400, c_w - 60, 435, fill="#292b2f", outline=config.ACCENT_AMBER)
    canvas.create_text(c_w / 2, 418, text="💡 PRECAUTION: Venturi pressure drop drops temperature up to 40°F! Apply carb heat before descending in humid air.",
                       font=("Helvetica", 9, "bold"), fill=config.ACCENT_AMBER)

def draw_load_factor_diagram(canvas, c_w=760, c_h=460):
    """Draws Bank Angle vs. Load Factor (G) and Stall Speed multiplier curve."""
    canvas.delete("all")
    ox, oy = 90, 360
    gw, gh = 600, 280

    # Danger background zone (>60 deg bank)
    x_60 = ox + (60.0 / 75.0) * gw
    canvas.create_rectangle(x_60, oy - gh, ox + gw, oy, fill="#362225", outline="")
    canvas.create_text(x_60 + 55, oy - gh + 20, text="DANGER ZONE\n(STRUCTURAL &\nSTALL HAZARD)", font=("Helvetica", 8, "bold"), fill=config.ACCENT_RED, justify="center")

    # Axes
    canvas.create_line(ox, oy, ox + gw, oy, width=2, fill="#ffffff")
    canvas.create_line(ox, oy, ox, oy - gh, width=2, fill="#ffffff")

    # X-Axis: Bank Angle (0 to 75 deg)
    for deg in range(0, 80, 15):
        x = ox + (deg / 75.0) * gw
        canvas.create_line(x, oy, x, oy + 5, fill="#8e9297")
        canvas.create_text(x, oy + 16, text=f"{deg}°", font=("Helvetica", 9, "bold"), fill="#ffffff")
    canvas.create_text(ox + gw / 2, oy + 38, text="BANK ANGLE (DEGREES)", font=("Helvetica", 10, "bold"), fill="#ffffff")

    # Y-Axis: Load Factor (1.0 to 4.0 G)
    for g_val in [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]:
        y = oy - ((g_val - 1.0) / 3.0) * gh
        canvas.create_line(ox - 5, y, ox, y, fill="#8e9297")
        canvas.create_text(ox - 24, y, text=f"{g_val:.1f} G", font=("Helvetica", 8), fill="#8e9297")
    canvas.create_text(ox - 50, oy - gh / 2, text="LOAD\nFACTOR\n(G)", font=("Helvetica", 9, "bold"), fill="#ffffff", justify="center")

    # Plot G-Load Curve n = 1 / cos(theta)
    curve_pts = []
    for deg in range(0, 76):
        rad = math.radians(deg)
        g = 1.0 / math.cos(rad)
        if g <= 4.0:
            x = ox + (deg / 75.0) * gw
            y = oy - ((g - 1.0) / 3.0) * gh
            curve_pts.append((x, y))

    flat_pts = [c for pt in curve_pts for c in pt]
    canvas.create_line(flat_pts, fill=config.ACCENT_COLOR, width=4)

    # Key callouts
    callouts = [
        (30, 1.15, "+7% Stall Speed", config.ACCENT_GREEN),
        (45, 1.41, "+19% Stall Speed", config.ACCENT_AMBER),
        (60, 2.00, "+41% Stall Speed (2.0 G)", config.ACCENT_RED),
        (70, 2.92, "+71% Stall Speed (2.9 G)", config.ACCENT_RED)
    ]
    for deg, g, desc, col in callouts:
        x = ox + (deg / 75.0) * gw
        y = oy - ((g - 1.0) / 3.0) * gh
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=col, outline="#ffffff")
        canvas.create_text(x, y - 14, text=f"{deg}°: {desc}", font=("Helvetica", 8, "bold"), fill=col)

    # Summary box
    canvas.create_rectangle(50, 400, c_w - 50, 445, fill="#292b2f", outline=config.BORDER_COLOR)
    canvas.create_text(c_w / 2, 422, text="⚠️ STALL SPEED FORMULA: Vs(banked) = Vs(level) × √(Load Factor).\nAt 60° bank, a 24-knot stall speed spikes to 34 knots! Never execute steep turns when slow on base or final.",
                       font=("Helvetica", 9, "bold"), fill=config.ACCENT_AMBER, justify="center")