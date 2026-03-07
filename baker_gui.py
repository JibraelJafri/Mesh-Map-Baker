import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import glob
import baker_core


class AutoBakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Substance 3D Auto-Baker & Packer (Pro)")
        self.root.geometry("680x700")
        self.root.resizable(False, False)

        # Check Executables
        missing_tools = baker_core.check_executables()
        if missing_tools:
            messagebox.showerror("Setup Error", f"Missing Substance Tools:\n{', '.join(missing_tools)}\n\nPlease update paths in baker_core.py")
            self.root.destroy()
            return

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- SECTION 1: PATHS ---
        path_frame = ttk.LabelFrame(main_frame, text=" File Paths ", padding=10)
        path_frame.pack(fill=tk.X, pady=(0, 10))

        # Input Dir
        ttk.Label(path_frame, text="Meshes Folder:").grid(row=0, column=0, sticky="w", pady=2)
        self.var_input_dir = tk.StringVar()
        # Add a trace so that whenever this box changes (pasting, typing, or browsing), it triggers the auto-fill
        self.var_input_dir.trace_add("write", self.on_input_dir_change)

        ttk.Entry(path_frame, textvariable=self.var_input_dir, width=60).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(path_frame, text="Browse", command=lambda: self.browse_folder(self.var_input_dir)).grid(row=0, column=2, pady=2)

        # Output Dir
        ttk.Label(path_frame, text="Output Folder:").grid(row=1, column=0, sticky="w", pady=2)
        self.var_output_dir = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.var_output_dir, width=60).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(path_frame, text="Browse", command=lambda: self.browse_folder(self.var_output_dir)).grid(row=1, column=2, pady=2)

        # SBSAR File (Auto-Detect logic applied here)
        ttk.Label(path_frame, text="Packer SBSAR:").grid(row=2, column=0, sticky="w", pady=2)
        self.var_sbsar = tk.StringVar(value=self.find_default_sbsar())
        ttk.Entry(path_frame, textvariable=self.var_sbsar, width=60).grid(row=2, column=1, padx=5, pady=2)
        ttk.Button(path_frame, text="Browse", command=self.browse_sbsar).grid(row=2, column=2, pady=2)

        # --- SECTION 2: SETTINGS ---
        settings_frame = ttk.LabelFrame(main_frame, text=" Output & Quality Settings ", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        # Row 1: Output Formats
        ttk.Label(settings_frame, text="Resolution:").grid(row=0, column=0, sticky="w", pady=5)
        self.var_res = tk.StringVar(value="2048")
        res_combo = ttk.Combobox(
            settings_frame, textvariable=self.var_res, values=["512", "1024", "2048", "4096", "8192"], width=10, state="readonly"
        )
        res_combo.grid(row=0, column=1, sticky="w", padx=10)

        ttk.Label(settings_frame, text="Image Format:").grid(row=0, column=2, sticky="w", padx=(15, 0))
        self.var_format = tk.StringVar(value="png")
        fmt_combo = ttk.Combobox(
            settings_frame, textvariable=self.var_format, values=["png", "tiff", "exr", "jpeg", "tga"], width=10, state="readonly"
        )
        fmt_combo.grid(row=0, column=3, sticky="w", padx=10)

        

    def browse_folder(self, string_var):
        folder = filedialog.askdirectory()
        if folder:
            string_var.set(folder)

    def browse_sbsar(self):
        file = filedialog.askopenfilename(filetypes=[("Substance Archive", "*.sbsar")])
        if file:
            self.var_sbsar.set(file)

    def on_input_dir_change(self, *args):
        pass

    def find_default_sbsar(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        exact_match = os.path.join(script_dir, "Mesh_Maps_Packer.sbsar")
        if os.path.exists(exact_match):
            return exact_match
        sbsar_files = glob.glob(os.path.join(script_dir, "*.sbsar"))
        if sbsar_files:
            return sbsar_files[0]
        return ""


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoBakerApp(root)
    root.mainloop()
