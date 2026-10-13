"""
tui/tools.py - The six Upwind flight tools rebuilt as curses forms with
stepper inputs, live recalculation, and ASCII visualizations.
"""

import math
import config
from tui.widgets import (FormScreen, ChecklistScreen, NumInput, seg, bar, u, put)

# ---------------------------------------------------------------------------
# Shared ASCII visualizations
# ---------------------------------------------------------------------------
def cg_art(cg, fwd=config.WB_FWD_LIMIT, aft=config.WB_AFT_LIMIT, cl=config.WB_CL_ARM, safe=True):
    lo, hi, W = config.WB_SCALE_MIN_IN, config.WB_SCALE_MAX_IN, 62
    col = lambda v: max(0, min(W - 1, int(round((v - lo) / (hi - lo) * (W - 1)))))
    beam = [seg(u("─"), "muted") for _ in range(W)]
    for c in range(col(fwd), col(aft) + 1):
        beam[c] = seg(u("▓"), "green")
    ruler = [" "] * W
    # limit labels are centred on their tick so they never collide with the
    # scale ends, and they follow whatever envelope the caller passes in
    for c, t in ((0, "25.0\""), (col(fwd) - 4, f"FWD {fwd:.1f}\""),
                 (col(aft) - 4, f"AFT {aft:.1f}\""), (W - 6, "32.0\"")):
        for i, chx in enumerate(t):
            if 0 <= c + i < W:
                ruler[c + i] = chx
    mark = [" "] * W
    mark[col(cl)] = u("┼")
    mark[col(cg)] = u("▲")
    style = "green" if safe else "red"
    return [
        [seg(" " + "".join(ruler), "muted")],
        [seg(" " + "".join(b[0] for b in beam), "muted")],
        [seg(" " + "".join(mark), style)],
        [seg(f" CG = {cg:.2f}\" ", style), seg(u("▲"), style),
         seg(f"   {u('┼')} Center of Lift {cl:.1f}\"", "blue")],
    ]


