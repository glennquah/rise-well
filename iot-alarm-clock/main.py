import tkinter as tk
from tkinter import ttk
from gui.start_window import start_window


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("White.TRadiobutton", background="white", foreground="black")
    rb = ttk.Radiobutton(root, text="Option", variable=tk.StringVar(), value="1", style="White.TRadiobutton")
    start_window(root)
    root.mainloop()
