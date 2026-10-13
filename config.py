"""
config.py - Central design system, themes, and aeronautical constants.
"""

# Palette
BG_ROOT = '#18191c'
BG_SIDEBAR = '#202225'
BG_CONTENT = '#2f3136'
BG_CARD = '#36393f'
ACCENT_COLOR = '#5865f2'
ACCENT_GREEN = '#3ba55d'
ACCENT_AMBER = '#faa61a'
ACCENT_RED = '#ed4245'
TEXT_PRIMARY = '#ffffff'
TEXT_MUTED = '#b9bbbe'
BORDER_COLOR = '#40444b'

# Airspace Palette
AIRSPACE_COLORS = {
    "class_a": "#a92a34",
    "class_e_main": "#2a623d",
    "class_g": "#98c09f",
    "class_b_dark": "#4a63a2",
    "class_b_light": "#6c82c3",
    "class_c_dark": "#8e477f",
    "class_c_light": "#b06ca6",
    "class_d_dark": "#2a83a2",
    "class_d_light": "#4fa5c4",
    "background": "#ffffff",
    "text_light": "#ffffff",
    "text_dark": "#000000"
}

# Typography
FONT_TITLE = ("Helvetica", 17, "bold")
FONT_SECTION = ("Helvetica", 13, "bold")
FONT_BODY = ("Helvetica", 11)
FONT_BODY_BOLD = ("Helvetica", 11, "bold")
FONT_SMALL = ("Helvetica", 9)
FONT_SMALL_BOLD = ("Helvetica", 9, "bold")

# FAA FAR Part 103 Regulatory Limits
MAX_EMPTY_WEIGHT_POWERED_LBS = 254.0
MAX_EMPTY_WEIGHT_UNPOWERED_LBS = 155.0
MAX_FUEL_CAPACITY_GALLONS = 5.0
MAX_TOP_SPEED_KTS = 55.0          # 63 mph
MAX_STALL_SPEED_KTS = 24.0        # 28 mph
BRS_WEIGHT_ALLOWANCE_LBS = 24.0
AMPHIB_FLOAT_ALLOWANCE_LBS = 60.0
SINGLE_FLOAT_ALLOWANCE_LBS = 30.0

# Weight & Balance teaching model. Shared by the Tkinter and curses front ends
# so the two can never drift apart. Stations are inches aft of the datum. The
# baggage/equipment station sits well aft of the wing (52") so an aft-CG loading
# is genuinely reachable, and the legal band is only 3.0" wide, so a heavy pilot
# with no fuel or ballast runs out the forward limit. Both failure modes the
# lesson is meant to teach.
WB_EMPTY_ARM = 28.5
WB_PILOT_ARM = 25.0
WB_FUEL_ARM = 36.0
WB_BAGGAGE_ARM = 52.0
WB_CL_ARM = 28.5
WB_FWD_LIMIT = 27.5
WB_AFT_LIMIT = 30.5
WB_FUEL_LB_PER_GAL = 6.0
WB_MIN_PILOT_LBS = 100.0
WB_MAX_PILOT_LBS = 280.0
WB_MAX_BAGGAGE_LBS = 50.0
WB_SCALE_MIN_IN = 25.0            # beam diagram scale, in inches aft of datum
WB_SCALE_MAX_IN = 32.0