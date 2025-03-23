import tkinter as tk
import random
import pygame
import os
import datetime
import requests
from utils import play_alarm_sound 
from utils import stop_alarm_sound 

def trigger(alarm, root, go_back_callback):
    # Reuse the same window and set background to white
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Math Challenge Alarm")

    # Start playing the alarm sound
    sound_obj = play_alarm_sound()

    # Retrieve math configuration from alarm data
    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")
    operation = config.get("operation", "Addition")
    num_questions = config.get("num_questions", 3)

    # Initialize score, attempts, and question counter
    score = {"correct": 0}
    attempts = {"total": 0}
    current_q = {"question": None, "answer": None}
    questions_asked = [0]

    # Create UI elements with white backgrounds
    question_label = tk.Label(root, text="", font=("Arial", 18), bg="white")
    question_label.pack(pady=10)

    answer_entry = tk.Entry(root, font=("Arial", 14), bg="white")
    answer_entry.pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 14), bg="white")
    result_label.pack(pady=10)

    def generate_question():
        if difficulty == "Easy":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
        else:
            a = random.randint(10, 50)
            b = random.randint(10, 50)
        if operation == "Addition":
            q = f"{a} + {b} = ?"
            ans = a + b
        elif operation == "Subtraction":
            q = f"{a} - {b} = ?"
            ans = a - b
        elif operation == "Multiplication":
            q = f"{a} * {b} = ?"
            ans = a * b
        elif operation == "Division":
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
            q = f"{a} / {b} = ?"
            ans = a / b
        else:
            q = f"{a} + {b} = ?"
            ans = a + b
        return q, ans

    def next_question():
        if questions_asked[0] >= num_questions:
            finish_challenge()
            return
        q, ans = generate_question()
        current_q["question"] = q
        current_q["answer"] = ans
        question_label.config(text=q)
        answer_entry.delete(0, tk.END)
        questions_asked[0] += 1

    def submit_answer():
        attempts["total"] += 1
        try:
            user_ans = float(answer_entry.get())
            if abs(user_ans - current_q["answer"]) < 0.01:
                score["correct"] += 1
                result_label.config(text="Correct!", bg="white")
                next_question()
            else:
                result_label.config(text="Wrong! Try again.", bg="white")
        except:
            result_label.config(text="Invalid input. Please enter a number.", bg="white")

    submit_button = tk.Button(root, text="Submit", command=submit_answer, bg="white")
    submit_button.pack(pady=10)

    # Record the start time for measuring duration
    start_time = datetime.datetime.now()

    def finish_challenge():
        question_label.config(text="Challenge completed!")
        answer_entry.destroy()
        submit_button.destroy()
        end_time = datetime.datetime.now()
        time_taken = end_time - start_time
        result_label.config(text=f"Score: {score['correct']} / {num_questions}\nTime taken: {str(time_taken).split('.')[0]}\nTotal attempts: {attempts['total']}", bg="white")
        tk.Button(root, text="Back", command=go_back_callback, bg="white").pack(pady=10)
        stop_alarm_sound()
        
        try:
            response = requests.post("http://192.168.23.239:3000/api/alarm-history", json={
                "userId": "user_2uLEgW40wSAAR9BWMfSDX5cue22",
                "alarmType": "math",
                "alarmTime": start_time.isoformat(),
                "resolvedTime": end_time.isoformat(),
                "difficulty": difficulty,
                "mathOperations": operation,
                "numberOfQuestions": num_questions
            })
            print(f"POST status: {response.status_code} | Response: {response.text}")
        except Exception as e:
            print(f"Failed to post alarm history: {e}")

    next_question()