import tkinter as tk
import datetime
import speech_recognition as sr
import re
from difflib import SequenceMatcher
import threading

from utils import play_alarm_sound, stop_alarm_sound
from apis.api_client import post_alarm_history
from sensors.audio_sensor import AudioSensor

def clean_sentence(s):
    return re.sub(r'[^\w\s]', '', s).lower().strip()

def calculate_similarity(expected_sentence, user_sentence):
    a = clean_sentence(expected_sentence)
    b = clean_sentence(user_sentence)
    return SequenceMatcher(None, a, b).ratio() * 100

def trigger(alarm, root, go_back_callback, sentence):
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Speech Challenge Alarm")
    sound_obj = play_alarm_sound()

    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")
    num_of_words = int(config.get("num_of_words", 10))

    attempts = 0
    final_passed = False

    start_time = datetime.datetime.now()

    tk.Label(root, text="Repeat the sentence below:", font=("Arial", 14), bg="white").pack(pady=5)
    sentence_label = tk.Label(root, text=sentence["sentence"], wraplength=400, font=("Arial", 16), bg="white", justify="center")
    sentence_label.pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=5)

    score_label = tk.Label(root, text="Attempts: 0 | Score: 0%", font=("Arial", 12), bg="white")
    score_label.pack(pady=5)

    transcript_label = tk.Label(root, text="", font=("Arial", 12), bg="white", wraplength=400)
    transcript_label.pack(pady=5)

    finish_btn = tk.Button(root, text="Finish", bg="white", state="disabled")
    finish_btn.pack_forget()

    # Recording section using a single button to record for 15 seconds.
    record_btn = tk.Button(root, text="Record for 15 seconds", bg="white")
    record_btn.pack(pady=10)

    def record_15_seconds():
        nonlocal attempts, final_passed, sound_obj
        # Disable the record button to prevent multiple presses.
        record_btn.config(state="disabled")
        transcript_label.config(text="Recording for 15 seconds...")
        stop_alarm_sound()  # Stop any alarm sound while recording

        def record_thread():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                # Record for 15 seconds (blocking call).
                audio_data = r.record(source, duration=15)
            try:
                transcript = r.recognize_google(audio_data)
            except sr.UnknownValueError:
                transcript = "Could not understand audio."
            except sr.RequestError as e:
                transcript = f"Request error: {e}"
            def update_ui():
                nonlocal attempts, final_passed, sound_obj
                transcript_label.config(text="You said: " + transcript)
                attempts += 1
                sim = calculate_similarity(sentence["sentence"], transcript)
                if sim >= 80:
                    result_label.config(text=f"✅ {sim:.1f}% matched — Correct!", fg="green")
                    score_label.config(text=f"Attempts: {attempts} | Score: 100%")
                    final_passed = True
                    finish_btn.config(state="normal")
                else:
                    result_label.config(text=f"❌ {sim:.1f}% matched — Try again.", fg="red")
                    score_label.config(text=f"Attempts: {attempts} | Score: 0%")
                    record_btn.config(state="normal")
            root.after(0, update_ui)

        threading.Thread(target=record_thread, daemon=True).start()

    record_btn.config(command=record_15_seconds)

    def finish_challenge():
        end_time = datetime.datetime.now()
        time_taken = end_time - start_time
        stop_alarm_sound()
        record_btn.pack_forget()
        finish_btn.pack_forget()
        result_label.config(text="✅ Challenge Passed!", fg="green")
        tk.Label(root, text=f"Time taken: {str(time_taken).split('.')[0]}", bg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(root, text="Back", command=go_back_callback, bg="white").pack(pady=10)
        
        payload = {
            "userId": alarm.get("userId"),
            "alarmType": "Speech",
            "alarmTime": start_time.isoformat(),
            "resolvedTime": end_time.isoformat(),
            "difficulty": difficulty,
            "numOfWords": num_of_words,
            "givenWords": sentence["sentence"],
        }
        post_alarm_history(payload)

    finish_btn.config(command=finish_challenge)
    record_btn.pack(pady=10)
    finish_btn.pack(pady=10)