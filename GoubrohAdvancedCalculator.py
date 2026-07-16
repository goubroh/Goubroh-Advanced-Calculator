import tkinter as tk
from tkinter import messagebox
import math

class GoubrohAdvancedCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("GOUBROH - Multi-Edition")
        self.root.geometry("440x720")
        self.root.configure(bg="#1c1d21") # Dark matte shell color
        self.root.resizable(False, False)

        # Color Palette inspired by premium hardware
        self.COLOR_SHELL = "#1c1d21"
        self.COLOR_LCD = "#a2b7a5"      # Classic green LCD tint
        self.COLOR_LCD_TEXT = "#1b241d" # Deep dark LCD ink
        self.COLOR_NUM_BG = "#e1e2e5"   # Light gray number keys
        self.COLOR_NUM_FG = "#000000"
        self.COLOR_FUN_BG = "#383c42"   # Dark gray scientific keys
        self.COLOR_FUN_FG = "#ffffff"
        self.COLOR_GREEN = "#5d9e68"    # DEL/AC matte green
        self.COLOR_ACCENT = "#dca134"   # Shift/Mode gold accent

        self.current_mode = "SCI" # Modes: SCI, COMMERCE, CONVERT
        
        self.setup_ui()

    def setup_ui(self):
        # Top Branding Header
        header_frame = tk.Frame(self.root, bg=self.COLOR_SHELL)
        header_frame.pack(fill=tk.X, padx=20, pady=(10, 5))
        
        # Rebranded to GOUBROH (Name tag removed)
        tk.Label(header_frame, text="GOUBROH", font=("Arial", 16, "bold"), fg="#ffffff", bg=self.COLOR_SHELL).pack(side=tk.LEFT)
        
        # System Mode Indicators
        self.mode_indicator = tk.Label(header_frame, text="MODE: SCIENTIFIC", font=("Arial", 9, "bold"), fg=self.COLOR_ACCENT, bg=self.COLOR_SHELL)
        self.mode_indicator.pack(side=tk.RIGHT, pady=5)

        # --- DUAL-LINE LCD SCREEN ---
        screen_frame = tk.Frame(self.root, bg=self.COLOR_LCD, bd=8, relief=tk.SUNKEN)
        screen_frame.pack(fill=tk.X, padx=20, pady=5)

        # Top line for math formula history / contexts
        self.history_label = tk.Label(screen_frame, text="", font=("Courier", 11), anchor="w", bg=self.COLOR_LCD, fg=self.COLOR_LCD_TEXT, height=1)
        self.history_label.pack(fill=tk.X, padx=5)

        # Main interactive entry display
        self.display = tk.Entry(screen_frame, font=("Courier", 24, "bold"), bd=0, bg=self.COLOR_LCD, fg=self.COLOR_LCD_TEXT, justify="right", insertbackground=self.COLOR_LCD_TEXT)
        self.display.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.display.insert(0, "0")

        # --- MODE / SYSTEM KEYPAD ROW ---
        sys_frame = tk.Frame(self.root, bg=self.COLOR_SHELL)
        sys_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Mode selector buttons
        tk.Button(sys_frame, text="SCI MODE", font=("Arial", 9, "bold"), bg=self.COLOR_FUN_BG, fg=self.COLOR_ACCENT, bd=2, command=lambda: self.switch_mode("SCI")).pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)
        tk.Button(sys_frame, text="COMMERCE", font=("Arial", 9, "bold"), bg=self.COLOR_FUN_BG, fg=self.COLOR_ACCENT, bd=2, command=lambda: self.switch_mode("COMMERCE")).pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)
        tk.Button(sys_frame, text="CONVERTER", font=("Arial", 9, "bold"), bg=self.COLOR_FUN_BG, fg=self.COLOR_ACCENT, bd=2, command=lambda: self.switch_mode("CONVERT")).pack(side=tk.LEFT, padx=4, expand=True, fill=tk.X)

        # --- DYNAMIC INTERFACE CONTAINER ---
        self.container = tk.Frame(self.root, bg=self.COLOR_SHELL)
        self.container.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Initialize the default scientific grid layout
        self.build_scientific_ui()

    def switch_mode(self, mode):
        self.current_mode = mode
        # Clear everything inside dynamic frame container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        self.display.delete(0, tk.END)
        self.history_label.config(text="")

        if mode == "SCI":
            self.mode_indicator.config(text="MODE: SCIENTIFIC")
            self.display.insert(0, "0")
            self.build_scientific_ui()
        elif mode == "COMMERCE":
            self.mode_indicator.config(text="MODE: COMMERCE")
            self.build_commerce_ui()
        elif mode == "CONVERT":
            self.mode_indicator.config(text="MODE: CONVERTER")
            self.build_converter_ui()

    # ==========================================
    # SECTION 1: SCIENTIFIC KEYPAD LAYOUT
    # ==========================================
    def build_scientific_ui(self):
        sci_buttons = [
            ['sin', 'cos', 'tan', 'x²', '^'],
            ['log', 'ln', '√', '(', ')'],
            ['π', 'e', 'Abs', '1/x', '%']
        ]

        base_buttons = [
            ['7', '8', '9', 'DEL', 'AC'],
            ['4', '5', '6', '×', '÷'],
            ['1', '2', '3', '+', '-'],
            ['0', '.', 'Ans', 'Exp', '=']
        ]

        pad_frame = tk.Frame(self.container, bg=self.COLOR_SHELL)
        pad_frame.pack(fill=tk.BOTH, expand=True)

        row_idx = 0
        for row in sci_buttons:
            for col_idx, text in enumerate(row):
                btn = tk.Button(pad_frame, text=text, font=("Arial", 11, "bold"), bg=self.COLOR_FUN_BG, fg=self.COLOR_FUN_FG, bd=3, height=2, width=6)
                btn.grid(row=row_idx, column=col_idx, padx=3, pady=4, sticky="nsew")
                btn.bind("<Button-1>", self.on_sci_click)
            row_idx += 1

        spacer = tk.Frame(pad_frame, height=2, bg="#333333")
        spacer.grid(row=row_idx, column=0, columnspan=5, pady=6, sticky="ew")
        row_idx += 1

        for row in base_buttons:
            for col_idx, text in enumerate(row):
                if text in ['DEL', 'AC']:
                    bg_color, fg_color = self.COLOR_GREEN, "#ffffff"
                elif text in ['×', '÷', '+', '-', '=']:
                    bg_color, fg_color = self.COLOR_FUN_BG, self.COLOR_FUN_FG
                else:
                    bg_color, fg_color = self.COLOR_NUM_BG, self.COLOR_NUM_FG

                btn = tk.Button(pad_frame, text=text, font=("Arial", 13, "bold"), bg=bg_color, fg=fg_color, bd=3, height=2, width=5)
                btn.grid(row=row_idx, column=col_idx, padx=3, pady=4, sticky="nsew")
                
                if text == '=':
                    btn.config(command=self.evaluate_scientific)
                elif text == 'AC':
                    btn.config(command=self.clear_all)
                elif text == 'DEL':
                    btn.config(command=self.delete_last)
                else:
                    btn.bind("<Button-1>", self.on_base_click)
            row_idx += 1

        for i in range(5):
            pad_frame.columnconfigure(i, weight=1)

    def on_base_click(self, event):
        text = event.widget["text"]
        current = self.display.get()
        if current == "0" or current == "Error":
            self.display.delete(0, tk.END)
            current = ""
        self.display.insert(tk.END, text)

    def on_sci_click(self, event):
        text = event.widget["text"]
        current = self.display.get()
        if current == "0" or current == "Error":
            self.display.delete(0, tk.END)
            current = ""
        
        if text in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'Abs']:
            self.display.insert(tk.END, f"{text}(")
        elif text == 'x²':
            self.display.insert(tk.END, "^2")
        elif text == '1/x':
            self.display.insert(tk.END, "^-1")
        else:
            self.display.insert(tk.END, text)

    def clear_all(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")
        self.history_label.config(text="")

    def delete_last(self):
        current = self.display.get()
        if current and current != "0":
            self.display.delete(len(current)-1, tk.END)
        if not self.display.get():
            self.display.insert(0, "0")

    def evaluate_scientific(self):
        expr = self.display.get()
        self.history_label.config(text=expr + " =")
        
        expr = expr.replace('×', '*').replace('÷', '/')
        expr = expr.replace('^', '**')
        expr = expr.replace('π', 'math.pi').replace('e', 'math.e')
        expr = expr.replace('sin(', 'math.sin(math.radians(') 
        expr = expr.replace('cos(', 'math.cos(math.radians(')
        expr = expr.replace('tan(', 'math.tan(math.radians(')
        expr = expr.replace('log(', 'math.log10(')
        expr = expr.replace('ln(', 'math.log(')
        expr = expr.replace('√(', 'math.sqrt(')
        expr = expr.replace('Abs(', 'abs(')
        
        open_brackets = expr.count('(')
        close_brackets = expr.count(')')
        if open_brackets > close_brackets:
            expr += ')' * (open_brackets - close_brackets)
            if 'math.radians(' in expr: 
                expr += ')' * (open_brackets - close_brackets)

        try:
            result = eval(expr, {"__builtins__": None}, {"math": math, "abs": abs})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 8)
                
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
        except ZeroDivisionError:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Math ERROR")
        except Exception:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Syntax ERROR")

    # ==========================================
    # SECTION 2: COMMERCE INTERFACE LAYOUT
    # ==========================================
    def build_commerce_ui(self):
        self.display.insert(0, "[Finance Menu Active]")
        
        com_frame = tk.Frame(self.container, bg=self.COLOR_SHELL)
        com_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        fields = [
            ("Principal Amount:", "P_val"),
            ("Annual Interest (%):", "R_val"),
            ("Period (Years):", "T_val")
        ]
        
        self.com_inputs = {}
        for idx, (label_text, var_name) in enumerate(fields):
            lbl = tk.Label(com_frame, text=label_text, font=("Arial", 11, "bold"), fg="#ffffff", bg=self.COLOR_SHELL, anchor="w")
            lbl.grid(row=idx, column=0, sticky="ew", pady=12, padx=5)
            
            entry = tk.Entry(com_frame, font=("Arial", 12), bg=self.COLOR_NUM_BG, fg="#000000", bd=2, justify="right")
            entry.grid(row=idx, column=1, sticky="ew", pady=12, padx=5)
            self.com_inputs[var_name] = entry

        com_frame.columnconfigure(1, weight=1)

        btn_config = [
            ("Simple Interest", lambda: self.compute_commerce("SI")),
            ("Compound Interest", lambda: self.compute_commerce("CI")),
            ("Loan EMI / Month", lambda: self.compute_commerce("EMI"))
        ]

        for idx, (text, cmd) in enumerate(btn_config):
            btn = tk.Button(com_frame, text=text, font=("Arial", 11, "bold"), bg=self.COLOR_FUN_BG, fg=self.COLOR_ACCENT, bd=3, command=cmd, height=2)
            btn.grid(row=4, column=0, columnspan=2, sticky="ew", pady=6)

    def compute_commerce(self, mode_type):
        try:
            p = float(self.com_inputs["P_val"].get())
            r = float(self.com_inputs["R_val"].get())
            t = float(self.com_inputs["T_val"].get())
        except ValueError:
            messagebox.showerror("Input Error", "Please provide numeric value fields.")
            return

        self.display.delete(0, tk.END)
        if mode_type == "SI":
            interest = (p * r * t) / 100
            self.history_label.config(text=f"SI Total (P + Interest)")
            self.display.insert(0, f"{p + interest:.2f}")
        elif mode_type == "CI":
            total_amount = p * ((1 + r / 100) ** t)
            self.history_label.config(text=f"CI Compound Return")
            self.display.insert(0, f"{total_amount:.2f}")
        elif mode_type == "EMI":
            monthly_rate = r / (12 * 100)
            months = t * 12
            if monthly_rate == 0:
                emi = p / months
            else:
                emi = p * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
            self.history_label.config(text=f"Fixed Monthly Payment")
            self.display.insert(0, f"{emi:.2f}")

    # ==========================================
    # SECTION 3: CONVERTER UTILITY LAYOUT
    # ==========================================
    def build_converter_ui(self):
        self.display.insert(0, "[Converter Menu Active]")
        
        conv_frame = tk.Frame(self.container, bg=self.COLOR_SHELL)
        conv_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Label(conv_frame, text="Enter Value to Convert:", font=("Arial", 11, "bold"), fg="#ffffff", bg=self.COLOR_SHELL).pack(anchor="w", pady=5)
        self.conv_entry = tk.Entry(conv_frame, font=("Arial", 14), bg=self.COLOR_NUM_BG, fg="#000000", justify="center")
        self.conv_entry.pack(fill=tk.X, pady=5)

        conversions = [
            ("KG to Pounds (Lbs)", lambda: self.run_conversion("KG_LBS")),
            ("Pounds (Lbs) to KG", lambda: self.run_conversion("LBS_KG")),
            ("KM to Miles", lambda: self.run_conversion("KM_MI")),
            ("Miles to KM", lambda: self.run_conversion("MI_KM")),
            ("Celsius to Fahrenheit", lambda: self.run_conversion("C_F")),
            ("Fahrenheit to Celsius", lambda: self.run_conversion("F_C"))
        ]

        for text, cmd in conversions:
            btn = tk.Button(conv_frame, text=text, font=("Arial", 10, "bold"), bg=self.COLOR_FUN_BG, fg=self.COLOR_FUN_FG, bd=2, command=cmd, height=2)
            btn.pack(fill=tk.X, pady=4)

    def run_conversion(self, formula):
        try:
            val = float(self.conv_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please provide a valid numeric value.")
            return

        self.display.delete(0, tk.END)
        if formula == "KG_LBS":
            self.history_label.config(text=f"{val} KG to Lbs")
            self.display.insert(0, f"{val * 2.20462:.4f}")
        elif formula == "LBS_KG":
            self.history_label.config(text=f"{val} Lbs to KG")
            self.display.insert(0, f"{val / 2.20462:.4f}")
        elif formula == "KM_MI":
            self.history_label.config(text=f"{val} KM to Miles")
            self.display.insert(0, f"{val * 0.621371:.4f}")
        elif formula == "MI_KM":
            self.history_label.config(text=f"{val} Miles to KM")
            self.display.insert(0, f"{val / 0.621371:.4f}")
        elif formula == "C_F":
            self.history_label.config(text=f"{val}°C to °F")
            self.display.insert(0, f"{(val * 9/5) + 32:.2f}")
        elif formula == "F_C":
            self.history_label.config(text=f"{val}°F to °C")
            self.display.insert(0, f"{(val - 32) * 5/9:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GoubrohAdvancedCalculator(root)
    root.mainloop()