def compass_art(rwy_hdg, w_dir, w_spd):
    ROWS, COLS, CX, CY, R = 13, 42, 20, 6, 5.2
    grid = [[" "] * COLS for _ in range(ROWS)]
    sty = [["muted"] * COLS for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            dx, dy = (c - CX) / 2.0, r - CY
            d = math.hypot(dx, dy)
            if abs(d - R) < 0.45:
                grid[r][c] = u("·")
    for ang, lbl in ((0, "N"), (90, "E"), (180, "S"), (270, "W")):
        a = math.radians(ang)
        c = int(round(CX + (R + 1.2) * 2 * math.sin(a)))
        r = int(round(CY - (R + 1.2) * math.cos(a)))
        if 0 <= r < ROWS and 0 <= c < COLS:
            grid[r][c], sty[r][c] = lbl, "white"
    t = -4.6
    while t <= 4.6:
        a = math.radians(rwy_hdg)
        c = int(round(CX + t * 2 * math.sin(a)))
        r = int(round(CY - t * math.cos(a)))
        if 0 <= r < ROWS and 0 <= c < COLS:
            grid[r][c], sty[r][c] = u("█"), "side_hover"
        t += 0.35
    a = math.radians(w_dir)
    t = 0.8
    while t <= R:
        c = int(round(CX + t * 2 * math.sin(a)))
        r = int(round(CY - t * math.cos(a)))
        if 0 <= r < ROWS and 0 <= c < COLS:
            grid[r][c], sty[r][c] = u("░"), "blue"
        t += 0.35
    hc = int(round(CX + (R + 1.2) * 2 * math.sin(a)))
    hr = int(round(CY - (R + 1.2) * math.cos(a)))
    lines = []
    for r in range(ROWS):
        row = []
        run, run_style = "", None
        for c in range(COLS):
            if sty[r][c] != run_style:
                if run:
                    row.append(seg(run, run_style))
                run, run_style = "", sty[r][c]
            run += grid[r][c]
        if run:
            row.append(seg(run, run_style))
        lines.append(row)
    lines.append([seg(f" RWY {rwy_hdg:03d}  " + u("█") + " runway · WIND " + u("░") +
                      f" {int(w_spd)} kts from {w_dir:03d} deg", "muted")])
    return lines


# ---------------------------------------------------------------------------
# 1. Weight & Balance / CG
# ---------------------------------------------------------------------------
# Moment stations live in config.py so the Tkinter and curses front ends can
# never drift apart; the rationale for the numbers is documented there.
WB_EMPTY_ARM = config.WB_EMPTY_ARM
WB_PILOT_ARM = config.WB_PILOT_ARM
WB_FUEL_ARM = config.WB_FUEL_ARM
WB_BAGGAGE_ARM = config.WB_BAGGAGE_ARM
WB_CL_ARM = config.WB_CL_ARM
WB_FWD_LIMIT, WB_AFT_LIMIT = config.WB_FWD_LIMIT, config.WB_AFT_LIMIT
WB_FUEL_LB_PER_GAL = config.WB_FUEL_LB_PER_GAL
WB_MAX_BAGGAGE_LBS = config.WB_MAX_BAGGAGE_LBS


class WeightBalanceTool(FormScreen):
    title = "Weight & Balance: CG Envelope"
    description = ("In a 254-lb airframe a 200-lb pilot is ~44% of flight weight. "
                   "Fuel (arm 36\") and baggage (arm 52\") hang aft; the legal band is 3.0\" wide.")

    def build(self):
        self.inputs = [
            NumInput("Pilot Body Weight (lbs)", 100, 280, 1, 185),
            NumInput("Fuel Onboard (gal)", 0, 5, 0.5, 5),
            NumInput("Aft Equipment/Baggage (lbs)", 0, WB_MAX_BAGGAGE_LBS, 1, 10),
        ]

    def compute(self):
        p_wt = self.inputs[0].value
        f_wt = self.inputs[1].value * WB_FUEL_LB_PER_GAL
        b_wt = self.inputs[2].value
        empty_wt = config.MAX_EMPTY_WEIGHT_POWERED_LBS
        moment = (empty_wt * WB_EMPTY_ARM + p_wt * WB_PILOT_ARM +
                  f_wt * WB_FUEL_ARM + b_wt * WB_BAGGAGE_ARM)
        total = empty_wt + p_wt + f_wt + b_wt
        cg = moment / total
        fwd, aft = WB_FWD_LIMIT, WB_AFT_LIMIT
        safe = fwd <= cg <= aft
        if cg > aft:
            status = [[seg(f" !! DANGER: AFT CG VIOLATION ({cg:.2f}\")! Spin recovery impossible!", "red")]]
        elif cg < fwd:
            status = [[seg(f" !! DANGER: FORWARD CG ({cg:.2f}\")! Insufficient elevator to flare!", "amber")]]
        else:
            status = [[seg(f" v CG WITHIN SAFE ENVELOPE ({cg:.2f}\") - Total Weight: {int(total)} lbs", "green")]]
        results = [
            [seg(f" Total Moment: {int(moment)} in-lbs   Margin to limits: "
                 f"{cg - fwd:+.2f}\" fwd / {aft - cg:+.2f}\" aft")],
        ]
        return status, results, cg_art(cg, fwd, aft, cl=WB_CL_ARM, safe=safe)


# ---------------------------------------------------------------------------
# 2. Crosswind & Runway Compass
# ---------------------------------------------------------------------------
class CrosswindTool(FormScreen):
    title = "Crosswind Component & Runway Compass"
    description = ("Ultralights typically have 7-10 kt max crosswind limits. "
                   "Never land if the crosswind component exceeds your limit.")

    def build(self):
        self.inputs = [
            NumInput("Runway Number (x10 deg)", 1, 36, 1, 27),
            NumInput("Wind Direction (mag deg)", 0, 359, 1, 310),
            NumInput("Wind Speed (kts)", 0, 99, 1, 12),
        ]

    def compute(self):
        rwy_num = int(self.inputs[0].value)
        rwy_hdg = (rwy_num * 10) % 360
        w_dir = int(self.inputs[1].value) % 360
        w_spd = self.inputs[2].value
        diff = (w_dir - rwy_hdg + 180) % 360 - 180
        rad = math.radians(abs(diff))
        hw, xw = w_spd * math.cos(rad), w_spd * math.sin(rad)
        results = []
        if hw >= 0:
            results.append([seg(f" Headwind: {abs(int(hw))} kts", "green")])
        else:
            results.append([seg(f" !! TAILWIND HAZARD: {abs(int(hw))} kts!", "red")])
        side = "from Right" if diff > 0 else "from Left"
        results.append([seg(f" Crosswind Component: {abs(int(xw))} kts ({side})", "amber")])
        if abs(xw) > 9:
            results.append([seg(f" !! DANGER: Crosswind {abs(int(xw))} kts exceeds 8 kt ultralight limit! DO NOT FLY.", "red")])
        elif hw < 0:
            results.append([seg(" !! DANGER: Downwind landing! Use reciprocal runway into the wind.", "red")])
        else:
            results.append([seg(" v Conditions within typical safe ultralight envelope.", "green")])
        return [], results, compass_art(rwy_hdg, w_dir, w_spd)


# ---------------------------------------------------------------------------
# 3. Density Altitude & Fuel Endurance
# ---------------------------------------------------------------------------
class DensityAltTool(FormScreen):
    title = "Density Altitude & Fuel Endurance"
    description = ("Hot air kills climb performance. The 5-gallon fuel cap also makes "
                   "a 30-minute reserve mandatory planning.")

    def build(self):
        self.inputs = [
            NumInput("Airport Elevation (ft MSL)", 0, 10000, 50, 1500),
            NumInput("Ambient Air Temp (degF)", -20, 120, 1, 88),
            NumInput("Fuel Onboard (gal, max 5)", 0, 5, 0.5, 4.5),
            NumInput("Engine Burn Rate (GPH)", 0.5, 10, 0.1, 3.8),
        ]

    def compute(self):
        elev, temp = self.inputs[0].value, self.inputs[1].value
        fuel = min(5.0, self.inputs[2].value)
        burn = max(0.5, self.inputs[3].value)
        temp_c = (temp - 32.0) * 5.0 / 9.0
        std_c = 15.0 - (1.98 * elev / 1000.0)
        da = elev + 118.8 * (temp_c - std_c)
        roll = max(0, (da / 1000.0) * 11.5)
        usable = max(0.0, fuel - 0.5)
        end_min = int((usable / burn) * 60)
        safe_min = max(0, end_min - 30)
        results = [
            [seg(f" Density Altitude: {int(da):,} ft MSL", "white" if da < 3000 else "red")],
            [seg(f" Takeoff Ground Roll Penalty: +{int(roll)}% longer", "amber")],
            [seg(f" Total Fuel Endurance: {end_min // 60}h {end_min % 60}m")],
            [seg(f" Safe Cruising Radius: return to land within {safe_min} min!", "green")],
        ]
        viz = [[seg("  DA 0'   " + bar(da, 0, 8000, 40) + " 8,000'", "red" if da > 3000 else "green")]]
        return [], results, viz


# ---------------------------------------------------------------------------
# 4. Glide Cone / Forced Landing Footprint
# ---------------------------------------------------------------------------
class GlideConeTool(FormScreen):
    title = "Forced Landing Glide Cone & Wind Footprint"
    description = ("When the engine dies, altitude is your only currency. Slow 35-40 kt "
                   "glide speeds mean headwind compresses your reach drastically.")

    def build(self):
        self.inputs = [
            NumInput("Altitude Above Ground (ft AGL)", 100, 10000, 50, 1500),
            NumInput("Glide Ratio (L/D)", 3, 15, 0.5, 7.5),
            NumInput("Best Glide Airspeed (kts)", 20, 70, 1, 38),
            NumInput("Surface Wind Speed (kts)", 0, 40, 1, 12),
        ]

    def compute(self):
        alt, ld = self.inputs[0].value, self.inputs[1].value
        spd, wnd = self.inputs[2].value, self.inputs[3].value
        still = (alt * ld) / 5280.0
        hrs = still / spd
        head = max(5.0, spd - wnd) * hrs
        tail = (spd + wnd) * hrs
        tmin = hrs * 60.0
        results = [
            [seg(f" Still-Air Glide Radius: {still:.2f} SM ({int(alt * ld):,} ft)", "white")],
            [seg(f" !! Upwind Reach: {head:.2f} SM (-{int((1 - head/still)*100)}% shorter!)", "red")],
            [seg(f" v Downwind Reach: {tail:.2f} SM (+{int((tail/still - 1)*100)}% extra)", "green")],
            [seg(f" Time to Ground: {int(tmin)} min {int((tmin % 1) * 60)} sec (sink {int(alt/tmin)} fpm)", "blue")],
        ]
        viz = [
            [seg("  UPWIND  " + u("<") + bar(head, 0, 6, 20) + f" {head:.1f} SM", "red")],
            [seg("  DOWNWIND" + bar(tail, 0, 6, 20) + u(">") + f" {tail:.1f} SM", "green")],
        ]
        return [], results, viz


# ---------------------------------------------------------------------------
# 5. Propeller Tip Speed & PSRU
# ---------------------------------------------------------------------------
class PropTipSpeedTool(FormScreen):
    title = "Propeller Tip Speed & Drive Ratio"
    description = ("Tips above Mach 0.75 collapse efficiency. Direct-drive engines need "
                   "small props; big 54-60\" props need a reduction drive (PSRU).")

    def build(self):
        self.inputs = [
            NumInput("Propeller Diameter (in)", 36, 68, 1, 42),
            NumInput("Engine Operating RPM", 2000, 6500, 50, 3600),
            NumInput("Reduction Ratio (1.0=direct)", 1.0, 3.0, 0.1, 1.0),
        ]

    def compute(self):
        diam = self.inputs[0].value
        rpm = self.inputs[1].value
        ratio = max(0.5, self.inputs[2].value)
        prop_rpm = rpm / ratio
        tip_fps = (math.pi * diam * prop_rpm) / 720.0
        mach = tip_fps / 1116.4
        if mach < 0.65:
            st, ev = "green", " v OPTIMAL: subsonic flow, quiet, excellent thrust."
        elif mach <= 0.75:
            st, ev = "amber", " !! ACCEPTABLE BUT NOISY: compressibility drag rising at tips."
        else:
            st, ev = "red", " x DANGER TRANSONIC TIPS! Add a PSRU or shrink diameter!"
        results = [
            [seg(f" Prop Shaft RPM: {int(prop_rpm):,} (drive {ratio:.1f}:1)", "white")],
            [seg(f" Tip Velocity: {int(tip_fps)} ft/s ({int(tip_fps * 3600 / 5280)} mph)")],
            [seg(f" Tip Mach: {mach:.2f}", st)],
            [seg(ev, st)],
        ]
        viz = [[seg("  Mach 0   " + bar(mach * 100, 0, 100, 30) + " 1.0", st)]]
        return [], results, viz


# ---------------------------------------------------------------------------
# 6. Pre-Flight Checklist
# ---------------------------------------------------------------------------
CHECKLIST_SECTIONS = [
    ("COCKPIT & FLIGHT CONTROLS", [
        "Controls Free & Correct: stick left = left aileron up, stick back = elevator up",
        "Control Cables & Pulleys: no frayed strands, cables seated in grooves",
        "Restraint Harness: webbing undamaged, latch clicks firmly and locks",
        "Ballistic Parachute (BRS): SAFETY PIN REMOVED, activation handle clear",
    ]),
    ("POWERPLANT (2-STROKE & 4-STROKE)", [
        "4-Stroke Sump / 2-Stroke Premix: oil level verified, no crankcase leaks",
        "Engine Mounts: no hairline cracks in welded steel or aluminum tubes",
        "Exhaust System: retaining springs safety-wired, no cracks near manifold",
        "Spark Plug Caps: firmly seated with safety zip-ties / clips in place",
        "Reduction Belt / Gearbox: proper deflection tension, no gear oil leak",
    ]),
    ("PROPELLER (HIGH-STRESS COMPONENT)", [
        "Blades: no leading-edge nicks, stone chips, or delamination cracks",
        "Hub & Bolts: proper torque, safety wire intact, no tracking wobble",
    ]),
    ("FUEL SYSTEM (5-GALLON LIMIT)", [
        "Fuel Sump Drained: clear sample, ZERO water or ethanol phase separation",
        "Fuel Lines: no dry-rot cracking, hardening, or chafing on airframe tubes",
        "Fuel Cap: gasket seated, vented cap clear, firmly secured",
    ]),
    ("WINGS, STRUTS & RIGGING", [
        "Attachment Pins & Rings: all clevis pins locked with safety rings",
        "Sailcloth Integrity: Dacron firm, stitches intact, passes UV punch test",
        "Leading Edge & Ribs: no dented tubes, battens secured in trailing edge",
    ]),
    ("LANDING GEAR & FINAL WALKAROUND", [
        "Tire Inflation & Axles: properly inflated, no flat spots, axle nuts pinned",
        "Pusher Prop Clearance: ZERO loose articles that could blow into prop!",
    ]),
]


def build_tool_screens(app):
    from tui.widgets import ChecklistScreen
    return {
        "Weight & Balance / CG Tool": lambda: WeightBalanceTool(app),
        "Propeller Tip Speed & PSRU": lambda: PropTipSpeedTool(app),
        "Crosswind & Runway Compass": lambda: CrosswindTool(app),
        "Density Alt & Fuel Calc": lambda: DensityAltTool(app),
        "Glide Cone / Landing Reach": lambda: GlideConeTool(app),
        "Pre-Flight Checklist Tool": lambda: ChecklistScreen(
            app, "Ultralight Pre-Flight Inspection Checklist",
            "No FAA mechanic inspections exist for ultralights - your preflight is "
            "your only defense against structural or engine failure.",
            CHECKLIST_SECTIONS),
    }
