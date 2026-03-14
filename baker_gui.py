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

        # Selected Meshes (Now handles specific files)
        ttk.Label(path_frame, text="Selected Meshes:").grid(row=0, column=0, sticky="w", pady=2)
        self.var_input_files = tk.StringVar()
        self.var_input_files.trace_add("write", self.on_input_files_change)

        ttk.Entry(path_frame, textvariable=self.var_input_files, width=60).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(path_frame, text="Browse", command=self.browse_files).grid(row=0, column=2, pady=2)

        # Output Dir
        ttk.Label(path_frame, text="Output Folder:").grid(row=1, column=0, sticky="w", pady=2)
        self.var_output_dir = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.var_output_dir, width=60).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(path_frame, text="Browse", command=self.browse_output_folder).grid(row=1, column=2, pady=2)

        # SBSAR File (Auto-Detect logic)
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

        # Row 2: Baking Quality
        ttk.Label(settings_frame, text="Antialiasing:").grid(row=1, column=0, sticky="w", pady=5)
        self.var_aa = tk.StringVar(value="2x2")
        aa_combo = ttk.Combobox(settings_frame, textvariable=self.var_aa, values=["1x1", "2x2", "4x4", "8x8"], width=10, state="readonly")
        aa_combo.grid(row=1, column=1, sticky="w", padx=10)

        ttk.Label(settings_frame, text="Ray Count:").grid(row=1, column=2, sticky="w", padx=(15, 0))
        self.var_rays = tk.StringVar(value="256")
        rays_combo = ttk.Combobox(settings_frame, textvariable=self.var_rays, values=["16", "32", "64", "128", "256"], width=10, state="readonly")
        rays_combo.grid(row=1, column=3, sticky="w", padx=10)

        # Row 3: Housekeeping
        self.var_cleanup = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Clean up intermediate maps (Housekeeping)", variable=self.var_cleanup).grid(
            row=2, column=0, columnspan=4, sticky="w", pady=(10, 0)
        )

        # --- SECTION 3: LOG & PROGRESS ---
        log_frame = ttk.LabelFrame(main_frame, text=" Console Log ", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.txt_log = scrolledtext.ScrolledText(
            log_frame, wrap=tk.WORD, width=40, height=10, state=tk.DISABLED, bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 9)
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))

        # --- CONTROLS ---
        self.btn_start = ttk.Button(main_frame, text="START PIPELINE", command=self.start_pipeline)
        self.btn_start.pack(fill=tk.X, ipady=5)

    def on_input_files_change(self, *args):
        """Automatically fills the output directory based on the location of the first selected mesh."""
        in_str = self.var_input_files.get().strip()
        if in_str:
            # Grab the first path from the semicolon separated list
            first_path = in_str.split(";")[0].strip(" \"'")

            # If it's a valid path, extract its folder
            if first_path and os.path.exists(first_path):
                # If they pasted a folder, use it. If they pasted a file, get the parent folder.
                target_dir = first_path if os.path.isdir(first_path) else os.path.dirname(first_path)
                target_dir = target_dir.replace("\\", "/")

                auto_out = f"{target_dir}/Mesh_Maps"

                # Only overwrite the output box if it's currently empty or already auto-filled
                current_out = self.var_output_dir.get().strip()
                if not current_out or current_out.endswith("Mesh_Maps"):
                    self.var_output_dir.set(auto_out)

    def find_default_sbsar(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        exact_match = os.path.join(script_dir, "Mesh_Maps_Packer.sbsar")
        if os.path.exists(exact_match):
            return exact_match

        sbsar_files = glob.glob(os.path.join(script_dir, "*.sbsar"))
        return sbsar_files[0] if sbsar_files else ""

    def browse_files(self):
        """Allows user to multi-select specific mesh files."""
        files = filedialog.askopenfilenames(
            title="Select Meshes", filetypes=[("3D Meshes", "*.fbx *.obj *.usd *.usda *.usdc *.glb *.gltf"), ("All Files", "*.*")]
        )
        if files:
            # Join the tuple with semicolons so it looks clean in the text box
            self.var_input_files.set("; ".join(files))

    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.var_output_dir.set(folder)

    def browse_sbsar(self):
        file = filedialog.askopenfilename(filetypes=[("Substance Archive", "*.sbsar")])
        if file:
            self.var_sbsar.set(file)

    def log(self, message):
        self.root.after(0, self._log_insert, message)

    def _log_insert(self, message):
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    def update_progress(self, current, total):
        percentage = (current / total) * 100 if total > 0 else 0
        self.root.after(0, self.progress_var.set, percentage)

    def start_pipeline(self):
        in_str = self.var_input_files.get().strip()
        out_dir = self.var_output_dir.get().strip(" \"'")
        sbsar = self.var_sbsar.get().strip(" \"'")

        if not in_str:
            messagebox.showwarning("Missing Data", "Please select at least one mesh or folder.")
            return
        if not sbsar or not os.path.exists(sbsar):
            messagebox.showwarning("Missing Data", "Please select a valid SBSAR packer file.")
            return

        # Smart Input Parser: Handles specific files AND entire directories seamlessly
        raw_paths = [p.strip(" \"'") for p in in_str.split(";") if p.strip(" \"'")]
        final_files = []
        supported = (".fbx", ".obj", ".usd", ".usda", ".usdc", ".glb", ".gltf")

        for p in raw_paths:
            if os.path.isfile(p) and p.lower().endswith(supported):
                final_files.append(p)
            elif os.path.isdir(p):
                # If they dragged a whole folder, unpack it for them
                for f in os.listdir(p):
                    if f.lower().endswith(supported):
                        final_files.append(os.path.join(p, f))

        if not final_files:
            messagebox.showwarning("No Meshes Found", "Could not find any valid 3D files in the input box.")
            return

        # Lock UI
        self.btn_start.config(state=tk.DISABLED, text="PROCESSING...")
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.delete(1.0, tk.END)
        self.txt_log.config(state=tk.DISABLED)
        self.progress_var.set(0)

        # Gather arguments
        kwargs = {
            "input_files": final_files,
            "output_dir": out_dir,
            "sbsar_path": sbsar,
            "resolution": int(self.var_res.get()),
            "out_format": self.var_format.get(),
            "sampling_rate": self.var_aa.get(),
            "ray_count": self.var_rays.get(),
            "cleanup_temps": self.var_cleanup.get(),
            "log_callback": self.log,
            "progress_callback": self.update_progress,
        }

        # Run backend in a separate thread so GUI doesn't freeze
        thread = threading.Thread(target=self._run_backend_thread, kwargs=kwargs, daemon=True)
        thread.start()

    def _run_backend_thread(self, **kwargs):
        try:
            baker_core.run_pipeline(**kwargs)
        except Exception as e:
            self.log(f"\n[FATAL ERROR] {str(e)}")
        finally:
            self.root.after(0, self._reset_ui)

    def _reset_ui(self):
        self.btn_start.config(state=tk.NORMAL, text="START PIPELINE")


if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.tk.call("sv_ttk", "set_theme", "dark")
    except:
        pass

    app = AutoBakerApp(root)
    root.mainloop()
