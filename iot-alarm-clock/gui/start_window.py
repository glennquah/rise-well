import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from add_alarm_window import add_alarm_window

def start_window(alarm_manager):
    root = tk.Tk()
    root.title("RiseWell")
    root.geometry("500x400")
    root.configure(bg="white")

    title_label = ttk.Label(root, text="Welcome to RiseWell", font=("Arial", 18, "bold"), background="white")
    title_label.pack(pady=10)

    desc_label = ttk.Label(root, text="Your IoT alarm clock to ensure you wake up!", font=("Arial", 12), background="white")
    desc_label.pack()

    guide_label = ttk.Label(root, text="How to start?\nAdd an alarm, pick activities, and start your day well!", font=("Arial", 10), background="white")
    guide_label.pack(pady=5)

    try:
        image = Image.open("assets/RiseWellLogo.png")
        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        alarm_image = ImageTk.PhotoImage(image)

        img_label = tk.Label(root, image=alarm_image, background="white")
        img_label.image = alarm_image
        img_label.pack(pady=10)
    except Exception as e:
        print(f"Image Error: {e}")

    add_alarm_btn = ttk.Button(root, text="Add Alarm", command=add_alarm_window(alarm_manager))
    add_alarm_btn.pack(pady=10)

    root.mainloop()