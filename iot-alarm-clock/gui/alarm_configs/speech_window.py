import tkinter as tk
from tkinter import ttk
from gui.count_down_window import count_down_window
import speech_recognition as sr
import re
from difflib import SequenceMatcher
from sensors.audio_sensor import AudioSensor

def speech_window(root, alarm_data, go_back_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Speech Alarm Configuration")
    alarm_data["config"] = {}

    tk.Label(root, text="Select Difficulty", bg="white").pack(pady=5)
    difficulty = tk.StringVar(value="Easy")
    ttk.Radiobutton(root, text="Easy", variable=difficulty, value="Easy", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Medium", variable=difficulty, value="Medium", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Hard", variable=difficulty, value="Hard", style="White.TRadiobutton").pack()
    
    tk.Label(root, text="Number of Words", bg="white").pack(pady=5)
    num_of_words = ttk.Combobox(root, values=[10, 20, 30], state="readonly", width=5)
    num_of_words.set(10)
    num_of_words.pack()

    def next_action():
        alarm_data["config"]["difficulty"] = difficulty.get()
        alarm_data["config"]["num_of_words"] = int(num_of_words.get())
        count_down_window(root, alarm_data, go_back_callback)

    ttk.Button(root, text="Submit Alarm", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=go_back_callback).pack(pady=5)

    # Record Section
    # Transcription label with wraplength set so that long text wraps.
    record_transcription_label = tk.Label(root, text="", bg="white", wraplength=300)
    record_transcription_label.pack(pady=5)

    def record_test():
        record_transcription_label.config(text="Recording for 10 seconds...")
        r = sr.Recognizer()
        # Blocking call: records 10 seconds of audio.
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio_data = r.record(source, duration=10)
        try:
            transcript = r.recognize_google(audio_data)
            record_transcription_label.config(text="Transcribed: " + transcript)
        except sr.UnknownValueError:
            record_transcription_label.config(text="Could not understand audio.")
        except sr.RequestError as e:
            record_transcription_label.config(text=f"Request error: {e}")

    ttk.Button(root, text="Record for 10 seconds", command=record_test).pack(pady=10)