#!/usr/bin/env python3
"""
upwind_tui.py - Terminal (curses) front end for Upwind: FAA FAR Part 103
Prep Ground School. Runs alongside the Tkinter app (upwind.py); shares the
same data/curriculum, question pool, and regulatory constants.

Run:  python3 upwind_tui.py
Keys: Tab focus | Enter open | 1-4 answer | Space toggle/reveal |
      Esc back/quit | Ctrl+Q quit
"""

# ==============================================================================
# DISCLAIMER OF LIABILITY, WARRANTY, AND AVIATION SAFETY NOTICE
# ==============================================================================
# This software ("Upwind" / "Upwind-103 Flight Prep & Ground School Suite") is 
# provided "AS IS", without warranty of any kind, express or implied, including 
# but not limited to the warranties of merchantability, fitness for a particular 
# purpose, noninfringement, and accuracy of data.
#
# 1. EDUCATIONAL & INFORMATIONAL USE ONLY:
# This software is designed solely for informal self-study, recreational education, 
# and conceptual training. It is NOT an FAA-certificated ground school, flight 
# training course, or official airman syllabus. It does NOT replace qualified dual 
# flight instruction, certified ground instruction, or official FAA publications.
#
# 2. FLIGHT PLANNING & CALCULATOR APPROXIMATIONS:
# All mathematical models, performance estimates, and calculators provided by 
# this software—including but not limited to Weight & Balance, Center of Gravity, 
# Density Altitude, Crosswind Vectors, Propeller Tip Speeds, and Forced Landing 
# Glide Cones—are theoretical approximations based on generic algorithms. They do 
# NOT substitute for actual weight scales, physical center of gravity balancing, 
# manufacturer pilot operating handbooks (POH), or certified weather briefings.
#
# 3. SOLE RESPONSIBILITY OF THE PILOT-IN-COMMAND:
# Aviation, particularly the operation of ultralight vehicles and amateur-built 
# aircraft, involves inherent risks of property damage, serious bodily injury, 
# and death. Under Title 14 CFR Part 103, the operator bears 100% of the legal, 
# operational, and physical responsibility for vehicle airworthiness, regulatory 
# compliance, and flight safety.
#
# 4. LIMITATION OF LIABILITY & INDEMNIFICATION:
# In no event shall the author(s), contributor(s), or copyright holder(s) be 
# liable for any claim, damages, injury, death, or other liability—whether in an 
# action of contract, tort (including negligence), or otherwise—arising from, 
# out of, or in connection with the software, its calculations, or the use or 
# other dealings in the software.
#
# By downloading, running, or referencing this software, you explicitly agree to 
# assume all risks associated with its use and hold the author(s) harmless from 
# any and all claims, demands, damages, or litigation.
# ==============================================================================

import curses
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tui.app import UpwindApp  # noqa: E402

MIN_H, MIN_W = 24, 100


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    h, w = stdscr.getmaxyx()
    if h < MIN_H or w < MIN_W:
        stdscr.addstr(0, 0, f"Upwind TUI needs at least {MIN_W}x{MIN_H}; "
                            f"terminal is {w}x{h}. Resize and rerun.")
        stdscr.getch()
        return
    UpwindApp(stdscr).run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    print("Upwind TUI closed. Fly safe.")
