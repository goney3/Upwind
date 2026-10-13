"""
tui/app.py - Upwind TUI shell: header, sidebar navigation, screen router,
and the curses main loop.
"""

import curses
from tui.theme import Theme
from tui.widgets import Menu, TextView, put, seg, draw_lines, wrap_text, u
from tui.asciiart import LOGO, MARK
from tui.diagrams import build_diagram_screens, ArtScreen
from tui.tools import build_tool_screens
from tui.study import QuizSelectorScreen, FlashcardScreen
from tui.quiz import QuizScreen
from data.curriculum import get_study_content
from data.questions import get_question_pool

SIDEBAR_W = 32

CURRICULUM_GROUPS = [
    ("REGULATIONS & LEGAL", [
        "FAR Part 103 Overview", "FAR Part 103 Operations", "FAA AC 103-7 Weight Credits"]),
    ("ENGINES & PROPULSION", [
        "Two-Stroke Engines & Fuel Systems",
        "Four-Stroke Aero Engines: Half-VW & Conversions",
        "Industrial Four-Stroke Conversions (Briggs Vanguard & Kohler V-Twins)"]),
    ("FLIGHT ENVIRONMENT", [
        "Airspace for Ultralights", "Basic Weather for VFR Flight",
        "Navigation and Sectional Charts", "Airport Operations and Markings"]),
    ("HANDLING & SAFETY", [
        "Aerodynamics & Low Wing Loading", "Weight, Balance & Control Types",
        "Ultralight Systems & Preflight", "Human Factors (ADM & IMSAFE)",
        "Emergency Procedures & Survival"]),
]


class DashboardScreen(ArtScreen):
    def __init__(self, app):
        lines = []
        for ln in LOGO:
            lines.append([seg(ln, "accent")])
        lines.append([seg(" PART 103 GROUND SCHOOL & FLIGHT SUITE", "white")])
        lines.append([])
        intro = ("Because FAR Part 103 mandates zero flight training, medical exams, or written "
                 "tests, ultralight aviators bear 100% of the responsibility for their own "
                 "airworthiness and survival. This ground school delivers the aerodynamics, "
                 "regulations, two-stroke/four-stroke engine management, and emergency recovery "
                 "disciplines necessary to protect your life.")
        for ln in wrap_text(intro, 66):
            lines.append([seg(" " + ln, "muted")])
        lines.append([])
        cards = [
            ("LEGAL THRESHOLDS", "green",
             "Empty Weight < 254 lbs (Powered) | Fuel 5 gal max | Speed 55 kts | Stall 24 kts"),
            ("ENGINE ENVELOPES", "amber",
             "2-Stroke: idle descents starve oil; CHT > 250F warmup. 4-Stroke: oil 160-220F, "
             "30-40 PSI; cold valve lash 0.006\"."),
            ("AIRSPACE RULES", "accent",
             "Class G native ground. Prior ATC authorization for B, C, D & surface E. "
             "Class G <=1,200': 1 SM visibility, clear of clouds."),
        ]
        for title, style, body in cards:
            lines.append([seg(" " + u("╔") + " " + title + " ", style)])
            for ln in wrap_text(body, 64):
                lines.append([seg(" " + u("║") + " " + ln, style)])
            lines.append([seg(" " + u("╚") + u("═" * 66), style)])
        lines.append([])
        lines.append([seg(" Start here: press ", "white"), seg("Tab", "accent"),
                      seg(" to reach the sidebar, then Enter on ", "white"),
                      seg("20-QUESTION PRACTICE EXAM", "cta"), seg(".", "white")])
        super().__init__(app, "Dashboard & Overview", lines)


_CSI_FINALS = {
    ord("A"): curses.KEY_UP, ord("B"): curses.KEY_DOWN,
    ord("C"): curses.KEY_RIGHT, ord("D"): curses.KEY_LEFT,
    ord("H"): curses.KEY_HOME, ord("F"): curses.KEY_END,
}


def read_key(scr):
    """
    getch() plus a fallback for arrow / PgUp / PgDn escape sequences.

    curses decodes the SS3 forms its terminfo advertises (it switches the
    keypad to application mode), but a terminal left in normal cursor mode
    sends the CSI forms instead, and getch hands those back as a bare ESC -
    which would read as "go back", and twice in a row as "quit". Decode them
    here so an arrow key always means an arrow key. Returns None for a
    sequence we do not understand, so it is swallowed instead of misread.
    """
    ch = scr.getch()
    if ch != 27:
        return ch
    scr.timeout(50)
    try:
        nxt = scr.getch()
        if nxt == -1:                       # a lone Escape press
            return 27
        if nxt in (ord("["), ord("O")):
            last = scr.getch()
            if last in _CSI_FINALS:
                return _CSI_FINALS[last]
            if last == ord("5"):
                scr.getch()                 # trailing '~'
                return curses.KEY_PPAGE
            if last == ord("6"):
                scr.getch()
                return curses.KEY_NPAGE
            return None
        curses.ungetch(nxt)                 # Escape then a real key: two presses
        return 27
    finally:
        scr.timeout(-1)


