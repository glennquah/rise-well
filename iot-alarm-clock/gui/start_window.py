import tkinter as tk
from tkinter import ttk
from PIL import Image 
from gui.add_alarm_window import add_alarm_window

def start_window(root: tk.Tk):
    for widget in root.winfo_children():
        widget.destroy()
        
    root.title("RiseWell")
    root.geometry("500x450")
    root.configure(bg="white")

    title_label = ttk.Label(root, text="Welcome to RiseWell", font=("Arial", 24, "bold"), background="white")
    title_label.pack(pady=10)

    try:
        print(Image.__version__)
        # image = Image.open("assets/RiseWellLogo.png")
        # image = image.resize((150, 150), Image.ANTIALIAS)
        # alarm_image = ImageTk.PhotoImage(image)
        # img_label = tk.Label(root, image=alarm_image, background="white")
        # img_label.image = alarm_image
        # img_label.pack(pady=10)
    except Exception as e:
        print(f"Image Error: {e}")
        
    desc_label = ttk.Label(root, text="Your IoT alarm clock to ensure you wake up!", font=("Arial", 12), background="white", justify="center")
    desc_label.pack()
    guide_label = ttk.Label(root, text="How to start?\nAdd an alarm, pick activities, and start your day well!", font=("Arial", 10), background="white", justify="center")
    guide_label.pack(pady=5)
    userId = 'user_2uWbVB0Sa5nzCaYSrQjpJ4cU5YY' #TODO: update to your userId so that you wont have to keep entering ur userId in login page
    
    tk.Label(root, text="Enter User ID", bg="white").pack(pady=5)
    user_id_var = tk.StringVar(value=userId)
    user_id_entry = tk.Entry(root, textvariable=user_id_var, width=30)
    user_id_entry.pack(pady=5)

    add_alarm_btn = ttk.Button(root, text="Add Alarm", command=lambda: add_alarm_window(root, user_id_var.get()))
    add_alarm_btn.pack(pady=10)
    
    