import tkinter as tk
import random
import pygame
import os

def init_sound():
    pygame.mixer.init()

def play_alarm_sound():
    if not pygame.mixer.get_init():
        init_sound()
    # Adjust the path as necessary. Here it assumes a "ringtones" folder is in the same folder as this file.
    sound_file = os.path.join(os.path.dirname(__file__), "ringtones", "alarm1.wav")
    if os.path.exists(sound_file):
        sound = pygame.mixer.Sound(sound_file)
        sound.play(loops=-1)  # Play indefinitely until stopped
        return sound
    return None

def stop_alarm_sound(sound):
    if sound:
        sound.stop()

def trigger(alarm, root):
    # Clear the current Tk screen (reuse the same window)
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Math Challenge Alarm")

    # Start playing the alarm sound and keep a reference to stop it later
    sound_obj = play_alarm_sound()

    # Retrieve math configuration from alarm data (if provided)
    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")
    operation = config.get("operation", "Addition")
    num_questions = config.get("num_questions", 3)

    # Setup UI for the math challenge on the same root
    score = {"correct": 0}
    current_q = {"question": None, "answer": None}
    questions_asked = [0]

    question_label = tk.Label(root, text="", font=("Arial", 18))
    question_label.pack(pady=10)

    answer_entry = tk.Entry(root, font=("Arial", 14))
    answer_entry.pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 14))
    result_label.pack(pady=10)

    def generate_question():
        # Generate numbers based on difficulty
        if difficulty == "Easy":
            a = random.randint(1, 10)
            b = random.randint(1, 10)
        else:
            a = random.randint(10, 50)
            b = random.randint(10, 50)
        # Create question based on selected operation
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
            question_label.config(text="Challenge completed!")
            answer_entry.destroy()
            submit_button.destroy()
            result_label.config(text=f"Score: {score['correct']} / {num_questions}")
            # Stop the alarm sound when the challenge is done
            stop_alarm_sound(sound_obj)
            return
        q, ans = generate_question()
        current_q["question"] = q
        current_q["answer"] = ans
        question_label.config(text=q)
        answer_entry.delete(0, tk.END)
        questions_asked[0] += 1

    def submit_answer():
        try:
            user_ans = float(answer_entry.get())
            if abs(user_ans - current_q["answer"]) < 0.01:
                score["correct"] += 1
                result_label.config(text="Correct!")
            else:
                result_label.config(text=f"Wrong! Answer: {current_q['answer']}")
        except:
            result_label.config(text="Invalid input")
        next_question()

    submit_button = tk.Button(root, text="Submit", command=submit_answer)
    submit_button.pack(pady=10)

    # Start the challenge with the first question
    next_question()

    # Optionally add a Back button that stops the alarm sound and goes back
    tk.Button(root, text="Back", command=lambda: [stop_alarm_sound(sound_obj), root.destroy()]).pack(pady=10)