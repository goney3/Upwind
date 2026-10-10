"""
main.py - Upwind: Part 103 Prep Ground School Application Launcher.
Features global, cross-platform mousewheel scrolling for both Sidebar and Content panes.
"""

import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, Label
import random
import sys

import config
from ui_components import ModernButton, draw_fitted_logo
from data.curriculum import get_study_content
from data.questions import get_question_pool
import views.diagrams as diagrams
import views.tools as tools

class UltralightGroundSchoolApp:
    def __init__(self, master):
        self.master = master
        master.title("Upwind: FAA FAR Part 103 Prep Ground School & Flight Suite")
        master.geometry("1140x840")
        master.minsize(980, 720)

        # Content & Question Engine State
        self.study_topics_content = get_study_content()
        self.question_pool = get_question_pool()
        self.sidebar_buttons = {}
        self.checklist_vars = {}

        self.quiz_questions = []
        self.quiz_index = 0
        self.quiz_user_answers = {}
        self.flashcard_index = 0

        self._build_main_interface()
        self.show_dashboard()

    def _build_main_interface(self):
        # 1. Header Bar
        header_frame = Frame(self.master, bg=config.BG_SIDEBAR, height=54)
        header_frame.pack(side="top", fill="x")

        logo_canvas = Canvas(header_frame, width=44, height=44, bg=config.BG_SIDEBAR, highlightthickness=0)
        logo_canvas.pack(side="left", padx=(14, 8), pady=5)
        draw_fitted_logo(logo_canvas, 44, bg_circle_color=config.ACCENT_COLOR)

        Label(header_frame, text="Upwind: Part 103 Prep", font=("Helvetica", 14, "bold"),
              bg=config.BG_SIDEBAR, fg=config.TEXT_PRIMARY).pack(side="left", pady=12)
        Label(header_frame, text="•  FAA FAR Part 103 Flight Safety & 2/4-Stroke Suite", 
              font=("Helvetica", 10), bg=config.BG_SIDEBAR, fg=config.TEXT_MUTED).pack(side="left", padx=8, pady=14)

        status_badge = Label(header_frame, text=f"{len(self.question_pool)} Exam Questions", 
                             font=("Helvetica", 9, "bold"), bg="#292b2f", fg=config.ACCENT_GREEN, padx=8, pady=3)
        status_badge.pack(side="right", padx=15, pady=12)

        # 2. Main Workspace
        self.workspace_frame = Frame(self.master, bg=config.BG_ROOT)
        self.workspace_frame.pack(fill="both", expand=True)

        self._build_sidebar()
        self._build_content_pane()
        
        # 3. Setup Global Mousewheel Listener
        self._setup_mousewheel_scrolling()

    def _build_sidebar(self):
        self.sidebar_container = Frame(self.workspace_frame, bg=config.BG_SIDEBAR, width=285)
        self.sidebar_container.pack(side="left", fill="y")
        self.sidebar_container.pack_propagate(False)

        self.sb_canvas = Canvas(self.sidebar_container, bg=config.BG_SIDEBAR, highlightthickness=0)
        sb_scrollbar = Scrollbar(self.sidebar_container, orient="vertical", command=self.sb_canvas.yview)
        self.sb_inner_frame = Frame(self.sb_canvas, bg=config.BG_SIDEBAR)

        self.sb_inner_frame.bind("<Configure>", lambda e: self.sb_canvas.configure(scrollregion=self.sb_canvas.bbox("all")))
        sb_window_id = self.sb_canvas.create_window((0, 0), window=self.sb_inner_frame, anchor="nw")
        self.sb_canvas.bind("<Configure>", lambda e: self.sb_canvas.itemconfig(sb_window_id, width=e.width))

        self.sb_canvas.configure(yscrollcommand=sb_scrollbar.set)
        sb_scrollbar.pack(side="right", fill="y")
        self.sb_canvas.pack(side="left", fill="both", expand=True)

        # CTA Exam Launcher
        exam_btn = ModernButton(
            self.sb_inner_frame, text="⚡ 20-QUESTION PRACTICE EXAM",
            command=lambda: self.start_quiz(category_filter=None), bg=config.ACCENT_COLOR, fg="#ffffff",
            hover_bg="#4752c4", active_bg="#3c45a5", font=("Helvetica", 10, "bold"),
            padx=10, pady=9, anchor="center"
        )
        exam_btn.pack(fill="x", padx=12, pady=(12, 6))

        self._add_sidebar_nav_button("Dashboard & Overview", self.show_dashboard, icon="📌")

        # PRACTICAL FLIGHT TOOLS
        Label(self.sb_inner_frame, text="PRACTICAL FLIGHT TOOLS", font=("Helvetica", 9, "bold"),
              bg=config.BG_SIDEBAR, fg="#8e9297").pack(anchor="w", padx=14, pady=(10, 4))
        self._add_sidebar_nav_button("Weight & Balance / CG Tool ⚖️", lambda: self._show_tool(tools.WeightBalanceTool.render, "Weight & Balance / CG Tool ⚖️"))
        self._add_sidebar_nav_button("Propeller Tip Speed & PSRU ⚙️", lambda: self._show_tool(tools.PropellerTipSpeedTool.render, "Propeller Tip Speed & PSRU ⚙️"))
        self._add_sidebar_nav_button("Crosswind & Runway Compass 🧭", lambda: self._show_tool(tools.CrosswindTool.render, "Crosswind & Runway Compass 🧭"))
        self._add_sidebar_nav_button("Density Alt & Fuel Calc 🧮", lambda: self._show_tool(tools.DensityAltTool.render, "Density Alt & Fuel Calc 🧮"))
        self._add_sidebar_nav_button("Glide Cone / Landing Reach 🪂", lambda: self._show_tool(tools.GlideConeTool.render, "Glide Cone / Landing Reach 🪂"))
        self._add_sidebar_nav_button("Pre-Flight Checklist Tool ✅", lambda: self._show_tool(lambda p: tools.PreflightChecklistTool.render(p, self.checklist_vars), "Pre-Flight Checklist Tool ✅"))

        # VISUAL DIAGRAMS & CHARTS
        Label(self.sb_inner_frame, text="VISUAL CHARTS & DIAGRAMS", font=("Helvetica", 9, "bold"),
              bg=config.BG_SIDEBAR, fg="#8e9297").pack(anchor="w", padx=14, pady=(10, 4))
        self._add_sidebar_nav_button("Airspace Visual Chart 🗺️", self.show_airspace_chart_view)
        self._add_sidebar_nav_button("Traffic Pattern & Spin Trap ✈️", lambda: self._show_diagram_view("Traffic Pattern & Spin Trap ✈️", diagrams.draw_traffic_pattern))
        self._add_sidebar_nav_button("2-Stroke vs 4-Stroke Gauges ⏱️", lambda: self._show_diagram_view("2-Stroke vs 4-Stroke Gauges ⏱️", diagrams.draw_engine_gauges_comparative))
        self._add_sidebar_nav_button("Carb Icing Probability Matrix ❄️", lambda: self._show_diagram_view("Carb Icing Probability Matrix ❄️", diagrams.draw_carb_icing_matrix))
        self._add_sidebar_nav_button("Bank Angle & G-Load Chart 📈", lambda: self._show_diagram_view("Bank Angle & G-Load Chart 📈", diagrams.draw_load_factor_diagram))

        # CURRICULUM MODULES
        curriculum_groups = [
            ("REGULATIONS & LEGAL", [
                "FAR Part 103 Overview",
                "FAR Part 103 Operations",
                "FAA AC 103-7 Weight Credits"
            ]),
            ("ENGINES & PROPULSION", [
                "Two-Stroke Engines & Fuel Systems",
                "Four-Stroke Aero Engines: Half-VW & Conversions",
                "Industrial Four-Stroke Conversions (Briggs Vanguard & Kohler V-Twins)"
            ]),
            ("FLIGHT ENVIRONMENT", [
                "Airspace for Ultralights",
                "Basic Weather for VFR Flight",
                "Navigation and Sectional Charts",
                "Airport Operations and Markings"
            ]),
            ("HANDLING & SAFETY", [
                "Aerodynamics & Low Wing Loading",
                "Weight, Balance & Control Types",
                "Ultralight Systems & Preflight",
                "Human Factors (ADM & IMSAFE)",
                "Emergency Procedures & Survival"
            ])
        ]

        for group_title, topics in curriculum_groups:
            Label(self.sb_inner_frame, text=group_title, font=("Helvetica", 9, "bold"),
                  bg=config.BG_SIDEBAR, fg="#8e9297").pack(anchor="w", padx=14, pady=(10, 4))
            for topic in topics:
                self._add_sidebar_nav_button(topic, lambda t=topic: self.show_topic(t), icon="•")

        # TESTING & STUDY
        Label(self.sb_inner_frame, text="STUDY & TESTING", font=("Helvetica", 9, "bold"),
              bg=config.BG_SIDEBAR, fg="#8e9297").pack(anchor="w", padx=14, pady=(10, 4))
        self._add_sidebar_nav_button("Topic-Targeted Quizzes 🎯", self.show_topic_quiz_selector, icon="•")
        self._add_sidebar_nav_button("Flashcard Review Mode 🃏", self.show_flashcards, icon="•")

        Label(self.sb_inner_frame, text="Public Domain Safety Tool.", font=("Helvetica", 8),
              bg=config.BG_SIDEBAR, fg="#72767d").pack(pady=16)

    def _add_sidebar_nav_button(self, name, command, icon="•"):
        btn = ModernButton(
            self.sb_inner_frame, text=f"  {icon}  {name}", command=command,
            bg=config.BG_SIDEBAR, fg=config.TEXT_MUTED, hover_bg="#292b2f", active_bg=config.ACCENT_COLOR,
            font=("Helvetica", 10), padx=8, pady=5, anchor="w"
        )
        btn.pack(fill="x", padx=8, pady=1)
        self.sidebar_buttons[name] = btn

    def _set_active_sidebar_button(self, active_name):
        for name, btn in self.sidebar_buttons.items():
            btn.set_active_state(name == active_name)

    def _build_content_pane(self):
        self.content_container = Frame(self.workspace_frame, bg=config.BG_CONTENT)
        self.content_container.pack(side="left", fill="both", expand=True)

        self.main_canvas = Canvas(self.content_container, bg=config.BG_CONTENT, highlightthickness=0)
        self.main_scrollbar = Scrollbar(self.content_container, orient="vertical", command=self.main_canvas.yview)
        self.content_frame = Frame(self.main_canvas, bg=config.BG_CONTENT)

        self.content_frame.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.canvas_window_id = self.main_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.main_canvas.bind("<Configure>", lambda e: self.main_canvas.itemconfig(self.canvas_window_id, width=e.width))

        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        self.main_scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)

    # -------------------------------------------------------------------------
    # GLOBAL SCROLL CONTROLLER
    # -------------------------------------------------------------------------
    def _setup_mousewheel_scrolling(self):
        """Binds mousewheel events globally and targets the hovered pane."""
        self.master.bind_all("<MouseWheel>", self._on_global_mousewheel, add="+")
        self.master.bind_all("<Button-4>", self._on_global_mousewheel, add="+")
        self.master.bind_all("<Button-5>", self._on_global_mousewheel, add="+")

    def _on_global_mousewheel(self, event):
        # 1. Compute scroll steps across OS platforms
        units = 0
        if getattr(event, "num", None) == 4:
            # Linux scroll up
            units = -2
        elif getattr(event, "num", None) == 5:
            # Linux scroll down
            units = 2
        elif getattr(event, "delta", 0):
            if sys.platform == "darwin":
                # macOS delta is small (+/- 1)
                units = int(-1 * event.delta)
            else:
                # Windows delta is (+/- 120)
                steps = int(-1 * (event.delta / 120))
                units = steps if steps != 0 else (-1 if event.delta > 0 else 1)

        if units == 0:
            return

        # 2. Identify which widget is directly under the pointer
        try:
            widget = self.master.winfo_containing(event.x_root, event.y_root)
        except Exception:
            widget = None

        if widget is None:
            widget = event.widget

        # 3. Determine if pointer is over Sidebar or Main Content Area
        target_canvas = self.main_canvas
        curr = widget
        while curr is not None:
            if curr in (self.sidebar_container, self.sb_canvas, self.sb_inner_frame):
                target_canvas = self.sb_canvas
                break
            if curr in (self.content_container, self.main_canvas, self.content_frame):
                target_canvas = self.main_canvas
                break
            curr = getattr(curr, "master", None)

        # 4. Scroll the resolved canvas
        try:
            target_canvas.yview_scroll(units, "units")
        except Exception:
            pass

    def _clear_content_pane(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.main_canvas.yview_moveto(0)

    # -------------------------------------------------------------------------
    # ROUTING HANDLERS
    # -------------------------------------------------------------------------
    def _show_tool(self, render_func, title):
        self._clear_content_pane()
        self._set_active_sidebar_button(title)
        render_func(self.content_frame)

    def _show_diagram_view(self, title, draw_func):
        self._clear_content_pane()
        self._set_active_sidebar_button(title)

        card = Frame(self.content_frame, bg=config.BG_CARD, padx=20, pady=16)
        card.pack(fill="x", padx=25, pady=(20, 10))
        Label(card, text=title, font=config.FONT_TITLE, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")

        c_w, c_h = 760, 480
        chart_canvas = Canvas(self.content_frame, width=c_w, height=c_h, bg="#1e2124", highlightthickness=0)
        chart_canvas.pack(padx=25, pady=8)
        draw_func(chart_canvas)

    def show_airspace_chart_view(self):
        self._clear_content_pane()
        self._set_active_sidebar_button("Airspace Visual Chart 🗺️")

        card = Frame(self.content_frame, bg=config.BG_CARD, padx=20, pady=15)
        card.pack(fill="x", padx=25, pady=(20, 10))
        Label(card, text="U.S. Airspace Classes at a Glance", font=config.FONT_TITLE,
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="Profile diagram showing Class A, B, C, D, E, and Class G airspace relationships.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED).pack(anchor="w")

        chart_canvas = Canvas(self.content_frame, width=750, height=520, bg="#ffffff", highlightthickness=0)
        chart_canvas.pack(padx=25, pady=10)
        diagrams.draw_airspace_chart(chart_canvas)

    def show_dashboard(self):
        self._clear_content_pane()
        self._set_active_sidebar_button("Dashboard & Overview")

        dash_card = Frame(self.content_frame, bg=config.BG_CARD, padx=25, pady=20)
        dash_card.pack(fill="x", padx=25, pady=(20, 15))

        top_row = Frame(dash_card, bg=config.BG_CARD)
        top_row.pack(fill="x")

        big_logo = Canvas(top_row, width=90, height=90, bg=config.BG_CARD, highlightthickness=0)
        big_logo.pack(side="left", padx=(0, 20))
        draw_fitted_logo(big_logo, 90, bg_circle_color=config.ACCENT_COLOR)

        info_box = Frame(top_row, bg=config.BG_CARD)
        info_box.pack(side="left", fill="both", expand=True)

        Label(info_box, text="Part 103 Ground School & Flight Suite", font=config.FONT_TITLE,
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(info_box, 
              text="Because FAR Part 103 mandates zero flight training, medical exams, or written tests, "
                   "ultralight aviators bear 100% of the responsibility for their own airworthiness and survival. "
                   "This ground school delivers the aerodynamics, regulations, two-stroke/four-stroke engine management, "
                   "and emergency recovery disciplines necessary to protect your life.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED, wraplength=580, justify="left").pack(anchor="w", pady=(6, 10))

        ModernButton(
            dash_card, text="⚡ Begin 20-Question Practice Exam", command=lambda: self.start_quiz(category_filter=None),
            bg=config.ACCENT_COLOR, fg="#ffffff", hover_bg="#4752c4", font=("Helvetica", 11, "bold"),
            padx=14, pady=8
        ).pack(anchor="w", pady=(10, 0))

        summary_frame = Frame(self.content_frame, bg=config.BG_CONTENT)
        summary_frame.pack(fill="x", padx=25, pady=5)

        cards_data = [
            ("⚖️ Legal Thresholds", 
             "• Empty Weight: < 254 lbs (Powered)\n"
             "• Fuel Capacity: 5 Gallons Max\n"
             "• Max Speed: 55 Kts (63 mph)\n"
             "• Stall Speed: 24 Kts (28 mph)\n"
             "• Single Occupant (Sport/Pleasure)", config.ACCENT_GREEN),
            ("⏱️ Engine Envelopes", 
             "• 2-Stroke: Idle descents starve oil!\n"
             "  Warmup CHT > 250°F to stop cold seizures\n"
             "• 4-Stroke (Half-VW / V-Twin):\n"
             "  Oil Temp: 160°–220°F (30–40 PSI)\n"
             "  Cold valve lash strictly 0.006\"", config.ACCENT_AMBER),
            ("🗺️ Airspace Rules", 
             "• Uncontrolled: Class G native ground\n"
             "• Controlled: Prior ATC authorization\n"
             "  required for B, C, D, & Surface E\n"
             "• Weather: 1 SM visibility and\n"
             "  Clear of Clouds in Class G <=1,200'", config.ACCENT_COLOR)
        ]

        for title, text, border_color in cards_data:
            c = Frame(summary_frame, bg=config.BG_CARD, padx=15, pady=12, highlightbackground=border_color, highlightthickness=1)
            c.pack(side="left", fill="both", expand=True, padx=5)
            Label(c, text=title, font=("Helvetica", 11, "bold"), bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w", pady=(0, 6))
            Label(c, text=text, font=("Helvetica", 9), bg=config.BG_CARD, fg=config.TEXT_MUTED, justify="left").pack(anchor="w")

    def show_topic(self, topic_title):
        self._clear_content_pane()
        self._set_active_sidebar_button(topic_title)

        header = Frame(self.content_frame, bg=config.BG_CARD, padx=20, pady=16)
        header.pack(fill="x", padx=25, pady=(20, 15))

        Label(header, text="STUDY MODULE", font=("Helvetica", 9, "bold"), bg=config.BG_CARD, fg=config.ACCENT_COLOR).pack(anchor="w")
        Label(header, text=topic_title, font=config.FONT_TITLE, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w", pady=(2, 4))

        body_frame = Frame(self.content_frame, bg=config.BG_CARD, padx=22, pady=20)
        body_frame.pack(fill="x", padx=25, pady=5)

        content = self.study_topics_content.get(topic_title, "Content being updated.")
        Label(body_frame, text=content, font=config.FONT_BODY, bg=config.BG_CARD, fg="#dcddde",
              wraplength=720, justify="left").pack(anchor="w", fill="x")

    def show_topic_quiz_selector(self):
        self._clear_content_pane()
        self._set_active_sidebar_button("Topic-Targeted Quizzes 🎯")

        card = Frame(self.content_frame, bg=config.BG_CARD, padx=24, pady=20)
        card.pack(fill="x", padx=25, pady=(20, 15))

        Label(card, text="Topic-Targeted Knowledge Exams", font=config.FONT_TITLE, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="Focus on specific disciplines. Select a module below to launch a tailored quiz.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED).pack(anchor="w", pady=(4, 15))

        topics = [
            ("FAR Part 103 Regulations", "Empty weights, fuel capacity, daylight/twilight, right-of-way.", ["103", "empty weight", "gallons", "twilight", "congested"]),
            ("Engine Management (2-Stroke & 4-Stroke)", "Half-VW, V-Twins, governors, PSRU, cold seizures, phase separation.", ["stroke", "half-vw", "v-twin", "governor", "seizure", "oil", "egt", "lash", "propeller"]),
            ("Aerodynamics, Load Factors & Turns", "Stalls, spins, bank angle G-loads, base-to-final skid traps.", ["stall", "bank", "load factor", "g-load", "spin", "rudder"]),
            ("Airspace, Weather & Forced Landings", "Class B/C/D/G minimums, density altitude, glide cone reach.", ["class", "airspace", "density altitude", "glide", "headwind"])
        ]

        for title, desc, keywords in topics:
            t_frame = Frame(self.content_frame, bg=config.BG_CARD, padx=18, pady=12)
            t_frame.pack(fill="x", padx=25, pady=6)
            Label(t_frame, text=title, font=("Helvetica", 12, "bold"), bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
            Label(t_frame, text=desc, font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED).pack(anchor="w", pady=(2, 8))
            ModernButton(t_frame, text=f"Start {title} Quiz", command=lambda kw=keywords: self.start_quiz(category_filter=kw),
                         bg=config.ACCENT_COLOR, fg="#ffffff", hover_bg="#4752c4", font=("Helvetica", 10, "bold"),
                         padx=12, pady=6).pack(anchor="w")

    def show_flashcards(self):
        self._clear_content_pane()
        self._set_active_sidebar_button("Flashcard Review Mode 🃏")

        card = Frame(self.content_frame, bg=config.BG_CARD, padx=25, pady=20)
        card.pack(fill="x", padx=25, pady=(20, 15))

        Label(card, text="Rapid-Fire Flashcard Study", font=config.FONT_TITLE, bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w")
        Label(card, text="Review key concepts without test pressure. Read the prompt, test your memory, then reveal the safety explanation.",
              font=config.FONT_BODY, bg=config.BG_CARD, fg=config.TEXT_MUTED).pack(anchor="w", pady=(4, 15))

        q_data = self.question_pool[self.flashcard_index]

        q_frame = Frame(self.content_frame, bg=config.BG_CARD, padx=25, pady=22)
        q_frame.pack(fill="x", padx=25, pady=6)

        Label(q_frame, text=f"CARD {self.flashcard_index + 1} OF {len(self.question_pool)}",
              font=("Helvetica", 10, "bold"), bg=config.BG_CARD, fg=config.ACCENT_COLOR).pack(anchor="w", pady=(0, 6))
        Label(q_frame, text=q_data['question_text'], font=("Helvetica", 13, "bold"),
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY, wraplength=700, justify="left").pack(anchor="w", pady=(0, 14))

        ans_card = Frame(q_frame, bg="#292b2f", padx=16, pady=12)
        ans_lbl = Label(ans_card, text="Click 'Reveal Answer' to check your knowledge.", font=config.FONT_BODY,
                        bg="#292b2f", fg=config.TEXT_MUTED, wraplength=660, justify="left")
        ans_lbl.pack(anchor="w")

        def _reveal():
            ans_card.pack(fill="x", pady=8)
            ans_lbl.config(
                text=f"CORRECT ANSWER:\n✓ {q_data['correct_answer']}\n\nSAFETY EXPLANATION:\n{q_data['explanation']}",
                fg=config.ACCENT_GREEN, font=config.FONT_BODY_BOLD
            )

        btn_row = Frame(q_frame, bg=config.BG_CARD)
        btn_row.pack(anchor="w", pady=(15, 0))

        ModernButton(btn_row, text="Reveal Answer", command=_reveal, bg=config.ACCENT_COLOR, fg="#ffffff", padx=12, pady=7).pack(side="left", padx=4)
        ModernButton(btn_row, text="Previous Card", command=lambda: self._step_flashcard(-1), bg="#292b2f", fg="#ffffff", padx=12, pady=7).pack(side="left", padx=4)
        ModernButton(btn_row, text="Next Card ➔", command=lambda: self._step_flashcard(1), bg=config.ACCENT_GREEN, fg="#ffffff", padx=12, pady=7).pack(side="left", padx=4)
        ModernButton(btn_row, text="Random Shuffle", command=self._shuffle_flashcard, bg="#40444b", fg="#ffffff", padx=12, pady=7).pack(side="left", padx=4)

    def _step_flashcard(self, step):
        self.flashcard_index = (self.flashcard_index + step) % len(self.question_pool)
        self.show_flashcards()

    def _shuffle_flashcard(self):
        self.flashcard_index = random.randint(0, len(self.question_pool) - 1)
        self.show_flashcards()

    # -------------------------------------------------------------------------
    # EXAM ENGINE
    # -------------------------------------------------------------------------
    def start_quiz(self, category_filter=None):
        self._clear_content_pane()
        self._set_active_sidebar_button("⚡ 20-QUESTION PRACTICE EXAM")

        pool = self.question_pool
        if category_filter:
            pool = [
                q for q in self.question_pool
                if any(k.lower() in q['question_text'].lower() or k.lower() in q['explanation'].lower() for k in category_filter)
            ]
            if len(pool) < 5:
                pool = self.question_pool

        self.quiz_questions = random.sample(pool, min(20, len(pool)))
        self.quiz_index = 0
        self.quiz_user_answers = {}
        self._render_current_quiz_question()

    def _render_current_quiz_question(self):
        self._clear_content_pane()
        q_data = self.quiz_questions[self.quiz_index]

        top_bar = Frame(self.content_frame, bg=config.BG_CARD, padx=20, pady=14)
        top_bar.pack(fill="x", padx=25, pady=(20, 12))

        Label(top_bar, text=f"QUESTION {self.quiz_index + 1} OF {len(self.quiz_questions)}",
              font=("Helvetica", 10, "bold"), bg=config.BG_CARD, fg=config.ACCENT_COLOR).pack(side="left")

        pct = int(((self.quiz_index) / len(self.quiz_questions)) * 100)
        Label(top_bar, text=f"Progress: {pct}%", font=("Helvetica", 9),
              bg=config.BG_CARD, fg=config.TEXT_MUTED).pack(side="right")

        q_card = Frame(self.content_frame, bg=config.BG_CARD, padx=25, pady=22)
        q_card.pack(fill="x", padx=25, pady=6)

        Label(q_card, text=q_data['question_text'], font=("Helvetica", 13, "bold"),
              bg=config.BG_CARD, fg=config.TEXT_PRIMARY, wraplength=700, justify="left").pack(anchor="w", pady=(0, 16))

        self.selected_option_var = tk.StringVar(value="")
        self.option_buttons = []
        for opt in q_data['options']:
            btn = ModernButton(
                q_card, text=f"   {opt}", command=lambda o=opt: self._select_quiz_option(o),
                bg="#292b2f", fg="#dcddde", hover_bg="#32353b", active_bg=config.ACCENT_COLOR,
                font=config.FONT_BODY, padx=12, pady=10, anchor="w"
            )
            btn.pack(fill="x", pady=4)
            self.option_buttons.append((opt, btn))

        action_bar = Frame(self.content_frame, bg=config.BG_CONTENT)
        action_bar.pack(fill="x", padx=25, pady=18)

        self.quiz_feedback_lbl = Label(action_bar, text="", font=config.FONT_BODY_BOLD,
                                       bg=config.BG_CONTENT, fg=config.ACCENT_AMBER)
        self.quiz_feedback_lbl.pack(side="left", padx=5)

        next_text = "Submit Exam" if self.quiz_index == len(self.quiz_questions) - 1 else "Next Question  ➔"
        ModernButton(
            action_bar, text=next_text, command=self._handle_next_question,
            bg=config.ACCENT_COLOR, fg="#ffffff", hover_bg="#4752c4",
            font=("Helvetica", 11, "bold"), padx=18, pady=8, anchor="center"
        ).pack(side="right")

    def _select_quiz_option(self, chosen_opt):
        self.selected_option_var.set(chosen_opt)
        for opt_text, btn in self.option_buttons:
            btn.set_active_state(opt_text == chosen_opt)

    def _handle_next_question(self):
        choice = self.selected_option_var.get()
        if not choice:
            self.quiz_feedback_lbl.config(text="Please select an answer to proceed.")
            return

        self.quiz_user_answers[self.quiz_index] = choice
        self.quiz_index += 1

        if self.quiz_index < len(self.quiz_questions):
            self._render_current_quiz_question()
        else:
            self._render_quiz_results()

    def _render_quiz_results(self):
        self._clear_content_pane()
        score = sum(1 for idx, q in enumerate(self.quiz_questions) if self.quiz_user_answers.get(idx) == q['correct_answer'])
        score_pct = (score / len(self.quiz_questions)) * 100
        passed = score_pct >= 80

        card = Frame(self.content_frame, bg=config.BG_CARD, padx=25, pady=20)
        card.pack(fill="x", padx=25, pady=(20, 14))

        status_text = "EXAM PASSED (Proficient)" if passed else "SAFETY REVIEW RECOMMENDED (<80%)"
        status_color = config.ACCENT_GREEN if passed else config.ACCENT_RED

        Label(card, text=status_text, font=("Helvetica", 16, "bold"), bg=config.BG_CARD, fg=status_color).pack(anchor="w")
        Label(card, text=f"Your Score: {score} / {len(self.quiz_questions)} ({score_pct:.1f}%)",
              font=("Helvetica", 13), bg=config.BG_CARD, fg=config.TEXT_PRIMARY).pack(anchor="w", pady=(4, 12))

        ModernButton(
            card, text="Take Another Exam", command=lambda: self.start_quiz(category_filter=None),
            bg=config.ACCENT_COLOR, fg="#ffffff", hover_bg="#4752c4", font=("Helvetica", 11, "bold"),
            padx=14, pady=8
        ).pack(anchor="w")

        # Review Incorrect Answers
        incorrect_items = [
            (q, self.quiz_user_answers.get(idx, "None"))
            for idx, q in enumerate(self.quiz_questions)
            if self.quiz_user_answers.get(idx) != q['correct_answer']
        ]

        if incorrect_items:
            Label(self.content_frame, text="QUESTIONS REQUIRING SAFETY REVIEW", font=("Helvetica", 12, "bold"),
                  bg=config.BG_CONTENT, fg=config.ACCENT_RED).pack(anchor="w", padx=25, pady=(15, 6))

            for q_data, user_ans in incorrect_items:
                q_card = Frame(self.content_frame, bg=config.BG_CARD, padx=18, pady=14,
                               highlightbackground=config.ACCENT_RED, highlightthickness=1)
                q_card.pack(fill="x", padx=25, pady=5)
                Label(q_card, text=q_data['question_text'], font=config.FONT_BODY_BOLD,
                      bg=config.BG_CARD, fg=config.TEXT_PRIMARY, wraplength=700, justify="left").pack(anchor="w")
                Label(q_card, text=f"  ✗ Your Answer: {user_ans}", font=config.FONT_BODY,
                      bg=config.BG_CARD, fg=config.ACCENT_RED).pack(anchor="w", pady=(2, 0))
                Label(q_card, text=f"  ✓ Correct: {q_data['correct_answer']}", font=config.FONT_BODY_BOLD,
                      bg=config.BG_CARD, fg=config.ACCENT_GREEN).pack(anchor="w", pady=(2, 4))
                Label(q_card, text=f"Explanation: {q_data['explanation']}", font=config.FONT_SMALL,
                      bg=config.BG_CARD, fg=config.TEXT_MUTED, wraplength=700, justify="left").pack(anchor="w")

# -----------------------------------------------------------------------------
# APPLICATION ENTRY POINT
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = UltralightGroundSchoolApp(root)
    root.mainloop()