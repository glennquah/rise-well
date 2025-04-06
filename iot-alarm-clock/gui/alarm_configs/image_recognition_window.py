import tkinter as tk
from tkinter import ttk, messagebox
import os
import time
import subprocess
import RPi.GPIO as GPIO
from gui.count_down_window import count_down_window
import cv2


BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

CATEGORIES = {
    "furniture": ["chair", "couch", "bed", "dining table", "toilet", "bench"],
    "electronics": ["tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "refrigerator", "hair drier"],
    "kitchenware": ["sink", "knife", "spoon", "fork", "bowl", "cup", "wine glass", "bottle"],
    "accessories": ["backpack", "umbrella", "handbag", "suitcase"],
    "food": ["banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake"],
    "decor/misc": ["potted plant", "clock", "vase", "book"]
}
CATEGORY_OPTIONS = list(CATEGORIES.keys())

def preview_camera_and_capture(image_path):
    cap = cv2.VideoCapture(0)  # /dev/video0
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam")

    cv2.namedWindow("USB Camera Preview", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("USB Camera Preview", 640, 480)

    print("Press the physical button to capture.")

    captured_frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("USB Camera Preview", frame)

        # Non-blocking key check
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button pressed
            captured_frame = frame
            break

    cap.release()
    cv2.destroyAllWindows()

    if captured_frame is not None:
        cv2.imwrite(image_path, captured_frame)
        print(f"Image saved to {image_path}")
        return True
    else:
        print("Capture cancelled")
        return False


def wait_for_button():
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        time.sleep(0.1)

def preview_camera():
    return subprocess.Popen(["rpicam-still", "--preview", "0,0,640,480", "--timeout", "0"])

def capture_image(image_path, preview_frame):
    if preview_frame is None:
        raise RuntimeError("No image to save")
    cv2.imwrite(image_path, preview_frame)

def image_recognition_window(root, alarm_data, go_back_callback):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Image Recognition Alarm Configuration")
    if "config" not in alarm_data:
        alarm_data["config"] = {}

    tk.Label(root, text="Select Mode", bg="white").pack(pady=5)
    mode = tk.StringVar(value=alarm_data["config"].get("mode", "reference"))
    ttk.Radiobutton(root, text="Reference Match", variable=mode, value="reference", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Category Match", variable=mode, value="category", style="White.TRadiobutton").pack()

    category_frame = tk.Frame(root, bg="white")
    tk.Label(category_frame, text="Select Category", bg="white").pack(pady=5)
    category = tk.StringVar(value=alarm_data["config"].get("category", CATEGORY_OPTIONS[0]))
    dropdown = ttk.Combobox(category_frame, values=CATEGORY_OPTIONS, textvariable=category)
    dropdown.pack()

    object_display = tk.Label(category_frame, text="", bg="white", wraplength=400, justify="left")
    object_display.pack(pady=5)

    def update_objects_display(*_):
        selected = category.get()
        items = CATEGORIES.get(selected, [])
        object_display.config(text="Includes: " + ", ".join(items))

    dropdown.bind("<<ComboboxSelected>>", update_objects_display)
    category_frame.pack(pady=5)
    update_objects_display()

    ref_label = tk.Label(root, text="Capture Reference Image", bg="white")
    ref_button = ttk.Button(root, text="Capture", command=lambda: capture_reference_image(alarm_data))

    def toggle_mode():
        if mode.get() == "reference":
            category_frame.pack_forget()
            ref_label.pack(pady=5)
            ref_button.pack(pady=5)
        else:
            ref_label.pack_forget()
            ref_button.pack_forget()
            category_frame.pack(pady=5)
            update_objects_display()

    def capture_reference_image(alarm_data):
        ref_path = f"data/references/ref.jpg"
        os.makedirs(os.path.dirname(ref_path), exist_ok=True)
        absolute_path = os.path.abspath(ref_path)

        messagebox.showinfo("Ready", "Camera preview will start.\nPress the button to capture.")

        success = preview_camera_and_capture(absolute_path)
        if success:
            messagebox.showinfo("Saved", f"Reference image saved to {absolute_path}")
        else:
            messagebox.showwarning("Cancelled", "Image capture was cancelled.")

    def next_action():
        alarm_data["config"]["mode"] = mode.get()
        if mode.get() == "category":
            alarm_data["config"]["category"] = category.get()
        count_down_window(root, alarm_data, lambda: go_back_callback())

    toggle_mode()
    mode.trace_add("write", lambda *_: toggle_mode())

    ttk.Button(root, text="Submit Alarm", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=go_back_callback).pack(pady=5)
