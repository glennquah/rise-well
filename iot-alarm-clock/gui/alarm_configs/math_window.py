import tkinter as tk
from tkinter import ttk
from gui.count_down_window import count_down_window


def math_window(root, alarm_data, go_back_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Math Alarm Configuration")
    root.configure(bg="white")

    if "config" not in alarm_data:
        alarm_data["config"] = {}

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(expand=True)

    title_label = ttk.Label(
        content_frame,
        text="Math Alarm Configuration",
        font=("Arial", 36, "bold"),
        background="white",
    )
    title_label.pack(pady=20)

    tk.Label(
        content_frame,
        text="Select Difficulty",
        bg="white",
        font=("Arial", 32, "underline"),
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

    tk.Label(
        content_frame,
        text="Select Operation",
        bg="white",
        font=("Arial", 32, "underline"),
    ).pack(pady=10)

    operation = tk.StringVar(value="Addition")
    operation_frame = tk.Frame(content_frame, bg="white")
    operation_frame.pack(pady=5)

    for opt in ["Addition", "Subtraction", "Multiplication", "Division"]:
        ttk.Radiobutton(
            operation_frame,
            text=opt,
            variable=operation,
            value=opt,
            style="White.TRadiobutton",
        ).pack(side="left", padx=10)

    tk.Label(
        content_frame,
        text="Number of Questions",
        bg="white",
        font=("Arial", 32, "underline"),
    ).pack(pady=10)

    num_questions_var = tk.IntVar(value=5)
    num_questions = tk.Spinbox(
        content_frame,
        from_=1,
        to=10,
        width=5,
        font=("Arial", 28),
        textvariable=num_questions_var,
        justify="center",
    )
    num_questions.pack(pady=5)

    def next_action():
        alarm_data["config"]["difficulty"] = difficulty.get()
        alarm_data["config"]["operation"] = operation.get()
        alarm_data["config"]["num_questions"] = int(num_questions.get())

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
        font=("Arial", 28),
        background="white",
    )