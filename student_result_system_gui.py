import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter

# ==========================================
# 🎓 Smart Student Result Management System (Modern GUI)
# ==========================================
# Author: Senior Python Engineer
# Description: A Modern, Sidebar-based GUI application for managing student results, including Analytics.

DATA_FILE = "students_data.json"
ADMIN_CREDENTIALS = {"admin": "password123"}

# 🎨 Modern Color Palette
COLORS = {
    "sidebar_bg": "#2C3E50",     # Dark Blue/Grey
    "sidebar_active": "#34495E", # Lighter Blue/Grey
    "content_bg": "#ECF0F1",     # Light Grey
    "card_bg": "#FFFFFF",        # White
    "accent": "#1ABC9C",         # Teal (Primary Action)
    "danger": "#E74C3C",         # Red (Delete/Logout)
    "text_dark": "#2C3E50",      # Dark Text
    "text_light": "#ECF0F1",     # Light Text
    "border": "#BDC3C7"          # Light Border
}

class ModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Smart Student System")
        self.root.geometry("1100x700")
        self.root.configure(bg=COLORS["content_bg"])

        # Global Data Variable
        self.students = []
        self.load_data()

        # Styles
        self.setup_styles()

        # Start with Login
        self.build_login_screen()

    def setup_styles(self):
        """Configures ttk styles for a modern look."""
        style = ttk.Style()
        style.theme_use('clam') # Use 'clam' as base for better customization

        # Treeview (Table) Style
        style.configure("Treeview", 
                        background="white",
                        foreground=COLORS["text_dark"],
                        rowheight=30,
                        fieldbackground="white",
                        font=("Segoe UI", 10))
        style.map('Treeview', background=[('selected', COLORS["accent"])])
        
        # Treeview Header
        style.configure("Treeview.Heading", 
                        background=COLORS["secondary"] if "secondary" in COLORS else "#BDC3C7",
                        foreground=COLORS["text_dark"],
                        font=("Segoe UI", 10, "bold"))
        
        # Entries
        style.configure("Modern.TEntry", padding=10, relief="flat", borderwidth=0)

    def load_data(self):
        """Loads data from JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    self.students = json.load(f)
            except:
                self.students = []
        else:
            self.students = []

    def save_data(self):
        """Saves data to JSON file."""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.students, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    # ================= HELPER WIDGETS =================
    def create_btn(self, parent, text, command, bg=COLORS["accent"], fg="white", width=15):
        """Creates a modern flat button."""
        btn = tk.Button(parent, text=text, command=command, 
                        bg=bg, fg=fg, 
                        font=("Segoe UI", 10, "bold"),
                        relief="flat", activebackground=COLORS["sidebar_active"], 
                        activeforeground="white", width=width, pady=5, cursor="hand2")
        return btn

    def create_card(self, parent):
        """Creates a white card-like frame."""
        card = tk.Frame(parent, bg=COLORS["card_bg"], relief="flat", padx=20, pady=20)
        # Add a subtle border effect manually if needed, or keeping it clean flat
        return card

    # ================= LOGIN SCREEN =================
    def build_login_screen(self):
        self.clear_frame()
        self.root.configure(bg=COLORS["sidebar_bg"]) # Dark BG for Login

        login_card = tk.Frame(self.root, bg="white", padx=40, pady=50, width=400)
        login_card.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Title
        tk.Label(login_card, text="🎓", font=("Segoe UI", 50), bg="white", fg=COLORS["accent"]).pack()
        tk.Label(login_card, text="Student System", font=("Segoe UI", 24, "bold"), bg="white", fg=COLORS["text_dark"]).pack(pady=(0, 20))

        # Inputs
        tk.Label(login_card, text="Username", font=("Segoe UI", 10, "bold"), bg="white", fg="gray").pack(anchor="w")
        self.username_entry = tk.Entry(login_card, font=("Segoe UI", 12), relief="solid", bd=1, fg=COLORS["text_dark"])
        self.username_entry.pack(fill="x", pady=(5, 15), ipady=5)
        self.username_entry.insert(0, "admin")

        tk.Label(login_card, text="Password", font=("Segoe UI", 10, "bold"), bg="white", fg="gray").pack(anchor="w")
        self.password_entry = tk.Entry(login_card, font=("Segoe UI", 12), relief="solid", bd=1, show="•", fg=COLORS["text_dark"])
        self.password_entry.pack(fill="x", pady=(5, 20), ipady=5)
        self.password_entry.insert(0, "password123")

        # Login Button
        self.create_btn(login_card, "LOGIN TO DASHBOARD", self.verify_login, bg=COLORS["sidebar_bg"], width=25).pack(pady=10)

    def verify_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if ADMIN_CREDENTIALS.get(user) == pwd:
            self.build_dashboard_layout()
        else:
            messagebox.showerror("Login Failed", "❌ Invalid credentials")

    # ================= MAIN DASHBOARD LAYOUT =================
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_dashboard_layout(self):
        self.clear_frame()
        self.root.configure(bg=COLORS["content_bg"])

        # --- Sidebar ---
        self.sidebar = tk.Frame(self.root, bg=COLORS["sidebar_bg"], width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Force width

        # App Title in Sidebar
        tk.Label(self.sidebar, text="🎓 SmartSys", font=("Segoe UI", 20, "bold"), bg=COLORS["sidebar_bg"], fg="white").pack(pady=(30, 40))

        # Sidebar Buttons
        self.nav_btns = []
        self.add_sidebar_btn("➕  Add Student", self.show_add_student)
        self.add_sidebar_btn("📋  View Records", self.show_view_students)
        self.add_sidebar_btn("📊  Analytics", self.show_analytics)
        
        # Spacer
        tk.Frame(self.sidebar, bg=COLORS["sidebar_bg"]).pack(fill="y", expand=True)
        
        # Logout
        self.add_sidebar_btn("🚪  Logout", self.build_login_screen, bg=COLORS["danger"])

        # --- Content Area ---
        self.content_area = tk.Frame(self.root, bg=COLORS["content_bg"])
        self.content_area.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # Default View
        self.show_add_student()

    def add_sidebar_btn(self, text, command, bg=COLORS["sidebar_bg"]):
        btn = tk.Button(self.sidebar, text=text, font=("Segoe UI", 11), 
                        bg=bg, fg="white", activebackground=COLORS["sidebar_active"], activeforeground="white",
                        bd=0, cursor="hand2", anchor="w", padx=20, command=command)
        btn.pack(fill="x", pady=2, ipady=10)
        self.nav_btns.append(btn)
        return btn

    def set_active_view(self, title):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Header for the view
        tk.Label(self.content_area, text=title, font=("Segoe UI", 22, "bold"), 
                 bg=COLORS["content_bg"], fg=COLORS["text_dark"]).pack(anchor="w", pady=(0, 20))

    # ================= VIEW: ADD STUDENT =================
    def show_add_student(self):
        self.set_active_view("Add New Student")
        
        # Card Container
        card = self.create_card(self.content_area)
        card.pack(fill="both", expand=True)

        # Form Grid
        form_frame = tk.Frame(card, bg="white")
        form_frame.pack(fill="x", pady=10)

        # Roll Number
        tk.Label(form_frame, text="Roll Number", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.ent_roll = tk.Entry(form_frame, bg="#F9F9F9", relief="flat", font=("Segoe UI", 11))
        self.ent_roll.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15), ipady=5)

        # Name
        tk.Label(form_frame, text="Full Name", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.ent_name = tk.Entry(form_frame, bg="#F9F9F9", relief="flat", font=("Segoe UI", 11))
        self.ent_name.grid(row=1, column=1, sticky="ew", padx=10, pady=(0, 15), ipady=5)

        # Class
        tk.Label(form_frame, text="Class", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.ent_class = tk.Entry(form_frame, bg="#F9F9F9", relief="flat", font=("Segoe UI", 11))
        self.ent_class.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 15), ipady=5)

        # Section
        tk.Label(form_frame, text="Section", font=("Segoe UI", 10, "bold"), bg="white").grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.ent_section = tk.Entry(form_frame, bg="#F9F9F9", relief="flat", font=("Segoe UI", 11))
        self.ent_section.grid(row=3, column=1, sticky="ew", padx=10, pady=(0, 15), ipady=5)

        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=1)

        # Separator
        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=10)

        # Marks Section
        tk.Label(card, text="Enter Marks (0-100)", font=("Segoe UI", 12, "bold"), bg="white", fg=COLORS["accent"]).pack(anchor="w", pady=10)
        
        marks_frame = tk.Frame(card, bg="white")
        marks_frame.pack(fill="x")

        self.subjects = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]
        self.mark_vars = {}

        for i, sub in enumerate(self.subjects):
            lbl = tk.Label(marks_frame, text=sub, font=("Segoe UI", 10), bg="white")
            lbl.grid(row=0, column=i, padx=5, sticky="w")
            
            ent = tk.Entry(marks_frame, bg="#F9F9F9", relief="flat", font=("Segoe UI", 11), width=10, justify="center")
            ent.grid(row=1, column=i, padx=5, pady=(5, 10), ipady=5)
            self.mark_vars[sub] = ent

        # Action Buttons
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(pady=30, anchor="w")
        
        self.create_btn(btn_frame, "💾  SAVE RECORD", self.save_student).pack(side="left", padx=(0, 10))
        self.create_btn(btn_frame, "🔄  CLEAR FORM", self.clear_inputs, bg=COLORS["sidebar_active"]).pack(side="left")

    def save_student(self):
        roll = self.ent_roll.get().strip()
        name = self.ent_name.get().strip()
        student_class = self.ent_class.get().strip()
        section = self.ent_section.get().strip()

        if not roll or not name or not student_class or not section:
            messagebox.showwarning("Validation", "All fields (Roll, Name, Class, Section) are required!")
            return

        if any(s['roll_no'] == roll for s in self.students):
            messagebox.showerror("Duplicate", "Student with this Roll Number already exists!")
            return

        marks = {}
        total = 0
        try:
            for sub, ent in self.mark_vars.items():
                m_str = ent.get()
                m = float(m_str) if m_str else 0.0
                if not (0 <= m <= 100): raise ValueError
                marks[sub] = m
                total += m
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric marks (0-100).")
            return

        percentage = (total / 500) * 100
        grade = self.calculate_grade(percentage)

        new_student = {
            "roll_no": roll, "name": name, "class": student_class, "section": section,
            "marks": marks, "total": total, "percentage": round(percentage, 2), "grade": grade
        }

        self.students.append(new_student)
        self.save_data()
        messagebox.showinfo("Success", f"Student {name} added successfully!")
        self.clear_inputs()

    def calculate_grade(self, percentage):
        if percentage >= 90: return "A+"
        elif percentage >= 80: return "A"
        elif percentage >= 70: return "B"
        elif percentage >= 60: return "C"
        elif percentage >= 50: return "D"
        else: return "Fail"

    def clear_inputs(self):
        self.ent_roll.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_class.delete(0, tk.END)
        self.ent_section.delete(0, tk.END)
        for ent in self.mark_vars.values():
            ent.delete(0, tk.END)

    # ================= VIEW: MANAGE STUDENTS =================
    def show_view_students(self):
        self.set_active_view("Student Records")

        card = self.create_card(self.content_area)
        card.pack(fill="both", expand=True)

        # Toolbar
        toolbar = tk.Frame(card, bg="white")
        toolbar.pack(fill="x", pady=(0, 15))

        self.create_btn(toolbar, "🔄 Refresh", self.refresh_table, bg=COLORS["sidebar_active"], width=10).pack(side="left", padx=(0, 10))
        
        # Filter
        tk.Label(toolbar, text="Filter by Class:", bg="white", font=("Segoe UI", 10)).pack(side="left", padx=(10, 5))
        self.class_filter = ttk.Combobox(toolbar, state="readonly", width=15)
        self.class_filter.pack(side="left", padx=(0, 10))
        self.class_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())
        
        self.create_btn(toolbar, "🗑️ Delete Selected", self.delete_selected, bg=COLORS["danger"], width=15).pack(side="left", padx=(0, 10))
        self.create_btn(toolbar, "📄 Result Card", self.generate_pdf_report, bg="#8E44AD", width=15).pack(side="left") 
        self.create_btn(toolbar, "📥 Import CSV", self.import_csv_data, bg="#D35400", width=15).pack(side="right", padx=(0, 10))
        self.create_btn(toolbar, "📊 PDF Report", self.export_pdf_list, bg="#27AE60", width=15).pack(side="right", padx=(0, 10))

        # Table Frame
        table_frame = tk.Frame(card)
        table_frame.pack(fill="both", expand=True)

        cols = ("Roll No", "Name", "Class", "Section", "Total", "%", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Headings
        self.tree.heading("Roll No", text="Roll No")
        self.tree.heading("Name", text="Student Name")
        self.tree.heading("Class", text="Class")
        self.tree.heading("Section", text="Section")
        self.tree.heading("Total", text="Total Marks")
        self.tree.heading("%", text="Percentage")
        self.tree.heading("Grade", text="Grade")

        # Column Config
        self.tree.column("Roll No", width=80, anchor="center")
        self.tree.column("Name", width=180, anchor="w")
        self.tree.column("Class", width=80, anchor="center")
        self.tree.column("Section", width=60, anchor="center")
        self.tree.column("Total", width=80, anchor="center")
        self.tree.column("%", width=80, anchor="center")
        self.tree.column("Grade", width=60, anchor="center")

        # Load Data
        self.refresh_table()

    def refresh_table(self):
        # Update Filter Values
        classes = sorted(list(set(s.get('class', 'N/A') for s in self.students)))
        current_filter = self.class_filter.get()
        self.class_filter['values'] = ["All Classes"] + classes
        if current_filter not in self.class_filter['values']:
             self.class_filter.current(0)

        # Filter Data
        selected_class = self.class_filter.get()
        if selected_class == "All Classes" or not selected_class:
            filtered_data = self.students
        else:
            filtered_data = [s for s in self.students if s.get('class', 'N/A') == selected_class]

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for s in filtered_data:
            self.tree.insert("", "end", values=(
                s['roll_no'], s['name'], s.get('class', '-'), s.get('section', '-'),
                s['total'], f"{s['percentage']}%", s['grade']
            ))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected record(s)?"):
            for item in selected:
                val = self.tree.item(item, "values")
                self.students = [s for s in self.students if s['roll_no'] != str(val[0])]
            self.save_data()
            self.refresh_table()

    # ================= VIEW: ANALYTICS =================
    def show_analytics(self):
        self.set_active_view("Class Analytics")
        
        if not self.students:
            tk.Label(self.content_area, text="No student data available to analyze.", 
                     font=("Segoe UI", 14), bg=COLORS["content_bg"], fg="gray").pack(pady=50)
            return

        # Control Bar
        control_frame = tk.Frame(self.content_area, bg=COLORS["content_bg"])
        control_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(control_frame, text="Filter by Class:", bg=COLORS["content_bg"], font=("Segoe UI", 12)).pack(side="left", padx=(0, 10))
        
        classes = sorted(list(set(s.get('class', 'N/A') for s in self.students)))
        self.analytics_filter = ttk.Combobox(control_frame, values=["All Classes"] + classes, state="readonly", width=20)
        self.analytics_filter.pack(side="left")
        self.analytics_filter.current(0)
        self.analytics_filter.bind("<<ComboboxSelected>>", self.update_analytics_dashboard)

        # Dashboard Container
        self.dashboard_frame = tk.Frame(self.content_area, bg=COLORS["content_bg"])
        self.dashboard_frame.pack(fill="both", expand=True)
        
        self.update_analytics_dashboard()

    def update_analytics_dashboard(self, event=None):
        # Clear existing
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
            
        # Filter Data
        selected_class = self.analytics_filter.get()
        if selected_class == "All Classes":
            data = self.students
        else:
            data = [s for s in self.students if s.get('class', 'N/A') == selected_class]
            
        if not data:
             tk.Label(self.dashboard_frame, text="No data for selected class.", font=("Segoe UI", 12), bg=COLORS["content_bg"]).pack(pady=20)
             return

        # --- Calculations ---
        total_students = len(data)
        passed = sum(1 for s in data if s['grade'] != 'Fail')
        failed = total_students - passed
        pass_rate = (passed / total_students) * 100
        
        if total_students > 0:
            avg_percentage = sum(s['percentage'] for s in data) / total_students
        else:
            avg_percentage = 0
        
        sorted_students = sorted(data, key=lambda x: x['total'], reverse=True)
        topper = f"{sorted_students[0]['name']} ({sorted_students[0]['percentage']}%)" if sorted_students else "N/A"

        # --- KPI Cards ---
        kpi_frame = tk.Frame(self.dashboard_frame, bg=COLORS["content_bg"])
        kpi_frame.pack(fill="x", pady=(0, 20))

        self.create_kpi_card(kpi_frame, "Total Students", str(total_students), "#3498DB").pack(side="left", fill="x", expand=True, padx=5)
        self.create_kpi_card(kpi_frame, "Pass Rate", f"{pass_rate:.1f}%", "#27AE60").pack(side="left", fill="x", expand=True, padx=5)
        self.create_kpi_card(kpi_frame, "Class Average", f"{avg_percentage:.1f}%", "#F39C12").pack(side="left", fill="x", expand=True, padx=5)
        self.create_kpi_card(kpi_frame, "Top Performer", topper, "#8E44AD").pack(side="left", fill="x", expand=True, padx=5)

        # --- Charts ---
        chart_frame = tk.Frame(self.dashboard_frame, bg=COLORS["content_bg"])
        chart_frame.pack(fill="both", expand=True)

        # 1. Grade Distribution (Bar Chart)
        grades = [s['grade'] for s in data]
        grade_counts = Counter(grades)
        grade_order = ["A+", "A", "B", "C", "D", "Fail"]
        counts = [grade_counts.get(g, 0) for g in grade_order]

        # Close previous figures to avoid memory leak
        plt.close('all')

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), dpi=100)
        fig.patch.set_facecolor(COLORS["content_bg"])

        # Bar Chart
        color_map = ["#2ECC71", "#27AE60", "#F1C40F", "#E67E22", "#E74C3C", "#C0392B"]
        bars = ax1.bar(grade_order, counts, color=color_map)
        ax1.set_title("Grade Distribution", fontsize=12, fontweight='bold')
        ax1.set_facecolor("#F9F9F9")
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                         f'{int(height)}',
                         ha='center', va='bottom')

        # 2. Pass vs Fail (Pie Chart)
        if total_students > 0:
            ax2.pie([passed, failed], labels=['Passed', 'Failed'], autopct='%1.1f%%', 
                    colors=['#2ECC71', '#E74C3C'], startangle=90, explode=(0.1, 0), shadow=True)
            ax2.set_title("Pass vs Fail Ratio", fontsize=12, fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_kpi_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg="white", padx=15, pady=15)
        
        # Color Strip
        tk.Frame(card, bg=color, width=5).pack(side="left", fill="y", padx=(0, 10))
        
        content = tk.Frame(card, bg="white")
        content.pack(side="left", fill="both")
        
        tk.Label(content, text=title, font=("Segoe UI", 10), bg="white", fg="gray").pack(anchor="w")
        tk.Label(content, text=value, font=("Segoe UI", 16, "bold"), bg="white", fg=COLORS["text_dark"]).pack(anchor="w")
        
        return card

    def import_csv_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path: return

        success_count = 0
        skip_count = 0

        try:
            with open(file_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                
                # Check for empty file or wrong format
                if not reader.fieldnames:
                    messagebox.showerror("Error", "CSV file is empty or invalid.")
                    return

                for row in reader:
                    # Clean up keys (strip whitespace)
                    row = {k.strip(): v.strip() for k, v in row.items() if k}
                    
                    try:
                        roll = row.get("Roll No")
                        name = row.get("Name")
                        
                        if not roll or not name:
                            skip_count += 1
                            continue

                        # Check Duplicate
                        if any(s['roll_no'] == roll for s in self.students):
                            skip_count += 1
                            continue
                        
                        # Parse Marks
                        marks = {}
                        total = 0
                        
                        # Flexible Subject Mapping
                        subjects_map = {
                            "Mathematics": ["Mathematics", "Maths", "Math", "MATH", "MATHEMATICS"],
                            "Physics": ["Physics", "Phy", "PHY", "PHYSICS"],
                            "Chemistry": ["Chemistry", "Chem", "CHEM", "CHEMISTRY"],
                            "English": ["English", "Eng", "ENG", "ENGLISH"],
                            "Computer Science": ["Computer Science", "CS", "Comp Sci", "COMPUTER SCIENCE"]
                        }
                        
                        valid_marks = True
                        for internal_sub, aliases in subjects_map.items():
                            found = False
                            # Try direct match first (case-sensitive from CSV headers but mapped here)
                            # Actually, let's just loop aliases.
                            for alias in aliases:
                                if alias in row:
                                    m = float(row[alias])
                                    if 0 <= m <= 100:
                                        marks[internal_sub] = m
                                        total += m
                                        found = True
                                        break
                            
                            if not found:
                                # Try case-insensitive matching for keys in row
                                row_lower = {k.lower(): v for k, v in row.items()}
                                for alias in aliases:
                                    if alias.lower() in row_lower:
                                        m = float(row_lower[alias.lower()])
                                        if 0 <= m <= 100:
                                            marks[internal_sub] = m
                                            total += m
                                            found = True
                                            break

                            if not found:
                                valid_marks = False
                                break # Missing a subject
                        
                        if not valid_marks:
                            skip_count += 1
                            continue
                        
                        # Get Class/Section (Optional in CSV)
                        student_class = row.get("Class", "Unassigned")
                        section = row.get("Section", "Unassigned")

                        percentage = (total / 500) * 100
                        grade = self.calculate_grade(percentage)

                        new_student = {
                            "roll_no": roll, "name": name, "class": student_class, "section": section,
                            "marks": marks,
                            "total": total, "percentage": round(percentage, 2), "grade": grade
                        }
                        self.students.append(new_student)
                        success_count += 1

                    except ValueError:
                        skip_count += 1
                        continue

            self.save_data()
            self.refresh_table()
            messagebox.showinfo("Import Summary", f"✅ Successfully Imported: {success_count}\n❌ Skipped (Duplicate/Invalid): {skip_count}")

        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to read CSV: {e}\nStructure: Roll No, Name, Mathematics, Physics, Chemistry, English, Computer Science")

    def export_pdf_list(self):
        if not self.students:
            messagebox.showwarning("No Data", "No student data to export.")
            return

        # Apply Filter if active
        if hasattr(self, 'class_filter'):
            selected_class = self.class_filter.get()
            if selected_class == "All Classes" or not selected_class:
                data_to_export = self.students
                report_title = "Student Result Report (All Classes)"
            else:
                data_to_export = [s for s in self.students if s.get('class', 'N/A') == selected_class]
                report_title = f"Student Result Report - Class {selected_class}"
        else:
            data_to_export = self.students
            report_title = "Student Result Report"
        
        if not data_to_export:
             messagebox.showinfo("Export", "No students found for the selected filter.")
             return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("PDF File", "*.pdf")],
            initialfile=f"Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )
        if not file_path: return

        try:
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4
            
            # Header
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width/2, height-50, report_title)
            c.setFont("Helvetica", 12)
            c.drawCentredString(width/2, height-70, f"Generated on: {datetime.now().strftime('%d-%b-%Y %H:%M')}")
            
            # Table Header
            data = [['Roll No', 'Name', 'Class', 'Sec', 'Total', '%', 'Grd']]
            
            # Table Data
            for s in data_to_export:
                data.append([
                    s['roll_no'], 
                    s['name'], 
                    s.get('class', '-'),
                    s.get('section', '-'),
                    str(s['total']), 
                    f"{s['percentage']}%", 
                    s['grade']
                ])

            # Styling
            table = Table(data, colWidths=[60, 160, 60, 40, 60, 60, 50])
            style = TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ])
            table.setStyle(style)
            
            # Draw
            table.wrapOn(c, width, height)
            table.drawOn(c, (width-500)/2, height-150)
            
            c.save()
            messagebox.showinfo("Success", f"Full Report saved successfully at:\n{file_path}")
            os.startfile(file_path)
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export PDF: {e}")

    # ================= PDF GENERATION =================
    def generate_pdf_report(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Student", "Please select a student to generate the result card.")
            return

        # Get student data
        item = self.tree.item(selected[0])
        roll_no = item['values'][0]
        student = next((s for s in self.students if s['roll_no'] == str(roll_no)), None)
        
        if not student: return

        # Ask where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", 
            filetypes=[("PDF File", "*.pdf")],
            initialfile=f"Result_{student['name']}_{student['roll_no']}.pdf"
        )
        if not file_path: return

        try:
            self.create_realistic_result(file_path, student)
            messagebox.showinfo("Success", f"Result Card generated successfully!\nSaved at: {file_path}")
            os.startfile(file_path) # Auto-open file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {e}")

    def create_realistic_result(self, file_path, student):
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        
        # --- BORDER & BACKGROUND ---
        # Double Border
        c.setStrokeColor(colors.darkblue)
        c.setLineWidth(5)
        c.rect(20, 20, width-40, height-40)
        c.setStrokeColor(colors.gold)
        c.setLineWidth(2)
        c.rect(25, 25, width-50, height-50)
        
        # Watermark (Light Grey Text)
        c.saveState()
        c.translate(width/2, height/2)
        c.rotate(45)
        c.setFillColor(colors.lightgrey)
        c.setFont("Helvetica-Bold", 100)
        c.drawCentredString(0, 0, "OFFICIAL RESULT")
        c.restoreState()

        # --- HEADER ---
        # School Logo (Simulated with text/shape)
        c.setFillColor(colors.darkblue)
        c.circle(80, height-80, 40, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Times-Bold", 30)
        c.drawString(63, height-90, "🎓") # Emoji might not render perfectly in all PDF readers without font support, using standard text typically safer, but standard fonts support widespread symbols. Or draw simple shape.
        
        # Header Text
        c.setFillColor(colors.darkblue)
        c.setFont("Times-Bold", 30)
        c.drawCentredString(width/2, height-90, "SKYLINE INTERNATIONAL ACADEMY")
        
        c.setFont("Times-Roman", 14)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, height-115, "Excellence in Education | Estd. 1998")
        c.drawCentredString(width/2, height-135, "123 Education Lane, Knowledge City, NY 10001")

        c.setLineWidth(2)
        c.line(100, height-150, width-100, height-150)

        # --- TITLE ---
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width/2, height-200, "STATEMENT OF MARKS")
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height-225, "Annual Examination 2025-2026")

        # --- STUDENT DETAILS ---
        y_details = height - 280
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y_details, f"Student Name  :  {student['name'].upper()}")
        c.drawString(width-250, y_details, f"Roll Number   :  {student['roll_no']}")
        
        student_class = student.get('class', 'X')
        section = student.get('section', 'A')
        c.drawString(60, y_details-25, f"Class / Batch   :  {student_class} - {section}")
        c.drawString(width-250, y_details-25, f"Date of Issue :  {datetime.now().strftime('%d-%b-%Y')}")

        # --- MARKS TABLE ---
        data = [['SUBJECT', 'MAX MARKS', 'OBTAINED MARKS', 'GRADE']]
        
        # Add Rows
        for subject, marks in student['marks'].items():
            data.append([subject, "100", f"{marks}", self.calculate_grade((marks/100)*100)]) # Calculate individual grade if needed or use overall logic
        
        # Total Row
        data.append(['', '', '', ''])
        data.append(['GRAND TOTAL', '500', f"{student['total']}", f"{student['grade']}"])

        # Table Style
        table = Table(data, colWidths=[200, 100, 120, 80])
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-3), 1, colors.black),
            ('GRID', (0,-1), (-1,-1), 1, colors.black), # Grid for Total row
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ])
        table.setStyle(style)
        
        # Draw Table
        table.wrapOn(c, width, height)
        table.drawOn(c, (width-500)/2, height-550)

        # --- RESULT STATUS & SUMMARY ---
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.darkgreen if student['grade'] != 'Fail' else colors.red)
        status = "PASSED" if student['grade'] != 'Fail' else "FAILED"
        c.drawCentredString(width/2, height-580, f"RESULT STATUS: {status}")

        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2, height-600, "Grading Scale: A+ (90-100) | A (80-89) | B (70-79) | C (60-69) | D (50-59)")

        # --- SIGNATURES ---
        y_sig = 100
        c.setLineWidth(1)
        c.line(80, y_sig, 200, y_sig)
        c.drawCentredString(140, y_sig-15, "Class Teacher")
        
        c.line(width-200, y_sig, width-80, y_sig)
        c.drawCentredString(width-140, y_sig-15, "Principal")

        # Decorative Stamp
        c.setStrokeColor(colors.green)
        c.setLineWidth(3)
        c.circle(width-140, y_sig+50, 40)
        c.saveState()
        c.translate(width-140, y_sig+50)
        c.rotate(15)
        c.setFillColor(colors.green)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(0, -5, "VERIFIED")
        c.restoreState()

        c.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernApp(root)
    root.mainloop()
