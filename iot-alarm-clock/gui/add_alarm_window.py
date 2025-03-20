import tkinter as tk
from tkinter import ttk
from gui.alarm_configs.math_window import math_window
from gui.start_window import start_window

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
        ttk.Radiobutton(root, text=opt, variable=alarm_type, value=opt).pack()

    # Next button: When pressed, create a temporary alarm_data and route accordingly
    def next_action():
        alarm_data = {
            "time": time_entry.get(),
            "type": alarm_type.get(),
            "triggered": False
        }
        # Route to the specific config screen
        if alarm_type.get() == "Math":
            math_window(alarm_manager, root, alarm_data, lambda: go_back(alarm_manager, root))
        # else:
        #     show_generic_config(alarm_manager, root, alarm_data, lambda: go_back(root, alarm_manager))

    ttk.Button(root, text="Next", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=lambda: start_window(root, alarm_manager)).pack(pady=5)

def go_back(alarm_manager, root):
    add_alarm_window(alarm_manager, root)