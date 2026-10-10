"""
ui_components.py - Custom Modern Controls & Aviator Academy Vector Logo Engine.
Features mathematical procedural rendering for the "Upwind" 2-Blade Scimitar & Compass Emblem.
Zero external image or library dependencies (Pure Python Standard Library).
"""

import tkinter as tk
from tkinter import Label
import math

# -----------------------------------------------------------------------------
# HIGH-CONTRAST CUSTOM BUTTON (CROSS-PLATFORM TKINTER COMPLIANT)
# -----------------------------------------------------------------------------
class ModernButton(Label):
    """Cross-platform custom button built on Tkinter Label to bypass macOS Aqua theming limits."""
    def __init__(self, master=None, text="", command=None, bg="#2f3136", fg="#ffffff",
                 hover_bg="#3ba55d", active_bg="#5865f2", font=("Helvetica", 10, "bold"),
                 padx=10, pady=6, width=None, anchor="w", cursor="hand2", **kwargs):
        super().__init__(master=master, text=text, font=font, bg=bg, fg=fg,
                         padx=padx, pady=pady, anchor=anchor, cursor=cursor, **kwargs)
        if width:
            self.configure(width=width)
        self.default_bg = bg
        self.default_fg = fg
        self.hover_bg = hover_bg
        self.active_bg = active_bg
        self.command = command
        self.is_selected = False

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, e):
        if not self.is_selected:
            self.configure(bg=self.hover_bg, fg="#ffffff")

    def _on_leave(self, e):
        if not self.is_selected:
            self.configure(bg=self.default_bg, fg=self.default_fg)

    def _on_click(self, e):
        if self.command:
            self.command()

    def set_active_state(self, active=True):
        self.is_selected = active
        if active:
            self.configure(bg=self.active_bg, fg="#ffffff")
        else:
            self.configure(bg=self.default_bg, fg=self.default_fg)


# -----------------------------------------------------------------------------
# PROCEDURAL GEOMETRY GENERATORS (AVIATOR ACADEMY ROUNDEL)
# -----------------------------------------------------------------------------
def _get_prop_blade_polygon(cx, cy, length, width, sweep, angle_deg, steps=16):
    """Calculates smooth, aerodynamic scimitar blade contours."""
    rad = math.radians(angle_deg)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    pts_left, pts_right = [], []
    
    for i in range(steps + 1):
        t = i / float(steps)
        # Airfoil bulge curve (peaks at ~60% span)
        w = width * (math.sin(math.pi * t) ** 0.7)
        sw = sweep * (t ** 1.8)
        y = length * t
        pts_left.append((-w * 0.45 + sw, y))
        pts_right.append((w * 0.55 + sw, y))
    
    # Smooth rounded tip
    tip_pts = []
    tip_r = width * 0.2
    for j in range(5):
        th = math.pi - (j / 4.0) * math.pi
        tip_pts.append((sweep + tip_r * math.cos(th), length + tip_r * math.sin(th)))
        
    loop = pts_left + tip_pts + pts_right[::-1]
    
    # Rotate points and translate to canvas center (inverting Y for Tkinter canvas)
    flat = []
    for x, y in loop:
        rx = x * cos_a - y * sin_a
        ry = x * sin_a + y * cos_a
        flat.extend([cx + rx, cy - ry])
    return flat


def _get_book_page_polygon(cx, cy, x_sign, layer, scale, steps=14):
    """Calculates smooth gull-wing open book curves representing flight manual pages."""
    pts_top, pts_bot = [], []
    for i in range(steps + 1):
        t = i / float(steps)
        x = x_sign * (3.5 + 32.0 * t) * scale
        # S-curve page arch
        y_top = (-12.0 + 9.5 * math.sin(t * math.pi * 0.8) + layer * 3.5) * scale
        y_bot = y_top - 5.0 * scale
        pts_top.append((x, y_top))
        pts_bot.append((x, y_bot))
        
    loop = pts_top + pts_bot[::-1]
    flat = []
    for x, y in loop:
        flat.extend([cx + x, cy - y])
    return flat


