import tkinter as tk
from tkinter import scrolledtext, Canvas, Frame, Scrollbar, Label
import random
import textwrap
import re
import math

#  Canvas created Logo at the top of the app:
def hex_to_rgb(hex_color):
    return hex_color

def parse_style_string(style_str):
    styles = {}
    if style_str:
        for part in style_str.split(';'):
            if ':' in part:
                key, value = part.split(':', 1)
                styles[key.strip()] = value.strip()
    return styles

def parse_transform_matrix(transform_str):
    match = re.match(r'matrix\(([^)]*)\)', transform_str)
    if match:
        values = [float(x) for x in re.split(r'[,\s]+', match.group(1).strip())]
        if len(values) == 6:
            return values
    return [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

def apply_matrix_transform(x, y, matrix):
    a, b, c, d, e, f = matrix
    new_x, new_y = a * x + c * y + e, b * x + d * y + f
    return new_x, new_y

def get_ellipse_points(cx, cy, rx, ry, num_segments=100):
    points = []
    for i in range(num_segments + 1):
        angle = 2 * math.pi * i / num_segments
        x, y = cx + rx * math.cos(angle), cy + ry * math.sin(angle)
        points.append((x, y))
    return points

def parse_svg_path_d(d_string):
    points, current_x, current_y = [], 0.0, 0.0
    pattern = re.compile(r'([MLlv])\s*([^MLlv]*)', re.IGNORECASE)
    for match in pattern.finditer(d_string):
        cmd, args_str = match.group(1), match.group(2).strip()
        numbers = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', args_str)]
        if cmd.upper() == 'M':
            if len(numbers) % 2 != 0: continue
            current_x, current_y = (numbers[0], numbers[1]) if cmd == 'M' else (current_x + numbers[0], current_y + numbers[1])
            points.append((current_x, current_y))
            for i in range(2, len(numbers), 2):
                current_x, current_y = (numbers[i], numbers[i+1]) if cmd == 'M' else (current_x + numbers[i], current_y + numbers[i+1])
                points.append((current_x, current_y))
        elif cmd.upper() == 'L':
            if len(numbers) % 2 != 0: continue
            for i in range(0, len(numbers), 2):
                current_x, current_y = (numbers[i], numbers[i+1]) if cmd == 'L' else (current_x + numbers[i], current_y + numbers[i+1])
                points.append((current_x, current_y))
        elif cmd.upper() == 'V':
            for val in numbers:
                current_y = val if cmd == 'V' else current_y + val
                points.append((current_x, current_y))
    return points

# --- Main Drawing Function ---
def draw_svg_elements_on_tkinter(canvas, svg_elements_data, x_offset=0, y_offset=0):
    """
    Draws a list of simplified SVG elements onto a Tkinter Canvas,
    applying an offset to all coordinates.
    """
    for element in svg_elements_data:
        element_type, styles = element['type'], parse_style_string(element['style'])
        fill_color = hex_to_rgb(styles.get('fill', ''))
        stroke_color = hex_to_rgb(styles.get('stroke', ''))
        stroke_width = float(styles.get('stroke-width', 1.0))
        
        if styles.get('stroke') == 'none': stroke_color = ''
        if styles.get('fill') == 'none': fill_color = ''

        if element_type == 'circle':
            cx, cy, r = float(element['cx']), float(element['cy']), float(element['r'])
            x1, y1 = cx - r + x_offset, cy - r + y_offset
            x2, y2 = cx + r + x_offset, cy + r + y_offset
            canvas.create_oval(x1, y1, x2, y2, fill=fill_color, outline=stroke_color, width=stroke_width)

        elif element_type == 'ellipse':
            cx, cy, rx, ry = float(element['cx']), float(element['cy']), float(element['rx']), float(element['ry'])
            transform_matrix = parse_transform_matrix(element.get('transform', ''))
            ellipse_points = get_ellipse_points(cx, cy, rx, ry)
            
            transformed_points = [apply_matrix_transform(px, py, transform_matrix) for px, py in ellipse_points]
            offset_points = [(px + x_offset, py + y_offset) for px, py in transformed_points]
            flat_points = [coord for point in offset_points for coord in point]
            
            canvas.create_polygon(flat_points, fill=fill_color, outline=stroke_color, width=stroke_width, smooth=False)

        elif element_type == 'path':
            path_points = parse_svg_path_d(element['d'])
            
            offset_points = [(px + x_offset, py + y_offset) for px, py in path_points]
            flat_coords = [coord for point in offset_points for coord in point]
            
            if len(flat_coords) >= 4:
                canvas.create_line(flat_coords, fill=stroke_color, width=stroke_width, joinstyle=tk.ROUND, capstyle=tk.ROUND)

# --- SVG Data (for the actual application to import) ---
svg_elements_data = [
    {'type':'circle','cx':'62.419357','cy':'65.758064','r':'7.5483871','style':'opacity:1;fill:#ffffff;stroke:none;stroke-width:0.514016'},
    {'type':'ellipse','cx':'-1.1778357','cy':'86.117943','rx':'34.085022','ry':'6.1921449','transform':'matrix(0.89688675,-0.44226029,0.44546856,0.89529758,0,0)','style':'opacity:1;fill:#ffffff;stroke:none;stroke-width:0.656621'},
    {'type':'ellipse','cx':'54.199963','cy':'87.045128','rx':'34.085022','ry':'6.1921449','transform':'matrix(0.89688675,-0.44226029,0.44546856,0.89529758,0,0)','style':'opacity:1;fill:#ffffff;stroke:none;stroke-width:0.656621'},
    {'type':'path','d':'M 11.540323,99.798388 62.709678,126.72581','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 21.33871,97.983872 62.637098,126.50807','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 46.01613,110.54032 21.120968,97.838711','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 24.604839,95.588711 45.653226,110.54032','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 40.862904,101.54032 24.75,95.588711','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'m 30.629033,94.35484 10.08871,7.25806','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'m 41.153226,96.677421 -10.451613,-2.25','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'m 35.129033,91.959679 5.951613,4.862903','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 40.354839,92.685485 34.983871,91.741937','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'m 39.919355,89.564517 0.362904,3.266129','style':'opacity:1;fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 108.87097,31.336156 57.70161,4.408734','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 99.072579,33.150672 57.77419,4.626474','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 74.395159,20.594224 99.290321,33.295833','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 95.80645,35.545833 74.758063,20.594224','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'m 79.548385,29.594224 16.112904,5.951609','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'m 89.782256,36.779704 -10.08871,-7.25806','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'m 79.258063,34.457123 10.451613,2.25','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 85.282256,39.174865 79.330643,34.311962','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'m 80.05645,38.449059 5.370968,0.943548','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
    {'type':'path','d':'M 80.491934,41.570027 80.12903,38.303898','style':'fill:none;stroke:#ffffff;stroke-width:0.514016'},
]

#  Start of the acutal Applicaiton:
class UltralightGroundSchoolApp:
    def __init__(self, master):
        self.master = master
        master.title("Upwind: Part 103 Prep")
        # 1. Master geometry updated as requested
        master.geometry("800x800")
        master.minsize(600, 800)

        # --- Styling ---
        self.dark_bg = '#1e2124'
        self.light_bg = '#282b30'
        self.button_bg = '#424549'
        self.accent_color = '#7289da'
        self.light_text = '#ffffff'
        self.gray_text = '#808080'
        self.header_font = ("Helvetica", 26, "bold")
        self.subheader_font = ("Helvetica", 12, "normal")
        self.button_font = ("Helvetica", 11, "bold")
        self.body_font = ("Helvetica", 12, "normal")
        self.quiz_font = ("Helvetica", 14, "bold")
        
        # Define colors and fonts for easy modification of Airspace Chart
        self.colors = {
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
            "text_dark": "#000000",
            "line_color": "#333333"
        }
        self.fonts = {
            "main_title": ("Helvetica", 18, "bold"),
            "class_label": ("Helvetica", 14, "bold"),
            "altitude_label": ("Helvetica", 10, "bold"),
            "legend_label": ("Helvetica", 10, "normal"),
            "legend_title": ("Helvetica", 10, "bold"),
        }

        # --- Data Initialization ---
        self.question_pool = self._get_question_pool()
        self.study_topics_content = self._get_study_content()
        self.quiz_questions = []

        # --- Main Container ---
        self.container = Frame(master, bg=self.dark_bg)
        self.container.pack(fill="both", expand=True)
        
        self.study_categories = {
            "Regulations & Rules": [
                "FAR Part 103 Overview",
                "FAR Part 103 Operations"
            ],
            "Flight Environment": [
                "Airspace for Ultralights",
                "Basic Weather for VFR Flight",
                "Navigation and Sectional Charts",
                "Airport Operations and Markings"
            ],
            "Aircraft & Pilot": [
                "Aerodynamics for Ultralights",
                "Ultralight Systems and Preflight",
                "Human Factors (ADM & IMSAFE)",
                "Emergency Procedures"
            ]
        }

        self.show_main_menu()

    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_main_menu(self, selected_category=None):
        self._clear_container()

        # --- A SIMPLE, COMPACT LAYOUT ---

        # 1. Create and pack the footer frame FIRST to reserve its space at the bottom.
        footer_frame = Frame(self.container, bg=self.dark_bg)
        footer_frame.pack(side="bottom", fill="x", pady=10)
        Label(footer_frame, text="Use at own risk! No Rights Reserved. This work is dedicated to the Public Domain. Fly Safe!", 
              font=("Helvetica", 10), bg=self.dark_bg, fg=self.gray_text).pack()

        # 2. Create a single main frame to hold all other content.
        main_content_frame = Frame(self.container, bg=self.dark_bg)
        
        # --- THIS IS THE CHANGE ---
        # By removing `expand=True` and setting the anchor to "n" (North),
        # the entire content block is pushed to the top of the available space.
        # We add some top padding to prevent it from touching the window edge.
        main_content_frame.pack(anchor="n", pady=(20, 0))

        # --- All widgets below are placed in this frame with REDUCED PADDING ---

        # Logo
        logo_canvas = Canvas(main_content_frame, width=140, height=140, bg=self.dark_bg, highlightthickness=0)
        logo_canvas.pack(pady=(0, 10)) # Reduced bottom padding
        logo_canvas.create_oval(2, 2, 138, 138, fill=self.accent_color, outline="")
        draw_svg_elements_on_tkinter(logo_canvas, svg_elements_data, x_offset=6, y_offset=6)

        # Titles
        Label(main_content_frame, text="Upwind: Part 103 Prep", font=self.header_font,
                 bg=self.dark_bg, fg=self.light_text).pack(pady=5)
        Label(main_content_frame, text="Prepare for your ultralight adventures. Study key topics and test your knowledge.",
                 font=self.subheader_font, bg=self.dark_bg, fg=self.light_text, wraplength=700).pack(pady=(0, 15))

        # Quiz Button
        quiz_button = tk.Button(main_content_frame, text="Start Quiz (20 Questions)", command=self.start_quiz,
                                font=("Helvetica", 14, "bold"), bg=self.accent_color, fg=self.light_text,
                                relief="flat", padx=20, pady=5, width=25)
        quiz_button.pack(pady=5)

        # "OR" Label
        Label(main_content_frame, text="OR", font=self.subheader_font, bg=self.dark_bg, fg=self.light_text).pack(pady=5)

        # Frame for the study topics
        topics_frame = Frame(main_content_frame, bg=self.dark_bg)
        topics_frame.pack(pady=5)

        if selected_category is None:
            # Display Main Category Buttons
            Label(topics_frame, text="Study Categories", font=("Helvetica", 16, "bold"), bg=self.dark_bg, fg=self.light_text).pack(pady=(0, 10))
            for category_name in self.study_categories.keys():
                btn = tk.Button(topics_frame, text=category_name,
                                command=lambda c=category_name: self.show_main_menu(selected_category=c),
                                font=self.button_font, bg=self.button_bg, fg=self.light_text, relief="flat",
                                padx=10, pady=5, width=45)
                btn.pack(pady=2)
        else:
            # Display Sub-Topic Buttons
            Label(topics_frame, text=selected_category, font=("Helvetica", 16, "bold"), bg=self.dark_bg, fg=self.light_text).pack(pady=(0, 10))
            for topic_name in self.study_categories[selected_category]:
                btn = tk.Button(topics_frame, text=topic_name,
                                command=lambda t=topic_name: self.show_study_page(t),
                                font=self.button_font, bg=self.button_bg, fg=self.light_text, relief="flat",
                                padx=10, pady=5, width=45)
                btn.pack(pady=2)

            # Add a "Back to Categories" button
            back_button = tk.Button(topics_frame, text="< Back to Categories",
                                    command=self.show_main_menu,
                                    font=self.button_font, bg=self.accent_color, fg=self.light_text, relief="flat",
                                    padx=10, pady=5, width=45)
            back_button.pack(pady=(10, 0))
            
    def show_study_page(self, topic_title):
        """ 2. Displays a specific study topic page within a scrollable frame. """
        self._clear_container()

        back_button = tk.Button(self.container, text="< Back to Main Menu", command=self.show_main_menu,
                                font=self.button_font, bg=self.button_bg, fg=self.light_text, relief="flat")
        back_button.pack(pady=10, padx=20, anchor="w")

        # Create a canvas and a scrollbar
        canvas = Canvas(self.container, bg=self.dark_bg, highlightthickness=0)
        scrollbar = Scrollbar(self.container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas
        scrollable_frame = Frame(canvas, bg=self.dark_bg)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def on_frame_configure(_):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", on_frame_configure)

        # --- Add content to the scrollable frame ---
        Label(scrollable_frame, text=topic_title, font=self.header_font,
                 bg=self.dark_bg, fg=self.light_text).pack(pady=20, padx=30)

        content = self.study_topics_content[topic_title]
        Label(scrollable_frame, text=content, font=self.body_font, bg=self.dark_bg, fg=self.light_text,
                 wraplength=700, justify="left").pack(pady=10, padx=30, fill="x")

        if topic_title == "Airspace for Ultralights":
            self._create_airspace_graphic(scrollable_frame)

    def _draw_cylinder(self, canvas, x_center, y_top, y_bottom, radius, dark_color, light_color):
        """Helper function to draw a 3D cylinder with a highlight."""
        # Main cylinder body
        canvas.create_rectangle(x_center - radius, y_top, x_center + radius, y_bottom,
                                fill=dark_color, outline="")
        # Highlight/Sheen for 3D effect
        canvas.create_rectangle(x_center - radius / 2, y_top, x_center + radius / 2, y_bottom,
                                fill=light_color, outline="")
        # Top cap of the cylinder
        canvas.create_oval(x_center - radius, y_top - 8, x_center + radius, y_top + 8,
                           fill=dark_color, outline=self.colors["line_color"])
        canvas.create_oval(x_center - radius + 5, y_top - 5, x_center + radius - 5, y_top + 5,
                           fill=light_color, outline="")

    def _create_airspace_graphic(self, parent_frame):
        """
        Creates a detailed profile view of US airspace classes.
        """
        canvas_width = 850
        canvas_height = 650

        # --- Canvas and Title ---
        Label(parent_frame, text="U.S. Airspace Classes at a Glance", font=self.fonts["main_title"],
              fg=self.colors["text_dark"]).pack(pady=(10, 0))

        canvas = Canvas(parent_frame, width=canvas_width, height=canvas_height,
                        bg=self.colors["background"], highlightthickness=0)
        canvas.pack(pady=5, padx=10)

        # --- Y-Axis Altitude Coordinates ---
        y_top_text = 30
        y_fl600 = 60
        y_180 = 90
        y_145 = 130
        y_class_b_shelf_1 = 250
        y_class_b_shelf_2 = 350
        y_1200_agl = 420
        y_700_agl = 450
        y_surface = 500

        # --- Background Layers (A, E, G) ---
        canvas.create_rectangle(0, y_fl600, canvas_width, y_180, fill=self.colors["class_a"], outline="")
        canvas.create_rectangle(0, y_180, canvas_width, y_surface, fill=self.colors["class_e_main"], outline="")
        
        # Class G floor (creates the stepped look for Class E's floor)
        canvas.create_polygon(
            0, y_surface,
            200, y_surface,
            200, y_700_agl,
            380, y_700_agl,
            380, y_surface,
            550, y_surface,
            550, y_1200_agl,
            canvas_width, y_1200_agl,
            canvas_width, y_surface,
            fill=self.colors["class_g"], outline=""
        )
        canvas.create_line(0, y_surface, canvas_width, y_surface, width=2) # Ground line

        # --- Class B Airspace (Blue Stacked Cylinders) ---
        x_b_center = 290
        # Tiers (top down)
        self._draw_cylinder(canvas, x_b_center, y_145, y_class_b_shelf_1, 100, self.colors["class_b_dark"], self.colors["class_b_light"])
        self._draw_cylinder(canvas, x_b_center, y_class_b_shelf_1, y_class_b_shelf_2, 70, self.colors["class_b_dark"], self.colors["class_b_light"])
        self._draw_cylinder(canvas, x_b_center, y_class_b_shelf_2, y_surface, 40, self.colors["class_b_dark"], self.colors["class_b_light"])
        # Bottom dashed line for airport area
        canvas.create_oval(x_b_center - 40, y_surface - 8, x_b_center + 40, y_surface + 8,
                           outline=self.colors["text_light"], width=2, dash=(4, 4))
        # Airport symbol
        canvas.create_line(x_b_center - 12, y_surface - 12, x_b_center + 12, y_surface + 12, width=2, fill=self.colors["text_light"])
        canvas.create_line(x_b_center - 12, y_surface + 12, x_b_center + 12, y_surface - 12, width=2, fill=self.colors["text_light"])
        
        # --- Class C Airspace (Purple Stacked Cylinders) ---
        x_c_center = 480
        self._draw_cylinder(canvas, x_c_center, 320, 380, 60, self.colors["class_c_dark"], self.colors["class_c_light"])
        self._draw_cylinder(canvas, x_c_center, 380, y_surface, 40, self.colors["class_c_dark"], self.colors["class_c_light"])
        canvas.create_oval(x_c_center - 40, y_surface - 8, x_c_center + 40, y_surface + 8,
                           outline=self.colors["text_light"], width=2, dash=(4, 4))
        canvas.create_line(x_c_center - 12, y_surface - 12, x_c_center + 12, y_surface + 12, width=2, fill=self.colors["text_light"])
        canvas.create_line(x_c_center - 12, y_surface + 12, x_c_center + 12, y_surface - 12, width=2, fill=self.colors["text_light"])

        # --- Class D Airspace (Cyan Cylinder) ---
        x_d_center = 650
        self._draw_cylinder(canvas, x_d_center, 350, y_surface, 50, self.colors["class_d_dark"], self.colors["class_d_light"])
        canvas.create_oval(x_d_center - 50, y_surface - 8, x_d_center + 50, y_surface + 8,
                           outline=self.colors["text_light"], width=2, dash=(4, 4))
        canvas.create_line(x_d_center - 12, y_surface - 12, x_d_center + 12, y_surface + 12, width=2, fill=self.colors["text_light"])
        canvas.create_line(x_d_center - 12, y_surface + 12, x_d_center + 12, y_surface - 12, width=2, fill=self.colors["text_light"])

        # --- Text Labels ---
        canvas.create_text(50, y_top_text, text="Upper Limit Undefined", font=self.fonts["altitude_label"], anchor="w")
        canvas.create_text(425, y_fl600 + 15, text="CLASS A", font=self.fonts["class_label"], fill=self.colors["text_light"])
        canvas.create_text(x_b_center, y_145 + 40, text="CLASS B", font=self.fonts["class_label"], fill=self.colors["text_light"])
        canvas.create_text(x_c_center, 350, text="CLASS C", font=self.fonts["class_label"], fill=self.colors["text_light"])
        canvas.create_text(x_d_center, 380, text="CLASS D", font=self.fonts["class_label"], fill=self.colors["text_light"])
        canvas.create_text(420, y_700_agl + 15, text="CLASS G", font=self.fonts["legend_title"])
        canvas.create_text(590, y_1200_agl + 15, text="CLASS G", font=self.fonts["legend_title"])

        # --- Altitude Labels and Lines ---
        canvas.create_text(40, y_fl600 + 15, text="FL 600\n18,000' MSL", font=self.fonts["altitude_label"], fill=self.colors["text_light"], anchor="w")
        canvas.create_line(0, y_145, 100, y_145, fill=self.colors["text_light"])
        canvas.create_text(105, y_145, text="14,500' MSL", font=self.fonts["altitude_label"], fill=self.colors["text_light"], anchor="w")
        canvas.create_line(200, y_700_agl, 180, y_700_agl, fill=self.colors["text_dark"])
        canvas.create_text(175, y_700_agl, text="700' AGL", font=self.fonts["altitude_label"], fill=self.colors["text_dark"], anchor="e")
        canvas.create_line(550, y_1200_agl, 530, y_1200_agl, fill=self.colors["text_dark"])
        canvas.create_text(525, y_1200_agl, text="1,200' AGL", font=self.fonts["altitude_label"], fill=self.colors["text_dark"], anchor="e")

        # --- Legend at the bottom ---
        legend_y_start = 550
        legend_x_start = 50
        canvas.create_text(legend_x_start, legend_y_start, text="AGL", font=self.fonts["legend_title"], anchor="w")
        canvas.create_text(legend_x_start + 40, legend_y_start, text="Above Ground Level", font=self.fonts["legend_label"], anchor="w")
        canvas.create_text(legend_x_start, legend_y_start + 20, text="FL", font=self.fonts["legend_title"], anchor="w")
        canvas.create_text(legend_x_start + 40, legend_y_start + 20, text="Flight Level", font=self.fonts["legend_label"], anchor="w")
        canvas.create_text(legend_x_start, legend_y_start + 40, text="MSL", font=self.fonts["legend_title"], anchor="w")
        canvas.create_text(legend_x_start + 40, legend_y_start + 40, text="Mean Sea Level", font=self.fonts["legend_label"], anchor="w")

        legend_x_start_2 = 400
        canvas.create_text(legend_x_start_2, legend_y_start, text="*", font=self.fonts["legend_label"], anchor="w")
        canvas.create_text(legend_x_start_2 + 20, legend_y_start, text="Airport in Class G without IAP", font=self.fonts["legend_label"], anchor="w")
        canvas.create_text(legend_x_start_2, legend_y_start + 20, text="**", font=self.fonts["legend_label"], anchor="w")
        canvas.create_text(legend_x_start_2 + 20, legend_y_start + 20, text="Airport in Class G with IAP", font=self.fonts["legend_label"], anchor="w")
        canvas.create_text(legend_x_start_2, legend_y_start + 40, text="***", font=self.fonts["legend_label"], anchor="w")
        canvas.create_text(legend_x_start_2 + 20, legend_y_start + 40, text="Airport in Class E with IAP", font=self.fonts["legend_label"], anchor="w")

        canvas.create_text(canvas_width - 20, legend_y_start + 60, text="Airspace Volumes Not to Scale", font=self.fonts["legend_label"], anchor="e")
        
    def start_quiz(self):
        self._clear_container()
        self.quiz_questions = random.sample(self.question_pool, 20)
        self.current_question_index = 0
        self.user_answers = {}

        self.question_label = Label(self.container, text="", font=self.quiz_font,
                                       bg=self.dark_bg, fg=self.light_text, wraplength=750, justify="left")
        self.question_label.pack(pady=(50, 30), padx=25)

        self.radio_var = tk.StringVar()
        self.radio_buttons = []
        options_frame = Frame(self.container, bg=self.dark_bg)
        options_frame.pack(padx=50, anchor="w")

        for _ in range(4):
            rb = tk.Radiobutton(options_frame, text="", variable=self.radio_var, value="",
                                font=self.body_font, bg=self.dark_bg, fg=self.light_text,
                                selectcolor=self.button_bg, activebackground=self.dark_bg, 
                                activeforeground=self.light_text, wraplength=700, justify="left", anchor="w")
            rb.pack(anchor="w", pady=5)
            self.radio_buttons.append(rb)

        self.feedback_label = Label(self.container, text="", font=self.body_font, bg=self.dark_bg, fg=self.light_text)
        self.feedback_label.pack(pady=20)

        self.next_button = tk.Button(self.container, text="Next Question", command=self.next_question,
                                     font=self.button_font, bg=self.button_bg, fg=self.light_text, relief="flat", width=20, height=2)
        self.next_button.pack(pady=40)
        self.display_question()
    
    def display_question(self):
        self.feedback_label.config(text="")
        if self.current_question_index < len(self.quiz_questions):
            question_data = self.quiz_questions[self.current_question_index]
            self.question_label.config(text=f"Question {self.current_question_index + 1} of {len(self.quiz_questions)}\n\n{question_data['question_text']}")
            self.radio_var.set("")
            options = question_data['options']
            random.shuffle(options)
            for i, option in enumerate(options):
                self.radio_buttons[i].config(text=option, value=option)
            if self.current_question_index == len(self.quiz_questions) - 1:
                self.next_button.config(text="Submit Quiz", command=self.show_results)
        
    def next_question(self):
        selected_answer = self.radio_var.get()
        if selected_answer and selected_answer != "None":
            self.user_answers[self.current_question_index] = selected_answer
            self.current_question_index += 1
            if self.current_question_index < len(self.quiz_questions):
                self.display_question()
        else:
            self.feedback_label.config(text="Please select an answer before proceeding.", fg='yellow')

    def show_results(self):
        if self.current_question_index < len(self.quiz_questions):
            self.user_answers[self.current_question_index] = self.radio_var.get()
        self._clear_container()
        
        score = 0
        wrong_answers = []
        for i, question_data in enumerate(self.quiz_questions):
            if self.user_answers.get(i) == question_data['correct_answer']:
                score += 1
            else:
                wrong_answers.append({
                    "question": question_data['question_text'],
                    "user_answer": self.user_answers.get(i, "No answer"),
                    "correct_answer": question_data['correct_answer'],
                    "explanation": question_data['explanation']
                })
        
        Label(self.container, text="Quiz Results", font=self.header_font,
                 bg=self.dark_bg, fg=self.light_text).pack(pady=20)

        score_percentage = (score / len(self.quiz_questions)) * 100
        Label(self.container, text=f"You scored: {score}/{len(self.quiz_questions)} ({score_percentage:.2f}%)",
                 font=("Helvetica", 18), bg=self.dark_bg, fg=self.light_text).pack(pady=10)

        results_text_area = scrolledtext.ScrolledText(self.container, wrap=tk.WORD, bg=self.light_bg, fg=self.light_text,
                                                      font=self.body_font, relief="flat", borderwidth=0, padx=15, pady=15)
        results_text_area.pack(pady=10, padx=50, fill="both", expand=True)

        if not wrong_answers:
            results_text_area.insert(tk.INSERT, "Excellent! You got all questions correct. You have a strong understanding of FAR Part 103.\n")
        else:
            results_text_area.insert(tk.INSERT, "Review of Incorrect Answers:\n\n")
            for item in wrong_answers:
                results_text_area.insert(tk.INSERT, f"Q: {item['question']}\n\n")
                results_text_area.insert(tk.INSERT, f"  Your Answer: {item['user_answer']}\n", 'wrong')
                results_text_area.insert(tk.INSERT, f"  Correct Answer: {item['correct_answer']}\n\n", 'correct')
                wrapped_explanation = '\n'.join(textwrap.wrap(f"Explanation: {item['explanation']}", width=80))
                results_text_area.insert(tk.INSERT, f"{wrapped_explanation}\n\n" + "-"*80 + "\n\n")
        
        results_text_area.tag_config('correct', foreground='#4CAF50', font=(self.body_font[0], self.body_font[1], "bold"))
        results_text_area.tag_config('wrong', foreground='#F44336', font=(self.body_font[0], self.body_font[1], "bold"))
        results_text_area.config(state=tk.DISABLED)

        home_button = tk.Button(self.container, text="Return to Main Menu", command=self.show_main_menu,
                                font=self.button_font, bg=self.accent_color, fg=self.light_text, relief="flat", width=25, height=2)
        home_button.pack(pady=20)

    def _get_study_content(self):
        return {
            "FAR Part 103 Overview": textwrap.dedent("""..."""), # Content from previous response
            "FAR Part 103 Operations": textwrap.dedent("""..."""), # Content from previous response
            "Airspace for Ultralights": textwrap.dedent("""..."""), # Content from previous response
            "Basic Weather for VFR Flight": textwrap.dedent("""..."""), # Content from previous response
            "Aerodynamics for Ultralights": textwrap.dedent("""..."""), # Content from previous response
            "Ultralight Systems and Preflight": textwrap.dedent("""..."""), # Content from previous response
            "Navigation and Sectional Charts": textwrap.dedent("""..."""), # Content from previous response
            "Airport Operations and Markings": textwrap.dedent("""..."""), # Content from previous response
            "Emergency Procedures": textwrap.dedent("""..."""), # Content from previous response
            "Human Factors (ADM & IMSAFE)": textwrap.dedent("""...""") # Content from previous response
        }

    def _get_question_pool(self):
        """ 3. Returns an expanded list of over 300 quiz questions. """
        return [
            # Category: FAR Part 103 Overview (31 Questions)
            {"question_text": "What is the maximum empty weight for a powered ultralight vehicle according to FAR Part 103?", "options": ["155 pounds", "254 pounds", "300 pounds", "500 pounds"], "correct_answer": "254 pounds", "explanation": "FAR Part 103.1(e)(1) states a powered ultralight must weigh less than 254 pounds empty weight, excluding floats and safety devices."},
            {"question_text": "What is the maximum fuel capacity for a powered ultralight?", "options": ["5 U.S. gallons", "10 U.S. gallons", "3 U.S. gallons", "There is no limit"], "correct_answer": "5 U.S. gallons", "explanation": "FAR Part 103.1(e)(2) limits the fuel capacity of a powered ultralight to a maximum of 5 U.S. gallons."},
            {"question_text": "What is the maximum full-power level flight speed for a powered ultralight?", "options": ["55 mph", "55 knots (63 mph)", "70 knots", "45 knots"], "correct_answer": "55 knots (63 mph)", "explanation": "FAR Part 103.1(e)(3) specifies that a powered ultralight must not be capable of more than 55 knots calibrated airspeed at full power in level flight."},
            {"question_text": "Is a pilot certificate required to operate a legal Part 103 ultralight?", "options": ["Yes, a Sport Pilot certificate is required.", "Yes, at least a Student Pilot certificate.", "No, no pilot or medical certificate is required.", "Only if flying near an airport."], "correct_answer": "No, no pilot or medical certificate is required.", "explanation": "According to FAR 103.7, operators of ultralight vehicles are not required to meet any airman or medical certificate requirements."},
            {"question_text": "An unpowered ultralight vehicle, such as a hang glider, must weigh less than:", "options": ["100 pounds", "155 pounds", "200 pounds", "254 pounds"], "correct_answer": "155 pounds", "explanation": "FAR 103.1(d) specifies that an unpowered ultralight must weigh less than 155 pounds to be operated under these rules."},
            {"question_text": "A vehicle has an empty weight of 260 pounds. Can it be operated under Part 103?", "options": ["Yes, if the pilot is light.", "No, it exceeds the 254-pound weight limit.", "Yes, if it has a small engine.", "Only with an FAA waiver."], "correct_answer": "No, it exceeds the 254-pound weight limit.", "explanation": "Any powered vehicle exceeding the 254-pound empty weight limit cannot be legally operated as a Part 103 ultralight."},
            {"question_text": "The empty weight of a powered ultralight does NOT include:", "options": ["The engine", "The propeller", "The wings", "A deployable ballistic parachute"], "correct_answer": "A deployable ballistic parachute", "explanation": "FAR 103.1(e)(1) specifically excludes 'safety devices which are intended for deployment in a potentially catastrophic situation' from the empty weight calculation to encourage their use."},
            {"question_text": "An ultralight has a fuel tank that can hold 6 gallons. Is it Part 103 compliant?", "options": ["Yes, if you only fill it with 5 gallons.", "No, the fuel capacity cannot exceed 5 U.S. gallons.", "Yes, the limit is 10 gallons.", "Only if it's an unpowered ultralight."], "correct_answer": "No, the fuel capacity cannot exceed 5 U.S. gallons.", "explanation": "The regulation applies to the vehicle's fuel capacity, not how much fuel is in the tank at any given time. The tank itself cannot be larger than 5 U.S. gallons."},
            {"question_text": "What is the maximum power-off stall speed for a powered ultralight?", "options": ["24 knots", "30 knots", "20 mph", "There is no stall speed requirement."], "correct_answer": "24 knots", "explanation": "FAR 103.1(e)(4) requires a power-off stall speed which does not exceed 24 knots calibrated airspeed. This ensures the vehicle has gentle landing characteristics."},
            {"question_text": "Can you legally fly a two-seat ultralight for training under Part 103?", "options": ["Yes, if the instructor is certified.", "No, Part 103 vehicles are strictly single-occupant.", "Yes, if the combined weight is under 400 pounds.", "Only with a waiver from the FAA."], "correct_answer": "No, Part 103 vehicles are strictly single-occupant.", "explanation": "FAR 103.1(a) defines an ultralight as a vehicle 'used or intended to be used for manned operation in the air by a single occupant'. Two-seat trainers operate as Experimental or Light-Sport Aircraft (LSA)."},
            {"question_text": "Is an airworthiness certificate required for a Part 103 vehicle?", "options": ["Yes, a special airworthiness certificate.", "No, no airworthiness certificate is required.", "Only for powered ultralights.", "Only if it has been repaired."], "correct_answer": "No, no airworthiness certificate is required.", "explanation": "FAR 103.7 exempts these vehicles from airworthiness certification requirements, placing the responsibility for safety entirely on the pilot/owner."},
            {"question_text": "Is a Part 103 ultralight required to be registered with the FAA and have an 'N' number?", "options": ["Yes, all aircraft need an N number.", "No, ultralights are exempt from registration requirements.", "Only if they are flown for compensation.", "Only if they have a radio."], "correct_answer": "No, ultralights are exempt from registration requirements.", "explanation": "FAR 103.7(c) explicitly states that ultralight vehicles are not required to be registered or to bear markings of any type."},
            {"question_text": "What is the primary purpose of FAR Part 103?", "options": ["To regulate air carriers.", "To provide a simplified set of rules for recreational and sport flying.", "To set standards for aircraft manufacturing.", "To license pilots and mechanics."], "correct_answer": "To provide a simplified set of rules for recreational and sport flying.", "explanation": "Part 103 was created to allow flight with minimal regulation for the purposes of recreation and sport, separating these simple vehicles from more complex certified aircraft."},
            {"question_text": "If you add amphibious floats to your powered ultralight, how does that affect the empty weight calculation?", "options": ["The weight of the floats is not counted towards the 254-pound limit.", "The weight of the floats is counted.", "You are allowed an extra 50 pounds for floats.", "Floats are not permitted on ultralights."], "correct_answer": "The weight of the floats is not counted towards the 254-pound limit.", "explanation": "FAR 103.1(e)(1) allows the weight of floats to be excluded from the 254-pound empty weight limit."},
            {"question_text": "A vehicle meets all Part 103 criteria except its top speed is 60 knots. What is its status?", "options": ["It is a legal Part 103 ultralight.", "It is not a legal Part 103 ultralight and must be registered as an aircraft.", "It can be flown under Part 103 if the pilot has a license.", "It can be flown under Part 103 if power is limited to stay below 55 knots."], "correct_answer": "It is not a legal Part 103 ultralight and must be registered as an aircraft.", "explanation": "The vehicle must not be CAPABLE of more than 55 knots. If its design allows for higher speeds, it fails the Part 103 definition, regardless of how it's flown."},
            {"question_text": "Which of the following activities is NOT considered 'recreational or sport purposes'?", "options": ["Flying on a calm evening to enjoy the sunset.", "Flying to a local fly-in event.", "Commuting to work in your ultralight.", "Practicing takeoffs and landings."], "correct_answer": "Commuting to work in your ultralight.", "explanation": "Using an ultralight for hire, compensation, or for business purposes like commuting is not permitted under Part 103."},
            {"question_text": "Does a medical certificate from a doctor allow you to fly a Part 103 ultralight?", "options": ["Yes, it is required.", "It is recommended but not required.", "No, it is prohibited.", "A medical certificate is irrelevant to Part 103 operations."], "correct_answer": "A medical certificate is irrelevant to Part 103 operations.", "explanation": "FAR 103.7 states that no medical certificate is required. The responsibility to be medically fit to fly rests solely with the pilot (see IMSAFE checklist)."},
            {"question_text": "If an unpowered ultralight weighs 160 pounds, can it be flown under Part 103?", "options": ["Yes, the limit is 254 pounds.", "No, it exceeds the 155-pound limit for unpowered ultralights.", "Yes, if it has no engine.", "Only in Class G airspace."], "correct_answer": "No, it exceeds the 155-pound limit for unpowered ultralights.", "explanation": "The weight limit for unpowered vehicles like hang gliders and paragliders is a strict 155 pounds."},
            {"question_text": "Your powered ultralight weighs 250 lbs. You add a 10 lb radio and GPS. What is its new empty weight for Part 103 purposes?", "options": ["250 lbs", "260 lbs", "254 lbs", "240 lbs"], "correct_answer": "260 lbs", "explanation": "Radios and GPS are not considered safety devices for deployment in a catastrophic situation, so their weight counts towards the 254-pound limit. This aircraft would no longer be Part 103 compliant."},
            {"question_text": "The stall speed of your ultralight is 25 knots. Is it compliant with Part 103?", "options": ["Yes, the limit is 30 knots.", "No, the power-off stall speed cannot exceed 24 knots.", "Yes, if the top speed is under 55 knots.", "Only if it is unpowered."], "correct_answer": "No, the power-off stall speed cannot exceed 24 knots.", "explanation": "Exceeding the 24-knot stall speed limit makes the vehicle non-compliant with Part 103."},
            {"question_text": "Who is ultimately responsible for ensuring a Part 103 vehicle is safe to fly?", "options": ["The FAA", "The manufacturer", "The pilot-in-command", "The EAA"], "correct_answer": "The pilot-in-command", "explanation": "The lack of certification and registration requirements under Part 103 places the entire responsibility for airworthiness and safety on the pilot."},
            {"question_text": "Can you carry a passenger in a Part 103 ultralight if they are also a pilot?", "options": ["Yes, if they are an instructor.", "No, Part 103 vehicles are limited to a single occupant.", "Yes, if the total weight is under the limit.", "Only with a special permit."], "correct_answer": "No, Part 103 vehicles are limited to a single occupant.", "explanation": "The single-occupant rule is absolute and does not depend on the qualifications of the second person."},
            {"question_text": "Which document is required to be in your possession to fly a Part 103 ultralight?", "options": ["Pilot certificate", "Medical certificate", "Aircraft registration", "None of the above"], "correct_answer": "None of the above", "explanation": "Part 103 is unique in that it does not require the pilot to have any specific certificates or documents to operate the vehicle legally."},
            {"question_text": "If a powered ultralight has no engine, what weight limit must it meet?", "options": ["254 pounds", "155 pounds", "It is no longer an ultralight.", "The weight of the engine can be subtracted."], "correct_answer": "155 pounds", "explanation": "If it is operated without a power source, it would be considered an unpowered vehicle and must adhere to the 155-pound weight limit."},
            {"question_text": "Your ultralight has a top speed of 54 knots and a stall speed of 23 knots. Is it compliant?", "options": ["No, top speed is too high.", "No, stall speed is too high.", "Yes, it meets both the speed and stall requirements.", "Only if it weighs less than 200 lbs."], "correct_answer": "Yes, it meets both the speed and stall requirements.", "explanation": "The vehicle is compliant as its top speed is not more than 55 knots and its stall speed does not exceed 24 knots."},
            {"question_text": "Can you use a Part 103 ultralight for commercial aerial photography?", "options": ["Yes, if the client is not in the aircraft.", "No, commercial operations are prohibited.", "Yes, with a commercial pilot license.", "Only over rural areas."], "correct_answer": "No, commercial operations are prohibited.", "explanation": "Part 103 vehicles are limited to recreational and sport use only. Any flight for compensation or hire is forbidden."},
            {"question_text": "What is the key trade-off for the freedom granted by Part 103?", "options": ["Higher insurance costs", "Limited flight distance", "The pilot assumes all responsibility for safety and legality.", "Inability to fly at night."], "correct_answer": "The pilot assumes all responsibility for safety and legality.", "explanation": "The FAA grants freedom from regulation in exchange for the pilot taking on the full burden of responsibility for every aspect of the flight."},
            {"question_text": "If you modify your engine and it now allows the ultralight to fly at 65 knots, what must you do?", "options": ["Fly at a lower power setting.", "Nothing, as long as you don't fly that fast.", "You must register the vehicle as an Experimental aircraft.", "Inform the EAA of the change."], "correct_answer": "You must register the vehicle as an Experimental aircraft.", "explanation": "Once the vehicle is CAPABLE of exceeding any Part 103 limit, it no longer qualifies as an ultralight and must be certified and registered in another category, like Experimental Amateur-Built."},
            {"question_text": "An ultralight is defined as a vehicle intended for operation by how many people?", "options": ["One or two", "A single occupant", "Up to three", "No more than four"], "correct_answer": "A single occupant", "explanation": "The regulation at 103.1(a) is explicit: 'manned operation in the air by a single occupant.'"},
            {"question_text": "Does adding a second fuel tank of 3 gallons to your 4-gallon main tank comply with Part 103?", "options": ["Yes, because the main tank is under 5 gallons.", "No, the total fuel capacity would be 7 gallons, exceeding the 5-gallon limit.", "Yes, if you only use one tank per flight.", "Only if the second tank is for emergencies."], "correct_answer": "No, the total fuel capacity would be 7 gallons, exceeding the 5-gallon limit.", "explanation": "The limit applies to the total fuel capacity of the vehicle, not individual tanks. The combined capacity cannot exceed 5 U.S. gallons."},
            {"question_text": "Are there any age restrictions for operating a Part 103 ultralight?", "options": ["Yes, you must be 16 years old.", "Yes, you must be 18 years old.", "No, FAR Part 103 does not specify a minimum age.", "Yes, you must be 21 years old."], "correct_answer": "No, FAR Part 103 does not specify a minimum age.", "explanation": "While no legal age is specified, safe operation requires a high level of maturity and judgment. Flight training organizations will impose their own age minimums."},
            
            # Category: FAR Part 103 Operations (30 Questions)
            {"question_text": "When are you permitted to fly an ultralight vehicle?", "options": ["Anytime, day or night", "Only between sunrise and sunset", "Only with navigation lights", "Only on weekends"], "correct_answer": "Only between sunrise and sunset", "explanation": "FAR 103.11(a) restricts ultralight operations to daylight hours. An exception exists for twilight with proper lighting in Class G airspace."},
            {"question_text": "Under what condition can you operate an ultralight during the 30-minute twilight period after sunset?", "options": ["If you have a radio", "If you stay below 500 feet", "If the vehicle has an operating anti-collision light visible for 3 miles and you are in Class G airspace", "If you have permission from the local airport"], "correct_answer": "If the vehicle has an operating anti-collision light visible for 3 miles and you are in Class G airspace", "explanation": "FAR 103.11(b) allows for twilight operations only if the vehicle is equipped with a suitable anti-collision light and remains in uncontrolled (Class G) airspace."},
            {"question_text": "Flying over a small town's downtown area in an ultralight is:", "options": ["Permitted if you are above 1,000 feet", "Permitted if you are just passing through", "Prohibited", "Permitted on Sundays"], "correct_answer": "Prohibited", "explanation": "FAR 103.15 explicitly prohibits operating an ultralight vehicle over any congested area of a city, town, or settlement."},
            {"question_text": "Who has the right-of-way when a powered ultralight and a conventional airplane are converging?", "options": ["The ultralight, because it is slower", "The aircraft on the right", "The conventional airplane", "The faster aircraft"], "correct_answer": "The conventional airplane", "explanation": "FAR 103.13(a) states that an ultralight vehicle shall yield the right-of-way to all aircraft."},
            {"question_text": "A powered parachute (a powered ultralight) and a hang glider (an unpowered ultralight) are approaching each other. Who must give way?", "options": ["The hang glider", "The powered parachute", "The one that is higher", "The one that is faster"], "correct_answer": "The powered parachute", "explanation": "FAR 103.13(c) states that powered ultralights shall yield the right-of-way to unpowered ultralights."},
            {"question_text": "Is it permissible to drop objects from an ultralight?", "options": ["Yes, at any time.", "Only over unpopulated areas.", "No, it is never permitted.", "Only if it creates no hazard to persons or property."], "correct_answer": "Only if it creates no hazard to persons or property.", "explanation": "FAR 103.9(b) allows for dropping objects as long as the action does not create a hazard to people or property on the ground."},
            {"question_text": "Can you fly an ultralight over an open-air concert?", "options": ["Yes, if you fly above 1,500 feet.", "No, it is prohibited.", "Yes, if you get permission from the event organizer.", "Only if it's during the day."], "correct_answer": "No, it is prohibited.", "explanation": "FAR 103.15 explicitly prohibits operating an ultralight vehicle over any open-air assembly of persons."},
            {"question_text": "The definition of a 'congested area' under FAR 103.15 is:", "options": ["Clearly defined as any area with more than 50 houses per square mile.", "Marked in yellow on sectional charts.", "Not strictly defined and subject to interpretation, requiring conservative pilot judgment.", "Only major cities like New York or Los Angeles."], "correct_answer": "Not strictly defined and subject to interpretation, requiring conservative pilot judgment.", "explanation": "The FAA does not provide a precise definition. Legal precedent has shown that even sparsely populated areas can be considered 'congested', so pilots must use extremely conservative judgment."},
            {"question_text": "What is the key principle of the right-of-way rules?", "options": ["The fastest aircraft always has right-of-way.", "The pilot on the left has right-of-way.", "The responsibility of every pilot to 'see and avoid' other aircraft.", "Ultralights have right-of-way over balloons."], "correct_answer": "The responsibility of every pilot to 'see and avoid' other aircraft.", "explanation": "While specific rules exist, the fundamental concept underpinning all right-of-way regulations is that every pilot must maintain vigilance to see and avoid other aircraft."},
            {"question_text": "To fly during civil twilight, an ultralight's anti-collision light must be visible from how far away?", "options": ["1 statute mile", "3 statute miles", "5 statute miles", "10 nautical miles"], "correct_answer": "3 statute miles", "explanation": "FAR 103.11(b)(1) requires that for twilight operations, the anti-collision light must be visible for at least 3 statute miles."},
            {"question_text": "An ultralight and a hot air balloon are converging. Which has the right-of-way?", "options": ["The ultralight", "The hot air balloon", "Whichever is lower", "Whichever is on the right"], "correct_answer": "The hot air balloon", "explanation": "An ultralight must yield to all other aircraft. A balloon is less maneuverable than an ultralight, so the ultralight pilot must give way."},
            {"question_text": "What does 'hazardous operation' under 103.9 refer to?", "options": ["Flying in high winds", "Flying an unpainted aircraft", "Any action that creates a danger to people or property", "Flying without a radio"], "correct_answer": "Any action that creates a danger to people or property", "explanation": "This is a broad rule that prohibits reckless flying, such as buzzing houses, flying extremely low over roads, or any other maneuver that could endanger someone."},
            {"question_text": "You are flying an ultralight and see another ultralight approaching from your right. Who has the right of way?", "options": ["You do, because you are on the left.", "The other ultralight, because it is on your right.", "Whoever is flying higher.", "Whoever saw the other first."], "correct_answer": "The other ultralight, because it is on your right.", "explanation": "While Part 103 says to yield to all 'aircraft', the general 'see and avoid' and right-of-way rules from general aviation are the standard for safety. The aircraft on the right has the right-of-way."},
            {"question_text": "Can you operate an ultralight from a public road?", "options": ["Yes, if there is no traffic.", "No, this is generally illegal and unsafe.", "Yes, if it is a rural road.", "Only if the speed limit is under 30 mph."], "correct_answer": "No, this is generally illegal and unsafe.", "explanation": "Operating from public roads is typically prohibited by state and local laws and is considered a hazardous operation under FAR 103.9."},
            {"question_text": "What is the primary reason for the prohibition on flying over congested areas?", "options": ["Noise complaints", "To prevent pilots from getting lost", "In case of engine failure, there is no safe place to land without endangering people on the ground.", "To keep ultralights away from tall buildings."], "correct_answer": "In case of engine failure, there is no safe place to land without endangering people on the ground.", "explanation": "The rule is designed to protect people on the ground. An engine failure over a congested area leaves the pilot with no safe options."},
            {"question_text": "If you are overtaking a slower aircraft, how should you pass it?", "options": ["Pass underneath it.", "Pass by altering course to the right.", "Pass over the top of it.", "Announce your intentions and pass on the left."], "correct_answer": "Pass by altering course to the right.", "explanation": "The standard procedure for overtaking another aircraft is to pass on the right, maintaining a safe distance."},
            {"question_text": "What is the official definition of 'daylight hours' for Part 103 operations?", "options": ["From 8 AM to 8 PM", "From sunrise to sunset", "When the sun is 6 degrees above the horizon", "Anytime you don't need a landing light"], "correct_answer": "From sunrise to sunset", "explanation": "FAR 103.11(a) is explicit: 'No person may operate an ultralight vehicle except between the hours of sunrise and sunset.'"},
            {"question_text": "You are flying an unpowered paraglider. A powered parachute approaches you. Who must give way?", "options": ["You must give way.", "The powered parachute must give way.", "Whoever is lower must give way.", "Both should turn right."], "correct_answer": "The powered parachute must give way.", "explanation": "FAR 103.13(c) states that a powered ultralight shall yield the right-of-way to an unpowered ultralight."},
            {"question_text": "Is it legal to perform aerobatic maneuvers in a Part 103 ultralight?", "options": ["Yes, if you are over an unpopulated area.", "No, most ultralights are not stressed for aerobatics and it could be considered a hazardous operation.", "Yes, if you have a parachute.", "Only with a waiver."], "correct_answer": "No, most ultralights are not stressed for aerobatics and it could be considered a hazardous operation.", "explanation": "While not explicitly forbidden by a specific rule, aerobatics in a vehicle not designed for it would likely be considered a hazardous operation under 103.9."},
            {"question_text": "If you are approaching an airport to land, who has the right-of-way: you, or an aircraft on final approach?", "options": ["You do, if you are lower.", "The aircraft on final approach has the right-of-way.", "You do, if you are faster.", "Whoever is on the CTAF first."], "correct_answer": "The aircraft on final approach has the right-of-way.", "explanation": "An aircraft that is landing or on final approach has the right-of-way over other aircraft in the air or on the surface."},
            {"question_text": "Can you fly your ultralight over a national park?", "options": ["Yes, without restriction.", "No, it is prohibited.", "Generally, flight below 2,000 feet AGL over national parks and wildlife refuges is requested to be avoided.", "Only if you take off from within the park."], "correct_answer": "Generally, flight below 2,000 feet AGL over national parks and wildlife refuges is requested to be avoided.", "explanation": "To protect wildlife and the natural experience, pilots are strongly requested to maintain a minimum of 2,000 feet AGL over such areas. It is not an explicit Part 103 rule but a general aviation best practice."},
            {"question_text": "What is the only exception to the 'sunrise to sunset' rule?", "options": ["If you have a flashlight.", "The 30-minute civil twilight period, with proper lighting in Class G.", "If you are over water.", "There are no exceptions."], "correct_answer": "The 30-minute civil twilight period, with proper lighting in Class G.", "explanation": "FAR 103.11(b) provides the sole exception for twilight operations under specific equipment and airspace conditions."},
            {"question_text": "You are approaching another aircraft head-on. What is the correct procedure?", "options": ["Both aircraft should alter course to the right.", "The aircraft on the left should give way.", "The higher aircraft should climb.", "The lower aircraft should descend."], "correct_answer": "Both aircraft should alter course to the right.", "explanation": "When approaching head-on, or nearly so, each pilot of each aircraft shall alter course to the right to pass safely."},
            {"question_text": "Can you be compensated for fuel if you take a friend for a joyride in your ultralight?", "options": ["Yes, they can pay for the fuel.", "No, all flights must be for recreation or sport, and no compensation is allowed.", "Only if you have a commercial license.", "Yes, but only the exact cost of the fuel."], "correct_answer": "No, all flights must be for recreation or sport, and no compensation is allowed.", "explanation": "This is a trick question. You cannot take a friend for a joyride in a Part 103 ultralight because it is single-occupant only. Furthermore, no compensation of any kind is allowed."},
            {"question_text": "Does Part 103 specify a maximum altitude for ultralight operations?", "options": ["Yes, 10,000 feet MSL.", "Yes, 1,200 feet AGL.", "No, but you must adhere to airspace rules and VFR weather minimums.", "Yes, 18,000 feet MSL."], "correct_answer": "No, but you must adhere to airspace rules and VFR weather minimums.", "explanation": "There is no specific maximum altitude in Part 103 itself, but flight is effectively limited by the ceiling of Class G/E airspace and the prohibition from entering Class A airspace at 18,000 feet."},
            {"question_text": "If you are flying in the twilight period with an anti-collision light, can you enter Class D airspace?", "options": ["Yes, the light gives you permission.", "No, you must remain in Class G airspace during twilight operations.", "Only if you call the tower.", "Only if you are landing at that airport."], "correct_answer": "No, you must remain in Class G airspace during twilight operations.", "explanation": "The exception for twilight flight under 103.11(b) explicitly requires that the flight be conducted in Class G airspace."},
            {"question_text": "What is the fundamental purpose of the 'see and avoid' concept?", "options": ["To make sure you see nice scenery.", "To prevent mid-air collisions.", "To help you navigate.", "To avoid bad weather."], "correct_answer": "To prevent mid-air collisions.", "explanation": "The entire concept of 'see and avoid' is the primary method used by VFR pilots to maintain safe separation from other aircraft."},
            {"question_text": "An ultralight must yield the right of way to which of the following?", "options": ["Airplanes", "Gliders", "Balloons", "All of the above"], "correct_answer": "All of the above", "explanation": "FAR 103.13 states that ultralight vehicles shall yield the right-of-way to all aircraft, without exception."},
            {"question_text": "You see a stadium with an ongoing football game. Can you fly over it?", "options": ["Yes, if you are above 1,000 feet.", "No, this is an open-air assembly of persons.", "Only during halftime.", "Yes, if you are not directly over the field."], "correct_answer": "No, this is an open-air assembly of persons.", "explanation": "Flying over an active stadium is a clear violation of FAR 103.15, which prohibits flight over open-air assemblies of people."},
            {"question_text": "If you drop a small, weighted streamer from your ultralight over an empty field to gauge wind, is this a hazardous operation?", "options": ["Yes, dropping anything is illegal.", "No, as it creates no hazard to persons or property.", "Only if it lands on the field.", "Yes, because it could distract you."], "correct_answer": "No, as it creates no hazard to persons or property.", "explanation": "This is a common practice for some pilots. As long as the object is harmless and dropped in an area where it cannot cause harm or damage, it is not considered a hazardous operation."},
            
            # Category: Airspace for Ultralights (30 Questions)
            {"question_text": "What is the primary type of airspace where ultralights can operate without ATC authorization?", "options": ["Class B", "Class C", "Class G", "Class E"], "correct_answer": "Class G", "explanation": "Class G (uncontrolled) airspace is where ultralight vehicles are intended to be flown without needing to contact Air Traffic Control."},
            {"question_text": "To fly an ultralight within Class D airspace, what must you do?", "options": ["Fly above the airspace", "Obtain prior authorization from the controlling ATC facility", "Equip your ultralight with a transponder", "You cannot enter Class D airspace"], "correct_answer": "Obtain prior authorization from the controlling ATC facility", "explanation": "FAR 103.17 requires any person operating an ultralight within Class D airspace to get prior authorization from the ATC facility having jurisdiction over that airspace."},
            {"question_text": "On a VFR Sectional Chart, what does a dashed blue line surrounding an airport indicate?", "options": ["Class B Airspace", "Class C Airspace", "Class D Airspace", "A Military Operations Area"], "correct_answer": "Class D Airspace", "explanation": "A dashed blue line on a sectional chart depicts the lateral boundaries of Class D airspace, which extends from the surface up to a specified altitude."},
            {"question_text": "Can you fly an ultralight in Class A airspace?", "options": ["Yes, with a transponder.", "Yes, if you stay VFR.", "No, under no circumstances.", "Only if you are an airline pilot."], "correct_answer": "No, under no circumstances.", "explanation": "Class A airspace (from 18,000 feet MSL up to FL600) requires flight under Instrument Flight Rules (IFR) and specific equipment, making it inaccessible to ultralights."},
            {"question_text": "What does a solid magenta line on a sectional chart depict?", "options": ["Class C Airspace", "Class D Airspace", "Class B Airspace", "The boundary of Class G airspace"], "correct_answer": "Class C Airspace", "explanation": "Solid magenta lines are used to show the lateral boundaries of Class C airspace."},
            {"question_text": "You are flying in Class G airspace. At 800 feet AGL, what is your cloud clearance requirement?", "options": ["500 feet below, 1000 above", "1000 feet horizontal", "Remain clear of clouds", "3 miles visibility"], "correct_answer": "Remain clear of clouds", "explanation": "In Class G airspace at 1,200 feet AGL or less, the only cloud clearance requirement is to remain clear of clouds, with 1 mile of visibility."},
            {"question_text": "When can you operate in Class E airspace without ATC authorization?", "options": ["Never", "Only at night", "When it does not extend to the surface at an airport", "Anytime, as it is uncontrolled"], "correct_answer": "When it does not extend to the surface at an airport", "explanation": "Ultralights can operate in Class E airspace, but are prohibited from the surface-based Class E areas designated for an airport without prior ATC authorization."},
            {"question_text": "What is the main reason ultralights are restricted from Class B, C, and D airspace?", "options": ["Ultralights are too slow.", "The high volume of fast, IFR traffic being managed by ATC.", "The air is too thin at those altitudes.", "Ultralights don't have radios."], "correct_answer": "The high volume of fast, IFR traffic being managed by ATC.", "explanation": "These classes of airspace surround the nation's busiest airports. Keeping slow, often non-radio equipped ultralights out is essential for the safety and efficiency of air traffic control."},
            {"question_text": "What does a solid blue line on a sectional chart depict?", "options": ["Class C Airspace", "Class D Airspace", "Class B Airspace", "A state border"], "correct_answer": "Class B Airspace", "explanation": "Solid blue lines are used to show the lateral boundaries of Class B airspace, the most restrictive type around major airports."},
            {"question_text": "You are approaching an airport surrounded by a dashed magenta line. What does this mean?", "options": ["It is a Class D airport.", "It is a Class C airport.", "It is a Class E surface area, and you need permission to enter.", "It is a military airport and is off-limits."], "correct_answer": "It is a Class E surface area, and you need permission to enter.", "explanation": "A dashed magenta line indicates that Class E airspace extends down to the surface. You must have prior ATC authorization to operate within it."},
            {"question_text": "What is the floor of Class A airspace in the United States?", "options": ["10,000 feet MSL", "14,500 feet MSL", "18,000 feet MSL", "60,000 feet MSL"], "correct_answer": "18,000 feet MSL", "explanation": "Class A airspace begins at 18,000 feet Mean Sea Level (MSL) and extends up to Flight Level 600 (approximately 60,000 feet)."},
            {"question_text": "What is the minimum flight visibility required to operate in Class G airspace at 10,500 feet MSL during the day?", "options": ["1 statute mile", "3 statute miles", "5 statute miles", "Clear of clouds"], "correct_answer": "5 statute miles", "explanation": "Above 10,000 feet MSL in Class G airspace, the visibility requirement increases to 5 statute miles."},
            {"question_text": "You see an area on your chart marked with 'P-40'. What does this 'P' stand for?", "options": ["Private", "Prohibited", "Practice", "Parachute"], "correct_answer": "Prohibited", "explanation": "'P' followed by a number denotes a Prohibited Area. Entry into this airspace is strictly forbidden at all times for all aircraft."},
            {"question_text": "What does a shaded magenta line on a sectional chart indicate?", "options": ["The floor of Class E airspace is at the surface.", "The floor of Class E airspace is at 700 feet AGL.", "The floor of Class G airspace is at 700 feet AGL.", "A military training route."], "correct_answer": "The floor of Class E airspace is at 700 feet AGL.", "explanation": "This shading, or vignette, indicates that the floor of the controlled Class E airspace begins at 700 feet above the ground, with Class G below it."},
            {"question_text": "What is a MOA (Military Operations Area)?", "options": ["An area where all flight is prohibited.", "An area where military training activities are conducted; VFR flight is allowed but extreme caution is advised.", "An area reserved for military landings.", "An area with mandatory radio contact."], "correct_answer": "An area where military training activities are conducted; VFR flight is allowed but extreme caution is advised.", "explanation": "Pilots are not forbidden from entering a MOA, but should be aware that high-speed military aircraft may be operating. It is wise to check the active times of the MOA before flight."},
            {"question_text": "What is the typical vertical limit of Class D airspace?", "options": ["1,200 feet AGL", "2,500 feet AGL", "4,000 feet AGL", "10,000 feet MSL"], "correct_answer": "2,500 feet AGL", "explanation": "Class D airspace typically extends from the surface up to 2,500 feet above the airport elevation."},
            {"question_text": "What are the cloud clearance requirements in Class G airspace above 1,200 feet AGL but below 10,000 feet MSL?", "options": ["Clear of clouds", "500 ft below, 1000 ft above, 2000 ft horizontal", "1000 ft below, 1000 ft above, 1 mile horizontal", "500 ft on all sides"], "correct_answer": "500 ft below, 1000 ft above, 2000 ft horizontal", "explanation": "These are the standard '512' cloud clearance requirements for this block of airspace."},
            {"question_text": "You are flying at 1,000 feet AGL in Class G airspace. What is the minimum flight visibility required?", "options": ["1 statute mile", "3 statute miles", "5 statute miles", "1/2 statute mile"], "correct_answer": "1 statute mile", "explanation": "Below 1,200 feet AGL in Class G, the minimum visibility is 1 statute mile and you must remain clear of clouds."},
            {"question_text": "What does an 'R' followed by a number (e.g., R-2501) on a sectional chart denote?", "options": ["A radio frequency", "A Restricted Area", "A runway", "A reporting point"], "correct_answer": "A Restricted Area", "explanation": "Restricted Areas contain unusual, often invisible hazards like artillery firing or aerial gunnery. Flight within these areas is not wholly prohibited, but is subject to restrictions. You cannot enter when it is 'active' without permission."},
            {"question_text": "What is the primary difference between Class C and Class D airspace?", "options": ["Class C is larger and has more stringent equipment/communication requirements.", "Class D is for military airports only.", "Class C is uncontrolled.", "There is no difference."], "correct_answer": "Class C is larger and has more stringent equipment/communication requirements.", "explanation": "Class C airspace surrounds busier airports than Class D and generally requires two-way radio communication and a transponder with altitude reporting for all aircraft, not just ultralights seeking entry."},
            {"question_text": "What does the 'ceiling' of Class G airspace refer to?", "options": ["The maximum altitude an ultralight can fly.", "The altitude where the overlying controlled airspace (usually Class E) begins.", "18,000 feet MSL.", "The height of the clouds."], "correct_answer": "The altitude where the overlying controlled airspace (usually Class E) begins.", "explanation": "Class G is the airspace that exists underneath controlled airspace. The 'ceiling' is simply the floor of the Class E or other airspace above it."},
            {"question_text": "What is a TFR (Temporary Flight Restriction)?", "options": ["A permanent restricted area.", "A type of military training route.", "A temporary area where flight is restricted due to hazards, security, or special events.", "A type of weather forecast."], "correct_answer": "A temporary area where flight is restricted due to hazards, security, or special events.", "explanation": "TFRs are issued for events like wildfires, VIP movements (like the President), airshows, or major sporting events. It is critical to check for TFRs before every flight as violations are taken very seriously."},
            {"question_text": "If you are flying toward a Class B airspace boundary shown on your GPS, what should you do?", "options": ["Fly directly over it.", "Turn to avoid entering it well before you reach the boundary.", "Climb above it.", "Try to contact ATC on the radio."], "correct_answer": "Turn to avoid entering it well before you reach the boundary.", "explanation": "As an ultralight pilot, you do not have permission to enter Class B airspace. You must remain clear of it at all times, and turning away early is the safest course of action."},
            {"question_text": "What is an Alert Area, marked with an 'A' on a chart?", "options": ["An area with a high volume of pilot training or unusual aerial activity.", "An area where alerts are broadcast on the radio.", "An area with alerts for bad weather.", "An area where aerobatics are prohibited."], "correct_answer": "An area with a high volume of pilot training or unusual aerial activity.", "explanation": "Similar to a MOA, entry is not prohibited, but pilots should be extra vigilant for other aircraft when flying through an Alert Area."},
            {"question_text": "The lateral dimensions of Class D airspace are typically based on:", "options": ["A 5-nautical-mile radius from the airport.", "The instrument approach procedures for that airport.", "A 10-nautical-mile radius from the airport.", "The size of the city it serves."], "correct_answer": "The instrument approach procedures for that airport.", "explanation": "The size and shape of Class D airspace are tailored to contain the instrument approach paths for that specific airport, which is why they are not all perfect circles."},
            {"question_text": "What are the cloud clearance requirements above 10,000 feet MSL in Class G airspace?", "options": ["500 ft below, 1000 ft above, 2000 ft horizontal", "1000 ft below, 1000 ft above, 1 statute mile horizontal", "Clear of clouds", "2000 ft below, 2000 ft above, 2 miles horizontal"], "correct_answer": "1000 ft below, 1000 ft above, 1 statute mile horizontal", "explanation": "Along with 5 miles visibility, these are the '111' cloud clearance rules for high-altitude Class G airspace."},
            {"question_text": "What does an un-shaded (white) area on a sectional chart in the Western US generally signify?", "options": ["The floor of Class E airspace begins at 700 feet AGL.", "The floor of Class E airspace begins at 1,200 feet AGL.", "The floor of Class E airspace begins at 14,500 feet MSL.", "The area is prohibited."], "correct_answer": "The floor of Class E airspace begins at 14,500 feet MSL.", "explanation": "In the western US, particularly in mountainous areas, the white un-shaded areas indicate that Class G airspace extends from the surface all the way up to 14,500 feet MSL."},
            {"question_text": "You see a group of parachutists on your chart. What should you do when flying near this area?", "options": ["Nothing, they will avoid you.", "Be extra vigilant and yield the right of way to any parachutists.", "Fly directly over the symbol.", "Avoid the area by at least 20 miles."], "correct_answer": "Be extra vigilant and yield the right of way to any parachutists.", "explanation": "The parachute symbol indicates a parachute jumping area. While flying through is not prohibited, it requires extreme caution to look for both the jump plane and the jumpers themselves."},
            {"question_text": "Is two-way radio communication required for an ultralight to operate in Class G airspace?", "options": ["Yes, at all times.", "No, radio communication is not required in Class G.", "Only above 1,200 feet AGL.", "Only near airports."], "correct_answer": "No, radio communication is not required in Class G.", "explanation": "Class G is uncontrolled airspace, and as such, there are no equipment or communication requirements for VFR aircraft, including ultralights."},
            {"question_text": "If you inadvertently fly into a cloud in Class G airspace, what have you violated?", "options": ["The speed limit.", "The right-of-way rules.", "VFR weather minimums.", "The hazardous operation rule."], "correct_answer": "VFR weather minimums.", "explanation": "Part 103.23 requires you to remain clear of clouds (or at specific distances from them). Entering a cloud means you are no longer meeting these VFR requirements."},

            # Category: Basic Weather for VFR Flight (30 Questions)
            {"question_text": "What is density altitude?", "options": ["The altitude shown on the altimeter.", "The physical height of the aircraft above the ground.", "Pressure altitude corrected for non-standard temperature.", "The legal ceiling for ultralight flight."], "correct_answer": "Pressure altitude corrected for non-standard temperature.", "explanation": "Density altitude is a measure of air density. High temperature, high altitude, and high humidity all lead to high density altitude, which significantly degrades aircraft performance."},
            {"question_text": "How does high density altitude affect your ultralight's performance?", "options": ["It improves performance.", "It has no effect.", "It significantly degrades takeoff, climb, and engine performance.", "It only affects landing distance."], "correct_answer": "It significantly degrades takeoff, climb, and engine performance.", "explanation": "In less dense air (high density altitude), the engine produces less power and the wings produce less lift, resulting in longer takeoff rolls and poor climb rates."},
            {"question_text": "What is the primary danger of flying a VFR-only vehicle like an ultralight into clouds (IMC)?", "options": ["The engine might get wet.", "The wings could ice up.", "Spatial disorientation leading to loss of control.", "It is harder to navigate."], "correct_answer": "Spatial disorientation leading to loss of control.", "explanation": "Without visual reference to the horizon, the human body's inner ear can give false sensations of turning or climbing, leading to spatial disorientation and subsequent loss of aircraft control."},
            {"question_text": "You are on the ground and see a windsock that is limp. What does this indicate?", "options": ["Strong winds", "Variable winds", "Winds are calm or very light", "The airport is closed"], "correct_answer": "Winds are calm or very light", "explanation": "A limp windsock indicates there is little to no wind at the surface."},
            {"question_text": "What is mechanical turbulence?", "options": ["Turbulence from a failing engine.", "Turbulence created by rising columns of warm air.", "Turbulence caused by wind flowing over uneven terrain, buildings, or trees.", "Turbulence from another aircraft's wake."], "correct_answer": "Turbulence caused by wind flowing over uneven terrain, buildings, or trees.", "explanation": "Mechanical turbulence is the result of friction and disruption of airflow as it moves over obstacles on the surface."},
            {"question_text": "What kind of weather is typically associated with a stable air mass?", "options": ["Thunderstorms and good visibility.", "Steady precipitation and poor visibility (stratiform clouds).", "Gusty winds and clear skies.", "Rapidly changing conditions."], "correct_answer": "Steady precipitation and poor visibility (stratiform clouds).", "explanation": "Stable air resists vertical motion, leading to the formation of widespread, layered clouds (stratus) and conditions like fog and drizzle with poor visibility."},
            {"question_text": "What is a primary characteristic of an unstable air mass?", "options": ["Smooth air", "Widespread fog", "Good visibility and vertical cloud development (cumulus clouds).", "Consistent winds"], "correct_answer": "Good visibility and vertical cloud development (cumulus clouds).", "explanation": "Unstable air encourages vertical motion, which tends to lift pollutants upwards, leading to good surface visibility. It also leads to the formation of puffy cumulus clouds, which can grow into thunderstorms."},
            {"question_text": "You are planning a flight on a hot, humid summer day. What performance consideration is most important?", "options": ["The aircraft will be faster.", "High density altitude will increase your takeoff roll and reduce climb rate.", "The controls will feel mushy.", "The engine will be more efficient."], "correct_answer": "High density altitude will increase your takeoff roll and reduce climb rate.", "explanation": "Hot and humid conditions significantly increase density altitude, making the air less dense and reducing overall aircraft performance. This is a critical safety consideration."},
            {"question_text": "What is wind shear?", "options": ["A type of propeller.", "A sudden, drastic change in wind speed and/or direction over a small area.", "The average wind speed.", "A tool for measuring wind."], "correct_answer": "A sudden, drastic change in wind speed and/or direction over a small area.", "explanation": "Wind shear can occur at any altitude and is a serious hazard, especially during takeoff and landing, as it can cause rapid changes in airspeed and lift."},
            {"question_text": "What does the term 'VFR' stand for?", "options": ["Variable Flight Rules", "Visual Flight Rules", "Verified Flight Route", "Very Fast Route"], "correct_answer": "Visual Flight Rules", "explanation": "VFR are the set of regulations under which a pilot operates an aircraft in weather conditions clear enough to allow the pilot to see where the aircraft is going."},
            {"question_text": "If the temperature and dew point are very close together, what type of weather is likely to form?", "options": ["Strong winds", "Clear skies", "Fog or low clouds", "Thunderstorms"], "correct_answer": "Fog or low clouds", "explanation": "When the temperature cools to the dew point, the air becomes saturated, and the water vapor condenses into visible moisture, forming fog or clouds."},
            {"question_text": "What is a safe and prudent action if you are flying and encounter weather that is worse than forecast?", "options": ["Climb above it.", "Fly faster to get through it.", "Turn around and return to your departure point or land at a nearby suitable airport.", "Continue, as the forecast is probably right."], "correct_answer": "Turn around and return to your departure point or land at a nearby suitable airport.", "explanation": "The safest course of action is always to avoid bad weather. Pressing on into deteriorating conditions is a leading cause of accidents."},
            {"question_text": "Why is it dangerous to fly on the leeward (downwind) side of a mountain in strong winds?", "options": ["The air is too thin.", "It is colder.", "The presence of powerful downdrafts and rotor turbulence.", "The visibility is always poor."], "correct_answer": "The presence of powerful downdrafts and rotor turbulence.", "explanation": "Air flowing over a mountain can create strong downdrafts on the leeward side that can exceed the climb capability of an aircraft, as well as severe turbulence."},
            {"question_text": "What is 'radiation fog'?", "options": ["Fog caused by nuclear fallout.", "Fog that forms on clear nights as the ground cools, cooling the air above it to the dew point.", "Fog that advects in from the ocean.", "Fog that forms when rain falls through cool air."], "correct_answer": "Fog that forms on clear nights as the ground cools, cooling the air above it to the dew point.", "explanation": "This type of fog is common in calm, clear conditions at night and typically burns off in the morning as the sun heats the ground."},
            {"question_text": "What is the best way to get a weather briefing before a flight?", "options": ["Look outside.", "Call a friend who is a pilot.", "Use official sources like aviationweather.gov or call 1-800-WX-BRIEF.", "Watch the evening news."], "correct_answer": "Use official sources like aviationweather.gov or call 1-800-WX-BRIEF.", "explanation": "Official sources provide the most accurate, comprehensive, and legally recognized weather information tailored for aviation."},
            {"question_text": "What is a microburst?", "options": ["A small thunderstorm.", "A short burst of rain.", "A powerful, localized downdraft that can be extremely hazardous to aircraft.", "A type of cloud."], "correct_answer": "A powerful, localized downdraft that can be extremely hazardous to aircraft.", "explanation": "Microbursts are often associated with thunderstorms and create intense wind shear, posing a severe threat to aircraft, especially at low altitudes."},
            {"question_text": "What effect does a strong headwind have on your groundspeed?", "options": ["It increases groundspeed.", "It decreases groundspeed.", "It has no effect on groundspeed.", "It only affects airspeed."], "correct_answer": "It decreases groundspeed.", "explanation": "A headwind opposes your forward motion over the ground, reducing your groundspeed and increasing the time it takes to reach your destination."},
            {"question_text": "What effect does a strong tailwind have on your landing distance?", "options": ["It decreases landing distance.", "It increases landing distance.", "It has no effect.", "It makes the landing smoother."], "correct_answer": "It increases landing distance.", "explanation": "A tailwind increases your speed over the ground, meaning you will touch down at a higher groundspeed and require a much longer runway to stop."},
            {"question_text": "What is 'advection fog'?", "options": ["Fog that forms on mountains.", "Fog that forms when moist air moves over a colder surface, cooling it to the dew point.", "Fog that forms at night.", "Fog that is man-made."], "correct_answer": "Fog that forms when moist air moves over a colder surface, cooling it to the dew point.", "explanation": "This is common in coastal areas where moist sea air blows over cooler land."},
            {"question_text": "Why is it a good idea to add a 'personal weather minimums' buffer to the legal VFR minimums?", "options": ["It is required by the FAA.", "It provides an extra margin of safety and reduces stress.", "It makes the flight more challenging.", "It is not a good idea."], "correct_answer": "It provides an extra margin of safety and reduces stress.", "explanation": "Legal minimums are not always safe minimums. Having higher personal minimums (e.g., 3 miles visibility instead of 1) keeps you further away from dangerous conditions."},
            {"question_text": "What is a 'crosswind'?", "options": ["Wind blowing directly at the nose of the aircraft.", "Wind blowing directly from behind the aircraft.", "Wind blowing from the side, across the runway or flight path.", "A type of turbulence."], "correct_answer": "Wind blowing from the side, across the runway or flight path.", "explanation": "Crosswinds are a major factor in takeoffs and landings, as they require specific pilot control inputs to keep the aircraft aligned with the runway."},
            {"question_text": "What is a likely consequence of flying an ultralight in winds that are gusting close to its stall speed?", "options": ["A smoother ride.", "Better engine performance.", "A high risk of losing control of the aircraft.", "A shorter takeoff roll."], "correct_answer": "A high risk of losing control of the aircraft.", "explanation": "If a gust causes the airspeed to drop suddenly below the stall speed, the aircraft can stall and lose lift at a very low altitude with no room for recovery."},
            {"question_text": "What does a line of thunderstorms indicate?", "options": ["A stable airmass.", "The passage of a cold front.", "Calm weather is on the way.", "Good flying conditions."], "correct_answer": "The passage of a cold front.", "explanation": "Squall lines, or lines of thunderstorms, often form along or ahead of a fast-moving cold front, indicating severe weather and unstable air."},
            {"question_text": "What is 'rime ice'?", "options": ["A type of clear ice.", "A rough, milky, opaque ice formed by the instantaneous freezing of small supercooled water droplets.", "Ice that forms on the ground.", "A type of anti-icing fluid."], "correct_answer": "A rough, milky, opaque ice formed by the instantaneous freezing of small supercooled water droplets.", "explanation": "Rime ice can build up on airfoils and disrupt the smooth flow of air, reducing lift and increasing drag. Ultralights are not equipped to fly in icing conditions."},
            {"question_text": "If you see towering cumulus clouds, what does this suggest about the air?", "options": ["It is stable.", "It is unstable and contains strong vertical air currents.", "It is very cold.", "It is safe to fly through them."], "correct_answer": "It is unstable and contains strong vertical air currents.", "explanation": "Towering cumulus clouds are a sign of significant lifting action and instability, and they can quickly develop into thunderstorms."},
            {"question_text": "Why is it important to know the freezing level?", "options": ["To know when to turn on the heater.", "To avoid structural icing if flying in visible moisture.", "It is not important for ultralights.", "To calculate density altitude."], "correct_answer": "To avoid structural icing if flying in visible moisture.", "explanation": "The freezing level is the altitude at which the temperature is 0° Celsius. Flying above this level in clouds or precipitation can cause dangerous ice to form on the aircraft."},
            {"question_text": "What is a simple way to determine the direction of the wind on the ground?", "options": ["Look at the direction the clouds are moving.", "Observe a windsock or the smoke from a chimney.", "Check the GPS.", "Assume it is the same as the runway direction."], "correct_answer": "Observe a windsock or the smoke from a chimney.", "explanation": "Visual indicators on the ground like windsocks, flags, or smoke provide a direct and reliable indication of the surface wind direction and general strength."},
            {"question_text": "What is a 'sea breeze'?", "options": ["A wind that blows from the sea toward the land, typically during the day.", "A wind that blows from the land toward the sea, typically during the day.", "A type of fog.", "A coastal storm."], "correct_answer": "A wind that blows from the sea toward the land, typically during the day.", "explanation": "During the day, the land heats up faster than the sea, causing the cooler, denser air from the sea to move inland to replace the rising warm air."},
            {"question_text": "You check the weather and the forecast calls for 'gusts to 30 knots'. Your ultralight has a top speed of 55 knots. Is this a safe condition to fly in?", "options": ["Yes, because the top speed is higher than the gusts.", "No, strong and gusty winds are extremely hazardous to a lightweight ultralight.", "Yes, if you fly into the wind.", "Only if you are an experienced pilot."], "correct_answer": "No, strong and gusty winds are extremely hazardous to a lightweight ultralight.", "explanation": "Gusty conditions can cause rapid changes in airspeed and control challenges that can easily exceed the capability of an ultralight and its pilot, regardless of experience."},
            {"question_text": "What is the primary cause of all weather?", "options": ["The rotation of the Earth.", "Uneven heating of the Earth's surface by the sun.", "The phases of the moon.", "Volcanic eruptions."], "correct_answer": "Uneven heating of the Earth's surface by the sun.", "explanation": "The differential heating of the planet creates temperature and pressure differences in the atmosphere, which in turn drives wind and all other weather phenomena."},
            
            # Category: Aerodynamics for Ultralights (23 Questions)
            {"question_text": "An aerodynamic stall is caused by:", "options": ["The engine quitting", "Flying too slowly", "Exceeding the wing's critical angle of attack", "Flying in turbulence"], "correct_answer": "Exceeding the wing's critical angle of attack", "explanation": "A stall is a purely aerodynamic event that occurs when the angle of attack becomes so great that the airflow separates from the wing's upper surface, causing a loss of lift. It can happen at any airspeed."},
            {"question_text": "In a 60-degree banked turn, the load factor on the aircraft is 2 Gs. How does this affect stall speed?", "options": ["Stall speed decreases", "Stall speed is unaffected", "Stall speed increases", "Stall speed doubles"], "correct_answer": "Stall speed increases", "explanation": "Increased load factor increases the weight the wings must support, which requires more lift. Since stall speed increases with weight (and load factor), the aircraft will stall at a higher indicated airspeed."},
            {"question_text": "What are the four forces of flight in equilibrium during straight-and-level, unaccelerated flight?", "options": ["Lift, Weight, Thrust, Drag", "Gravity, Power, Inertia, Friction", "Lift, Gravity, Speed, Drag", "Weight, Thrust, AOA, Speed"], "correct_answer": "Lift, Weight, Thrust, Drag", "explanation": "In steady flight, the upward force of Lift equals the downward force of Weight, and the forward force of Thrust equals the rearward force of Drag."},
            {"question_text": "What is the immediate and correct recovery procedure from an aerodynamic stall?", "options": ["Increase power to full and pull back.", "Level the wings with aileron.", "Decrease the angle of attack by lowering the nose.", "Deploy flaps immediately."], "correct_answer": "Decrease the angle of attack by lowering the nose.", "explanation": "The only way to recover from a stall is to reduce the angle of attack below the critical AOA. This is done by pushing the control stick forward to lower the nose."},
            {"question_text": "What is 'adverse yaw'?", "options": ["The tendency of the aircraft to yaw in the opposite direction of the roll.", "A type of engine problem.", "Yawing caused by a crosswind.", "A desirable flight characteristic."], "correct_answer": "The tendency of the aircraft to yaw in the opposite direction of the roll.", "explanation": "When rolling into a turn, the outside, upward-deflected aileron creates more drag, pulling the nose away from the turn. This must be corrected with rudder."},
            {"question_text": "Which flight control surface controls the aircraft's pitch (movement around the lateral axis)?", "options": ["Ailerons", "Rudder", "Elevator", "Flaps"], "correct_answer": "Elevator", "explanation": "The elevator, located on the horizontal stabilizer, controls the pitch of the aircraft, causing the nose to move up or down."},
            {"question_text": "Which flight control surface controls the aircraft's roll (movement around the longitudinal axis)?", "options": ["Ailerons", "Rudder", "Elevator", "Trim tab"], "correct_answer": "Ailerons", "explanation": "The ailerons, located on the trailing edge of the wings, move in opposite directions to create a differential in lift, causing the aircraft to roll or bank."},
            {"question_text": "What is the purpose of flaps?", "options": ["To increase the aircraft's top speed.", "To increase both lift and drag, allowing for a steeper approach and slower landing speed.", "To help steer the aircraft on the ground.", "To cool the engine."], "correct_answer": "To increase both lift and drag, allowing for a steeper approach and slower landing speed.", "explanation": "Flaps are high-lift devices that allow an aircraft to fly at a slower airspeed and descend at a steeper angle without increasing its speed."},
            {"question_text": "What is 'ground effect'?", "options": ["The tendency of the aircraft to be pulled towards the ground by magnetism.", "An aerodynamic effect where the wings become more efficient due to the compression of air between the wings and the ground.", "The turbulence felt when flying close to the ground.", "The effect of wind on groundspeed."], "correct_answer": "An aerodynamic effect where the wings become more efficient due to the compression of air between the wings and the ground.", "explanation": "Ground effect reduces induced drag and allows the aircraft to 'float' during landing. It can also cause an aircraft to become airborne before it has reached a safe climbing speed."},
            {"question_text": "What is the relationship between airspeed and lift?", "options": ["Lift decreases as airspeed increases.", "Lift increases as the square of the airspeed increases.", "Airspeed and lift are not related.", "Lift is directly proportional to airspeed."], "correct_answer": "Lift increases as the square of the airspeed increases.", "explanation": "The lift equation shows that lift is proportional to the square of the velocity (L ~ V^2). This means doubling your airspeed quadruples the amount of lift generated, all else being equal."},
            {"question_text": "What is 'induced drag'?", "options": ["Drag from the landing gear.", "Drag that is a byproduct of producing lift.", "Drag from the friction of air over the fuselage.", "Drag from a dirty windscreen."], "correct_answer": "Drag that is a byproduct of producing lift.", "explanation": "Induced drag is created by the wingtip vortices that form as a result of the high-pressure air below the wing trying to move to the low-pressure area above it. It is greatest at slow airspeeds and high angles of attack."},
            {"question_text": "What is 'parasite drag'?", "options": ["Drag that helps the aircraft fly.", "Drag that is a byproduct of lift.", "Drag caused by the shape of the aircraft and the friction of air moving over its surfaces.", "Drag that is induced by a passenger."], "correct_answer": "Drag caused by the shape of the aircraft and the friction of air moving over its surfaces.", "explanation": "Parasite drag is composed of form drag, skin friction drag, and interference drag. It increases as the square of the airspeed."},
            {"question_text": "At what point is total drag at a minimum?", "options": ["At the slowest possible airspeed.", "At the fastest possible airspeed.", "Where parasite drag and induced drag are equal.", "Total drag is always constant."], "correct_answer": "Where parasite drag and induced drag are equal.", "explanation": "This point on the drag curve corresponds to the aircraft's best glide speed and maximum endurance speed."},
            {"question_text": "What is the 'angle of incidence'?", "options": ["The angle between the wing and the relative wind.", "The fixed angle at which the wing is mounted to the fuselage.", "The angle of the engine on its mount.", "The angle of the landing gear."], "correct_answer": "The fixed angle at which the wing is mounted to the fuselage.", "explanation": "This is a built-in design feature and, unlike the angle of attack, cannot be changed by the pilot during flight."},
            {"question_text": "What is the primary function of the rudder?", "options": ["To turn the aircraft.", "To control yaw, the movement of the nose left and right.", "To make the aircraft climb.", "To slow the aircraft down."], "correct_answer": "To control yaw, the movement of the nose left and right.", "explanation": "While the rudder can be used to help initiate a turn, its primary purpose is to control yaw and to counteract adverse yaw during a roll."},
            {"question_text": "What is 'longitudinal stability'?", "options": ["Stability around the vertical axis (yaw).", "Stability around the longitudinal axis (roll).", "Stability around the lateral axis (pitch).", "The overall strength of the aircraft."], "correct_answer": "Stability around the lateral axis (pitch).", "explanation": "This refers to the aircraft's tendency to resist pitching up or down and to return to a level flight attitude on its own."},
            {"question_text": "What is the center of gravity (CG)?", "options": ["The center point of the wings.", "The point where the aircraft would balance if suspended.", "The location of the fuel tank.", "The point where thrust is generated."], "correct_answer": "The point where the aircraft would balance if suspended.", "explanation": "The CG is a critical point for stability and control. Its position relative to the center of lift determines the aircraft's handling characteristics."},
            {"question_text": "What happens if the CG is too far aft (rearward)?", "options": ["The aircraft becomes excessively nose-heavy.", "The aircraft becomes unstable and difficult or impossible to recover from a stall.", "The aircraft becomes more stable.", "The aircraft will not take off."], "correct_answer": "The aircraft becomes unstable and difficult or impossible to recover from a stall.", "explanation": "An aft CG is extremely dangerous as it reduces the authority of the elevator and can make the aircraft longitudinally unstable, leading to a flat spin from which recovery is not possible."},
            {"question_text": "What is 'P-factor'?", "options": ["A type of propeller.", "A tendency for the aircraft to yaw to the left at high power and high angles of attack.", "A measure of engine power.", "A factor in the lift equation."], "correct_answer": "A tendency for the aircraft to yaw to the left at high power and high angles of attack.", "explanation": "In most American engines, the descending propeller blade on the right has a higher angle of attack than the ascending blade on the left, creating more thrust on the right side and yawing the aircraft to the left."},
            {"question_text": "What is the purpose of a trim tab?", "options": ["To make the aircraft turn faster.", "To relieve control pressures and reduce pilot fatigue.", "To act as a backup control surface.", "To increase drag for landing."], "correct_answer": "To relieve control pressures and reduce pilot fatigue.", "explanation": "Trim tabs are small, adjustable surfaces on the trailing edge of the main control surfaces (like the elevator) that can be set to hold the control surface in a desired position, so the pilot doesn't have to maintain constant pressure on the stick."},
            {"question_text": "A 'canard' is a type of aircraft design that features:", "options": ["No tail.", "The horizontal stabilizer at the front of the aircraft.", "Two sets of wings.", "A V-shaped tail."], "correct_answer": "The horizontal stabilizer at the front of the aircraft.", "explanation": "In a canard design, the smaller foreplane (the canard) is located ahead of the main wing, providing pitch control and lift."},
            {"question_text": "What is a 'spin'?", "options": ["A steep, spiraling descent.", "An aggravated stall that results in autorotation.", "A type of aerobatic maneuver.", "A sharp turn."], "correct_answer": "An aggravated stall that results in autorotation.", "explanation": "A spin occurs when one wing is stalled more deeply than the other, causing the aircraft to descend in a corkscrew path. Recovery requires a specific control sequence and is extremely dangerous at low altitudes."},
            {"question_text": "How does frost on the wings affect flight characteristics?", "options": ["It makes the wings smoother and more efficient.", "It disrupts the smooth flow of air, reducing lift and increasing the stall speed.", "It has no significant effect.", "It helps cool the wings."], "correct_answer": "It disrupts the smooth flow of air, reducing lift and increasing the stall speed.", "explanation": "Even a thin layer of frost, as rough as sandpaper, can disrupt airflow enough to prevent the aircraft from becoming airborne or cause it to stall at a much higher speed than normal. All frost must be removed before flight."},
            {"question_text": "What is the 'chord line' of a wing?", "options": ["The top surface of the wing.", "The bottom surface of the wing.", "An imaginary straight line from the leading edge to the trailing edge of the wing.", "The thickest part of the wing."], "correct_answer": "An imaginary straight line from the leading edge to the trailing edge of the wing.", "explanation": "The chord line is the standard reference line used to define the angle of attack, which is the angle between the chord line and the relative wind."},
            {"question_text": "What is the primary reason for 'wing washout' (a slight upward twist at the wingtips)?", "options": ["To improve the aircraft's appearance.", "To ensure the wing root stalls before the wingtip, maintaining aileron control during a stall.", "To increase the aircraft's top speed.", "To reduce the weight of the wings."], "correct_answer": "To ensure the wing root stalls before the wingtip, maintaining aileron control during a stall.", "explanation": "Washout causes the wingtips to have a lower angle of attack than the wing roots. This design feature helps prevent a sudden, complete loss of aileron control when the aircraft approaches a stall."},
            {"question_text": "What is 'Bernoulli's Principle' as it relates to lift?", "options": ["For every action, there is an equal and opposite reaction.", "The pressure of a fluid (like air) decreases as its speed increases.", "An object in motion stays in motion.", "Energy can neither be created nor destroyed."], "correct_answer": "The pressure of a fluid (like air) decreases as its speed increases.", "explanation": "Air flowing over the curved top surface of a wing travels faster than the air below it, creating lower pressure on top. This pressure differential results in an upward force called lift."},
            {"question_text": "What happens to the center of pressure as the angle of attack increases?", "options": ["It moves forward.", "It moves backward.", "It does not move.", "It moves to the wingtip."], "correct_answer": "It moves forward.", "explanation": "As the angle of attack increases (up to the point of stall), the center of pressure, which is the average point of the lifting force, tends to move forward along the wing's chord line."},
            {"question_text": "What is 'dihedral'?", "options": ["The downward angle of the wings.", "The upward angle of the wings from the root to the tip.", "The sweepback angle of the wings.", "The shape of the wingtip."], "correct_answer": "The upward angle of the wings from the root to the tip.", "explanation": "Dihedral increases lateral (roll) stability. If a wing drops, the dihedral causes it to generate more lift than the opposite wing, helping to level the aircraft."},
            {"question_text": "What is the 'best glide speed' (L/D max)?", "options": ["The speed that provides the greatest forward distance for a given loss of altitude.", "The speed that allows the aircraft to stay in the air for the longest time.", "The fastest safe speed to fly.", "The slowest safe speed to fly."], "correct_answer": "The speed that provides the greatest forward distance for a given loss of altitude.", "explanation": "This is the speed where the lift-to-drag ratio (L/D) is at its maximum. It is the most important speed to know during an engine failure."},
            {"question_text": "What is a 'winglet'?", "options": ["A small, secondary wing on the tail.", "A type of flap.", "A vertical extension at the wingtip that reduces induced drag.", "A control surface on the canard."], "correct_answer": "A vertical extension at the wingtip that reduces induced drag.", "explanation": "Winglets work by disrupting the formation of wingtip vortices, which are a primary source of induced drag. This makes the wing more efficient, especially at high altitudes and during long flights."},
            
            # Systems and Preflight
            {"question_text": "During a preflight, you find a small crack in a structural tube near the engine mount. What should you do?", "options": ["Fly a short, gentle flight to see if it gets worse.", "Wrap it with duct tape as a temporary fix.", "Ground the aircraft until it is properly repaired by a qualified person.", "Ignore it if it's less than an inch long."], "correct_answer": "Ground the aircraft until it is properly repaired by a qualified person.", "explanation": "Structural integrity is paramount. A small crack, especially in a high-stress area like an engine mount, can propagate rapidly under flight loads, leading to catastrophic failure. The aircraft must not be flown."},
            {"question_text": "Why is a consistent, methodical pre-flight inspection flow (e.g., always walking the same direction) important?", "options": ["It looks more professional to other pilots.", "It is the fastest way to complete the inspection.", "It significantly reduces the chance of forgetting to inspect a critical item.", "It is required by the FAA for all aircraft types."], "correct_answer": "It significantly reduces the chance of forgetting to inspect a critical item.", "explanation": "By developing a consistent habit and a physical flow around the aircraft, you build muscle memory and are far less likely to overlook a component, which could have serious safety implications."},
            {"question_text": "What are you looking for when you check the propeller before a flight?", "options": ["A high-gloss finish.", "The correct brand name.", "Nicks, cracks, security, and delamination.", "The proper torque on the spinner."], "correct_answer": "Nicks, cracks, security, and delamination.", "explanation": "A propeller is a highly stressed airfoil. Even a small nick can create a stress riser that develops into a crack and leads to blade failure in flight. It must be in near-perfect condition."},
            {"question_text": "Before the first flight of the day, what should be done with the fuel system?", "options": ["The fuel should be drained and replaced.", "A sample should be taken from the lowest point to check for water and contaminants.", "The fuel tank should be pressurized.", "The fuel lines should be polished for better flow."], "correct_answer": "A sample should be taken from the lowest point to check for water and contaminants.", "explanation": "Water can condense in fuel tanks and is heavier than fuel, settling at the bottom. Draining a sample from the sump or lowest point into a clear container allows you to check for water or debris that could clog the fuel system and cause engine failure."},
            {"question_text": "When checking flight control surfaces like ailerons and elevators, what should you be looking for?", "options": ["Correct color and paint condition.", "Free and correct movement, and security of hinges and connections.", "The manufacturer's logo.", "A specific amount of stiffness."], "correct_answer": "Free and correct movement, and security of hinges and connections.", "explanation": "You must ensure the controls move freely in the correct directions without binding, and that all hinges, control horns, cables, and pushrods are securely attached and not worn."},
            {"question_text": "What is a primary reason to check engine mounts during every preflight?", "options": ["To make sure they are clean.", "Engine vibration can cause cracks to form in the mounts, which can lead to engine separation.", "To check the engine's serial number.", "To ensure the paint is not chipped."], "correct_answer": "Engine vibration can cause cracks to form in the mounts, which can lead to engine separation.", "explanation": "Engine mounts are a very high-stress, high-vibration area. A failure of a mount in flight would be catastrophic. They must be inspected meticulously for any signs of cracking or distress."},
            {"question_text": "You notice your tire pressure seems a little low on one side. What is the correct action?", "options": ["Fly anyway, it will even out on landing.", "Properly inflate the tire to the manufacturer's recommended pressure before flying.", "Just add a little air, even if you don't know the correct pressure.", "Take off from the grass to cushion it."], "correct_answer": "Properly inflate the tire to the manufacturer's recommended pressure before flying.", "explanation": "Low tire pressure can cause poor ground handling, swerving on takeoff or landing, and potential damage to the wheel rim or landing gear."},
            {"question_text": "What is the main danger of a loose or cracked exhaust system component?", "options": ["It will be too loud.", "It can allow hot exhaust gases to blow on flammable parts of the airframe or create carbon monoxide hazards.", "It will reduce engine power slightly.", "It looks unprofessional."], "correct_answer": "It can allow hot exhaust gases to blow on flammable parts of the airframe or create carbon monoxide hazards.", "explanation": "A compromised exhaust system poses a significant fire risk and can introduce deadly carbon monoxide into the cockpit area."},
            {"question_text": "When inspecting the airframe's fabric covering, you should look for:", "options": ["The correct color.", "Tears, punctures, and areas that are becoming brittle or detached.", "A smooth, glossy finish.", "The amount of dust on the surface."], "correct_answer": "Tears, punctures, and areas that are becoming brittle or detached.", "explanation": "The fabric is the skin of the aircraft and is essential for producing lift. Any damage can disrupt airflow and compromise the structural integrity of the wing."},
            {"question_text": "Why should you check that the fuel cap is secure before flight?", "options": ["To prevent it from being stolen.", "To prevent fuel from siphoning out in flight and to keep water and debris out of the tank.", "To make sure it looks good.", "It is not a critical preflight item."], "correct_answer": "To prevent fuel from siphoning out in flight and to keep water and debris out of the tank.", "explanation": "A loose fuel cap can lead to a significant loss of fuel in flight due to the low pressure over the wing. It also allows contaminants to enter the fuel system."},
            {"question_text": "If your ultralight has a ballistic parachute system, what is an important preflight check?", "options": ["Test deploy it slightly.", "Ensure the safety pin is removed before flight and the activation handle is unobstructed.", "Check the parachute's color.", "Make sure the parachute is packed tightly."], "correct_answer": "Ensure the safety pin is removed before flight and the activation handle is unobstructed.", "explanation": "The system is useless if it cannot be activated. The safety pin must be in place during transport and storage, but removed before flight so the system can be deployed in an emergency."},
            {"question_text": "When checking control cables, what should you look for?", "options": ["Proper tension and any signs of fraying or corrosion.", "The correct color of the cable housing.", "How shiny the cable is.", "The length of the cable."], "correct_answer": "Proper tension and any signs of fraying or corrosion.", "explanation": "A frayed cable is a sign of impending failure. Broken strands significantly weaken the cable and can lead to a complete loss of control for that surface."},
            {"question_text": "What is the purpose of wiggling the wings and tail surfaces during a preflight?", "options": ["To warm up the aircraft.", "To check for structural looseness, bearing wear, or failed attachment points.", "To make sure they are flexible.", "To knock dust off the surfaces."], "correct_answer": "To check for structural looseness, bearing wear, or failed attachment points.", "explanation": "There should be no excessive play or clunking sounds. Any looseness could indicate a serious structural problem that needs to be addressed before flight."},
            {"question_text": "You find a single, non-critical bolt on a fairing is missing. What should you do?", "options": ["Fly, it's not a structural part.", "Replace the bolt before flying.", "Use a zip tie as a temporary replacement.", "Remove the bolt on the other side to make it symmetrical."], "correct_answer": "Replace the bolt before flying.", "explanation": "Even a 'non-critical' part can become a hazard if it detaches in flight and strikes a critical component like the propeller or a control surface. All parts should be properly secured."},
            {"question_text": "Why is it important to check your harness or seatbelt system before each flight?", "options": ["To make sure it is the right color.", "To check for wear, fraying on the webbing, and proper latching and adjustment.", "To make sure it is comfortable.", "To see if it needs to be cleaned."], "correct_answer": "To check for wear, fraying on the webbing, and proper latching and adjustment.", "explanation": "Your restraint system is your primary protection in a rough landing or accident. It must be in perfect working order to be effective."},
            {"question_text": "What does a 'chafed' fuel line mean?", "options": ["The fuel line is new.", "The fuel line has been rubbed and worn, creating a weak spot.", "The fuel line is clogged.", "The fuel line is the wrong color."], "correct_answer": "The fuel line has been rubbed and worn, creating a weak spot.", "explanation": "Chafing, often from vibration against another component, can wear through a fuel line, causing a dangerous fuel leak and potential in-flight fire."},
            {"question_text": "If your ultralight has basic instruments, what is a key check in the cockpit?", "options": ["Ensure the altimeter is set to the correct field elevation (if adjustable).", "Make sure the GPS has the latest maps.", "Polish the instrument glass.", "Check that the clock is set to the correct time."], "correct_answer": "Ensure the altimeter is set to the correct field elevation (if adjustable).", "explanation": "Setting the altimeter to the known field elevation before takeoff ensures it will provide accurate altitude readings relative to sea level during the flight."},
            {"question_text": "What is the danger of a small nick on the leading edge of a propeller?", "options": ["It reduces engine power.", "It creates a stress riser that can lead to a crack and blade failure.", "It makes the propeller unbalanced.", "It is only a cosmetic issue."], "correct_answer": "It creates a stress riser that can lead to a crack and blade failure.", "explanation": "The forces on a propeller are immense. A tiny point of damage concentrates these forces, making it the most likely point for a crack to form and propagate, with catastrophic results."},
            {"question_text": "When you drain fuel into a sampler cup, you see a bubble of clear liquid at the bottom. What is this likely to be?", "options": ["High-octane fuel.", "Water.", "Two-stroke oil.", "Air."], "correct_answer": "Water.", "explanation": "Water is denser than fuel and does not mix with it. It will sink to the bottom of the tank and the sampler cup. You must continue to drain fuel until no more water is present."},
            {"question_text": "Why should you never rush a preflight inspection?", "options": ["It can make you tired before the flight.", "A rushed inspection is more likely to miss a critical safety item.", "It's better to wait for the wind to calm down.", "You might get the aircraft dirty."], "correct_answer": "A rushed inspection is more likely to miss a critical safety item.", "explanation": "Complacency and rushing are major contributors to accidents. Taking your time and being methodical is a hallmark of a safe and professional pilot."},
            {"question_text": "What does 'control continuity' mean in a preflight check?", "options": ["The controls feel smooth.", "The control surfaces move in the correct direction in response to cockpit inputs.", "The control cables are new.", "The controls are connected electronically."], "correct_answer": "The control surfaces move in the correct direction in response to cockpit inputs.", "explanation": "It is a check to ensure that moving the stick left makes the left aileron go up, moving the stick back makes the elevator go up, etc. Mis-rigged controls are a rare but potentially fatal mistake."},
            {"question_text": "You find a puddle of oil under your engine. What does this indicate?", "options": ["The engine is properly lubricated.", "A potential oil leak that must be investigated before flight.", "Normal operation for a two-stroke engine.", "Someone spilled oil during the last servicing."], "correct_answer": "A potential oil leak that must be investigated before flight.", "explanation": "Any sign of a fluid leak (oil, fuel, or coolant) is a red flag. An oil leak could lead to engine seizure, while a fuel leak is a severe fire hazard. The source must be found and fixed."},
            {"question_text": "What is the purpose of checking for 'sludge' in a fuel filter bowl?", "options": ["Sludge is a sign of high-quality fuel.", "To ensure the filter is working.", "Sludge or debris indicates contamination in the fuel system that could clog the carburetor.", "To check the fuel color."], "correct_answer": "Sludge or debris indicates contamination in the fuel system that could clog the carburetor.", "explanation": "The filter is designed to trap contaminants. Finding significant debris means the fuel source may be contaminated or the tank has debris, which requires further investigation."},
            {"question_text": "If you have brakes on your ultralight, a preflight check should include:", "options": ["Checking for brake fluid leaks and firm pedal pressure.", "Making sure the brake pedals are shiny.", "Testing them at high speed.", "Adjusting them to be as loose as possible."], "correct_answer": "Checking for brake fluid leaks and firm pedal pressure.", "explanation": "You must ensure the brake system is functional before relying on it. This includes checking for leaks in the lines and ensuring the pedals or hand lever feels firm, not spongy."},
            {"question_text": "What is the final action of a preflight inspection?", "options": ["Wiping down the propeller.", "A final walk-around to ensure everything is secure and no items (like fuel caps or pitot covers) are out of place.", "Starting the engine.", "Getting in the cockpit."], "correct_answer": "A final walk-around to ensure everything is secure and no items (like fuel caps or pitot covers) are out of place.", "explanation": "After completing the detailed inspection, a final 'big picture' look can help you catch anything you might have missed, like a tool left on a wing or an unsecured cowling."},
            {"question_text": "Why is it important to know how much fuel you have before a flight?", "options": ["To calculate the aircraft's top speed.", "To ensure you have enough fuel for the planned flight plus a safe reserve.", "To make sure the aircraft is not too heavy.", "Fuel level is not a critical preflight item."], "correct_answer": "To ensure you have enough fuel for the planned flight plus a safe reserve.", "explanation": "Fuel exhaustion is a common cause of engine failure. You must know your fuel consumption rate and plan to have more than enough fuel for your intended flight, with a margin for error."},
            {"question_text": "You find a bird's nest inside the engine cowling. What should you do?", "options": ["Assume the bird will fly out when you start the engine.", "Remove the nest and inspect the area for any damage to wires or lines before flying.", "Fly, but keep the flight short.", "It is considered good luck and should be left alone."], "correct_answer": "Remove the nest and inspect the area for any damage to wires or lines before flying.", "explanation": "Nests can obstruct airflow, create a serious fire hazard, and the birds may have damaged critical components like ignition wires or fuel lines while building it."},
            {"question_text": "What does a 'flat spot' on a tire indicate?", "options": ["The tire is new.", "The tire has been sitting for a long time.", "The tire may have been worn unevenly due to skidding or misalignment.", "The tire is properly inflated."], "correct_answer": "The tire may have been worn unevenly due to skidding or misalignment.", "explanation": "A flat spot is a sign of abnormal wear and could be a weak point in the tire, increasing the risk of a blowout during takeoff or landing."},
            {"question_text": "During your cockpit check, you move the control stick and it feels 'gritty' or 'notchy'. What should you do?", "options": ["Fly anyway, it will smooth out in the air.", "This is normal for ultralights.", "Ground the aircraft and investigate the control system for a potential problem like a frayed cable or a failing bearing.", "Apply some lubricant to the stick pivot."], "correct_answer": "Ground the aircraft and investigate the control system for a potential problem like a frayed cable or a failing bearing.", "explanation": "The flight controls should always feel smooth and responsive. Any unusual feeling is a sign of a potential mechanical problem that could lead to a control jam or failure."},
            {"question_text": "Why is it important to remove a pitot tube cover before flight?", "options": ["It looks unprofessional.", "The cover will make the aircraft fly crooked.", "Failure to remove it will cause the airspeed indicator to read incorrectly or not at all.", "It adds extra weight."], "correct_answer": "Failure to remove it will cause the airspeed indicator to read incorrectly or not at all.", "explanation": "The pitot tube provides ram air pressure to the airspeed indicator. If it is blocked, the pilot will have no reliable indication of their airspeed, which is a critical safety instrument."},
                    
            # Navigation and Sectional Charts
            {"question_text": "What is the primary method of navigation for VFR pilots, which involves referencing landmarks on the ground?", "options": ["Dead Reckoning", "Pilotage", "GPS", "Celestial Navigation"], "correct_answer": "Pilotage", "explanation": "Pilotage is the art of navigating by looking out the window and comparing prominent landmarks on the ground—such as roads, rivers, and towns—with their depiction on a sectional chart."},
            {"question_text": "On a VFR Sectional Chart, what does a dashed blue line surrounding an airport indicate?", "options": ["Class B Airspace", "Class C Airspace", "Class D Airspace", "A Military Operations Area"], "correct_answer": "Class D Airspace", "explanation": "A dashed blue line on a sectional chart depicts the lateral boundaries of Class D airspace, which extends from the surface up to a specified altitude and requires ATC communication to enter."},
            {"question_text": "On a sectional chart, what does the large number '4⁵' in a quadrant represent?", "options": ["A radio frequency", "An airport elevation", "The Maximum Elevation Figure (MEF) for that quadrant.", "The local magnetic variation."], "correct_answer": "The Maximum Elevation Figure (MEF) for that quadrant.", "explanation": "The MEF shows the height of the highest terrain or obstacle in that grid in MSL, rounded up to the next 100 feet. In this example, it's 4,500 feet MSL, a safe altitude to fly above."},
            {"question_text": "If you become lost, what is the first step in the 'Five Cs' procedure?", "options": ["Communicate", "Confess", "Climb", "Circle"], "correct_answer": "Climb", "explanation": "Climbing (while remaining VFR) is the first recommended step. It gives you a better view to spot landmarks and improves reception for radios and GPS, helping you re-orient yourself."},
            {"question_text": "If your GPS fails, what is your primary backup for navigation?", "options": ["Your smartphone's map app", "Flying towards the sun", "Your VFR sectional chart and pilotage", "Calling ATC on your phone"], "correct_answer": "Your VFR sectional chart and pilotage", "explanation": "Technology can fail. A paper chart (or an offline version on another device) and the ability to navigate by looking outside are the fundamental backup skills every pilot must have."},
            {"question_text": "What does a solid magenta line on a sectional chart depict?", "options": ["Class C Airspace", "Class D Airspace", "Class B Airspace", "The boundary of Class G airspace"], "correct_answer": "Class C Airspace", "explanation": "Solid magenta lines are used to show the lateral boundaries of Class C airspace, which surrounds airports that are busier than those in Class D airspace."},
            {"question_text": "An airport is depicted with a magenta circle on a sectional chart. What does this signify?", "options": ["It is a military airport.", "It is an airport with a control tower.", "It is a non-towered airport.", "It is a private airport."], "correct_answer": "It is a non-towered airport.", "explanation": "Magenta symbols are used for non-towered airports, while blue symbols are used for airports with control towers."},
            {"question_text": "What is 'dead reckoning'?", "options": ["Navigating by looking at landmarks.", "Navigating solely by GPS.", "Calculating your position based on a known starting point, heading, airspeed, and elapsed time.", "The process of recovering from being lost."], "correct_answer": "Calculating your position based on a known starting point, heading, airspeed, and elapsed time.", "explanation": "Dead reckoning is a systematic way of navigating that relies on calculations of time, speed, distance, and direction. It is a useful skill, especially when landmarks are scarce."},
            {"question_text": "You see a tower on a sectional chart with the numbers 1549 (449) next to it. What do these numbers mean?", "options": ["The tower is 1549 feet wide and 449 feet tall.", "The top of the tower is 1549 feet MSL, and it is 449 feet AGL.", "The tower is 1549 feet AGL and 449 feet MSL.", "These are radio frequencies for the tower."], "correct_answer": "The top of the tower is 1549 feet MSL, and it is 449 feet AGL.", "explanation": "The top number is the height of the obstruction above Mean Sea Level (MSL), while the number in parentheses is its height Above Ground Level (AGL)."},
            {"question_text": "What does a star on top of an airport symbol indicate?", "options": ["The airport has a rotating beacon.", "The airport is an international airport.", "The airport has fuel available 24/7.", "The airport is closed."], "correct_answer": "The airport has a rotating beacon.", "explanation": "A star symbol indicates that a rotating beacon operates at the airport from sunset to sunrise, and sometimes during the day if the weather is below VFR minimums."},
            {"question_text": "What is the purpose of contour lines on a sectional chart?", "options": ["To show roads and highways.", "To depict areas of equal magnetic variation.", "To show the elevation and shape of the terrain.", "To mark the boundaries of airspace."], "correct_answer": "To show the elevation and shape of the terrain.", "explanation": "Contour lines connect points of equal elevation. When they are close together, the terrain is steep; when they are far apart, the terrain is flat."},
            {"question_text": "What does 'magnetic variation' refer to?", "options": ["The error in the compass caused by the aircraft's electronics.", "The difference between true north and magnetic north.", "The change in the Earth's magnetic field over time.", "A type of turbulence."], "correct_answer": "The difference between true north and magnetic north.", "explanation": "Since your compass points to magnetic north, you must account for magnetic variation (shown by isogonic lines on a chart) to determine your true course over the ground."},
            {"question_text": "You are planning a flight with a true course of 090 degrees. The magnetic variation is 10° East. What is your magnetic course?", "options": ["090 degrees", "100 degrees", "080 degrees", "270 degrees"], "correct_answer": "080 degrees", "explanation": "When converting from a true course to a magnetic course, you subtract an easterly variation. 'East is least.'"},
            {"question_text": "You are planning a flight with a true course of 270 degrees. The magnetic variation is 15° West. What is your magnetic course?", "options": ["270 degrees", "255 degrees", "285 degrees", "090 degrees"], "correct_answer": "285 degrees", "explanation": "When converting from a true course to a magnetic course, you add a westerly variation. 'West is best.'"},
            {"question_text": "What is a major advantage of using a GPS for navigation in an ultralight?", "options": ["It never fails.", "It provides excellent real-time situational awareness of your position relative to airspace boundaries.", "It eliminates the need for a preflight weather briefing.", "It can fly the aircraft for you."], "correct_answer": "It provides excellent real-time situational awareness of your position relative to airspace boundaries.", "explanation": "One of the greatest safety benefits of GPS is its ability to clearly show you where you are in relation to controlled or special use airspace, helping to prevent an inadvertent airspace violation."},
            {"question_text": "What is a significant limitation of relying solely on GPS?", "options": ["It is not very accurate.", "It can suffer from signal loss, battery failure, or database errors.", "It is too complicated to use.", "The screen is too small to be useful."], "correct_answer": "It can suffer from signal loss, battery failure, or database errors.", "explanation": "Like any electronic device, a GPS can fail. Pilots must always maintain proficiency in pilotage and dead reckoning and have a paper chart as a backup."},
            {"question_text": "What does the 'C' in the 'Five Cs' lost procedure stand for?", "options": ["Course", "Chart", "Communicate", "Caution"], "correct_answer": "Communicate", "explanation": "After you Climb, Circle, and Conserve, the next step is to Communicate if you have a radio. This can be with a nearby flight service station or on the emergency frequency 121.5 MHz."},
            {"question_text": "On a sectional chart, what does a shaded blue line (vignette) indicate?", "options": ["The floor of Class B airspace.", "The floor of Class E airspace begins at 1,200 feet AGL.", "A river or body of water.", "A national security area."], "correct_answer": "The floor of Class E airspace begins at 1,200 feet AGL.", "explanation": "The blue shading indicates that the floor of the controlled Class E airspace is at 1,200 feet AGL. Below that is Class G airspace."},
            {"question_text": "What is the best way to orient your sectional chart in flight?", "options": ["Align it with the nose of the aircraft.", "Align it with the direction of true north.", "Align it with the landmarks you see on the ground.", "Keep it folded in your pocket."], "correct_answer": "Align it with the landmarks you see on the ground.", "explanation": "By turning the chart so that the features on the chart align with the features you see outside, you make it much easier to maintain situational awareness and track your position."},
            {"question_text": "You are flying over a featureless area with few landmarks. Which navigation method would be most useful?", "options": ["Pilotage", "Dead Reckoning", "Looking for other aircraft", "Following power lines"], "correct_answer": "Dead Reckoning", "explanation": "When there are no landmarks to reference (pilotage), dead reckoning allows you to track your progress by using your compass, airspeed indicator, and a clock."},
            {"question_text": "What does the airport information 'CT - 118.3' next to an airport symbol mean?", "options": ["The airport elevation is 1183 feet.", "The control tower frequency is 118.3 MHz.", "The runway length is 11,830 feet.", "The CTAF frequency is 118.3 MHz."], "correct_answer": "The control tower frequency is 118.3 MHz.", "explanation": "The 'CT' indicates a control tower, and the number is the primary radio frequency for communicating with that tower."},
            {"question_text": "What does a 'C' in a solid blue circle next to a CTAF frequency mean?", "options": ["The frequency is for the control tower.", "The frequency is the Common Traffic Advisory Frequency.", "The frequency is for the UNICOM service.", "The frequency is closed."], "correct_answer": "The frequency is the Common Traffic Advisory Frequency.", "explanation": "The circled 'C' denotes that the listed frequency is the CTAF, which is the frequency pilots use to announce their positions and intentions at a non-towered airport."},
            {"question_text": "What is a VOR station on a sectional chart?", "options": ["A visual reporting point for ultralights.", "A ground-based radio navigation aid.", "A type of airport.", "A weather station."], "correct_answer": "A ground-based radio navigation aid.", "explanation": "VORs (VHF Omnidirectional Range) are ground stations that aircraft with appropriate receivers can use for navigation. While most ultralights are not so equipped, the VOR symbol (a large compass rose) is a prominent landmark on the chart."},
            {"question_text": "If you are truly lost and have a radio, what is the universal emergency frequency?", "options": ["123.45 MHz", "122.8 MHz", "121.5 MHz", "118.3 MHz"], "correct_answer": "121.5 MHz", "explanation": "121.5 MHz is the international aviation emergency frequency. Any air traffic facility, and many airliners, monitor this frequency. Transmitting 'Mayday' on this frequency will get you help."},
            {"question_text": "What is the primary danger of not using a current sectional chart?", "options": ["The colors might be faded.", "Airspace, obstacles, and airport information can change, making the chart dangerously inaccurate.", "It is a violation of Part 103.", "The paper might be brittle."], "correct_answer": "Airspace, obstacles, and airport information can change, making the chart dangerously inaccurate.", "explanation": "New towers can be built, airspace boundaries can be modified, and airport frequencies can change. Using an out-of-date chart is a significant safety hazard."},
            {"question_text": "What does an 'L' in a circle next to an airport name signify?", "options": ["The airport has a low-intensity runway lighting system.", "The airport is a seaplane base (L for Lake).", "The airport has fuel available.", "The airport is a left-hand traffic pattern."], "correct_answer": "The airport has a low-intensity runway lighting system.", "explanation": "The circled 'L' indicates that the airport has pilot-controlled lighting. The star next to it indicates the beacon, and the L indicates the type of lighting available."},
            {"question_text": "What is a good technique for tracking your progress on a cross-country flight?", "options": ["Guessing based on the time.", "Using a flight timer and marking your position on the chart every 10-15 minutes.", "Waiting until you see your destination.", "Following a highway and hoping it goes to the right place."], "correct_answer": "Using a flight timer and marking your position on the chart every 10-15 minutes.", "explanation": "This systematic approach helps you keep track of where you are and allows you to notice if you are drifting off course due to wind, enabling you to make corrections early."},
            {"question_text": "What does the 'last C' in the 'Five Cs' lost procedure stand for?", "options": ["Course", "Chart", "Conserve", "Confess"], "correct_answer": "Confess", "explanation": "Confess means to admit to yourself that you are lost and to accept help. Don't let pride or embarrassment prevent you from using available resources (like ATC) to get un-lost."},
            {"question_text": "On a sectional chart, what does a line of blue tick marks with arrows pointing inwards represent?", "options": ["A river.", "An Air Defense Identification Zone (ADIZ).", "A state boundary.", "A recommended VFR route."], "correct_answer": "An Air Defense Identification Zone (ADIZ).", "explanation": "An ADIZ is an area of airspace over land or water in which the ready identification, location, and control of civil aircraft are required in the interest of national security. While not typically a concern for ultralights, it's important to know what the symbol means."},
            {"question_text": "Why is it important to identify prominent landmarks BOTH ahead of and behind your aircraft?", "options": ["It is not important to look behind.", "It helps you confirm your position and track and makes it easier to turn back if needed.", "It helps you fly in a straight line.", "It is a requirement for dead reckoning."], "correct_answer": "It helps you confirm your position and track and makes it easier to turn back if needed.", "explanation": "Knowing what is behind you confirms the path you have flown and makes a 180-degree turn back to a known area much easier if you encounter bad weather or other problems ahead."},
                    
            # Airport Operations and Markings
            {"question_text": "At a non-towered airport, what is the standard traffic pattern direction?", "options": ["Right-hand turns", "Left-hand turns", "To the direction of the windsock", "There is no standard"], "correct_answer": "Left-hand turns", "explanation": "Unless visual indicators like a segmented circle specify otherwise, all traffic patterns at U.S. airports are to be made with left-hand turns."},
            {"question_text": "What does a runway number '36' indicate?", "options": ["The runway is 3600 feet long.", "It is the 36th runway at the airport.", "The runway is aligned to a magnetic heading of 360 degrees (North).", "The runway has a weight limit of 36,000 pounds."], "correct_answer": "The runway is aligned to a magnetic heading of 360 degrees (North).", "explanation": "Runway numbers represent the first two digits of their magnetic heading. Runway 36 is aligned with 360 degrees, and its reciprocal would be Runway 18 (180 degrees)."},
            {"question_text": "You see a fully extended windsock at an airport. What does this suggest?", "options": ["The winds are calm.", "The wind is variable in direction.", "The wind is strong, likely 15 knots or more.", "The airport is closed."], "correct_answer": "The wind is strong, likely 15 knots or more.", "explanation": "A windsock's inflation provides a general indication of wind speed. A fully extended sock indicates a strong, steady wind, while a limp sock indicates calm or very light winds."},
            {"question_text": "What is the purpose of a displaced threshold on a runway?", "options": ["It marks an area for helicopter landings only.", "It indicates the runway is closed.", "You can taxi and take off from it, but you cannot land on it.", "It is the designated area for engine run-ups."], "correct_answer": "You can taxi and take off from it, but you cannot land on it.", "explanation": "A displaced threshold, marked with white arrows, is put in place to provide obstacle clearance for aircraft on final approach. The pavement before the solid white threshold line is usable for takeoff roll but not for landing."},
            {"question_text": "What is the recommended practice for an ultralight pilot operating at a non-towered airport with other traffic?", "options": ["Fly straight in to land quickly.", "Use a handheld aviation radio to announce your position and intentions on the CTAF.", "Assume other traffic will see you.", "Land on the taxiway to stay out of the way."], "correct_answer": "Use a handheld aviation radio to announce your position and intentions on the CTAF.", "explanation": "While not required by Part 103, using a radio to communicate on the Common Traffic Advisory Frequency (CTAF) is a critical safety measure to let other pilots know where you are and what you are doing."},
            {"question_text": "What does a large 'X' painted on a runway indicate?", "options": ["The runway is for helicopters only.", "The runway is closed to all operations.", "The runway is a designated STOL (Short Takeoff and Landing) runway.", "The runway has a displaced threshold."], "correct_answer": "The runway is closed to all operations.", "explanation": "A large, conspicuous 'X' at each end of a runway signifies that the runway is permanently closed to all traffic."},
            {"question_text": "What is the name for the leg of the traffic pattern that is parallel to the landing runway but flown in the opposite direction?", "options": ["Final approach", "Base leg", "Upwind leg", "Downwind leg"], "correct_answer": "Downwind leg", "explanation": "The downwind leg is flown parallel to the runway in the direction opposite to landing. This is typically where a pilot will perform pre-landing checks."},
            {"question_text": "What is the purpose of a VASI or PAPI lighting system?", "options": ["To indicate wind direction.", "To provide visual glide slope guidance for landing.", "To light up the taxiways.", "To show the direction of the traffic pattern."], "correct_answer": "To provide visual glide slope guidance for landing.", "explanation": "VASI (Visual Approach Slope Indicator) and PAPI (Precision Approach Path Indicator) are systems of lights that help a pilot maintain the correct vertical path to the runway. 'Red over white, you're alright' is a common mnemonic for a PAPI."},
            {"question_text": "You are on a taxiway approaching a runway. You see a sign with a red background and white numbers. What is this?", "options": ["A location sign.", "A direction sign.", "A mandatory instruction sign indicating an entrance to a runway.", "A distance remaining sign."], "correct_answer": "A mandatory instruction sign indicating an entrance to a runway.", "explanation": "Red background signs are mandatory instructions. This sign indicates you are approaching a runway and must hold short and get clearance from ATC (at a towered field) or ensure it's clear (at a non-towered field) before proceeding."},
            {"question_text": "What color are runway edge lights?", "options": ["Blue", "Green", "Red", "White"], "correct_answer": "White", "explanation": "Runway edge lights are white. An exception is on instrument runways, where the last 2,000 feet of the runway edge lights are yellow."},
            {"question_text": "What color are taxiway edge lights and centerlines?", "options": ["White", "Red", "Blue and Green, respectively", "Yellow"], "correct_answer": "Blue and Green, respectively", "explanation": "Taxiway edges are marked with blue lights, and the taxiway centerline is marked with green lights."},
            {"question_text": "What is the recommended entry to a standard airport traffic pattern?", "options": ["A straight-in approach to the final leg.", "Enter at a 45-degree angle to the downwind leg, at pattern altitude.", "Fly directly over the center of the airport and descend.", "Enter on the crosswind leg."], "correct_answer": "Enter at a 45-degree angle to the downwind leg, at pattern altitude.", "explanation": "This provides the best opportunity to see and be seen by other aircraft already in the pattern and to establish proper spacing."},
            {"question_text": "A segmented circle has L-shaped indicators with the long leg parallel to the runway. What do they indicate?", "options": ["The length of the runway.", "The direction of the traffic pattern.", "The location of the fuel pumps.", "The best place to park."], "correct_answer": "The direction of the traffic pattern.", "explanation": "The L-shaped indicators show how to fly the pattern. For example, if the 'L' makes a box around the runway symbol, it indicates a standard left-hand pattern. If it points away, it indicates a right-hand pattern."},
            {"question_text": "What does a tetrahedron on an airport indicate?", "options": ["The traffic pattern direction.", "The direction of landing and takeoff.", "The location of a hazard.", "The elevation of the airport."], "correct_answer": "The direction of landing and takeoff.", "explanation": "A tetrahedron is a landing direction indicator. You land in the direction the tetrahedron's small end is pointing."},
            {"question_text": "What is the 'base leg' of the traffic pattern?", "options": ["The leg parallel to the runway.", "The leg flown after turning off the downwind leg and before turning to final.", "The initial climb after takeoff.", "The leg flown over the runway."], "correct_answer": "The leg flown after turning off the downwind leg and before turning to final.", "explanation": "The base leg is a transitional part of the pattern, perpendicular to the runway, that connects the downwind leg to the final approach."},
            {"question_text": "You are taxiing and approach a single solid yellow line next to a single dashed yellow line. What does this marking mean?", "options": ["The edge of the taxiway.", "A runway holding position marking.", "You can cross from either side.", "You can only cross from the dashed-line side."], "correct_answer": "You can only cross from the dashed-line side.", "explanation": "This is a taxiway holding position marking for an ILS critical area. You may not cross the solid line without permission, but you may cross from the dashed side."},
            {"question_text": "What does a rotating beacon showing alternating white and green flashes indicate?", "options": ["A lighted water airport.", "A military airport.", "A lighted land airport.", "A hospital heliport."], "correct_answer": "A lighted land airport.", "explanation": "White and green flashes signify a civilian land airport. White and yellow signify a water airport. Two white flashes and a green flash signify a military airport."},
            {"question_text": "What is the 'upwind leg' of the traffic pattern?", "options": ["The final approach.", "The leg flown parallel to the runway in the direction of landing after takeoff.", "The downwind leg.", "The crosswind leg."], "correct_answer": "The leg flown parallel to the runway in the direction of landing after takeoff.", "explanation": "The upwind leg is the initial climb out path, sometimes called the departure leg, which is flown into the wind."},
            {"question_text": "A sign on the taxiway has a black background with yellow letters. What type of sign is this?", "options": ["Mandatory Instruction Sign", "Location Sign", "Direction Sign", "Destination Sign"], "correct_answer": "Location Sign", "explanation": "'Black square, you are there.' A black sign with yellow letters tells you which taxiway or runway you are currently on."},
            {"question_text": "What is the 'crosswind leg' of the traffic pattern?", "options": ["The leg flown perpendicular to the runway after the upwind leg.", "The downwind leg.", "The final approach.", "The taxiway to the runway."], "correct_answer": "The leg flown perpendicular to the runway after the upwind leg.", "explanation": "After takeoff on the upwind leg, the first turn is onto the crosswind leg, which is flown at a 90-degree angle to the runway."},
            {"question_text": "What is the purpose of a runway 'hold short' line?", "options": ["To mark the end of the runway.", "To indicate where aircraft should stop before entering a runway.", "To mark a parking spot.", "To indicate the middle of the runway."], "correct_answer": "To indicate where aircraft should stop before entering a runway.", "explanation": "It consists of two solid and two dashed yellow lines. You must stop before crossing the solid lines when approaching the runway."},
            {"question_text": "A wind tee is another type of wind indicator. How does it show the wind direction?", "options": ["It points into the wind, like an airplane.", "It points away from the wind.", "The color indicates the wind speed.", "It spins to show gusts."], "correct_answer": "It points into the wind, like an airplane.", "explanation": "The wind tee is shaped like an airplane. You should take off and land in the direction it is pointing (the direction a real airplane would be pointing to take off into the wind)."},
            {"question_text": "What does CTAF stand for?", "options": ["Control Tower Air Frequency", "Common Traffic Advisory Frequency", "Crosswind Takeoff Advisory Frequency", "Cleared To Approach Frequency"], "correct_answer": "Common Traffic Advisory Frequency", "explanation": "CTAF is the designated frequency for pilots to communicate with each other at non-towered airports."},
            {"question_text": "What is the standard altitude for a traffic pattern at most airports?", "options": ["500 feet AGL", "1,000 feet AGL", "2,000 feet AGL", "3,000 feet MSL"], "correct_answer": "1,000 feet AGL", "explanation": "While ultralights may fly a lower pattern, the standard for general aviation aircraft is 1,000 feet above ground level. It is critical to know this to maintain separation."},
            {"question_text": "What does a sign with a yellow background and black letters indicate?", "options": ["A runway location.", "A mandatory instruction.", "A direction or destination sign.", "A closed taxiway."], "correct_answer": "A direction or destination sign.", "explanation": "These signs point the way toward other taxiways, runways, or airport locations like the FBO or fuel pumps. The arrow indicates the direction of turn."},
            {"question_text": "What is a 'LAHSO' operation?", "options": ["A type of emergency landing.", "Land and Hold Short Operation.", "A procedure for helicopters.", "A type of airshow maneuver."], "correct_answer": "Land and Hold Short Operation.", "explanation": "LAHSO is a procedure at towered airports where an aircraft is cleared to land and hold short of an intersecting runway. Ultralight pilots are not expected to participate in LAHSO."},
            {"question_text": "What does a runway threshold bar, a solid white line across the runway, indicate?", "options": ["The middle of the runway.", "A taxiway intersection.", "The beginning of the runway surface available for landing.", "A closed runway."], "correct_answer": "The beginning of the runway surface available for landing.", "explanation": "This line marks the start of the usable portion of the runway for landing."},
            {"question_text": "What is the primary difference in operations between a towered and non-towered airport?", "options": ["The runway length.", "At a towered airport, ATC provides instructions and clearances; at a non-towered airport, pilots coordinate amongst themselves.", "Non-towered airports do not have fuel.", "Towered airports are for jets only."], "correct_answer": "At a towered airport, ATC provides instructions and clearances; at a non-towered airport, pilots coordinate amongst themselves.", "explanation": "The key difference is the presence of an operating control tower that actively manages the flow of traffic versus a field where pilots are responsible for self-sequencing."},
            {"question_text": "What is UNICOM?", "options": ["A type of GPS.", "An air traffic control facility.", "A non-government air/ground communication station used to provide airport information.", "A type of emergency beacon."], "correct_answer": "A non-government air/ground communication station used to provide airport information.", "explanation": "Pilots can call the UNICOM frequency to ask for information like the active runway, wind conditions, or to request services like fuel from the local FBO (Fixed-Base Operator)."},
            {"question_text": "If you are departing a non-towered airport, when should you make your first turn from the upwind leg?", "options": ["Immediately after liftoff.", "After reaching a safe altitude (e.g., 300-500 feet AGL) and beyond the departure end of the runway.", "When you are clear of the traffic pattern.", "When you reach 1,000 feet AGL."], "correct_answer": "After reaching a safe altitude (e.g., 300-500 feet AGL) and beyond the departure end of the runway.", "explanation": "This ensures you have enough altitude to maneuver safely and are clear of the runway end before starting your turn to the crosswind leg, preventing conflicts with aircraft on final approach."},
                    
            # Emergency Procedures
            {"question_text": "What is the most critical and immediate action to take after an engine failure in flight?", "options": ["Attempt a restart.", "Establish the aircraft's best glide speed.", "Turn back to the airport.", "Declare an emergency on the radio."], "correct_answer": "Establish the aircraft's best glide speed.", "explanation": "Aviate first! Immediately lowering the nose to establish the best glide speed maximizes the distance you can travel without power and gives you the most time and options to find a safe landing spot."},
            {"question_text": "Why is attempting a 180-degree turn back to the runway after an engine failure on takeoff so dangerous?", "options": ["It wastes too much fuel.", "It can lead to a stall/spin at a low, unrecoverable altitude.", "It's against FAA regulations.", "It's difficult to see the runway from that angle."], "correct_answer": "It can lead to a stall/spin at a low, unrecoverable altitude.", "explanation": "The 'impossible turn' involves a steep bank at low airspeed, which dramatically increases the stall speed. The combination of trying to turn sharply and stretching the glide often leads to an aerodynamic stall and/or spin with no altitude to recover."},
            {"question_text": "What is the first step in the 'Aviate, Navigate, Communicate' philosophy?", "options": ["Navigate to the nearest airport.", "Communicate your emergency.", "Aviate - fly the aircraft and maintain control.", "Troubleshoot the problem."], "correct_answer": "Aviate - fly the aircraft and maintain control.", "explanation": "The absolute first priority in any abnormal situation is to fly the aircraft. Maintaining positive control is the foundation upon which all other emergency actions are built."},
            {"question_text": "In the emergency checklist 'A-B-C-D-E' for an engine failure at altitude, what does 'B' stand for?", "options": ["Best Field", "Brakes", "Bank", "Battery"], "correct_answer": "Best Field", "explanation": "After establishing Airspeed (A), your next priority is to select the Best Field for an emergency landing and turn towards it. This is a critical part of the 'Navigate' step."},
            {"question_text": "What is the correct emergency radio call to indicate a condition of distress?", "options": ["Help, Help, Help", "Pan-Pan, Pan-Pan, Pan-Pan", "Emergency, Emergency, Emergency", "Mayday, Mayday, Mayday"], "correct_answer": "Mayday, Mayday, Mayday", "explanation": "'Mayday' is the international standard radio call for a distress condition, meaning you are in grave and imminent danger and require immediate assistance."},
            {"question_text": "If you have an engine fire in flight, what is a critical first step after establishing a glide?", "options": ["Turn the fuel selector valve to OFF.", "Increase your airspeed to blow out the fire.", "Open the cockpit vents for fresh air.", "Fly towards the nearest lake."], "correct_answer": "Turn the fuel selector valve to OFF.", "explanation": "The immediate priority is to cut off the supply of fuel to the fire. Turning the fuel selector off is a critical step in attempting to extinguish an engine fire."},
            {"question_text": "You are at 200 feet AGL on takeoff when the engine quits. What is your primary course of action?", "options": ["Make a gentle 180-degree turn back to the runway.", "Maintain control, lower the nose to maintain airspeed, and land mostly straight ahead.", "Pull the nose up to stretch the glide as far as possible.", "Immediately deploy your ballistic parachute."], "correct_answer": "Maintain control, lower the nose to maintain airspeed, and land mostly straight ahead.", "explanation": "At such a low altitude, there is no time or room to turn back. The only safe option is to fly the aircraft into the most suitable landing area in front of you, even if it's not the runway."},
            {"question_text": "What does 'best glide speed' provide?", "options": ["The longest time in the air.", "The greatest forward distance covered for a given loss of altitude.", "The smoothest ride.", "The slowest possible landing speed."], "correct_answer": "The greatest forward distance covered for a given loss of altitude.", "explanation": "Best glide speed (L/D max) maximizes your gliding range, giving you the most options for a landing site during an engine-out emergency."},
            {"question_text": "If you inadvertently fly into clouds (IMC) and become disoriented, what is the recommended immediate action?", "options": ["Climb as fast as possible.", "Descend as fast as possible.", "Trust your senses and fly what feels level.", "Make a 180-degree turn, relying on your instruments (if available) to fly straight and level."], "correct_answer": "Make a 180-degree turn, relying on your instruments (if available) to fly straight and level.", "explanation": "The priority is to get out of the clouds as quickly as possible. A standard-rate 180-degree turn is the best way to reverse course and return to the VFR conditions you just left. Do not trust your body's senses; they will lie to you."},
            {"question_text": "What is the primary danger of spatial disorientation?", "options": ["It can make you feel nauseous.", "It leads to the pilot placing the aircraft in a dangerous attitude (like a steep bank or dive) without realizing it.", "It can cause the GPS to fail.", "It makes it hard to read the map."], "correct_answer": "It leads to the pilot placing the aircraft in a dangerous attitude (like a steep bank or dive) without realizing it.", "explanation": "Without visual references, the inner ear can give powerful and false sensations of motion, leading a pilot to lose control of the aircraft while thinking they are flying straight and level."},
            {"question_text": "When selecting an off-airport landing site, what is a primary consideration?", "options": ["Choosing a field with the softest-looking grass.", "Choosing a field that is long enough and clear of major obstacles like power lines, ditches, and trees.", "Choosing the closest field, regardless of its condition.", "Choosing a field near a road so help can arrive quickly."], "correct_answer": "Choosing a field that is long enough and clear of major obstacles like power lines, ditches, and trees.", "explanation": "The top priority is to find a survivable landing spot. This means avoiding obstacles that could cause the aircraft to flip over or be destroyed on impact."},
            {"question_text": "What is the recommended procedure for landing in a field with a known wind direction?", "options": ["Land with a tailwind to get on the ground faster.", "Land into the wind to have the slowest groundspeed at touchdown.", "Land crosswind to see the field better.", "Wind direction does not matter for off-airport landings."], "correct_answer": "Land into the wind to have the slowest groundspeed at touchdown.", "explanation": "Landing into the wind reduces your speed over the ground, which shortens your landing roll and reduces the energy that must be dissipated in the landing, making it much safer."},
            {"question_text": "If you have an electrical fire in the cockpit, what is the first action you should take?", "options": ["Turn on the cabin heat to burn off the smoke.", "Turn the master switch and all electrical equipment OFF.", "Open a window to let the smoke out.", "Pour water on it."], "correct_answer": "Turn the master switch and all electrical equipment OFF.", "explanation": "An electrical fire is fed by electricity. The first step is to remove the source of power by turning off the master switch, which may extinguish the fire on its own."},
            {"question_text": "What is the 'C' in the A-B-C-D-E engine failure checklist?", "options": ["Climb", "Circle", "Checklist", "Communicate"], "correct_answer": "Checklist", "explanation": "After establishing Airspeed and picking your Best field, the 'C' stands for performing a Checklist to attempt a restart (e.g., check fuel selector, magnetos, primer) if time and altitude permit."},
            {"question_text": "If one of your primary flight controls (like the elevator) becomes jammed, what is an alternative way to control pitch?", "options": ["Shifting your body weight.", "Using power and/or trim adjustments.", "Using only the ailerons.", "There is no alternative."], "correct_answer": "Using power and/or trim adjustments.", "explanation": "Adding power will tend to make the nose pitch up, while reducing power will make it pitch down. The elevator trim tab can also be used to help control pitch if it is still functional."},
            {"question_text": "What is the main goal of a forced landing after an engine failure?", "options": ["To save the aircraft from any damage.", "To land exactly on the intended spot.", "To fly the aircraft to the point of impact under control and protect the occupants.", "To restart the engine at all costs."], "correct_answer": "To fly the aircraft to the point of impact under control and protect the occupants.", "explanation": "The aircraft is replaceable; you are not. The primary goal is to maintain control and use the aircraft structure to protect yourself by landing at the slowest possible airspeed in the best possible spot."},
            {"question_text": "If you are lost and have a radio, but are not in grave danger, what is the appropriate urgency call?", "options": ["Mayday, Mayday, Mayday", "Help, Help, Help", "Pan-Pan, Pan-Pan, Pan-Pan", "Security, Security, Security"], "correct_answer": "Pan-Pan, Pan-Pan, Pan-Pan", "explanation": "'Pan-Pan' is the international urgency signal. It indicates that you have a situation that is serious but does not pose an immediate, grave threat to life or the aircraft."},
            {"question_text": "Why is it critical to continue flying the aircraft all the way through a crash landing?", "options": ["To impress any witnesses.", "It is not critical; you should brace for impact.", "Maintaining control allows you to touch down at the slowest possible speed and in the best possible attitude, which is key to survival.", "To ensure the insurance claim is valid."], "correct_answer": "Maintaining control allows you to touch down at the slowest possible speed and in the best possible attitude, which is key to survival.", "explanation": "Never give up on flying the aircraft. The difference between a controlled, slow-speed impact and an uncontrolled, high-speed stall/spin into the ground is the difference between walking away and a fatal accident."},
            {"question_text": "If your engine begins to run very rough in flight, what should be your immediate mindset?", "options": ["Assume it will clear up on its own.", "Treat it as an impending engine failure and begin looking for a precautionary landing site.", "Immediately turn back to your home airport, even if it's far away.", "Climb to a very high altitude."], "correct_answer": "Treat it as an impending engine failure and begin looking for a precautionary landing site.", "explanation": "A rough-running engine is a sign of a serious problem. You should assume it will fail completely and start planning for a forced landing while you still have some power and control over the situation."},
            {"question_text": "What is a good strategy for a forced landing in a forested area?", "options": ["Aim for the tallest, strongest trees to stop you.", "Try to land in a clearing or on a road if possible; if not, aim for a low, dense canopy at minimum speed.", "Deploy your parachute immediately.", "Stall the aircraft high above the trees."], "correct_answer": "Try to land in a clearing or on a road if possible; if not, aim for a low, dense canopy at minimum speed.", "explanation": "A clearing is best. If there are no clearings, using the tops of smaller, dense trees to absorb the impact energy at the slowest possible forward speed offers the best chance of survival."},
            {"question_text": "What is the first 'C' of the five Cs for getting un-lost?", "options": ["Communicate", "Circle", "Climb", "Confess"], "correct_answer": "Climb", "explanation": "Climbing gives you a better vantage point to see recognizable landmarks and improves radio/GPS reception."},
            {"question_text": "During an engine-out landing, when should you deploy flaps (if equipped)?", "options": ["Immediately after the engine fails.", "Once you are certain you can make your chosen landing spot.", "Never use flaps in an emergency.", "On the downwind leg."], "correct_answer": "Once you are certain you can make your chosen landing spot.", "explanation": "Flaps add a lot of drag. Deploying them too early could cause you to undershoot your field. It's best to wait until you have the field 'made' and then use flaps to steepen your descent and slow your touchdown speed."},
            {"question_text": "If you suspect a structural failure in flight (e.g., you hear a loud bang and the aircraft controls feel strange), what should you do?", "options": ["Test the limits of the aircraft to see what is broken.", "Reduce speed immediately to the bottom of the green arc or lower, and avoid abrupt control inputs.", "Turn back immediately, regardless of the distance.", "Continue the flight as planned."], "correct_answer": "Reduce speed immediately to the bottom of the green arc or lower, and avoid abrupt control inputs.", "explanation": "Reducing airspeed lessens the aerodynamic loads on the damaged airframe, increasing the chances of holding it together long enough for a gentle emergency landing at the nearest suitable spot."},
            {"question_text": "What is the primary risk of landing in a field with tall crops like corn?", "options": ["It will stain the aircraft.", "The crops can hide obstacles like ditches or rocks, and they can create a significant drag that could flip the aircraft.", "It is illegal.", "The farmer might be angry."], "correct_answer": "The crops can hide obstacles like ditches or rocks, and they can create a significant drag that could flip the aircraft.", "explanation": "Tall, dense crops can be very hazardous, concealing terrain variations and having the potential to grab the landing gear and nose the aircraft over."},
            {"question_text": "What is the 'Communicate' part of 'Aviate, Navigate, Communicate'?", "options": ["Talking to yourself to stay calm.", "Using the radio to declare an emergency or get assistance, but only after the first two steps are handled.", "Writing a note for rescuers.", "Honking a horn if you have one."], "correct_answer": "Using the radio to declare an emergency or get assistance, but only after the first two steps are handled.", "explanation": "Communication is last for a reason. Flying the plane and pointing it somewhere safe are the top priorities. Only when you have time and altitude should you use the radio."},
            {"question_text": "You are making a forced landing and have to cross a power line at the edge of a field. What is the best technique?", "options": ["Fly directly into the wires to break them.", "Fly under the wires.", "Fly over the wires with as much clearance as possible, and be prepared for a steep descent after.", "Ignore the wires as they are not a real threat."], "correct_answer": "Fly over the wires with as much clearance as possible, and be prepared for a steep descent after.", "explanation": "Power lines are extremely dangerous and hard to see. If you must cross them, aim to fly over the supporting poles where they are most visible and highest off the ground, then make a steep descent into the field."},
            {"question_text": "What is the best way to prepare for an in-flight emergency?", "options": ["Hope it never happens.", "Regularly practice simulated emergencies like engine failures with a qualified instructor.", "Read the aircraft manual once.", "Fly only on calm days."], "correct_answer": "Regularly practice simulated emergencies like engine failures with a qualified instructor.", "explanation": "Proficiency and preparedness are key. Actually practicing the procedures builds the muscle memory and mental calm needed to handle a real emergency effectively."},
            {"question_text": "If your engine fails over a large body of water, what should you do differently for your forced landing?", "options": ["Land with a tailwind.", "Try to land parallel to the shore and as close as possible.", "Attempt to ditch the aircraft parallel to the swells and into the wind.", "Remove your seatbelt before impact."], "correct_answer": "Attempt to ditch the aircraft parallel to the swells and into the wind.", "explanation": "Landing into the wind reduces your speed, and landing parallel to the swells (waves) prevents the wing from digging into an oncoming wave, which could flip the aircraft."},
            {"question_text": "What is the purpose of an emergency locator transmitter (ELT)?", "options": ["To transmit your voice communications.", "To automatically broadcast a distress signal on 121.5 MHz upon impact.", "To navigate to the nearest airport.", "To provide weather updates."], "correct_answer": "To automatically broadcast a distress signal on 121.5 MHz upon impact.", "explanation": "An ELT is a safety device that activates during a crash, sending out a signal that helps rescue crews locate the downed aircraft. While not required on Part 103 ultralights, they are common on other aircraft."},
            {"question_text": "After a forced landing, what should be one of your first priorities after ensuring you are safe?", "options": ["Update your logbook.", "Call your insurance company.", "Activate your emergency beacon (if equipped) and/or call 911.", "Try to hide the aircraft."], "correct_answer": "Activate your emergency beacon (if equipped) and/or call 911.", "explanation": "Once you have addressed any immediate medical needs, the next step is to signal for rescue so that help can be dispatched to your location."},
                    
            # Human Factors
            {"question_text": "In the IMSAFE checklist, what does the 'F' stand for?", "options": ["Fast", "Fear", "Fatigue", "Food"], "correct_answer": "Fatigue", "explanation": "The 'F' in IMSAFE stands for Fatigue. A tired pilot is a dangerous pilot, as fatigue significantly impairs judgment, reaction time, and decision-making skills."},
            {"question_text": "A pilot who thinks, 'Rules are for other people,' is exhibiting which hazardous attitude?", "options": ["Macho", "Invulnerability", "Resignation", "Anti-Authority"], "correct_answer": "Anti-Authority", "explanation": "This attitude reflects a resentment of rules and a belief that they are unnecessary or don't apply to oneself. The antidote is to recognize that rules and procedures are there for a reason and are based on years of experience."},
            {"question_text": "The PAVE checklist is a tool for assessing risk. What does the 'V' stand for?", "options": ["Vehicle", "enVironment", "Visibility", "Velocity"], "correct_answer": "enVironment", "explanation": "The 'V' in PAVE stands for enVironment, which includes assessing weather (current and forecast), terrain, airspace, and time of day to identify potential risks."},
            {"question_text": "Feeling rushed to get to a family event is an example of which element of the PAVE checklist?", "options": ["Pilot", "Aircraft", "enVironment", "External Pressures"], "correct_answer": "External Pressures", "explanation": "External pressures are influences outside the immediate flight (like schedules, passenger expectations, or wanting to get home) that can pressure a pilot into making unsafe decisions. Recognizing and resisting these pressures is a key part of good ADM."},
            {"question_text": "What is the antidote for the 'Macho' hazardous attitude?", "options": ["Rules are usually right.", "It could happen to me.", "Taking chances is foolish.", "I am not helpless."], "correct_answer": "Taking chances is foolish.", "explanation": "The antidote for Macho is to recognize that taking unnecessary risks is not a sign of skill, but of poor judgment."},
            {"question_text": "A pilot decides to fly through a narrow canyon to impress his friends. Which hazardous attitude is most clearly being displayed?", "options": ["Resignation", "Invulnerability", "Macho", "Impulsivity"], "correct_answer": "Macho", "explanation": "This is a classic example of the Macho attitude, where a pilot takes unnecessary risks to show off."},
            {"question_text": "What does the 'A' in the PAVE checklist stand for?", "options": ["Attitude", "Altitude", "Aircraft", "Airspace"], "correct_answer": "Aircraft", "explanation": "The 'A' in PAVE prompts the pilot to assess the risk associated with the Aircraft itself: its airworthiness, fuel status, and overall condition."},
            {"question_text": "You have a minor cold but decide to fly anyway. Which part of the IMSAFE checklist have you failed to consider properly?", "options": ["I - Illness", "M - Medication", "S - Stress", "F - Fatigue"], "correct_answer": "I - Illness", "explanation": "Even a minor illness can affect a pilot's ability to fly safely, potentially causing issues with sinus pressure, concentration, or general well-being."},
            {"question_text": "The feeling that 'accidents only happen to other people' is an example of which hazardous attitude?", "options": ["Anti-Authority", "Invulnerability", "Resignation", "Macho"], "correct_answer": "Invulnerability", "explanation": "This is the hazardous attitude of Invulnerability. The antidote is to remind yourself, 'It could happen to me.'"},
            {"question_text": "What is the antidote for the hazardous attitude of 'Impulsivity'?", "options": ["Not so fast, think first.", "Follow the rules.", "I'm not helpless.", "It could happen to me."], "correct_answer": "Not so fast, think first.", "explanation": "The antidote for Impulsivity is to slow down, take a moment, and consider the options and outcomes before acting."},
            {"question_text": "What does the 'E' in IMSAFE stand for?", "options": ["Energy", "Engine", "Emergency", "Emotion / Eating"], "correct_answer": "Emotion / Eating", "explanation": "The 'E' in IMSAFE prompts a pilot to consider their emotional state and whether they are properly nourished and hydrated before a flight."},
            {"question_text": "During a difficult situation, a pilot thinks, 'Oh well, whatever happens, happens.' This is an example of:", "options": ["Resignation", "Invulnerability", "Macho", "Anti-Authority"], "correct_answer": "Resignation", "explanation": "This feeling of helplessness is the hazardous attitude of Resignation. The antidote is to remember, 'I'm not helpless. I can make a difference.'"},
            {"question_text": "What is Aeronautical Decision Making (ADM)?", "options": ["A type of aircraft navigation system.", "A systematic approach to risk assessment and stress management.", "The process of getting a pilot's license.", "A preflight inspection checklist."], "correct_answer": "A systematic approach to risk assessment and stress management.", "explanation": "ADM provides structured frameworks like PAVE to help pilots consistently identify hazards, assess risk, and make safe decisions."},
            {"question_text": "You took an over-the-counter allergy medication that could cause drowsiness. Which part of the IMSAFE checklist is most relevant?", "options": ["I - Illness", "M - Medication", "S - Stress", "A - Alcohol"], "correct_answer": "M - Medication", "explanation": "Pilots must be aware of the potential side effects of any medication, prescription or over-the-counter, before flying."},
            {"question_text": "What is the antidote for the 'Anti-Authority' hazardous attitude?", "options": ["Follow the rules. They are usually right.", "It could happen to me.", "Taking chances is foolish.", "Think first."], "correct_answer": "Follow the rules. They are usually right.", "explanation": "The antidote for Anti-Authority is to acknowledge that regulations and procedures are created for safety based on collective experience."},
            {"question_text": "The 'P' in the PAVE checklist refers to what?", "options": ["Powerplant", "Propeller", "Pilot", "Performance"], "correct_answer": "Pilot", "explanation": "The 'P' in PAVE refers to the Pilot. The risk assessment process begins with the pilot assessing their own fitness to fly using the IMSAFE checklist."},
            {"question_text": "What is 'get-there-itis'?", "options": ["A fear of flying.", "An external pressure and human factor that causes a pilot to make poor decisions in an attempt to reach their destination.", "A type of engine problem.", "The desire to fly as fast as possible."], "correct_answer": "An external pressure and human factor that causes a pilot to make poor decisions in an attempt to reach their destination.", "explanation": "This is a classic example of an external pressure where the pilot fixates on the destination, often causing them to fly into deteriorating weather or ignore other warning signs."},
            {"question_text": "What is the antidote for the hazardous attitude of 'Resignation'?", "options": ["I can make a difference.", "I can do it.", "It won't happen to me.", "Follow the rules."], "correct_answer": "I can make a difference.", "explanation": "The correct response to feeling helpless is to actively take control of the situation and remember that your actions have a direct effect on the outcome."},
            {"question_text": "Why is it important to stay hydrated during a flight?", "options": ["It makes the aircraft lighter.", "Dehydration can cause fatigue, headaches, and impaired judgment.", "It is not important.", "It helps with night vision."], "correct_answer": "Dehydration can cause fatigue, headaches, and impaired judgment.", "explanation": "Even mild dehydration can significantly degrade a pilot's cognitive function and physical performance, making it a critical human factor to manage."},
            {"question_text": "What does the 'S' in the IMSAFE checklist stand for?", "options": ["Skill", "Safety", "Stress", "Stamina"], "correct_answer": "Stress", "explanation": "The 'S' stands for Stress. A pilot must honestly assess their level of life stress (from work, family, health, etc.) as high stress levels can severely impact decision-making."},
            {"question_text": "A pilot, not wanting to wait for a storm to pass, decides to 'just sneak under' the clouds. This is an example of which hazardous attitude?", "options": ["Resignation", "Impulsivity", "Anti-Authority", "Invulnerability"], "correct_answer": "Impulsivity", "explanation": "This demonstrates the 'Do it quickly' mindset. Instead of waiting for safe conditions, the pilot feels compelled to act immediately, which is a dangerous trait."},
            {"question_text": "What is the best way to mitigate risks identified during a PAVE checklist assessment?", "options": ["Ignore them and hope for the best.", "Establish personal minimums and be prepared to delay or cancel the flight.", "Fly faster to get through the risky part of the flight quickly.", "Assume the risks are not as bad as they seem."], "correct_answer": "Establish personal minimums and be prepared to delay or cancel the flight.", "explanation": "The entire point of ADM is to identify risks so you can make choices to mitigate them. The safest and most effective choice is often to wait for conditions to improve or to cancel the flight entirely."},
            {"question_text": "What is 'hypoxia'?", "options": ["A state of over-hydration.", "A state of oxygen deficiency in the body, which can impair brain function.", "A fear of heights.", "A type of spatial disorientation."], "correct_answer": "A state of oxygen deficiency in the body, which can impair brain function.", "explanation": "Hypoxia can occur at higher altitudes where the air is thinner. While less common for low-flying ultralights, it's a critical human factor in aviation that impairs judgment, vision, and coordination."},
            {"question_text": "What is the antidote for the 'Invulnerability' hazardous attitude?", "options": ["It could happen to me.", "I am not helpless.", "Taking chances is foolish.", "Not so fast, think first."], "correct_answer": "It could happen to me.", "explanation": "The correct mindset to counter the feeling of invulnerability is to have a healthy respect for the risks of aviation and to acknowledge that you are just as susceptible to an accident as anyone else."},
            {"question_text": "You are feeling angry and upset after an argument before heading to the airport. Which part of the IMSAFE checklist should you be most concerned with?", "options": ["I - Illness", "E - Emotion", "M - Medication", "F - Fatigue"], "correct_answer": "E - Emotion", "explanation": "Flying while emotionally distressed is dangerous. Anger, sadness, or anxiety can distract you from the task of flying and lead to poor, impulsive decisions."},
            {"question_text": "Why is peer pressure considered a significant human factor risk?", "options": ["It can make you feel popular.", "It can lead a pilot to fly beyond their personal limits or into unsafe conditions to avoid looking timid.", "It helps you learn from other pilots.", "It is not a significant risk."], "correct_answer": "It can lead a pilot to fly beyond their personal limits or into unsafe conditions to avoid looking timid.", "explanation": "The desire to 'keep up' with other pilots can be a powerful external pressure. A safe pilot must have the discipline to make their own decisions based on their own skill and comfort level, regardless of what others are doing."},
            {"question_text": "What is the relationship between stress and pilot performance?", "options": ["Stress always improves performance.", "Stress has no effect on performance.", "A small amount of stress can improve performance, but high stress levels degrade it significantly.", "Stress only affects new pilots."], "correct_answer": "A small amount of stress can improve performance, but high stress levels degrade it significantly.", "explanation": "Performance generally increases with low levels of stress (attentiveness), but as stress becomes high, performance drops off rapidly due to tunneling of attention and impaired judgment."},
            {"question_text": "What is the most effective tool a pilot has to combat hazardous attitudes?", "options": ["A fast airplane.", "A reliable GPS.", "Self-awareness and the use of their corresponding antidotes.", "A good co-pilot."], "correct_answer": "Self-awareness and the use of their corresponding antidotes.", "explanation": "Recognizing a hazardous thought process in yourself and consciously applying the correct antidote is the most effective way to manage these dangerous mental traps."},
            {"question_text": "What does the 'M' in the IMSAFE checklist stand for?", "options": ["Macho", "Mental state", "Medication", "Motivation"], "correct_answer": "Medication", "explanation": "The 'M' prompts a pilot to consider any prescription or over-the-counter medications they are taking and the potential effects those drugs could have on their ability to fly safely."},
            {"question_text": "The decision to continue a flight into deteriorating weather because you've already flown most of the way is an example of what cognitive bias?", "options": ["Confirmation Bias", "Optimism Bias", "Sunk Cost Fallacy", "Anchoring Bias"], "correct_answer": "Sunk Cost Fallacy", "explanation": "This is the fallacy of continuing a course of action because of the time or effort already invested. The safe decision is to turn around, regardless of how much progress you've made."},  
        ]

if __name__ == "__main__":
    root = tk.Tk()
    # This part ensures the full content is loaded correctly, replacing the "..." placeholders.
    app_instance = UltralightGroundSchoolApp(root)
    full_content = {
        "FAR Part 103 Overview": textwrap.dedent(app_instance.study_topics_content["FAR Part 103 Overview"].replace("...", """
            FAR Part 103 is the section of the Federal Aviation Regulations that governs ultralight vehicles in the United States. It was established in 1982 to create a safe and minimally regulated way for individuals to enjoy recreational flight.

            Key Principles of Part 103:
            - No Pilot Certificate: You are not required to have a pilot license or medical certificate.
            - No Registration: The vehicle does not need to be registered or have an N-number.
            - No Airworthiness Certificate: The vehicle is not certified by the FAA.

            This freedom means the pilot bears 100% of the responsibility for safety, maintenance, and legal operation.

            To qualify as a legal Part 103 ultralight, a vehicle must meet strict criteria:
            1.  Use: For recreational or sport purposes only.
            2.  Occupancy: Can only carry a single occupant.
            3.  Powered Vehicles:
                - Empty Weight: Less than 254 pounds (115 kg). This excludes floats and safety devices like ballistic parachutes.
                - Fuel Capacity: Maximum of 5 U.S. gallons.
                - Max Speed: Not capable of more than 55 knots (63 mph) in level flight.
                - Stall Speed: Power-off stall speed not exceeding 24 knots (28 mph).
            4.  Unpowered Vehicles (e.g., Hang Gliders, Paragliders):
                - Empty Weight: Less than 155 pounds (70 kg).

            If a vehicle exceeds ANY of these limitations, it is not a Part 103 ultralight and must be registered as an experimental or light-sport aircraft (LSA), requiring a pilot license to operate.
        """)),
        "FAR Part 103 Operations": textwrap.dedent(app_instance.study_topics_content["FAR Part 103 Operations"].replace("...", """
            Operating an ultralight vehicle legally and safely involves adhering to specific operational rules designed to protect both the pilot and people on the ground.

            §103.9 Hazardous operation:
            - No person may operate an ultralight vehicle in a manner that creates a hazard to other persons or property.
            - No person may allow an object to be dropped from an ultralight vehicle if such action creates a hazard.

            §103.11 Daylight operations:
            - Ultralights may only be operated between sunrise and sunset.
            - Exception: Operation is allowed during the 30-minute twilight periods (before sunrise and after sunset) ONLY IF the vehicle is equipped with an operating anti-collision light visible for 3 statute miles and remains in Class G (uncontrolled) airspace.

            §103.15 Operations over congested areas:
            - Flight over any congested area of a city, town, or settlement, or over any open-air assembly of persons is STRICTLY PROHIBITED.
            - What is "congested"? The FAA does not give a precise definition. Pilots must be extremely conservative. A single-engine failure must always allow for a safe emergency landing without endangering anyone on the ground. If you cannot guarantee that, you should not be flying there.

            §103.13 Right-of-way rules:
            - See and Avoid: Every pilot is responsible for seeing and avoiding other aircraft.
            - Yielding: An ultralight vehicle must yield the right-of-way to ALL other aircraft.
            - Powered vs. Unpowered: A powered ultralight must yield to an unpowered ultralight (e.g., hang glider).
        """)),
        "Airspace for Ultralights": textwrap.dedent(app_instance.study_topics_content["Airspace for Ultralights"].replace("...", """
            Understanding airspace is critical to avoid conflicts with other aircraft and to operate legally. Ultralights are primarily intended for use in uncontrolled airspace.

            §103.17 Airspace restrictions:
            No person may operate an ultralight vehicle within the following airspace without prior authorization from Air Traffic Control (ATC):
            - Class A (18,000 feet and above)
            - Class B (Surrounding major airports)
            - Class C (Surrounding busy airports)
            - Class D (Surrounding airports with a control tower)
            - The lateral boundaries of the surface area of Class E airspace designated for an airport.

            This means ultralights are FORBIDDEN from these controlled airspaces unless you call the controlling ATC facility on the phone beforehand and receive explicit permission. This is rarely granted.

            Primary Operating Airspace:
            - Class G (Golf) Airspace: This is uncontrolled airspace and where nearly all ultralight flying occurs. It typically exists from the surface up to 1,200 feet AGL or, in some remote areas, up to 14,500 feet MSL.
            - Class E (Echo) Airspace: You may operate in Class E airspace that is NOT at the surface. Most Class E airspace begins at 700 or 1,200 feet AGL. You must remain clear of clouds and meet visibility requirements.

            How to Identify Airspace:
            - You MUST learn to read a VFR Sectional Chart. It is the roadmap of the sky.
            - Solid blue lines depict Class B, solid magenta for Class C, dashed blue for Class D, and various magenta/blue shading for Class E floors. Unmarked areas are typically Class G.
        """)),
        "Basic Weather for VFR Flight": textwrap.dedent(app_instance.study_topics_content["Basic Weather for VFR Flight"].replace("...", """
            As an ultralight pilot, you fly under Visual Flight Rules (VFR). This means you must be able to see where you are going and avoid clouds. Weather is the single most significant external factor affecting flight safety.

            §103.23 Flight visibility and cloud clearance requirements:
            - In Class G Airspace (where you'll be flying):
              - 1,200 feet or less above the ground (AGL): 1 statute mile visibility and you must remain Clear of Clouds.
              - More than 1,200 feet AGL but below 10,000 feet MSL: 1 statute mile visibility, and maintain 500 feet below, 1,000 feet above, and 2,000 feet horizontal distance from clouds.

            Key Weather Phenomena for Ultralight Pilots:
            - Wind: Ultralights have low mass and large wing surfaces, making them very susceptible to wind. Always check wind speed and direction, including gusts. Avoid flying in conditions that approach your aircraft's crosswind limits.
            - Turbulence: Can be mechanical (from wind flowing over terrain/buildings) or thermal (from rising columns of warm air - "thermals"). Thermal turbulence is common on sunny afternoons. Both can cause loss of control.
            - Density Altitude: This is pressure altitude corrected for non-standard temperature. On hot days, the air is less dense. This significantly reduces engine performance and lift. Your takeoff roll will be longer, and your climb rate will be much weaker.
            - Fog/Low Clouds: If there is any chance of fog or low clouds forming, do not fly. VFR flight into IMC (Instrument Meteorological Conditions) is a leading cause of fatal accidents due to spatial disorientation.

            Weather Resources:
            - Before every flight, get a proper weather briefing. Use resources like aviationweather.gov or apps like ForeFlight. Look at METARs (current conditions) and TAFs (forecasts).
        """)),
        "Aerodynamics for Ultralights": textwrap.dedent(app_instance.study_topics_content["Aerodynamics for Ultralights"].replace("...", """
            Understanding the basic forces of flight is essential for safe control of your aircraft.

            The Four Forces:
            In steady, level flight, four forces are in equilibrium:
            - Lift: The upward force created by air flowing over the wings, opposing weight.
            - Weight: The downward force of gravity.
            - Thrust: The forward force generated by the engine/propeller, opposing drag.
            - Drag: The rearward force of air resistance.

            Angle of Attack (AOA):
            - This is the angle between the wing's chord line (an imaginary line from the leading to the trailing edge) and the oncoming air (the relative wind).
            - Lift is directly related to AOA. As you increase AOA (by pulling back on the stick), you increase lift, up to a certain point.

            Stalls:
            - A stall is NOT an engine failure. It is an aerodynamic event where the wing exceeds its critical angle of attack.
            - At the critical AOA, the smooth airflow over the top of the wing separates and becomes turbulent. This causes a sudden and dramatic loss of lift.
            - A stall can happen at ANY airspeed and ANY attitude if the critical AOA is exceeded.
            - Recovery: Immediately and automatically lower the nose to reduce the AOA below the critical angle. Once airflow is restored, you can level the wings and gently pull out of the resulting dive.

            Adverse Yaw:
            - When you roll into a turn, the outside, rising wing generates more lift (and thus more drag) than the inside, descending wing. This extra drag yaws the nose of the aircraft to the outside of the turn.
            - On aircraft with rudder control, you must apply rudder in the direction of the turn to counteract adverse yaw and keep the turn coordinated.

            Load Factor:
            - Load factor is the ratio of the total lift being produced to the aircraft's weight. In straight and level flight, it is 1 G.
            - In a banked turn, lift must support the aircraft's weight AND provide the horizontal force to make it turn. This increases the load factor.
            - In a 60-degree bank turn, the load factor is 2 Gs. The aircraft "feels" twice as heavy, and the stall speed increases by about 41%. This is a critical concept: you can stall at a much higher airspeed in a steep turn.
        """)),
        "Ultralight Systems and Preflight": textwrap.dedent(app_instance.study_topics_content["Ultralight Systems and Preflight"].replace("...", """
            You are the pilot AND the mechanic. A meticulous preflight inspection is your most important safety check.

            Develop a Flow:
            Create a consistent, logical flow for your walk-around inspection. Start at the same place and go in the same direction every time so you don't miss anything. A common method is to start at the cockpit and work your way around the aircraft.

            Key Inspection Areas (Example for a 3-axis Ultralight):
            1.  Cockpit: Master switch off, check controls for full and free movement, check fuel quantity.
            2.  Fuselage: Inspect the frame for cracks, dents, or loose bolts/rivets, especially around joints and high-stress areas.
            3.  Empennage (Tail): Check the vertical and horizontal stabilizers. Wiggle them to check for security. Check rudder and elevator hinges, control cables, and connections.
            4.  Right Wing: Walk the leading edge, checking the fabric/surface for tears or damage. Check the wing struts and their attachment points (very critical!). Check the aileron for free movement and secure hinges.
            5.  Engine & Propeller (The "Powerplant"):
                - Propeller: Check for nicks, cracks, and security. A small nick can turn into a crack and cause a catastrophic blade failure.
                - Spinner: Check for cracks and security.
                - Engine: Check for oil or fuel leaks. Check spark plug wires for security. Check engine mounts for cracks (very common failure point!). Check exhaust system for cracks. Check fluid levels.
                - Fuel System: Check fuel lines for brittleness or leaks. Check fuel filter for contaminants. Ensure fuel cap is secure.
            6.  Landing Gear: Check tires for proper inflation and wear. Check axles, struts, and brakes (if equipped) for damage or leaks.
            7.  Left Wing: Repeat the same inspection as the right wing.

            Never rush a preflight. If you find something wrong, do not fly until it is properly fixed.
        """)),
        "Navigation and Sectional Charts": textwrap.dedent(app_instance.study_topics_content["Navigation and Sectional Charts"].replace("...", """
            Even though most ultralight flights are local, basic navigation skills are essential for safety and for staying out of trouble (i.e., controlled airspace).

            Reading a VFR Sectional Chart:
            A sectional chart is your map of the sky. You must learn to identify key features:
            - Airports: Blue circles are airports with control towers; magenta circles are non-towered.
            - Airspace: As covered in the Airspace topic, learn to identify the boundaries of Class B, C, D, and E airspace.
            - Obstructions: Symbols indicate the location and height (in MSL and AGL) of towers and other tall obstacles.
            - Terrain: Colors and contour lines show elevation.
            - Maximum Elevation Figures (MEF): The large numbers in each quadrant show the height of the highest obstacle (or terrain) in that area, rounded up. This gives you a quick reference for a safe minimum altitude.

            Pilotage and Dead Reckoning:
            - Pilotage: This is the primary method for VFR navigation. It involves flying by reference to landmarks on the ground (roads, rivers, towns, lakes) and comparing them to what you see on your sectional chart.
            - Dead Reckoning: This involves calculating your heading and time to a destination based on a known starting point, your planned airspeed, and forecast winds. It's a good backup skill but requires more planning.

            Using GPS:
            - GPS is an excellent tool for situational awareness, but it should not be your only means of navigation.
            - Batteries can die, and signals can be lost. Always have your sectional chart and the ability to use pilotage as a backup.
            - A key benefit of GPS is its ability to clearly show your position relative to airspace boundaries. Use this feature to stay clear of controlled airspace.

            Lost Procedures (The 5 Cs):
            If you become lost:
            1.  Climb: To get a better view and improve radio/GPS reception (while staying VFR).
            2.  Circle: To avoid flying further into an unknown area.
            3.  Conserve: Reduce power to save fuel.
            4.  Communicate: If you have a radio, call for help on the universal emergency frequency 121.5 MHz.
            5.  Confess: Admit you are lost and need help. Don't let pride lead to a worse situation.
        """)),
        "Airport Operations and Markings": textwrap.dedent(app_instance.study_topics_content["Airport Operations and Markings"].replace("...", """
            Even if you fly from a private field, you may one day need to use a public airport. Understanding airport operations is key to safety and being a good neighbor in the aviation community. Most ultralights will operate from non-towered airports.

            Non-Towered Airport Procedures:
            - At an airport without a control tower, pilots are responsible for coordinating their arrivals and departures.
            - While radios are not required for Part 103, using a handheld aviation radio is a highly recommended safety practice. Announce your position and intentions on the airport's Common Traffic Advisory Frequency (CTAF).
            - Standard Traffic Pattern: The standard pattern is a left-hand traffic pattern (all turns are to the left). The standard altitude is 1,000 feet above the airport elevation (AGL), but ultralights often fly a lower pattern (e.g., 500 feet AGL) to stay clear of faster traffic. Always check the airport's specific procedures.

            Key Airport Markings:
            - Runway Numbers: The number indicates the runway's magnetic alignment, rounded to the nearest 10 degrees with the last zero omitted. Runway "09" is aligned to 090 degrees (East), and Runway "27" is aligned to 270 degrees (West).
            - Displaced Threshold: White arrows pointing to a thick white line across the runway indicate a displaced threshold. You can use this area for takeoff and taxi, but NOT for landing. This is usually done to provide obstacle clearance on approach.
            - Segmented Circle: This visual indicator system provides traffic pattern information. A wind cone in the center shows wind direction. L-shaped indicators show the direction of the traffic pattern (e.g., pointing away from the runway for a right-hand pattern).
            - Wind Sock/Cone: A simple, reliable indicator of wind direction and general speed. A fully extended sock indicates a strong wind (approx. 15 knots or more). A limp sock means calm winds.
        """)),
        "Emergency Procedures": textwrap.dedent(app_instance.study_topics_content["Emergency Procedures"].replace("...", """
            An emergency is any situation that threatens the safety of your flight. The key is to have a plan and fly the aircraft first. Always remember: Aviate, Navigate, Communicate.

            1. Aviate: Fly the aircraft! This is the absolute first priority. Maintain control. In case of engine failure, this means immediately establishing your best glide speed to maximize the distance you can travel without power.
            2. Navigate: Direct the aircraft toward a safe landing area.
            3. Communicate: If you have a radio and time permits, declare an emergency.

            Engine Failure: The most common emergency.
            - Engine Failure on Takeoff: This is the most critical.
              - If you have sufficient runway remaining: Land straight ahead on the runway.
              - If you are airborne but at low altitude (e.g., below 500 feet): DO NOT ATTEMPT TO TURN BACK. This is the "impossible turn" that has caused many fatal accidents. The steep bank required at low speed can lead to a stall/spin. Your only option is to land mostly straight ahead, selecting the best available field and avoiding major obstacles.
            - Engine Failure in Flight (at altitude):
              - A: Airspeed. Establish best glide speed immediately.
              - B: Best Field. Pick the best landing spot within gliding distance. Turn towards it.
              - C: Checklist. If time permits, attempt a restart (check fuel, ignition, etc.).
              - D: Declare. Announce "Mayday, Mayday, Mayday" on 121.5 MHz if you have a radio.
              - E: Execute. Perform the emergency landing. Try to land into the wind.

            In-Flight Fire:
            - Electrical Fire: Master switch OFF. Close vents. Use fire extinguisher if available.
            - Engine Fire: Turn fuel selector OFF. Master switch OFF. Establish a steep dive to try and extinguish the flames. Do not attempt to restart the engine. Execute an emergency landing immediately.

            Control System Failure:
            - If a control surface becomes jammed, use the remaining controls to maintain flight. You may need to use power and pitch trim to control airspeed and altitude. Find the largest, most suitable landing area possible.
        """)),
        "Human Factors (ADM & IMSAFE)": textwrap.dedent(app_instance.study_topics_content["Human Factors (ADM & IMSAFE)"].replace("...", """
            Human factors are the single largest contributor to aviation accidents. You, the pilot, are the most critical component of the flight system. Understanding your own limitations is as important as knowing the aircraft's limitations.

            Aeronautical Decision Making (ADM):
            ADM is a systematic approach to risk assessment and stress management. A good framework for this is the PAVE checklist. Before every flight, assess the:
            - P: Pilot. Are you fit to fly? (Use the IMSAFE checklist).
            - A: Aircraft. Is the aircraft airworthy? Has a thorough preflight been done? Is there enough fuel?
            - V: enVironment. What is the weather like now and forecast to be? What about airspace and terrain?
            - E: External Pressures. Are you feeling rushed? Are you trying to meet someone or get to an event? These pressures lead to bad decisions. Be strong enough to say "no" and cancel or delay a flight.

            The IMSAFE Checklist:
            A personal health checklist to determine your fitness to fly.
            - I: Illness. Are you feeling sick?
            - M: Medication. Are you taking any prescription or over-the-counter drugs?
            - S: Stress. Are you dealing with work, family, or financial stress?
            - A: Alcohol. Regulations require 8 hours from "bottle to throttle," but effects can last longer.
            - F: Fatigue. Are you tired or have you had enough restful sleep? Fatigue is a major cause of poor judgment.
            - E: Emotion / Eating. Are you emotionally upset? Are you properly hydrated and nourished?

            Hazardous Attitudes:
            All pilots must be aware of five hazardous attitudes that can lead to poor decisions.
            1. Anti-Authority ("Don't tell me."): Resenting rules and regulations.
            2. Impulsivity ("Do it quickly."): Feeling the need to do something, anything, immediately.
            3. Invulnerability ("It won't happen to me."): Believing accidents only happen to other people.
            4. Macho ("I can do it."): Trying to prove you are better than others by taking risks.
            5. Resignation ("What's the use?"): Feeling that you are not in control of a situation.
        """))
    }
    app_instance.study_topics_content = full_content
    # Re-initialize the main menu with the full content
    app_instance.show_main_menu()
    root.mainloop()
