import tkinter as tk
from tkinter import ttk
from gui.count_down_window import count_down_window

def speech_window(root, alarm_data, go_back_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Speech Alarm Configuration")
    # Prepare speech config in alarm_data
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
    
    # ADDED HERE JUST FOR TESTING PURPOSE
    sensor = AudioSensor()
    sensor.collected_transcripts = []

    transcript_label = tk.Label(root, text="Press 'Start Recording' to begin", wraplength=400, bg="white")
    transcript_label.pack(pady=10)

    def callback(recognizer, audio):
        try:
            text = recognizer.recognize_google(audio)
            sensor.collected_transcripts.append(text)
            # Update label on the main thread
            root.after(0, lambda: transcript_label.config(text="Heard: " + " | ".join(sensor.collected_transcripts)))
        except sr.UnknownValueError:
            root.after(0, lambda: transcript_label.config(text="(Could not understand audio)"))
        except sr.RequestError as e:
            root.after(0, lambda: transcript_label.config(text=f"(Request error: {e})"))

    def start_recording():
        sensor.collected_transcripts = []
        transcript_label.config(text="Listening... Speak until you press 'Stop Recording'.")
        with sensor.mic as source:
            sensor.recognizer.adjust_for_ambient_noise(source, duration=1)
        sensor.stop_listening = sensor.recognizer.listen_in_background(sensor.mic, callback)
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")

    def stop_recording():
        if sensor.stop_listening:
            sensor.stop_listening(wait_for_stop=False)
        transcript_label.config(text="Stopped. " + transcript_label.cget("text"))
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")

    start_btn = tk.Button(root, text="Start Recording", command=start_recording, bg="lightgreen")
    stop_btn = tk.Button(root, text="Stop Recording", command=stop_recording, bg="tomato", state="disabled")
    back_btn = tk.Button(root, text="Back", command=go_back_callback, bg="white")

    start_btn.pack(pady=5)
    stop_btn.pack(pady=5)
    back_btn.pack(pady=10)