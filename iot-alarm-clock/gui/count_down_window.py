import tkinter as tk
from tkinter import ttk
import datetime
import alarm.math_alarm as math_alarm
import alarm.speech_alarm as speech_alarm
from apis.api_client import post_alarm_history
from apis.api_client import post_speech_sentences
import alarm.shake_it_alarm as shake_it_alarm 
from utils import stop_alarm_sound
import serial
import threading

ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)

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

    back_button = ttk.Button(root, text="Back", command=go_back_callback)
    back_button.pack(pady=10)

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
                    speech_alarm.trigger(alarm_data, root, go_back_callback, sentence)

    def listen_for_stop_alarm():
        while True:
            if ser.in_waiting > 0: 
                message = ser.readline().decode('utf-8').strip()
                if message == "stop": 
                    stop_alarm_sound()
                    ser.write(b"reset\n")
                    ttk.Button(root, text="Exit", command=go_back_callback).pack(pady=10)

    listener_thread = threading.Thread(target=listen_for_stop_alarm)
    listener_thread.daemon = True  
    listener_thread.start()
            

    update_countdown()