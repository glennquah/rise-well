import tkinter as tk
import random
import pygame
import os
import datetime
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
                # Do not advance to the next question; allow user to try again.
        except:
            result_label.config(text="Invalid input. Please enter a number.", bg="white")
            # Allow user to retry without moving on.

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
        # Stop the alarm sound when the challenge is complete
        stop_alarm_sound()

    next_question()

    # Optionally, add a Back button that stops the alarm sound and exits the challenge.
    tk.Button(root, text="Back", command=go_back_callback, bg="white").pack(pady=10)