"""
views/tools.py - Interactive flight utility tools and performance calculators.
"""

import tkinter as tk
from tkinter import Frame, Label, Entry, Scale, Checkbutton, BooleanVar, Canvas, HORIZONTAL
import math
import config
from ui_components import ModernButton

class WeightBalanceTool:
    @staticmethod
    def render(parent):
        card = Frame(parent, bg=config.BG_CARD, padx=24, pady=18)
        card.pack(fill="x", padx=25, pady=(20, 10))

        Label(card, text="Ultralight Weight & Balance: Center of Gravity (CG) Envelope", font=config.FONT_TITLE,
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="In a 254-lb airframe, a 200-lb pilot accounts for ~44% of total flight weight! "
                        "An aft CG reduces elevator control authority, making stall and spin recovery aerodynamically impossible.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED, wraplength=720, justify="left").pack(anchor="w", pady=(4, 12))

        ctrl_frame = Frame(card, bg=config.BG_CARD)
        ctrl_frame.pack(fill="x", pady=5)

        Label(ctrl_frame, text="Pilot Body Weight (lbs):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=0, column=0, sticky="w", pady=4)
        pilot_slider = Scale(ctrl_frame, from_=100, to=280, orient=HORIZONTAL, bg=config.BG_CARD, fg="#ffffff", highlightthickness=0, length=240)
        pilot_slider.set(185)
        pilot_slider.grid(row=0, column=1, padx=10)

        Label(ctrl_frame, text="Fuel Onboard (Gallons):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=1, column=0, sticky="w", pady=4)
        fuel_slider = Scale(ctrl_frame, from_=0, to=5, resolution=0.5, orient=HORIZONTAL, bg=config.BG_CARD, fg="#ffffff", highlightthickness=0, length=240)
        fuel_slider.set(5.0)
        fuel_slider.grid(row=1, column=1, padx=10)

        Label(ctrl_frame, text="Aft Equipment / Baggage (lbs):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=2, column=0, sticky="w", pady=4)
        bag_slider = Scale(ctrl_frame, from_=0, to=30, orient=HORIZONTAL, bg=config.BG_CARD, fg="#ffffff", highlightthickness=0, length=240)
        bag_slider.set(5)
        bag_slider.grid(row=2, column=1, padx=10)

        c_w, c_h = 760, 240
        cg_canvas = Canvas(parent, width=c_w, height=c_h, bg="#1e2124", highlightthickness=0)
        cg_canvas.pack(padx=25, pady=10)

        status_lbl = Label(parent, text="", font=config.FONT_BODY_BOLD, bg=config.BG_CONTENT)
        status_lbl.pack(padx=25, pady=4)

        def _update_cg(*args):
            p_wt = pilot_slider.get()
            f_wt = fuel_slider.get() * 6.0
            b_wt = bag_slider.get()

            empty_wt, empty_arm = 254.0, 28.5
            p_arm, f_arm, b_arm = 25.0, 36.0, 42.0

            total_weight = empty_wt + p_wt + f_wt + b_wt
            total_moment = (empty_wt * empty_arm) + (p_wt * p_arm) + (f_wt * f_arm) + (b_wt * b_arm)
            cg = total_moment / total_weight

            fwd_limit, aft_limit = 26.5, 30.5
            cg_canvas.delete("all")

            beam_y = 120
            cg_canvas.create_rectangle(60, beam_y - 8, c_w - 60, beam_y + 8, fill="#40444b", outline="#ffffff")

            def _in_to_x(val):
                return 200 + (val - 25.0) * (360.0 / 7.0)

            x_fwd, x_aft = _in_to_x(fwd_limit), _in_to_x(aft_limit)
            cg_canvas.create_rectangle(x_fwd, beam_y - 18, x_aft, beam_y + 18, fill="#2a623d", outline=config.ACCENT_GREEN, width=2)
            cg_canvas.create_text((x_fwd + x_aft) / 2, beam_y, text="LEGAL SAFE CG ENVELOPE", font=("Helvetica", 9, "bold"), fill="#ffffff")

            cg_canvas.create_text(x_fwd, beam_y - 30, text=f"FWD LIMIT\n{fwd_limit}\"", font=("Helvetica", 8, "bold"), fill="#ffffff", justify="center")
            cg_canvas.create_text(x_aft, beam_y - 30, text=f"AFT LIMIT\n{aft_limit}\"", font=("Helvetica", 8, "bold"), fill="#ffffff", justify="center")

            cl_x = _in_to_x(28.5)
            cg_canvas.create_polygon(cl_x - 14, beam_y + 40, cl_x + 14, beam_y + 40, cl_x, beam_y + 10, fill="#00b0f4")
            cg_canvas.create_text(cl_x, beam_y + 55, text="Center of Lift (CL)", font=("Helvetica", 9, "bold"), fill="#00b0f4")

            cur_x = _in_to_x(cg)
            is_safe = fwd_limit <= cg <= aft_limit
            pin_color = config.ACCENT_GREEN if is_safe else config.ACCENT_RED

            cg_canvas.create_line(cur_x, beam_y - 60, cur_x, beam_y + 25, width=4, fill=pin_color)
            cg_canvas.create_oval(cur_x - 8, beam_y - 68, cur_x + 8, beam_y - 52, fill=pin_color, outline="#ffffff")
            cg_canvas.create_text(cur_x, beam_y - 80, text=f"ACTUAL CG: {cg:.2f}\"", font=("Helvetica", 11, "bold"), fill=pin_color)

            if cg > aft_limit:
                status_lbl.config(text=f"⚠️ DANGER: AFT CG VIOLATION ({cg:.2f}\")! Severe pitch instability — Spin recovery will be impossible!", fg=config.ACCENT_RED)
            elif cg < fwd_limit:
                status_lbl.config(text=f"⚠️ DANGER: FORWARD CG LIMIT EXCEEDED ({cg:.2f}\")! Heavy stick forces — Insufficient elevator to flare!", fg=config.ACCENT_AMBER)
            else:
                status_lbl.config(text=f"✓ CENTER OF GRAVITY WITHIN SAFE ENVELOPE ({cg:.2f}\") — Total Weight: {int(total_weight)} lbs", fg=config.ACCENT_GREEN)

        pilot_slider.config(command=_update_cg)
        fuel_slider.config(command=_update_cg)
        bag_slider.config(command=_update_cg)
        _update_cg()

class CrosswindTool:
    @staticmethod
    def render(parent):
        card = Frame(parent, bg=config.BG_CARD, padx=24, pady=16)
        card.pack(fill="x", padx=25, pady=(20, 10))

        Label(card, text="Crosswind Component & Runway Compass", font=config.FONT_TITLE,
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="Ultralights have large wing areas and slow landing speeds, giving them narrow crosswind limits (typically 7–10 knots max). "
                        "Never attempt landing if crosswind component exceeds your aircraft's demonstrated limit.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED, wraplength=720, justify="left").pack(anchor="w", pady=(4, 10))

        inputs_frame = Frame(card, bg=config.BG_CARD)
        inputs_frame.pack(fill="x", pady=4)

        Label(inputs_frame, text="Runway Number (e.g. 27 for 270°):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=0, column=0, sticky="w", pady=4)
        rwy_entry = Entry(inputs_frame, width=8, font=config.FONT_BODY)
        rwy_entry.insert(0, "27")
        rwy_entry.grid(row=0, column=1, padx=10, sticky="w")

        Label(inputs_frame, text="Wind Direction (Magnetic Degrees):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=1, column=0, sticky="w", pady=4)
        wind_dir_entry = Entry(inputs_frame, width=8, font=config.FONT_BODY)
        wind_dir_entry.insert(0, "310")
        wind_dir_entry.grid(row=1, column=1, padx=10, sticky="w")

        Label(inputs_frame, text="Wind Speed (Knots):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=2, column=0, sticky="w", pady=4)
        wind_spd_entry = Entry(inputs_frame, width=8, font=config.FONT_BODY)
        wind_spd_entry.insert(0, "12")
        wind_spd_entry.grid(row=2, column=1, padx=10, sticky="w")

        c_w, c_h = 760, 300
        cw_canvas = Canvas(parent, width=c_w, height=c_h, bg="#1e2124", highlightthickness=0)
        cw_canvas.pack(padx=25, pady=8)

        stats_card = Frame(parent, bg=config.BG_CARD, padx=20, pady=12)
        stats_card.pack(fill="x", padx=25, pady=4)

        hw_lbl = Label(stats_card, text="Headwind: —", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.ACCENT_GREEN)
        hw_lbl.pack(anchor="w")
        xw_lbl = Label(stats_card, text="Crosswind: —", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.ACCENT_AMBER)
        xw_lbl.pack(anchor="w")
        rec_lbl = Label(stats_card, text="Safety Assessment: —", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY)
        rec_lbl.pack(anchor="w", pady=(2, 0))

        def _do_calc():
            try:
                rwy_num = int(rwy_entry.get())
                rwy_hdg = (rwy_num * 10) % 360
                w_dir = int(wind_dir_entry.get()) % 360
                w_spd = float(wind_spd_entry.get())

                angle_diff = (w_dir - rwy_hdg + 180) % 360 - 180
                rad = math.radians(abs(angle_diff))
                headwind = w_spd * math.cos(rad)
                crosswind = w_spd * math.sin(rad)

                hw_text = f"Headwind: {abs(int(headwind))} kts" if headwind >= 0 else f"⚠️ TAILWIND HAZARD: {abs(int(headwind))} kts!"
                hw_lbl.config(text=hw_text, fg=config.ACCENT_GREEN if headwind >= 0 else config.ACCENT_RED)
                side = "from Right" if angle_diff > 0 else "from Left"
                xw_lbl.config(text=f"Crosswind Component: {abs(int(crosswind))} kts ({side})")

                if abs(crosswind) > 9:
                    rec_lbl.config(text=f"⚠️ DANGER: Crosswind ({abs(int(crosswind))} kts) exceeds ultralight safety limit (8 kts)! Do not fly.", fg=config.ACCENT_RED)
                elif headwind < 0:
                    rec_lbl.config(text="⚠️ DANGER: Downwind landing! Choose reciprocal runway to land into the wind.", fg=config.ACCENT_RED)
                else:
                    rec_lbl.config(text="✓ Conditions within typical safe ultralight crosswind envelope.", fg=config.ACCENT_GREEN)

                cw_canvas.delete("all")
                cx, cy, cr = 380, 150, 110
                cw_canvas.create_oval(cx - cr, cy - cr, cx + cr, cy + cr, outline="#40444b", width=2)
                for ang, lbl in [(0, "N"), (90, "E"), (180, "S"), (270, "W")]:
                    rad_c = math.radians(ang - 90)
                    cw_canvas.create_text(cx + (cr - 14) * math.cos(rad_c), cy + (cr - 14) * math.sin(rad_c),
                                          text=lbl, font=("Helvetica", 9, "bold"), fill="#8e9297")

                r_ang = math.radians(rwy_hdg - 90)
                rx1, ry1 = cx - (cr - 25) * math.cos(r_ang), cy - (cr - 25) * math.sin(r_ang)
                rx2, ry2 = cx + (cr - 25) * math.cos(r_ang), cy + (cr - 25) * math.sin(r_ang)
                cw_canvas.create_line(rx1, ry1, rx2, ry2, width=18, fill="#50545c")
                cw_canvas.create_line(rx1, ry1, rx2, ry2, width=2, fill="#ffffff", dash=(6, 4))
                cw_canvas.create_text(rx2, ry2, text=f"{rwy_num:02d}", font=("Helvetica", 9, "bold"), fill="#ffffff")

                w_ang = math.radians(w_dir - 90)
                wx1, wy1 = cx + (cr + 15) * math.cos(w_ang), cy + (cr + 15) * math.sin(w_ang)
                cw_canvas.create_line(wx1, wy1, cx, cy, width=4, fill="#00b0f4", arrow=tk.LAST)
                cw_canvas.create_text(wx1, wy1, text=f"WIND\n{int(w_spd)} kts", font=("Helvetica", 8, "bold"), fill="#00b0f4")
            except ValueError:
                rec_lbl.config(text="Please enter valid numerical inputs.")

        ModernButton(card, text="Calculate Wind Vector", command=_do_calc,
                     bg=config.ACCENT_COLOR, fg="#ffffff", hover_bg="#4752c4", font=("Helvetica", 10, "bold"),
                     padx=12, pady=6).pack(anchor="w", pady=(10, 0))
        _do_calc()

class DensityAltTool:
    @staticmethod
    def render(parent):
        card = Frame(parent, bg=config.BG_CARD, padx=24, pady=20)
        card.pack(fill="x", padx=25, pady=(20, 15))

        Label(card, text="Density Altitude & Fuel Endurance Calculator", font=config.FONT_TITLE,
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="Hot summer temperatures severely degrade ultralight climb and takeoff performance. "
                        "Additionally, strict 5-gallon fuel tanks require mandatory 30-minute reserve planning.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED, wraplength=720, justify="left").pack(anchor="w", pady=(4, 15))

        calc_form = Frame(card, bg=config.BG_CARD)
        calc_form.pack(fill="x")

        Label(calc_form, text="Airport Elevation (ft MSL):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=0, column=0, sticky="w", pady=4)
        elev_entry = Entry(calc_form, width=10, font=config.FONT_BODY)
        elev_entry.insert(0, "1500")
        elev_entry.grid(row=0, column=1, sticky="w", padx=10, pady=4)

        Label(calc_form, text="Ambient Air Temp (°F):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=1, column=0, sticky="w", pady=4)
        temp_entry = Entry(calc_form, width=10, font=config.FONT_BODY)
        temp_entry.insert(0, "88")
        temp_entry.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        Label(calc_form, text="Fuel Onboard (gal, max 5.0):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=2, column=0, sticky="w", pady=4)
        fuel_entry = Entry(calc_form, width=10, font=config.FONT_BODY)
        fuel_entry.insert(0, "4.5")
        fuel_entry.grid(row=2, column=1, sticky="w", padx=10, pady=4)

        Label(calc_form, text="Engine Burn Rate (GPH):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=3, column=0, sticky="w", pady=4)
        burn_entry = Entry(calc_form, width=10, font=config.FONT_BODY)
        burn_entry.insert(0, "3.8")
        burn_entry.grid(row=3, column=1, sticky="w", padx=10, pady=4)

        results_card = Frame(parent, bg=config.BG_CARD, padx=22, pady=18, highlightbackground=config.ACCENT_COLOR, highlightthickness=1)
        results_card.pack(fill="x", padx=25, pady=10)

        res_da = Label(results_card, text="Density Altitude: —", font=("Helvetica", 13, "bold"), bg=config.BG_CARD, fg=config.TEXT_PRIMARY)
        res_da.pack(anchor="w", pady=2)
        res_to = Label(results_card, text="Estimated Takeoff Roll Penalty: —", font=config.FONT_BODY, bg=config.BG_CARD, fg=config.ACCENT_AMBER)
        res_to.pack(anchor="w", pady=2)
        res_end = Label(results_card, text="Total Fuel Endurance: —", font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_PRIMARY)
        res_end.pack(anchor="w", pady=2)
        res_safe = Label(results_card, text="Safe Flight Window (with 30-min reserve): —", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.ACCENT_GREEN)
        res_safe.pack(anchor="w", pady=2)

        def _do_calc():
            try:
                elev = float(elev_entry.get())
                temp = float(temp_entry.get())
                fuel = min(5.0, float(fuel_entry.get()))
                burn = max(0.5, float(burn_entry.get()))

                temp_c = (temp - 32.0) * 5.0 / 9.0
                std_temp_c = 15.0 - (1.98 * elev / 1000.0)
                da = elev + 118.8 * (temp_c - std_temp_c)
                roll_pct = max(0, (da / 1000.0) * 11.5)

                usable_fuel = max(0.0, fuel - 0.5)
                endurance_mins = int((usable_fuel / burn) * 60)
                safe_mins = max(0, endurance_mins - 30)

                res_da.config(text=f"Calculated Density Altitude: {int(da):,} ft MSL")
                res_to.config(text=f"Takeoff Ground Roll Penalty: +{int(roll_pct)}% longer distance required!")
                res_end.config(text=f"Total Fuel Endurance: {endurance_mins // 60}h {endurance_mins % 60}m")
                res_safe.config(text=f"Safe Cruising Radius: Return to land within {safe_mins} minutes!")
            except ValueError:
                res_da.config(text="Please enter valid numbers.")

        calc_btn = ModernButton(card, text="Calculate Performance", command=_do_calc,
                                bg=config.ACCENT_COLOR, fg="#ffffff", hover_bg="#4752c4", font=("Helvetica", 11, "bold"),
                                padx=14, pady=8)
        calc_btn.pack(anchor="w", pady=(15, 0))
        _do_calc()

class GlideConeTool:
    """Calculates glide distance, duration, and downwind drift footprint during engine-out emergencies."""
    @staticmethod
    def render(parent):
        card = Frame(parent, bg=config.BG_CARD, padx=24, pady=18)
        card.pack(fill="x", padx=25, pady=(20, 10))

        Label(card, text="Forced Landing Glide Cone & Wind Footprint Calculator", font=config.FONT_TITLE,
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="When the engine dies, your altitude is your only currency. "
                        "Because ultralights have slow best glide speeds (35–40 kts), even a 10-knot headwind compresses your forward glide reach drastically!",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED, wraplength=720, justify="left").pack(anchor="w", pady=(4, 12))

        form = Frame(card, bg=config.BG_CARD)
        form.pack(fill="x")

        Label(form, text="Altitude Above Ground (ft AGL):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=0, column=0, sticky="w", pady=4)
        alt_entry = Entry(form, width=8, font=config.FONT_BODY)
        alt_entry.insert(0, "1500")
        alt_entry.grid(row=0, column=1, sticky="w", padx=10)

        Label(form, text="Glide Ratio (L/D, e.g. 7 for 7:1):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=1, column=0, sticky="w", pady=4)
        ld_entry = Entry(form, width=8, font=config.FONT_BODY)
        ld_entry.insert(0, "7.5")
        ld_entry.grid(row=1, column=1, sticky="w", padx=10)

        Label(form, text="Best Glide Airspeed (Knots):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=2, column=0, sticky="w", pady=4)
        speed_entry = Entry(form, width=8, font=config.FONT_BODY)
        speed_entry.insert(0, "38")
        speed_entry.grid(row=2, column=1, padx=10)

        Label(form, text="Surface Wind Speed (Knots):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=3, column=0, sticky="w", pady=4)
        wind_entry = Entry(form, width=8, font=config.FONT_BODY)
        wind_entry.insert(0, "12")
        wind_entry.grid(row=3, column=1, padx=10)

        res_box = Frame(parent, bg=config.BG_CARD, padx=22, pady=16, highlightbackground=config.ACCENT_AMBER, highlightthickness=1)
        res_box.pack(fill="x", padx=25, pady=10)

        res_still = Label(res_box, text="Still-Air Glide Range: —", font=("Helvetica", 12, "bold"), bg=config.BG_CARD, fg=config.TEXT_PRIMARY)
        res_still.pack(anchor="w")
        res_head = Label(res_box, text="Into Headwind Glide Range: —", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.ACCENT_RED)
        res_head.pack(anchor="w", pady=2)
        res_tail = Label(res_box, text="Downwind Glide Range: —", font=config.FONT_BODY, bg=config.BG_CARD, fg=config.ACCENT_GREEN)
        res_tail.pack(anchor="w", pady=2)
        res_time = Label(res_box, text="Time Available Until Impact: —", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg="#00b0f4")
        res_time.pack(anchor="w", pady=2)

        def _calc_glide():
            try:
                alt = float(alt_entry.get())
                ld = float(ld_entry.get())
                spd = float(speed_entry.get())
                wnd = float(wind_entry.get())

                still_dist_sm = (alt * ld) / 5280.0
                time_hrs = still_dist_sm / spd
                time_mins = time_hrs * 60.0

                head_gs = max(5.0, spd - wnd)
                head_dist_sm = head_gs * time_hrs

                tail_gs = spd + wnd
                tail_dist_sm = tail_gs * time_hrs

                res_still.config(text=f"Still-Air Glide Radius: {still_dist_sm:.2f} Statute Miles ({int(alt * ld):,} ft)")
                res_head.config(text=f"⚠️ Upwind Glide Reach: {head_dist_sm:.2f} SM (Penalty: -{int((1.0 - head_dist_sm/still_dist_sm)*100)}% shorter distance!)")
                res_tail.config(text=f"✓ Downwind Glide Reach: {tail_dist_sm:.2f} SM (+{int((tail_dist_sm/still_dist_sm - 1.0)*100)}% extra reach!)")
                res_time.config(text=f"⏱️ Descent Time to Ground: {int(time_mins)} min {int((time_mins % 1) * 60)} sec (Sink Rate: {int(alt/time_mins)} fpm)")
            except ValueError:
                res_still.config(text="Please enter valid numbers.")

        ModernButton(card, text="Compute Forced Landing Footprint", command=_calc_glide,
                     bg=config.ACCENT_COLOR, fg="#ffffff", hover_bg="#4752c4", font=("Helvetica", 10, "bold"),
                     padx=12, pady=6).pack(anchor="w", pady=(12, 0))
        _calc_glide()
        
class PropellerTipSpeedTool:
    """Calculates propeller tip speed, Mach number, and efficiency for Direct Drive & Reduction Drive setups."""
    @staticmethod
    def render(parent):
        card = Frame(parent, bg=config.BG_CARD, padx=24, pady=18)
        card.pack(fill="x", padx=25, pady=(20, 10))

        Label(card, text="Propeller Tip Speed & Drive Ratio Calculator", font=config.FONT_TITLE,
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="Propeller efficiency collapses when tips approach the speed of sound (> Mach 0.75). "
                        "Direct-drive industrial engines (like the Predator) turn at 3,600 RPM and must use smaller ~42\" props to keep tip speeds subsonic. "
                        "Engines turning large 54\"–60\" props require a reduction drive (PSRU) to slow the prop down.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED, wraplength=720, justify="left").pack(anchor="w", pady=(4, 12))

        ctrl_frame = Frame(card, bg=config.BG_CARD)
        ctrl_frame.pack(fill="x", pady=4)

        Label(ctrl_frame, text="Propeller Diameter (inches):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=0, column=0, sticky="w", pady=4)
        diam_slider = Scale(ctrl_frame, from_=36, to=68, orient=HORIZONTAL, bg=config.BG_CARD, fg="#ffffff", highlightthickness=0, length=240)
        diam_slider.set(42)
        diam_slider.grid(row=0, column=1, padx=10)

        Label(ctrl_frame, text="Engine Operating RPM:", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=1, column=0, sticky="w", pady=4)
        rpm_slider = Scale(ctrl_frame, from_=2000, to=6500, resolution=50, orient=HORIZONTAL, bg=config.BG_CARD, fg="#ffffff", highlightthickness=0, length=240)
        rpm_slider.set(3600)
        rpm_slider.grid(row=1, column=1, padx=10)

        Label(ctrl_frame, text="Reduction Ratio (1.0 = Direct Drive):", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).grid(row=2, column=0, sticky="w", pady=4)
        ratio_slider = Scale(ctrl_frame, from_=1.0, to=3.0, resolution=0.1, orient=HORIZONTAL, bg=config.BG_CARD, fg="#ffffff", highlightthickness=0, length=240)
        ratio_slider.set(1.0)
        ratio_slider.grid(row=2, column=1, padx=10)

        res_card = Frame(parent, bg=config.BG_CARD, padx=22, pady=16, highlightbackground=config.ACCENT_COLOR, highlightthickness=1)
        res_card.pack(fill="x", padx=25, pady=10)

        res_prop_rpm = Label(res_card, text="Propeller RPM: —", font=("Helvetica", 12, "bold"), bg=config.BG_CARD, fg=config.TEXT_PRIMARY)
        res_prop_rpm.pack(anchor="w")
        res_tip_fps = Label(res_card, text="Tip Speed (ft/sec & mph): —", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg="#00b0f4")
        res_tip_fps.pack(anchor="w", pady=2)
        res_mach = Label(res_card, text="Tip Mach Number: —", font=("Helvetica", 13, "bold"), bg=config.BG_CARD, fg=config.ACCENT_GREEN)
        res_mach.pack(anchor="w", pady=2)
        eval_lbl = Label(res_card, text="Aero Assessment: —", font=config.FONT_BODY_BOLD, bg=config.BG_CARD, fg=config.TEXT_PRIMARY)
        eval_lbl.pack(anchor="w", pady=2)

        def _calc_prop(*args):
            diam = diam_slider.get()
            eng_rpm = rpm_slider.get()
            ratio = max(0.5, ratio_slider.get())

            prop_rpm = eng_rpm / ratio
            tip_fps = (math.pi * diam * prop_rpm) / 720.0
            tip_mph = tip_fps * 3600.0 / 5280.0
            mach = tip_fps / 1116.4  # Speed of sound at standard sea level

            res_prop_rpm.config(text=f"Propeller Shaft RPM: {int(prop_rpm):,} RPM (Drive: {ratio:.1f}:1)")
            res_tip_fps.config(text=f"Tip Velocity: {int(tip_fps)} ft/s ({int(tip_mph)} mph)")
            res_mach.config(text=f"Propeller Tip Mach: Mach {mach:.2f}")

            if mach < 0.65:
                res_mach.config(fg=config.ACCENT_GREEN)
                eval_lbl.config(
                    text="✓ OPTIMAL EFFICIENCY: Subsonic flow across the entire blade. Quiet, excellent thrust, minimal tip losses.",
                    fg=config.ACCENT_GREEN
                )
            elif mach <= 0.75:
                res_mach.config(fg=config.ACCENT_AMBER)
                eval_lbl.config(
                    text="⚠️ ACCEPTABLE BUT NOISY: Higher acoustic output. Compressibility drag begins increasing at blade tips.",
                    fg=config.ACCENT_AMBER
                )
            else:
                res_mach.config(fg=config.ACCENT_RED)
                eval_lbl.config(
                    text="🛑 DANGER: TRANSONIC TIP SPEED! Severe shock wave drag, blade flutter, and massive power loss. Reduce diameter or add a PSRU!",
                    fg=config.ACCENT_RED
                )

        diam_slider.config(command=_calc_prop)
        rpm_slider.config(command=_calc_prop)
        ratio_slider.config(command=_calc_prop)
        _calc_prop()

class PreflightChecklistTool:
    @staticmethod
    def render(parent, checklist_vars):
        card = Frame(parent, bg=config.BG_CARD, padx=24, pady=18)
        card.pack(fill="x", padx=25, pady=(20, 10))

        Label(card, text="Ultralight Pre-Flight Inspection Checklist", font=config.FONT_TITLE,
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="Because ultralights receive no FAA mechanic inspections, your preflight is your only defense against structural or engine failure.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED, wraplength=720, justify="left").pack(anchor="w", pady=(4, 10))

        progress_lbl = Label(card, text="Progress: 0 / 20 items verified (0%)", font=config.FONT_BODY_BOLD,
                             bg=config.BG_CARD, fg=config.ACCENT_AMBER)
        progress_lbl.pack(anchor="w", pady=(0, 6))

        checklist_items = [
            ("COCKPIT & FLIGHT CONTROLS", [
                "Controls Free & Correct: Stick left = left aileron up, stick back = elevator up",
                "Control Cables & Pulleys: No frayed wire strands, cables seated in grooves",
                "Restraint Harness: Webbing undamaged, latch clicks firmly and locks",
                "Ballistic Parachute (BRS): SAFETY PIN REMOVED, activation handle clear"
            ]),
            ("POWERPLANT (2-STROKE & 4-STROKE)", [
                "4-Stroke Sump / 2-Stroke Premix: Oil level verified, no oil leaks around crankcase",
                "Engine Mounts: No hairline cracks in welded steel or aluminum tubes",
                "Exhaust System: Retaining springs safety-wired, no cracks near manifold",
                "Spark Plug Caps: Firmly seated with safety zip-ties / clips in place",
                "Reduction Belt / Gearbox: Proper belt deflection tension, no gear oil leak"
            ]),
            ("PROPELLER (HIGH-STRESS COMPONENT)", [
                "Blades: No leading edge nicks, stone chips, or delamination cracks",
                "Hub & Bolts: Proper torque checked, safety wire intact, no tracking wobble"
            ]),
            ("FUEL SYSTEM (5-GALLON LIMIT)", [
                "Fuel Sump Drained: Clear sample verified, ZERO water or ethanol phase separation",
                "Fuel Lines: No dry-rot cracking, hardening, or chafing against airframe tubes",
                "Fuel Cap: Gasket seated, vented cap clear, firmly secured to prevent siphoning"
            ]),
            ("WINGS, STRUTS & RIGGING", [
                "Attachment Pins & Rings: All clevis pins locked with safety rings / cotter pins",
                "Sailcloth Integrity: Dacron firm, stitches intact, passes Maule UV punch test",
                "Leading Edge & Ribs: No dented tubes, battens secured in trailing edge pockets"
            ]),
            ("LANDING GEAR & FINAL WALKAROUND", [
                "Tire Inflation & Axles: Tires properly inflated, no flat spots, axle nuts pinned",
                "Pusher Prop Clearance: ZERO loose articles in cockpit that could blow into prop!"
            ])
        ]

        def _update_progress():
            total = len(checklist_vars)
            checked = sum(1 for v in checklist_vars.values() if v.get())
            pct = int((checked / total) * 100) if total > 0 else 0
            color = config.ACCENT_GREEN if pct == 100 else config.ACCENT_AMBER
            progress_lbl.config(text=f"Progress: {checked} / {total} items verified ({pct}%)", fg=color)

        for phase_title, items in checklist_items:
            cat_frame = Frame(parent, bg=config.BG_CARD, padx=20, pady=12)
            cat_frame.pack(fill="x", padx=25, pady=6)
            Label(cat_frame, text=phase_title, font=("Helvetica", 11, "bold"), bg=config.BG_CARD, fg=config.ACCENT_COLOR).pack(anchor="w", pady=(0, 6))

            for item_text in items:
                if item_text not in checklist_vars:
                    checklist_vars[item_text] = BooleanVar(value=False)
                var = checklist_vars[item_text]
                cb = Checkbutton(
                    cat_frame, text=item_text, variable=var, command=_update_progress,
                    font=config.FONT_BODY, bg=config.BG_CARD, fg="#dcddde", activebackground=config.BG_CARD,
                    activeforeground="#ffffff", selectcolor=config.BG_SIDEBAR, wraplength=680, justify="left"
                )
                cb.pack(anchor="w", pady=2)

        _update_progress()