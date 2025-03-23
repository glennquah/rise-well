import tkinter as tk
from tkinter import ttk
from gui.alarm_configs.math_window import math_window
from gui.alarm_configs.shake_it_window import shake_it_window
from gui.alarm_configs.speech_window import speech_window
from gui.alarm_configs.image_recognition_window import image_recognition_window
from gui.count_down_window import count_down_window
from utils import play_alarm_sound 
from utils import stop_alarm_sound 

def add_alarm_window(root, userId):
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title("Add Alarm")

    tk.Label(root, text="Time (HH:MM)", bg="white").pack(pady=5)
    time_entry = tk.Entry(root)
    time_entry.pack(pady=5)

    tk.Label(root, text="Select Alarm Type", bg="white").pack(pady=5)
    alarm_type = tk.StringVar(value="Math")
    options = ["Math", "Nothing", "Shake It", "Speech", "Image Recognition"]
    for opt in options:
        ttk.Radiobutton(root, text=opt, variable=alarm_type, value=opt, style="White.TRadiobutton").pack()

    ttk.Button(root, text="Play Alarm Ring Tone", command=play_alarm_sound).pack(pady=5)
    ttk.Button(root, text="Stop Alarm Ring Tone", command=stop_alarm_sound).pack(pady=5)

    def next_action():
        alarm_data = {
            "userId": userId,
            "time": time_entry.get(),
            "type": alarm_type.get(),
            "triggered": False
        }
        # Route to the specific config screen based on alarm type
        if alarm_type.get() == "Math":
            math_window(root, alarm_data, lambda: go_back(root))
        elif alarm_type.get() == "Shake It":
            shake_it_window(root, alarm_data, lambda: go_back(root))
        elif alarm_type.get() == "Speech":
            speech_window(root, alarm_data, lambda: go_back(root))
        elif alarm_type.get() == "Image Recognition":
            image_recognition_window(root, alarm_data, lambda: go_back(root))
        elif alarm_type.get() == "Nothing":
            count_down_window(root, alarm_data, lambda: go_back(root))
        else:
            count_down_window(root, alarm_data, lambda: go_back(root))

    ttk.Button(root, text="Next", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=lambda: _go_to_start(root)).pack(pady=5)

def _go_to_start(root):
    from gui.start_window import start_window
    start_window(root)

def go_back(root):
    add_alarm_window(root, alarm_data.get("userId"))