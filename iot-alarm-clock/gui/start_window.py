import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from gui.add_alarm_window import add_alarm_window


def start_window(root: tk.Tk):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("RiseWell")
    root.configure(bg="white")

    root.attributes('-fullscreen', True)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill="both", expand=True)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(expand=True)

    title_label = ttk.Label(
        content_frame,
        text="Welcome to RiseWell",
        font=("Arial", 48, "bold"),
        background="white",
    )
    title_label.pack(pady=20)

    try:
        print(Image.__version__)
        image = Image.open("assets/RiseWellLogo.png")
        image = image.resize((300, 300), Image.LANCZOS)
        alarm_image = ImageTk.PhotoImage(image)
        img_label = tk.Label(content_frame, image=alarm_image, background="white")
        img_label.image = alarm_image
        img_label.pack(pady=10)
    except Exception as e:
        print(f"Image Error: {e}")        

    desc_label = ttk.Label(
        content_frame,
        text="Your IoT alarm clock to ensure you wake up!",
        font=("Arial", 28),
        background="white",
        justify="center",
    )
    desc_label.pack(pady=10)

    guide_label = ttk.Label(
        content_frame,
        text="How to start?\nAdd an alarm, pick activities, and start your day well!",
        font=("Arial", 24),
        background="white",
        justify="center",
    )
    guide_label.pack(pady=10)

    userId = "user_2uLEgW40wSAAR9BWMfSDX5cue22" 
    # FIXME: Change this when needed

    user_id_label = tk.Label(
        content_frame,
        text="Enter User ID",
        bg="white",
        font=("Arial", 24, "bold"),
    )
    user_id_label.pack(pady=5)

    user_id_var = tk.StringVar(value=userId)
    user_id_entry = tk.Entry(
        content_frame,
        textvariable=user_id_var,
        width=40,
        font=("Arial", 22),
        justify="center",
    )
    user_id_entry.pack(pady=5)

    button_frame = tk.Frame(content_frame, bg="white")
    button_frame.pack(pady=20)

    add_alarm_btn = ttk.Button(
        button_frame,
        text="Add Alarm",
        command=lambda: add_alarm_window(root, user_id_var.get()),
        style="Big.TButton",
    )
    add_alarm_btn.pack(pady=10, ipadx=50, ipady=20)

    def quit_app():
        root.destroy()

    quit_btn = ttk.Button(
        button_frame,
        text="Quit",
        command=quit_app,
        style="Big.TButton",
    )
    quit_btn.pack(pady=10, ipadx=50, ipady=20)

    # Press ESC / Button to quit
    root.bind("<Escape>", lambda event: quit_app())
    
    style = ttk.Style()
    style.configure(
        "Big.TButton",
        font=("Arial", 24),
        padding=10,
    )