def draw_fitted_logo(canvas, size, bg_circle_color="#5865f2"):
    """
    Renders Option 1: Aviator Academy Roundel.
    
    Elements:
      - Outer Accent Bezel & Graphite Inner Field
      - Navigational Compass Ring with Tick Marks
      - Golden North 'Upwind' Vector Chevron
      - Aerodynamic Open Flight Manual Pages & Gold Bookmark Ribbon
      - 2-Blade Polished Scimitar Propeller (38° Dynamic Pitch)
      - Polished Two-Tone Center Spinner & Bolt Core
    """
    canvas.delete("all")
    scale = size / 120.0
    cx = size / 2.0
    cy = size / 2.0

    # 1. Outer Accent Ring
    r_outer = 56.0 * scale
    canvas.create_oval(cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer, 
                       fill=bg_circle_color, outline="")

    # 2. Dark Instrument Field
    r_field = 52.0 * scale
    canvas.create_oval(cx - r_field, cy - r_field, cx + r_field, cy + r_field, 
                       fill="#1e2124", outline="")

    # 3. Inner Compass Bezel Ring
    r_ring = 48.0 * scale
    canvas.create_oval(cx - r_ring, cy - r_ring, cx + r_ring, cy + r_ring, 
                       fill="", outline=bg_circle_color, width=max(1.0, 1.5 * scale))

    # 4. Compass Tick Marks (Every 30 Degrees)
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        l = (6.0 if deg % 90 == 0 else 3.5) * scale
        col = "#ffffff" if deg % 90 == 0 else bg_circle_color
        x1 = cx + (r_ring - 1.0 * scale) * math.sin(rad)
        y1 = cy - (r_ring - 1.0 * scale) * math.cos(rad)
        x2 = cx + (r_ring - 1.0 * scale - l) * math.sin(rad)
        y2 = cy - (r_ring - 1.0 * scale - l) * math.cos(rad)
        canvas.create_line(x1, y1, x2, y2, fill=col, width=max(1.0, (1.5 if deg % 90 == 0 else 1.0) * scale))

    # 5. Golden North 'Upwind' Climb Arrow
    na = [[0, -47], [-4.0, -39], [0, -41], [4.0, -39]]
    na_flat = [coord for pt in na for coord in (cx + pt[0] * scale, cy + pt[1] * scale)]
    canvas.create_polygon(na_flat, fill="#faa61a", outline="")

    # 6. Open Book / Flight Manual (Lower Shadow Pages + Upper White Pages)
    canvas.create_polygon(_get_book_page_polygon(cx, cy, -1, 0, scale), fill="#4f545c", outline="")
    canvas.create_polygon(_get_book_page_polygon(cx, cy, 1, 0, scale), fill="#4f545c", outline="")
    canvas.create_polygon(_get_book_page_polygon(cx, cy, -1, 1, scale), fill="#dcddde", outline="")
    canvas.create_polygon(_get_book_page_polygon(cx, cy, 1, 1, scale), fill="#ffffff", outline="")

    # 7. Spine Ribbon Bookmark
    sp = [[-2.5, -20], [0, -18], [2.5, -20], [1.5, -7], [0, -6], [-1.5, -7]]
    sp_flat = [coord for pt in sp for coord in (cx + pt[0] * scale, cy - pt[1] * scale)]
    canvas.create_polygon(sp_flat, fill="#faa61a", outline="")

    # 8. 2-Blade Scimitar Propeller (Tilted 38°)
    b1_pts = _get_prop_blade_polygon(cx, cy, length=40.0 * scale, width=8.5 * scale, sweep=2.0 * scale, angle_deg=38)
    b2_pts = _get_prop_blade_polygon(cx, cy, length=40.0 * scale, width=8.5 * scale, sweep=2.0 * scale, angle_deg=218)
    canvas.create_polygon(b1_pts, fill="#ffffff", outline="#1e2124", width=max(1.0, 1.0 * scale))
    canvas.create_polygon(b2_pts, fill="#ffffff", outline="#1e2124", width=max(1.0, 1.0 * scale))

    # 9. Polished Hub / Spinner Core
    r_hub = 8.0 * scale
    canvas.create_oval(cx - r_hub, cy - r_hub, cx + r_hub, cy + r_hub, 
                       fill="#faa61a", outline="#ffffff", width=max(1.0, 1.5 * scale))
    r_hub_in = 4.0 * scale
    canvas.create_oval(cx - r_hub_in, cy - r_hub_in, cx + r_hub_in, cy + r_hub_in, 
                       fill="#ffffff", outline="")
    r_bolt = 1.8 * scale
    canvas.create_oval(cx - r_bolt, cy - r_bolt, cx + r_bolt, cy + r_bolt, 
                       fill="#18191c", outline="")