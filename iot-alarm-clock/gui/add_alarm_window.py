import tkinter as tk
from tkinter import ttk
from gui.alarm_configs.math_window import math_window
from gui.alarm_configs.shake_it_window import shake_it_window
from gui.alarm_configs.speech_window import speech_window
from gui.alarm_configs.image_recognition_window import image_recognition_window
from gui.count_down_window import count_down_window
# Do NOT import start_window at the top!

def add_alarm_window(alarm_manager, root):
    # Clear current widgets on root (we’re reusing the same window)
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title("Add Alarm")

    # Time Entry
    tk.Label(root, text="Time (HH:MM)", bg="white").pack(pady=5)
    time_entry = tk.Entry(root)
    time_entry.pack(pady=5)

    # Alarm type selection using radio buttons
    tk.Label(root, text="Select Alarm Type", bg="white").pack(pady=5)
    alarm_type = tk.StringVar(value="Math")
    options = ["Math", "Nothing", "Shake It", "Speech", "Image Recognition"]
    for opt in options:
        ttk.Radiobutton(root, text=opt, variable=alarm_type, value=opt, style="White.TRadiobutton").pack()

    # Next button: When pressed, create a temporary alarm_data and route accordingly
    def next_action():
        alarm_data = {
            "time": time_entry.get(),
            "type": alarm_type.get(),
            "triggered": False
        }
        # Route to the specific config screen based on alarm type
        if alarm_type.get() == "Math":
            math_window(alarm_manager, root, alarm_data, lambda: go_back(alarm_manager, root))
        elif alarm_type.get() == "Shake It":
            shake_it_window(alarm_manager, root, alarm_data, lambda: go_back(alarm_manager, root))
        elif alarm_type.get() == "Speech":
            speech_window(alarm_manager, root, alarm_data, lambda: go_back(alarm_manager, root))
        elif alarm_type.get() == "Image Recognition":
            image_recognition_window(alarm_manager, root, alarm_data, lambda: go_back(alarm_manager, root))
        else:
            count_down_window(alarm_manager, root, alarm_data, lambda: go_back(alarm_manager, root))

    ttk.Button(root, text="Next", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=lambda: _go_to_start(root, alarm_manager)).pack(pady=5)

def _go_to_start(root, alarm_manager):
    # Local import to break the circular dependency.
    from gui.start_window import start_window
    start_window(root, alarm_manager)

def go_back(alarm_manager, root):
    add_alarm_window(alarm_manager, root)