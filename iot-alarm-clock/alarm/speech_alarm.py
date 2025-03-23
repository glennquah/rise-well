import tkinter as tk
import datetime
import speech_recognition as sr
import re
from difflib import SequenceMatcher

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
    challenge_finished = False  # Flag to prevent UI updates after challenge ends

    start_time = datetime.datetime.now()

    tk.Label(root, text="Repeat the sentence below:", font=("Arial", 14), bg="white").pack(pady=5)
    sentence_label = tk.Label(root, text=sentence["sentence"], wraplength=400, font=("Arial", 16), bg="white", justify="center")
    sentence_label.pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=5)

    score_label = tk.Label(root, text="Attempts: 0 | Score: 0%", font=("Arial", 12), bg="white")
    score_label.pack(pady=5)

    transcript_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
    transcript_label.pack(pady=5)

    finish_btn = tk.Button(root, text="Finish", bg="white", state="disabled")
    finish_btn.pack_forget()

    # Patch AudioSensor with custom similarity logic.
    # Also, pass a device_index if needed (e.g., device_index=0)
    class CustomAudioSensor(AudioSensor):
        @staticmethod
        def calculate_similarity(expected_sentence, user_sentence):
            return calculate_similarity(expected_sentence, user_sentence)

    sensor = CustomAudioSensor()  # You can pass device_index=<number> here if needed

    def callback(recognizer, audio):
        if challenge_finished or not transcript_label.winfo_exists():
            return
        try:
            transcript = recognizer.recognize_google(audio)
            sensor.collected_transcripts.append(transcript)
            # Only update if widget still exists
            if transcript_label.winfo_exists():
                root.after(0, lambda: transcript_label.config(text="Heard: " + " ".join(sensor.collected_transcripts)))
        except sr.UnknownValueError:
            if transcript_label.winfo_exists():
                root.after(0, lambda: transcript_label.config(text="Could not understand audio."))
        except sr.RequestError as e:
            if transcript_label.winfo_exists():
                root.after(0, lambda: transcript_label.config(text=f"Request error: {e}"))

    def start_recording():
        nonlocal sound_obj
        stop_alarm_sound()
        sound_obj = None
        sensor.collected_transcripts = []
        transcript_label.config(text="Recording... (Click 'Stop Recording' to finish)")
        sensor.start_listening(callback)
        start_btn.pack_forget()
        stop_btn.pack(pady=10)

    def stop_recording():
        nonlocal attempts, final_passed, sound_obj
        try:
            sensor.stop_listening_func()
        except Exception as e:
            print("Error in stop_recording:", e)
        transcript_label.config(text="Transcribing... Please wait!")
        
        user_transcription = " ".join(sensor.collected_transcripts)
        transcript_label.config(text="You said: " + user_transcription)

        attempts += 1
        similarity = sensor.calculate_similarity(sentence["sentence"], user_transcription)
        
        if similarity >= 80:
            result_label.config(text=f"✅ {similarity:.1f}% matched — Correct!", fg="green")
            score_label.config(text=f"Attempts: {attempts} | Score: 100%")
            finish_btn.config(state="normal")
        else:
            if sound_obj is None:
                sound_obj = play_alarm_sound()
            result_label.config(text=f"❌ {similarity:.1f}% matched — Try again.", fg="red")
            score_label.config(text=f"Attempts: {attempts} | Score: 0%")

        stop_btn.pack_forget()
        if not final_passed:
            start_btn.pack(pady=10)

    def finish_challenge():
        nonlocal challenge_finished
        challenge_finished = True
        # Stop the listener if not already stopped.
        sensor.stop_listening_func()
        # Delay UI cleanup a bit longer (e.g., 300ms) to let any in-flight callbacks finish.
        root.after(300, perform_finish)

    def perform_finish():
        end_time = datetime.datetime.now()
        time_taken = end_time - start_time
        stop_alarm_sound()
        start_btn.pack_forget()
        stop_btn.pack_forget()
        finish_btn.pack_forget()

        result_label.config(text="✅ Challenge Passed!", fg="green")
        tk.Label(root, text=f"Time taken: {str(time_taken).split('.')[0]}", 
                 bg="white", font=("Arial", 12)).pack(pady=5)
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

    start_btn = tk.Button(root, text="Start Recording", command=start_recording, bg="white")
    stop_btn = tk.Button(root, text="Stop Recording", command=stop_recording, bg="white")
    finish_btn.config(command=finish_challenge)

    start_btn.pack(pady=10)
    finish_btn.pack(pady=10)