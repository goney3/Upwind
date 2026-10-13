"""tui/study.py - Study topic viewer, flashcard review, quiz topic selector."""

import curses
import random
from tui.widgets import Screen, TextView, Menu, seg, draw_lines, draw_box, wrap_text, put, u


class QuizSelectorScreen(Screen):
    TOPICS = [
        ("FAR Part 103 Regulations", "Empty weights, fuel, daylight/twilight, right-of-way.",
         ["103", "empty weight", "gallons", "twilight", "congested"]),
        ("Engine Management (2 & 4-Stroke)", "Half-VW, V-Twins, governors, PSRU, cold seizures.",
         ["stroke", "half-vw", "v-twin", "governor", "seizure", "oil", "egt", "lash", "propeller"]),
        ("Aerodynamics, Load Factors & Turns", "Stalls, spins, bank G-loads, base-to-final skid traps.",
         ["stall", "bank", "load factor", "g-load", "spin", "rudder"]),
        ("Airspace, Weather & Forced Landings", "Class B/C/D/G minimums, density alt, glide reach.",
         ["class", "airspace", "density altitude", "glide", "headwind"]),
    ]

    def __init__(self, app):
        super().__init__(app)
        items = [("section", "TOPIC-TARGETED KNOWLEDGE EXAMS")]
        for title, desc, kw in self.TOPICS:
            items.append(("item", f"Start: {title}", lambda kw=kw: self.app.start_quiz(kw)))
        self.menu = Menu(items)

    def draw(self, scr, x, y, w, h):
        theme = self.app.theme
        draw_box(scr, x + 1, y, w - 2, min(h - 1, 16), theme.attr("muted"))
        put(scr, y, x + 3, " Topic-Targeted Knowledge Exams ", theme.attr("card_title", bold=True))
        put(scr, y + 1, x + 3, "Focus on a discipline; Enter launches a tailored quiz.", theme.attr("muted"))
        self.menu.draw(scr, x + 3, y + 3, w - 6, min(h - 6, 12), theme, True)
        put(scr, y + min(h - 1, 16) - 1, x + 3, "Enter select · Esc back", theme.attr("muted"))

    def key(self, ch):
        return self.menu.key(ch)


class FlashcardScreen(Screen):
    def __init__(self, app, pool):
        super().__init__(app)
        self.pool = pool
        self.idx = 0
        self.revealed = False

    def draw(self, scr, x, y, w, h):
        theme = self.app.theme
        q = self.pool[self.idx]
        card_h = h - 2
        draw_box(scr, x + 1, y, w - 2, card_h, theme.attr("muted"))
        r = y + 1
        put(scr, r, x + 3, f"CARD {self.idx + 1} OF {len(self.pool)}", theme.attr("accent", bold=True))
        r += 2
        for ln in wrap_text(q["question_text"], w - 8):
            put(scr, r, x + 4, ln, theme.attr("card_title", bold=True))
            r += 1
        r += 1
        if self.revealed:
            put(scr, r, x + 4, "CORRECT ANSWER:", theme.attr("green", bold=True))
            r += 1
            for ln in wrap_text(q["correct_answer"], w - 10):
                put(scr, r, x + 6, u("v") + " " + ln, theme.attr("green"))
                r += 1
            r += 1
            put(scr, r, x + 4, "SAFETY EXPLANATION:", theme.attr("muted", bold=True))
            r += 1
            for ln in wrap_text(q["explanation"], w - 10):
                put(scr, r, x + 6, ln, theme.attr("card"))
                r += 1
        else:
            put(scr, r, x + 4, "Press SPACE to reveal the answer.", theme.attr("muted"))
        put(scr, y + card_h - 1, x + 3,
            "Space reveal · n/p next/prev · s shuffle · Esc back", theme.attr("muted"))

    def key(self, ch):
        if ch == ord(" ") or ch in (curses.KEY_ENTER, 10, 13):
            self.revealed = True
        elif ch == ord("n"):
            self.idx = (self.idx + 1) % len(self.pool)
            self.revealed = False
        elif ch == ord("p"):
            self.idx = (self.idx - 1) % len(self.pool)
            self.revealed = False
        elif ch == ord("s"):
            self.idx = random.randrange(len(self.pool))
            self.revealed = False
        else:
            return False
        return True
