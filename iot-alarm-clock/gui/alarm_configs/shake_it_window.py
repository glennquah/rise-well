import tkinter as tk
from tkinter import ttk
from gui.count_down_window import count_down_window

def shake_it_window(root: tk.Tk, alarm_data, go_back_callback):
    """GUI for selecting shake difficulty"""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Shake Game Configuration")
    alarm_data["config"] = {}

    tk.Label(root, text="Select Difficulty", bg="white").pack(pady=5)
    difficulty = tk.StringVar(value="Easy") 
    
    ttk.Radiobutton(root, text="Easy", variable=difficulty, value="Easy", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Medium", variable=difficulty, value="Medium", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Hard", variable=difficulty, value="Hard", style="White.TRadiobutton").pack()

    def next_action():
        alarm_data["config"]["difficulty"] = difficulty.get()
        count_down_window(root,alarm_data, go_back_callback)

    ttk.Button(root, text="Submit Alarm", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=go_back_callback).pack(pady=5)