class UpwindApp:
    def __init__(self, stdscr):
        self.scr = stdscr
        self.theme = Theme()
        self.theme.setup()
        self.study_content = get_study_content()
        self.question_pool = get_question_pool()
        self.current = None
        self.focus = "side"
        self.running = True
        self._diagram_screens = build_diagram_screens(self)
        self._tool_screens = build_tool_screens(self)
        self.sidebar = Menu(self._build_items())
        self.open_dashboard()

    # ------------------------------------------------------------------
    def _build_items(self):
        items = [("cta", u(" ^ ") + " 20-QUESTION PRACTICE EXAM",
                  lambda: self.start_quiz(None))]
        items.append(("item", "Dashboard & Overview", self.open_dashboard))
        items.append(("section", "PRACTICAL FLIGHT TOOLS"))
        for name in self._tool_screens:
            items.append(("item", name, lambda n=name: self.open_tool(n)))
        items.append(("section", "VISUAL CHARTS & DIAGRAMS"))
        for name in self._diagram_screens:
            items.append(("item", name, lambda n=name: self.open_diagram(n)))
        for group, topics in CURRICULUM_GROUPS:
            items.append(("section", group))
            for t in topics:
                items.append(("item", t, lambda tt=t: self.open_topic(tt)))
        items.append(("section", "STUDY & TESTING"))
        items.append(("item", "Topic-Targeted Quizzes", self.open_quiz_selector))
        items.append(("item", "Flashcard Review Mode", self.open_flashcards))
        return items

    def _set(self, screen):
        self.current = screen
        self.current.on_enter()
        self.focus = "content"

    def open_dashboard(self):
        self._set(DashboardScreen(self))

    def open_topic(self, title):
        body = self.study_content.get(title, "Content being updated.")
        self._set(TextView(self, title, body=body))

    def open_tool(self, name):
        self._set(self._tool_screens[name]())

    def open_diagram(self, name):
        self._set(self._diagram_screens[name]())

    def open_quiz_selector(self):
        self._set(QuizSelectorScreen(self))

    def open_flashcards(self):
        self._set(FlashcardScreen(self, self.question_pool))

    def start_quiz(self, category_filter):
        self._set(QuizScreen(self, self.question_pool, category_filter))

    def content_height(self):
        return curses.LINES - 4

    # ------------------------------------------------------------------
    def draw(self):
        scr, theme = self.scr, self.theme
        h, w = scr.getmaxyx()
        scr.erase()
        # header
        put(scr, 0, 1, MARK + " ", theme.attr("accent", bold=True))
        put(scr, 0, 1 + len(MARK) + 1, "Upwind: Part 103 Prep", theme.attr("header", bold=True))
        put(scr, 0, 24, u("· FAA FAR Part 103 Flight Safety & 2/4-Stroke Suite"),
            theme.attr("muted_hdr"))
        badge = f" {len(self.question_pool)} Exam Questions "
        put(scr, 0, max(0, w - len(badge) - 1), badge, theme.attr("badge", bold=True))
        put(scr, 1, 0, u("─" * w), theme.attr("muted"))
        # sidebar
        self.sidebar.draw(scr, 0, 2, SIDEBAR_W, h - 3, theme, self.focus == "side")
        put(scr, 2, SIDEBAR_W, u("│"), theme.attr("muted"))
        # content
        if self.current:
            self.current.draw(scr, SIDEBAR_W + 1, 2, w - SIDEBAR_W - 1, h - 3)
        # footer
        hints = ("Tab focus · Enter open · ↑/↓ move · Esc back · Ctrl+Q quit")
        put(scr, h - 1, 0, " " + hints, theme.attr("footer"))
        if self.current and self.current.cursor and self.focus == "content":
            try:
                curses.curs_set(1)
                scr.move(*self.current.cursor)
            except curses.error:
                pass
        else:
            try:
                curses.curs_set(0)
            except curses.error:
                pass
        scr.noutrefresh()
        curses.doupdate()

    def run(self):
        curses.curs_set(0)
        self.scr.keypad(True)
        try:  # let Ctrl+Q reach getch() instead of acting as XON flow control
            import sys, termios
            attrs = termios.tcgetattr(sys.stdin.fileno())
            # IXON/IXANY live in c_iflag (index 0), not c_oflag - with them set
            # the tty swallows Ctrl+Q as an XON restart character.
            attrs[0] &= ~(termios.IXON | termios.IXANY)
            attrs[0] &= ~getattr(termios, "IXOFF", 0)
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, attrs)
        except Exception:
            pass
        while self.running:
            self.draw()
            ch = read_key(self.scr)
            if ch is None:
                continue
            if ch == curses.KEY_RESIZE:
                curses.update_lines_cols()
                continue
            if ch == 17:  # Ctrl+Q
                self.running = False
            elif ch == 3:  # Ctrl+C
                self.running = False
            elif ch == 9:  # Tab
                self.focus = "side" if self.focus == "content" else "content"
            elif ch == 27:  # Esc
                if self.focus == "content":
                    self.focus = "side"
                else:
                    self.running = False
            elif ch == ord("q") and self.focus == "side":
                self.running = False
            elif ch == ord("q") and self.focus == "content":
                self.focus = "side"
            elif self.focus == "side":
                self.sidebar.key(ch)
            elif self.current:
                self.current.key(ch)
