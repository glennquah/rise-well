import tkinter as tk
from tkinter import ttk
from gui.alarm_configs.math_window import math_window
from gui.alarm_configs.speech_window import speech_window
from gui.alarm_configs.image_recognition_window import image_recognition_window
from gui.count_down_window import count_down_window
from gui.alarm_configs.shake_it_window import shake_it_window
from utils import play_alarm_sound
from utils import stop_alarm_sound




def add_alarm_window(root: tk.Tk, userId):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Add Alarm")
    root.configure(bg="white")

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    title_label = ttk.Label(
        main_frame,
        text="Add New Alarm",
        font=("Arial", 36, "bold"),
        background="white",
    )
    title_label.pack(pady=10)

    tk.Label(
        main_frame,
        text="Time (HH:MM)",
        bg="white",
        font=("Arial", 24),
    ).pack(pady=5)

    time_var = tk.StringVar()
    time_entry = tk.Entry(
        main_frame,
        textvariable=time_var,
        font=("Arial", 20),
        width=20,
        justify="center",
    )
    time_entry.pack(pady=5)

    alarm_type = tk.StringVar(value="Image Recognition")
    num_pad_frame = tk.Frame(main_frame, bg="white")
    num_pad_frame.pack(pady=5)

    def insert_number(num):
        current_value = time_var.get()
        if len(current_value) == 5:
            return
        elif len(current_value) == 2:
            time_var.set(f"{current_value}:{num}")
        elif len(current_value) == 4:
            time_var.set(current_value + num)
        else:
            time_var.set(current_value + num)

    def clear_time():
        time_var.set("")

    btn_texts = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["0", "⌫", "Clear"],
    ]

    for r, row in enumerate(btn_texts):
        for c, text in enumerate(row):
            if text == "⌫":
                btn = ttk.Button(
                    num_pad_frame,
                    text=text,
                    command=lambda: time_var.set(time_var.get()[:-1]),
                    style="Small.TButton",
                )
            elif text == "Clear":
                btn = ttk.Button(
                    num_pad_frame,
                    text=text,
                    command=clear_time,
                    style="Small.TButton",
                )
            else:
                btn = ttk.Button(
                    num_pad_frame,
                    text=text,
                    command=lambda t=text: insert_number(t),
                    style="Small.TButton",
                )
            btn.grid(row=r, column=c, padx=3, pady=3, ipadx=10, ipady=5)

    tk.Label(
        main_frame,
        text="Select Alarm Type",
        bg="white",
        font=("Arial", 28, "bold"),
    ).pack(pady=10)

    alarm_type = tk.StringVar(value="Math")
    options = ["Math", "Nothing", "Shake It", "Speech", "Image Recognition"]

    radio_frame = tk.Frame(main_frame, bg="white")
    radio_frame.pack(pady=5)

    for i, opt in enumerate(options):
        ttk.Radiobutton(
            radio_frame,
            text=opt,
            variable=alarm_type,
            value=opt,
            style="White.TRadiobutton",
        ).grid(row=i // 3, column=i % 3, padx=10, pady=5, sticky="w")

    btn_frame_1 = tk.Frame(main_frame, bg="white")
    btn_frame_1.pack(pady=15)

    ttk.Button(
        btn_frame_1,
        text="Play Alarm Ring Tone",
        command=play_alarm_sound,
        style="Big.TButton",
    ).grid(row=0, column=0, padx=10, ipadx=30, ipady=10)

    ttk.Button(
        btn_frame_1,
        text="Stop Alarm Ring Tone",
        command=stop_alarm_sound,
        style="Big.TButton",
    ).grid(row=0, column=1, padx=10, ipadx=30, ipady=10)

    def go_back():
        add_alarm_window(root, userId)

    def next_action():
        alarm_data = {
            "userId": userId,
            "time": time_var.get(),
            "type": alarm_type.get(),
            "triggered": False,
        }
        if alarm_type.get() == "Math":
            math_window(root, alarm_data, go_back)
        elif alarm_type.get() == "Shake It":
            shake_it_window(root, alarm_data, go_back)
        elif alarm_type.get() == "Speech":
            speech_window(root, alarm_data, go_back)
        elif alarm_type.get() == "Image Recognition":
            image_recognition_window(root, alarm_data, lambda: go_back(root, userId))
        elif alarm_type.get() == "Nothing":
            count_down_window(root, alarm_data, go_back)
        else:
            count_down_window(root, alarm_data, go_back)

    btn_frame_2 = tk.Frame(main_frame, bg="white")
    btn_frame_2.pack(pady=20)

    ttk.Button(
        btn_frame_2,
        text="Back",
        command=lambda: _go_to_start(root),
        style="Big.TButton",
    ).grid(row=0, column=0, padx=10, ipadx=30, ipady=10, sticky="w")

    ttk.Button(
        btn_frame_2,
        text="Next",
        command=next_action,
        style="Big.TButton",
    ).grid(row=0, column=1, padx=10, ipadx=30, ipady=10, sticky="e")

    style = ttk.Style()
    style.configure(
        "Big.TButton",
        font=("Arial", 24),
        padding=10,
    )

    style.configure(
        "Small.TButton",
        font=("Arial", 18),
        padding=5,
    )

    style.configure(
        "White.TRadiobutton",
        font=("Arial", 24),
        background="white",
    )


def _go_to_start(root):
    from gui.start_window import start_window

    start_window(root)
