import tkinter as tk
from tkinter import ttk, messagebox
import baker_core


class AutoBakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Substance 3D Auto-Baker & Packer")
        self.root.geometry("680x700")
        self.root.resizable(False, False)

        missing_tools = baker_core.check_executables()
        if missing_tools:
            messagebox.showerror("Setup Error", f"Missing Substance Tools:\n{', '.join(missing_tools)}\n\nPlease update paths in baker_core.py")
            self.root.destroy()
            return


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoBakerApp(root)
    root.mainloop()
