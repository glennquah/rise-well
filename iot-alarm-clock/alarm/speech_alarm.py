import tkinter as tk
import datetime
import speech_recognition as sr
from utils import play_alarm_sound, stop_alarm_sound
from apis.api_client import post_alarm_history
from sensors.audio_sensor import AudioSensor

def trigger(alarm, root, go_back_callback, sentence):
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Speech Challenge Alarm")
    sound_obj = play_alarm_sound()

    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")
    num_of_words = int(config.get("num_of_words", 10))

    attempts = {"total": 0}
    score = {"correct": 0}
    passed = {"status": False}

    # Record start time
    start_time = datetime.datetime.now()

    # UI Elements
    tk.Label(root, text="Repeat the sentence below:", font=("Arial", 14), bg="white").pack(pady=5)
    sentence_label = tk.Label(root, text=sentence["sentence"], wraplength=400, font=("Arial", 16), bg="white", justify="center")
    sentence_label.pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=5)

    score_label = tk.Label(root, text="Attempts: 0 | Score: 0%", font=("Arial", 12), bg="white")
    score_label.pack(pady=5)

    transcript_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
    transcript_label.pack(pady=5)

    # Create an instance of AudioSensor
    sensor = AudioSensor()

    # Define a callback to be called each time background listening returns audio.
    def callback(recognizer, audio):
        try:
            transcript = recognizer.recognize_google(audio)
            sensor.collected_transcripts.append(transcript)
            transcript_label.config(text="Heard: " + " ".join(sensor.collected_transcripts))
        except sr.UnknownValueError:
            transcript_label.config(text="Could not understand audio.")
        except sr.RequestError as e:
            transcript_label.config(text=f"Request error: {e}")

    # Start recording: start background listening and swap buttons.
    def start_recording():
        attempts["total"] += 1
        transcript_label.config(text="Recording... (Click 'Stop Recording' to finish)")
        sensor.start_listening(callback)
        start_btn.pack_forget()
        stop_btn.pack(pady=10)

    # Stop recording: stop background listening, process the captured text, and check similarity.
    def stop_recording():
        sensor.stop_listening_func()
        transcript_label.config(text="Transcribing... Please wait.")
        user_transcription = " ".join(sensor.collected_transcripts)
        transcript_label.config(text="You said: " + user_transcription)
        similarity = AudioSensor.calculate_similarity(sentence["sentence"], user_transcription)
        if similarity >= 80:
            score["correct"] += 1
            passed["status"] = True
            result_label.config(text=f"✅ {similarity:.1f}% matched — Correct!", fg="green")
            score_label.config(text=f"Attempts: {attempts['total']} | Score: 100%")
            finish_challenge()
        else:
            result_label.config(text=f"❌ {similarity:.1f}% matched — Try again.", fg="red")
            score_label.config(text=f"Attempts: {attempts['total']} | Score: 0%")
        stop_btn.pack_forget()
        if not passed["status"]:
            start_btn.pack(pady=10)

    start_btn = tk.Button(root, text="Start Recording", command=start_recording, bg="white")
    start_btn.pack(pady=10)
    stop_btn = tk.Button(root, text="Stop Recording", command=stop_recording, bg="white")

    # Finish challenge: display summary and send the POST request.
    def finish_challenge():
        end_time = datetime.datetime.now()
        time_taken = end_time - start_time

        start_btn.pack_forget()
        stop_btn.pack_forget()

        if passed["status"]:
            result_label.config(text="✅ Challenge Passed!", fg="green")
        else:
            result_label.config(text="❌ Challenge Failed. Try again later.", fg="red")

        tk.Label(root, text=f"Time taken: {str(time_taken).split('.')[0]}", bg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(root, text="Back", command=go_back_callback, bg="white").pack(pady=10)
        stop_alarm_sound()

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

    # End of trigger function.