import tkinter as tk
from tkinter import ttk
from gui.count_down_window import count_down_window

def math_window(root, alarm_data, go_back_callback):
    # Clear the root's current content
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Math Alarm Configuration")
    # Prepare math config in alarm_data
    alarm_data["config"] = {}

    tk.Label(root, text="Select Difficulty", bg="white").pack(pady=5)
    difficulty = tk.StringVar(value="Easy")
    ttk.Radiobutton(root, text="Easy", variable=difficulty, value="Easy", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Medium", variable=difficulty, value="Medium", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Hard", variable=difficulty, value="Hard", style="White.TRadiobutton").pack()

    tk.Label(root, text="Select Operation", bg="white").pack(pady=5)
    operation = tk.StringVar(value="Addition")
    ttk.Radiobutton(root, text="Addition", variable=operation, value="Addition", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Subtraction", variable=operation, value="Subtraction", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Multiplication", variable=operation, value="Multiplication", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Division", variable=operation, value="Division", style="White.TRadiobutton").pack()

    # Number of Questions
    tk.Label(root, text="Number of Questions", bg="white").pack(pady=5)
    num_questions = tk.Spinbox(root, from_=1, to=10, width=5)
    num_questions.pack()

    def next_action():
        alarm_data["config"]["difficulty"] = difficulty.get()
        alarm_data["config"]["operation"] = operation.get()
        alarm_data["config"]["num_questions"] = int(num_questions.get())
        count_down_window(root, alarm_data, go_back_callback)

    ttk.Button(root, text="Submit Alarm", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=go_back_callback).pack(pady=5)