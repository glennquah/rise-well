import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
import datetime
import re
import threading
import time
from services.sleep_detection.sleep_detection import checks_if_user_is_awake
from difflib import SequenceMatcher
from utils import play_alarm_sound, stop_alarm_sound
from apis.api_client import post_alarm_history
from services.sleep_detection.sleep_detection import checks_if_user_is_awake

def poll_user_awake_status(root, result_label, alarm, go_back_callback):
    countdown_seconds = 15  # Set to 300 for production

    def update_countdown(time_left):
        if time_left > 0:
            result_label.config(
                text=f"⏳ Checking if you're still awake in {time_left} seconds...",
                fg="blue"
            )
            root.update()
            root.after(1000, update_countdown, time_left - 1)
        else:
            check_awake_status()

    def check_awake_status():
        result_label.config(text="Checking if you're awake using AI...", fg="blue")
        root.update()

        if checks_if_user_is_awake():
            result_label.config(text="You're awake! Alarm complete.", fg="green")
            root.update()
            root.after(3000, root.quit)
        else:
            result_label.config(text="Still sleepy... Let's retry!", fg="orange")
            root.update()
            root.after(2000, lambda: trigger(alarm, root, go_back_callback, sentence))

    update_countdown(countdown_seconds)


def clean_sentence(s):
    return re.sub(r"[^\w\s]", "", s).lower().strip()


def calculate_similarity(expected_sentence, user_sentence):
    a = clean_sentence(expected_sentence)
    b = clean_sentence(user_sentence)
    return SequenceMatcher(None, a, b).ratio() * 100


def trigger(alarm, root, go_back_callback, sentence):
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Speech Challenge Alarm")

    # Start playing the alarm sound initially
    sound_obj = play_alarm_sound()

    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")
    num_of_words = int(config.get("num_of_words", 10))

    attempts = 0
    final_passed = False
    start_time = datetime.datetime.now()

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(expand=True)

    tk.Label(
        content_frame,
        text="Repeat the sentence below:",
        font=("Arial", 36, "underline"),
        bg="white",
    ).pack(pady=10)

    sentence_label = tk.Label(
        content_frame,
        text=sentence["sentence"],
        wraplength=1000,
        font=("Arial", 42),
        bg="white",
        justify="center",
    )
    sentence_label.pack(pady=20)

    result_label = tk.Label(
        content_frame,
        text="",
        font=("Arial", 24),
        bg="white",
    )
    result_label.pack(pady=10)

    score_label = tk.Label(
        content_frame,
        text="Attempts: 0 | Score: 0%",
        font=("Arial", 24),
        bg="white",
    )
    score_label.pack(pady=10)

    transcript_label = tk.Label(
        content_frame,
        text="",
        bg="white",
        font=("Arial", 24),
        wraplength=800,
    )
    transcript_label.pack(pady=10)

    btn_frame = tk.Frame(content_frame, bg="white")
    btn_frame.pack(pady=20)

    record_btn = ttk.Button(
        btn_frame,
        text="Start Recording (10s)",
        style="Big.TButton",
    )
    record_btn.grid(row=0, column=0, padx=20, ipadx=40, ipady=10)

    finish_btn = ttk.Button(
        btn_frame,
        text="Finish",
        style="Big.TButton",
        state="disabled",
    )
    finish_btn.grid(row=0, column=1, padx=20, ipadx=40, ipady=10)

    def record_10_seconds():
        """Record audio for 10 seconds and process the result."""
        nonlocal attempts, final_passed, sound_obj

        # Stop the alarm temporarily while recording
        stop_alarm_sound()

        record_btn.config(state="disabled")
        transcript_label.config(text="Recording for 10 seconds...")

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio_data = r.record(source, duration=10)

        try:
            transcript = r.recognize_google(audio_data)
        except sr.UnknownValueError:
            transcript = "Could not understand audio."
        except sr.RequestError as e:
            transcript = f"Request error: {e}"

        transcript_label.config(text="You said: " + transcript)
        attempts += 1
        sim = calculate_similarity(sentence["sentence"], transcript)

        if sim >= 80:
            result_label.config(
                text=f"✅ {sim:.1f}% matched — Correct!",
                fg="green",
                bg="white",
            )
            score_label.config(text=f"Attempts: {attempts} | Score: 100%")
            final_passed = True
            finish_btn.config(state="normal")
            record_btn.config(state="disabled")
            stop_alarm_sound()
        else:
            result_label.config(
                text=f"❌ {sim:.1f}% matched — Try again.",
                fg="red",
                bg="white",
            )
            score_label.config(text=f"Attempts: {attempts} | Score: 0%")

            # Re-trigger the alarm if the user fails
            if not final_passed:
                sound_obj = play_alarm_sound()
                record_btn.config(state="normal")

    record_btn.config(command=record_10_seconds)

    def finish_challenge():
        """Finish the speech challenge and send data to API."""
        end_time = datetime.datetime.now()
        time_taken = str(end_time - start_time).split(".")[0]
        stop_alarm_sound()
        record_btn.grid_forget()
        finish_btn.grid_forget()
        result_label.config(text="✅ Challenge Passed!", fg="green", bg="white")

        tk.Label(
            root,
            text=f"Time taken: {time_taken}",
            bg="white",
            font=("Arial", 24),
        ).pack(pady=10)

        payload = {
            "userId": alarm.get("userId"),
            "alarmType": "Speech",
            "alarmTime": start_time.isoformat(),
            "resolvedTime": end_time.isoformat(),
            "attempts": attempts,
            "difficulty": difficulty,
            "numberOfWords": num_of_words,
            "givenWords": sentence["sentence"],
        }
        post_alarm_history(payload)


        def start_awake_check():
            result_label.config(text="Now checking if you're awake...", fg="green")
            root.update()
            poll_user_awake_status(root, result_label, alarm, go_back_callback)

        root.after(2000, start_awake_check)

    finish_btn.config(command=finish_challenge)

    style = ttk.Style()
    style.configure(
        "Big.TButton",
        font=("Arial", 28),
        padding=15,
    )