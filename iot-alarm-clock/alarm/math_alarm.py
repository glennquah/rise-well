import tkinter as tk
import random

def trigger(alarm):
    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")
    operation = config.get("operation", "Addition")
    num_questions = config.get("num_questions", 3)
    root = tk.Toplevel()
    root.title("Math Challenge")
    score = {"correct": 0}
    question_label = tk.Label(root, text="")
    question_label.pack()
    answer_entry = tk.Entry(root)
    answer_entry.pack()
    result_label = tk.Label(root, text="")
    result_label.pack()
    def generate_question():
        a = random.randint(1, 10) if difficulty == "Easy" else random.randint(10, 50)
        b = random.randint(1, 10) if difficulty == "Easy" else random.randint(10, 50)
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
    current_q = {"question": None, "answer": None}
    questions_asked = [0]
    def next_question():
        if questions_asked[0] >= num_questions:
            question_label.config(text="Challenge completed!")
            answer_entry.destroy()
            submit_button.destroy()
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
    submit_button.pack()
    next_question()
    root.mainloop()