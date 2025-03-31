import speech_recognition as sr
import tkinter as tk
from tkinter import ttk
from gui.count_down_window import count_down_window


def speech_window(root, alarm_data, go_back_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Speech Alarm Configuration")
    root.configure(bg="white")

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(expand=True)

    title_label = ttk.Label(
        content_frame,
        text="Speech Alarm Configuration",
        font=("Arial", 36, "bold"),
        background="white",
    )
    title_label.pack(pady=20)

    tk.Label(
        content_frame,
        text="Select Difficulty",
        bg="white",
        font=("Arial", 32, "underline"),
    ).pack(pady=5)

    difficulty = tk.StringVar(value="Easy")
    difficulty_frame = tk.Frame(content_frame, bg="white")
    difficulty_frame.pack(pady=5)

    for opt in ["Easy", "Medium", "Hard"]:
        ttk.Radiobutton(
            difficulty_frame,
            text=opt,
            variable=difficulty,
            value=opt,
            style="White.TRadiobutton",
        ).pack(side="left", padx=20)

    tk.Label(
        content_frame,
        text="Number of Words",
        bg="white",
        font=("Arial", 32, "underline"),
    ).pack(pady=10)

    num_of_words = ttk.Combobox(
        content_frame,
        values=[10, 20, 30],
        state="readonly",
        width=5,
        font=("Arial", 28),
    )
    num_of_words.set(10)
    num_of_words.pack(pady=5)

    def next_action():
        if "config" not in alarm_data:
            alarm_data["config"] = {}

        alarm_data["config"]["difficulty"] = difficulty.get()
        alarm_data["config"]["num_of_words"] = int(num_of_words.get())
        count_down_window(root, alarm_data, go_back_callback)

    btn_frame = tk.Frame(content_frame, bg="white")
    btn_frame.pack(pady=20)

    ttk.Button(
        btn_frame,
        text="Back",
        command=go_back_callback,
        style="Big.TButton",
    ).grid(row=0, column=0, padx=20, ipadx=40, ipady=10)

    ttk.Button(
        btn_frame,
        text="Submit Alarm",
        command=next_action,
        style="Big.TButton",
    ).grid(row=0, column=1, padx=20, ipadx=40, ipady=10)

    record_transcription_label = tk.Label(
        content_frame,
        text="",
        bg="white",
        font=("Arial", 24),
        wraplength=600,
    )
    record_transcription_label.pack(pady=10)

    def record_test():
        record_transcription_label.config(text="Recording for 10 seconds...")
        r = sr.Recognizer()
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

    ttk.Button(
        content_frame,
        text="Record for 10 seconds",
        command=record_test,
        style="Big.TButton",
    ).pack(pady=10)

    style = ttk.Style()
    style.configure(
        "Big.TButton",
        font=("Arial", 28),
        padding=15,
    )
    style.configure(
        "White.TRadiobutton",
        font=("Arial", 28),
        background="white",
    )