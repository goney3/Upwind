"""
tui/quiz.py - Practice exam engine with IMMEDIATE feedback per question
(user's chosen flow): answer -> instantly shown correct/incorrect plus the
safety explanation, then advance.
"""

import curses
import random
from tui.widgets import Screen, seg, draw_lines, draw_box, wrap_text, put, u


class QuizScreen(Screen):
    def __init__(self, app, pool, category_filter=None):
        super().__init__(app)
        self.build_exam(pool, category_filter)

    def build_exam(self, pool, category_filter=None):
        if category_filter:
            sel = [q for q in pool if any(
                k.lower() in q["question_text"].lower() or k.lower() in q["explanation"].lower()
                for k in category_filter)]
            if len(sel) < 5:
                sel = pool
        else:
            sel = pool
        self.questions = random.sample(sel, min(20, len(sel)))
        self.idx = 0
        self.answers = {}
        self.phase = "question"
        self.sel = 0
        self.offset = 0

    # ------------------------------------------------------------------
    def draw(self, scr, x, y, w, h):
        theme = self.app.theme
        if self.phase == "results":
            self._draw_results(scr, x, y, w, h)
            return
        q = self.questions[self.idx]
        card_h = h - 2
        draw_box(scr, x + 1, y, w - 2, card_h, theme.attr("muted"))
        r = y + 1
        pct = int(self.idx / len(self.questions) * 100)
        put(scr, r, x + 3, f"QUESTION {self.idx + 1} OF {len(self.questions)}",
            theme.attr("accent", bold=True))
        put(scr, r, x + w - 18, f"Progress: {pct}%", theme.attr("muted"))
        r += 2
        for ln in wrap_text(q["question_text"], w - 8):
            put(scr, r, x + 4, ln, theme.attr("card_title", bold=True))
            r += 1
        r += 1
        answered = self.phase == "feedback"
        for i, opt in enumerate(q["options"]):
            mark = " "
            style = "card"
            if answered:
                if opt == q["correct_answer"]:
                    mark, style = u("v"), "green"
                elif i == self.answers.get(self.idx):
                    mark, style = u("x"), "red"
            elif i == self.sel:
                style = "side_sel"
            if answered and i == self.answers.get(self.idx):
                put(scr, r, x + 4, f" {i + 1}) {mark} " + opt[:w - 12], theme.attr(style, bold=True))
            else:
                a = theme.attr("side_sel") if style == "side_sel" else theme.attr(style)
                put(scr, r, x + 4, f" {i + 1}) " + opt[:w - 10], a)
            r += 1
        if answered:
            r += 1
            ok = self.answers.get(self.idx) == q["correct_answer"]
            put(scr, r, x + 4, "CORRECT - well airmanned!" if ok else "INCORRECT - study this:",
                theme.attr("green" if ok else "red", bold=True))
            r += 1
            for ln in wrap_text(q["explanation"], w - 10):
                put(scr, r, x + 6, ln, theme.attr("amber"))
                r += 1
            put(scr, y + card_h - 1, x + 3,
                ("n: next question" if self.idx < len(self.questions) - 1 else "n: finish exam")
                + " · Esc quit exam", theme.attr("muted"))
        else:
            put(scr, y + card_h - 1, x + 3,
                "1-4 or ↑/↓+Enter to answer · Esc quit exam", theme.attr("muted"))

    def _draw_results(self, scr, x, y, w, h):
        theme = self.app.theme
        score = sum(1 for i, q in enumerate(self.questions)
                    if self.answers.get(i) == q["correct_answer"])
        pct = score / len(self.questions) * 100
        passed = pct >= 80
        wrong = [(q, self.answers.get(i, "None")) for i, q in enumerate(self.questions)
                 if self.answers.get(i) != q["correct_answer"]]
        lines = [
            [seg(" EXAM PASSED (PROFICIENT)" if passed else " SAFETY REVIEW RECOMMENDED (<80%)",
                 "green" if passed else "red")],
            [seg(f" Your Score: {score} / {len(self.questions)} ({pct:.1f}%)", "white")],
            [seg(" a: take another exam · Esc back to dashboard", "muted")],
            [],
            [seg(" QUESTIONS REQUIRING SAFETY REVIEW" if wrong else " v FLAWLESS SWEEP - no misses.",
                 "red" if wrong else "green")],
        ]
        for q, ua in wrong:
            lines.append([seg(" x " + q["question_text"], "white")])
            lines.append([seg(f"   Your answer: {ua}", "red")])
            lines.append([seg(u(" v ") + "Correct: " + q["correct_answer"], "green")])
            for ln in wrap_text(q["explanation"], w - 10):
                lines.append([seg("   " + ln, "muted")])
            lines.append([])
        visible = h - 2
        self.offset = max(0, min(self.offset, max(0, len(lines) - visible)))
        draw_box(scr, x + 1, y, w - 2, h - 1, theme.attr("muted"))
        draw_lines(scr, y + 1, x + 3, w - 6, lines[self.offset:self.offset + visible],
                   theme, theme.attr("card"))

    # ------------------------------------------------------------------
    def key(self, ch):
        if self.phase == "results":
            if ch == ord("a"):
                self.build_exam(self.app.question_pool)
            elif ch in (curses.KEY_UP, ord("k")):
                self.offset -= 1
            elif ch in (curses.KEY_DOWN, ord("j")):
                self.offset += 1
            elif ch in (curses.KEY_NPAGE,):
                self.offset += 10
            elif ch in (curses.KEY_PPAGE,):
                self.offset -= 10
            else:
                return False
            return True
        q = self.questions[self.idx]
        if self.phase == "question":
            if 49 <= ch <= 52 and ch - 49 < len(q["options"]):
                self._answer(ch - 49)
            elif ch in (curses.KEY_UP, ord("k")):
                self.sel = (self.sel - 1) % len(q["options"])
            elif ch in (curses.KEY_DOWN, ord("j")):
                self.sel = (self.sel + 1) % len(q["options"])
            elif ch in (curses.KEY_ENTER, 10, 13):
                self._answer(self.sel)
            else:
                return False
            return True
        # feedback phase
        if ch == ord("n"):
            self.idx += 1
            self.sel = 0
            if self.idx >= len(self.questions):
                self.phase = "results"
                self.offset = 0
            else:
                self.phase = "question"
        elif 49 <= ch <= 52:
            pass  # ignore re-answers
        else:
            return False
        return True

    def _answer(self, i):
        q = self.questions[self.idx]
        self.answers[self.idx] = q["options"][i]
        self.phase = "feedback"
