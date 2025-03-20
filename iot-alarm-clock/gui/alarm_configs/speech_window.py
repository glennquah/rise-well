import tkinter as tk
from tkinter import ttk

def speech_window(root, alarm_data, go_back_callback):
    # GLENN, ADD YOUR STUFF HERE
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Alarm Configuration")
    alarm_data["config"] = {}

    tk.Label(root, text="Select Difficulty", bg="white").pack(pady=5)
    difficulty = tk.StringVar(value="Easy")
    ttk.Radiobutton(root, text="Easy", variable=difficulty, value="Easy", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Medium", variable=difficulty, value="Medium", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Hard", variable=difficulty, value="Hard", style="White.TRadiobutton").pack()

    def next_action():
        alarm_data["config"]["difficulty"] = difficulty.get()
        go_back_callback()

    ttk.Button(root, text="Submit Alarm", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=go_back_callback).pack(pady=5)