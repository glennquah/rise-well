import tkinter as tk
from tkinter import ttk
import datetime
import alarm.math_alarm as math_alarm
from alarm.image_recognition_alarm import trigger as image_trigger
from apis.api_client import post_alarm_history
import time
import alarm.speech_alarm as speech_alarm
from apis.api_client import post_speech_sentences
import alarm.shake_it_alarm as shake_it_alarm 
import alarm.speech_alarm as speech_alarm
from apis.api_client import post_alarm_history, post_speech_sentences
import alarm.shake_it_alarm as shake_it_alarm
from utils import play_alarm_sound, stop_alarm_sound



def count_down_window(root, alarm_data, go_back_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Countdown to Alarm")
    root.configure(bg="white")

    now = datetime.datetime.now()
    try:
        alarm_time = datetime.datetime.strptime(alarm_data["time"], "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if alarm_time < now:
            alarm_time += datetime.timedelta(days=1)
    except Exception as e:
        print("Time parsing error:", e)
        alarm_time = now

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(expand=True)

    countdown_label = ttk.Label(
        content_frame,
        text="",
        font=("Arial", 300, "bold"),
        background="white",
    )
    countdown_label.pack(pady=50)

    back_button = ttk.Button(
        content_frame,
        text="Back",
        command=lambda: stop_and_go_back(),
        style="Big.TButton",
    )
    back_button.pack(pady=20)

    def stop_and_go_back():
        """Stop alarm and return to previous page."""
        stop_alarm_sound()
        go_back_callback()

    def trigger_alarm():
        """Trigger the alarm and call the API when the countdown ends."""
        play_alarm_sound()
        time_now = datetime.datetime.now()

        payload = {
            "userId": alarm_data.get("userId"),
            "alarmType": alarm_data.get("type"),
            "alarmTime": time_now.isoformat(),
            "resolvedTime": time_now.isoformat(),
        }
        post_alarm_history(payload)

        # Route to the corresponding alarm type after triggering
        if alarm_data["type"] == "Math":
            math_alarm.trigger(alarm_data, root, go_back_callback)
        elif alarm_data["type"] == "Shake It":
            shake_it_alarm.trigger(alarm_data, root, go_back_callback)
        elif alarm_data["type"] == "Nothing":
            post_alarm_history(payload)
        elif alarm_data["type"] == "Speech":
            config = alarm_data.get("config", {})
            payload = {
                "difficulty": config.get("difficulty"),
                "numberOfWords": config.get("num_of_words"),
            }
            sentence = post_speech_sentences(payload)
            speech_alarm.trigger(alarm_data, root, go_back_callback, sentence)

    def update_countdown():
        """Update the countdown every second."""
        now = datetime.datetime.now()
        diff = alarm_time - now
        seconds_left = diff.total_seconds()
        if seconds_left > 0:
            countdown_label.config(text=str(diff).split(".")[0])
            root.after(1000, update_countdown)
        else:
            countdown_label.config(text="Time's up!", font=("Arial", 24, "bold"), background="white")

            if not alarm_data.get("triggered"):
                alarm_data["triggered"] = True
                
            if alarm_data["type"] == "Math":
                math_alarm.trigger(alarm_data, root, go_back_callback)

            elif alarm_data["type"] == "Image Recognition":
                image_trigger(alarm_data, root, go_back_callback)

            elif alarm_data["type"] == "Nothing":
                payload = {
                    "userId": alarm_data.get("userId"),
                    "alarmType": "Nothing",
                    "alarmTime": start_time.isoformat(),
                    "resolvedTime": end_time.isoformat(),
                }
                back_button.destroy()
                if alarm_data["type"] == "Math":
                    math_alarm.trigger(alarm_data, root, go_back_callback)
                elif alarm_data["type"] == "Shake It":
                    shake_it_alarm.trigger(alarm_data,root,go_back_callback)
                elif alarm_data["type"] == "Nothing":
                    time_now = datetime.datetime.now()
                    payload = {
                        "userId": alarm_data.get("userId"),
                        "alarmType": "Nothing",
                        "alarmTime": time_now.isoformat(),
                        "resolvedTime": time_now.isoformat(),
                    }
                    post_alarm_history(payload)
                elif alarm_data["type"] == "Speech":
                    config = alarm_data.get("config", {})
                    payload = {
                        "difficulty": config.get("difficulty"),
                        "numberOfWords": config.get("num_of_words"),
                    }
                    sentence = post_speech_sentences(payload)
            
            countdown_label.config(
                text="Rise and Shine!",
                font=("Arial", 140, "bold"),
                background="white",
            )
            if not alarm_data.get("triggered"):
                alarm_data["triggered"] = True
                trigger_alarm()

    update_countdown()

    style = ttk.Style()
    style.configure(
        "Big.TButton",
        font=("Arial", 32),
        padding=15,
    )