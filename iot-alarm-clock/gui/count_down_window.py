import tkinter as tk
from tkinter import ttk
import datetime
import alarm.math_alarm as math_alarm
import alarm.shake_it_alarm as shake_it_alarm 

def count_down_window(root, alarm_data, go_back_callback):
    # Clear current widgets on the root
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Countdown to Alarm")

    # Parse the alarm time (assumed format "HH:MM")
    now = datetime.datetime.now()
    try:
        alarm_time = datetime.datetime.strptime(alarm_data["time"], "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if alarm_time < now:
            # If the time has passed today, set for tomorrow
            alarm_time += datetime.timedelta(days=1)
    except Exception as e:
        # On parsing error, default to now (no countdown)
        print("Time parsing error:", e)
        alarm_time = now

    # Create a label to show the countdown
    countdown_label = ttk.Label(root, text="", font=("Arial", 64), background="white")
    countdown_label.pack(pady=20)

    def update_countdown():
        now = datetime.datetime.now()
        diff = alarm_time - now
        seconds_left = diff.total_seconds()
        if seconds_left > 0:
            # Format the time difference as HH:MM:SS
            countdown_label.config(text=str(diff).split('.')[0])
            root.after(1000, update_countdown)
        else:
            countdown_label.config(text="Time's up!", font=("Arial", 24, "bold"), background="white")
            if not alarm_data.get("triggered"):
                alarm_data["triggered"] = True
                if alarm_data["type"] == "Math":
                    math_alarm.trigger(alarm_data, root, go_back_callback)
                elif alarm_data["type"] == "Shake It":
                    shake_it_alarm.trigger(alarm_data,root,go_back_callback)
                elif alarm_data["type"] == "Nothing":
                    payload = {
                        "userId": alarm.get("userId"),
                        "alarmType": "Nothing",
                        "alarmTime": start_time.isoformat(),
                        "resolvedTime": end_time.isoformat(),
                    }
                    post_alarm_history(payload)
            

    update_countdown()

    # Back Button to return to the add alarm screen
    ttk.Button(root, text="Back", command=go_back_callback).pack(pady=10)