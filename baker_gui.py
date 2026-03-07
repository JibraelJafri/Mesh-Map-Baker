import tkinter as tk
from tkinter import ttk, messagebox


class AutoBakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Substance 3D Auto-Baker & Packer")
        self.root.geometry("680x700")
        self.root.resizable(False, False)


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoBakerApp(root)
    root.mainloop()
