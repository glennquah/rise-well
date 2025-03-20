import tkinter as tk
from tkinter import ttk

def add_alarm_window(alarm_manager):
    win = tk.Toplevel()
    win.title("Add Alarm")
    tk.Label(win, text="Time (HH:MM)").pack()
    time_entry = tk.Entry(win)
    time_entry.pack()
    tk.Label(win, text="Alarm Type").pack()
    alarm_type = tk.StringVar()
    options = ["Math", "Nothing", "Shake It", "Speech", "Image Recognition"]
    alarm_type.set(options[0])
    ttk.OptionMenu(win, alarm_type, options[0], *options, command=lambda v: show_math_options(v, config_frame)).pack()
    config_frame = tk.Frame(win)
    config_frame.pack()
    math_config = {}
    def show_math_options(val, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        if val == "Math":
            tk.Label(frame, text="Difficulty").pack()
            diff = tk.StringVar()
            diff.set("Easy")
            ttk.OptionMenu(frame, diff, "Easy", "Easy", "Medium").pack()
            tk.Label(frame, text="Operation").pack()
            op = tk.StringVar()
            op.set("Addition")
            ttk.OptionMenu(frame, op, "Addition", "Addition", "Subtraction", "Multiplication", "Division").pack()
            tk.Label(frame, text="Number of Questions").pack()
            num_q = tk.Spinbox(frame, from_=1, to=10, width=5)
            num_q.pack()
            math_config["difficulty"] = diff
            math_config["operation"] = op
            math_config["num_questions"] = num_q
    show_math_options(alarm_type.get(), config_frame)
    def submit_alarm():
        alarm = {"time": time_entry.get(), "type": alarm_type.get(), "triggered": False}
        if alarm_type.get() == "Math":
            alarm["config"] = {
                "difficulty": math_config["difficulty"].get(),
                "operation": math_config["operation"].get(),
                "num_questions": int(math_config["num_questions"].get())
            }
        alarm_manager.add_alarm(alarm)
        win.destroy()
    tk.Button(win, text="Submit Alarm", command=submit_alarm).pack()