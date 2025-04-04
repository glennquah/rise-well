import tkinter as tk
from tkinter import ttk
from gui.count_down_window import count_down_window


def shake_it_window(root: tk.Tk, alarm_data, go_back_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Shake Game Configuration")
    root.configure(bg="white")

    if "config" not in alarm_data:
        alarm_data["config"] = {}

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(expand=True)

    title_label = ttk.Label(
        content_frame,
        text="Shake Game Configuration",
        font=("Arial", 36, "bold"),
        background="white",
    )
    title_label.pack(pady=20)

    # Select Difficulty Label (Underlined)
    tk.Label(
        content_frame,
        text="Select Difficulty",
        bg="white",
        font=("Arial", 32, "underline"),  # Underlined header
    ).pack(pady=5)

    difficulty = tk.StringVar(value="Easy")
    difficulty_frame = tk.Frame(content_frame, bg="white")
    difficulty_frame.pack(pady=5)

    for opt in ["Easy", "Medium", "Hard"]:
        ttk.Radiobutton(
            difficulty_frame,
            text=opt,
            variable=difficulty,
            value=opt,
            style="White.TRadiobutton",
        ).pack(side="left", padx=20)

    def next_action():
        if "config" not in alarm_data:
            alarm_data["config"] = {}

        alarm_data["config"]["difficulty"] = difficulty.get()

        count_down_window(root, alarm_data, go_back_callback)

    btn_frame = tk.Frame(content_frame, bg="white")
    btn_frame.pack(pady=20)

    ttk.Button(
        btn_frame,
        text="Back",
        command=go_back_callback,
        style="Big.TButton",
    ).grid(row=0, column=0, padx=20, ipadx=40, ipady=10)

    ttk.Button(
        btn_frame,
        text="Submit Alarm",
        command=next_action,
        style="Big.TButton",
    ).grid(row=0, column=1, padx=20, ipadx=40, ipady=10)

    style = ttk.Style()
    style.configure(
        "Big.TButton",
        font=("Arial", 24),
        padding=15,
    )
    style.configure(
        "White.TRadiobutton",
        font=("Arial", 24),
        background="white",
    )