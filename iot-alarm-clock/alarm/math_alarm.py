import tkinter as tk
from tkinter import ttk
import random
import datetime
import time
import threading
from services.sleep_detection.sleep_detection import checks_if_user_is_awake
from utils import play_alarm_sound, stop_alarm_sound
from apis.api_client import post_alarm_history

def poll_user_awake_status(root, result_label, alarm, go_back_callback):
    countdown_seconds = 15  # Set to 300 for production

    def update_countdown(time_left):
        if time_left > 0:
            result_label.config(
                text=f"⏳ Alarm retriggering detection ends in {time_left} seconds...",
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
            root.after(3000, go_back_callback)
        else:
            result_label.config(text="Still sleepy... Let's retry!", fg="orange")
            root.update()
            root.after(2000, lambda: trigger(alarm, root, go_back_callback))

    update_countdown(countdown_seconds)


def trigger(alarm, root, go_back_callback):
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Math Challenge Alarm")

    sound_obj = play_alarm_sound()

    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")
    operation = config.get("operation", "Addition")
    num_questions = config.get("num_questions", 3)

    score = {"correct": 0}
    attempts = {"total": 0}
    current_q = {"question": None, "answer": None}
    questions_asked = [0]

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(expand=True)

    question_label = tk.Label(
        content_frame,
        text="",
        font=("Arial", 64, "bold"),
        bg="white",
    )
    question_label.pack(pady=20)

    answer_var = tk.StringVar()
    answer_entry = tk.Entry(
        content_frame,
        textvariable=answer_var,
        font=("Arial", 48),
        width=8,
        justify="center",
    )
    answer_entry.pack(pady=20)

    result_label = tk.Label(
        content_frame,
        text="",
        font=("Arial", 32),
        bg="white",
    )
    result_label.pack(pady=10)

    def generate_question():
        if difficulty == "Easy":
            a, b = random.randint(1, 10), random.randint(1, 10)
        elif difficulty == "Medium":
            a, b = random.randint(10, 50), random.randint(10, 50)
        elif difficulty == "Hard":
            a, b = random.randint(50, 100), random.randint(50, 100)
        else:
            a, b = random.randint(1, 10), random.randint(1, 10)

        if operation == "Addition":
            q, ans = f"{a} + {b} = ?", a + b
        elif operation == "Subtraction":
            q, ans = f"{a} - {b} = ?", a - b
        elif operation == "Multiplication":
            q, ans = f"{a} * {b} = ?", a * b
        elif operation == "Division":
            b = random.randint(1, 10)
            a = b * random.randint(1, 10)
            q, ans = f"{a} / {b} = ?", round(a / b, 2)
        else:
            q, ans = f"{a} + {b} = ?", a + b
        return q, ans

    def next_question():
        if questions_asked[0] >= num_questions:
            finish_challenge()
            return
        q, ans = generate_question()
        current_q["question"], current_q["answer"] = q, ans
        question_label.config(text=q)
        answer_var.set("")
        questions_asked[0] += 1

    def submit_answer():
        attempts["total"] += 1
        try:
            user_ans = float(answer_var.get())
            if abs(user_ans - current_q["answer"]) < 0.01:
                score["correct"] += 1
                result_label.config(text="✅ Correct!", bg="white")
                next_question()
            else:
                result_label.config(text="❌ Wrong! Try again.", bg="white")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a number.", bg="white")

    # Create a Num Pad for easier number input
    num_pad_frame = tk.Frame(content_frame, bg="white")
    num_pad_frame.pack(pady=20)

    def insert_number(num):
        current_value = answer_var.get()
        answer_var.set(current_value + str(num))

    def clear_entry():
        answer_var.set("")

    btn_texts = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["0", "⌫", "Clear"],
    ]

    for r, row in enumerate(btn_texts):
        for c, text in enumerate(row):
            if text == "⌫":
                btn = ttk.Button(
                    num_pad_frame,
                    text=text,
                    command=lambda: answer_var.set(answer_var.get()[:-1]),
                    style="Big.TButton",
                )
            elif text == "Clear":
                btn = ttk.Button(
                    num_pad_frame,
                    text=text,
                    command=clear_entry,
                    style="Big.TButton",
                )
            else:
                btn = ttk.Button(
                    num_pad_frame,
                    text=text,
                    command=lambda t=text: insert_number(t),
                    style="Big.TButton",
                )
            btn.grid(row=r, column=c, padx=5, pady=5, ipadx=20, ipady=20)

    submit_button = ttk.Button(
        content_frame,
        text="Submit",
        command=submit_answer,
        style="Big.TButton",
    )
    submit_button.pack(pady=20)

    start_time = datetime.datetime.now()

    def finish_challenge():
        question_label.config(text="🎉 Challenge completed!")
        answer_entry.destroy()
        submit_button.destroy()
        num_pad_frame.destroy()
        end_time = datetime.datetime.now()
        time_taken = str(end_time - start_time).split(".")[0]
        result_label.config(
            text=f" Score: {score['correct']} / {num_questions}\n Time taken: {time_taken}\n Total attempts: {attempts['total']}",
            bg="white",
        )


        stop_alarm_sound()
        payload = {
            "userId": alarm.get("userId"),
            "alarmType": "Math",
            "alarmTime": start_time.isoformat(),
            "resolvedTime": end_time.isoformat(),
            "attempts": attempts["total"],
            "difficulty": difficulty,
            "mathOperations": operation,
            "numberOfQuestions": num_questions,
        }
        post_alarm_history(payload)


        def start_awake_check():
            result_label.config(text="Now checking if you're awake...", fg="green")
            root.update()
            poll_user_awake_status(root, result_label, alarm, go_back_callback)

        root.after(2000, start_awake_check)

    next_question()

    style = ttk.Style()
    style.configure(
        "Big.TButton",
        font=("Arial", 28),
        padding=15,
    )