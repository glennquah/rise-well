import tkinter as tk
import datetime
from utils import play_alarm_sound, stop_alarm_sound
from apis.api_client import post_alarm_history

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

    # Start Time
    start_time = datetime.datetime.now()

    # UI
    tk.Label(root, text="Repeat the sentence below:", font=("Arial", 14), bg="white").pack(pady=5)

    sentence_label = tk.Label(root, text=sentence.sentence, wraplength=400, font=("Arial", 16), bg="white", justify="center")
    sentence_label.pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
    result_label.pack(pady=5)

    score_label = tk.Label(root, text=f"Attempts: 0 | Score: 0%", font=("Arial", 12), bg="white")
    score_label.pack(pady=5)

    def start_recording():
        attempts["total"] += 1

        # Simulate speech check: just assume correct on even attempts (you can replace this)
        is_correct = attempts["total"] % 2 == 0
        if is_correct:
            score["correct"] += 1
            result_label.config(text="✅ You pronounced it correctly!", fg="green")
        else:
            result_label.config(text="❌ Incorrect. Try again.", fg="red")

        # Update score
        percent = int((score["correct"] / attempts["total"]) * 100)
        score_label.config(text=f"Attempts: {attempts['total']} | Score: {percent}%")

        # Auto-finish if passed
        if percent >= 80:
            passed["status"] = True
            finish_challenge()

    record_btn = tk.Button(root, text="Start Recording", command=start_recording, bg="white")
    record_btn.pack(pady=10)

    def finish_challenge():
        end_time = datetime.datetime.now()
        time_taken = end_time - start_time

        record_btn.destroy()

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
            "givenWords": sentence.sentence,
        }
        post_alarm_history(payload)