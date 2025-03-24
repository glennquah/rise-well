import os
import time
import subprocess
import cv2
import numpy as np
import tkinter as tk
import random
from skimage.metrics import structural_similarity as ssim
import RPi.GPIO as GPIO
from ultralytics import YOLO
from utils import play_alarm_sound, stop_alarm_sound
from apis.api_client import post_alarm_history
from PIL import Image, ImageTk


BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
model = YOLO("yolov5su.pt")

CATEGORIES = {
    "furniture": ["chair", "couch", "bed", "dining table", "toilet", "bench"],
    "electronics": ["tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "refrigerator", "hair drier"],
    "kitchenware": ["sink", "knife", "spoon", "fork", "bowl", "cup", "wine glass", "bottle"],
    "accessories": ["backpack", "umbrella", "handbag", "suitcase"],
    "food": ["banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake"],
    "decor/misc": ["potted plant", "clock", "vase", "book"]
}
OBJECT_LIST = [item for sub in CATEGORIES.values() for item in sub]

def wait_for_button():
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        time.sleep(0.1)

def preview_camera():
    return subprocess.Popen(["rpicam-still", "--preview", "0,0,640,480", "--timeout", "0"])

def capture_image(path, preview):
    preview.terminate()
    subprocess.run(["rpicam-still", "-o", path, "--width", "640", "--height", "480"])

def compute_similarity(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return ssim(img1, img2)

def detect_objects(image_path):
    image = cv2.imread(image_path)
    results = model(image)
    return [model.names[int(obj[5])] for obj in results[0].boxes.data.cpu().numpy()]

def show_reference_popup(img_path):
    popup = tk.Toplevel(root)
    popup.title("📸 Reference Image")
    popup.configure(bg="white")

    img = Image.open(img_path)
    img = img.resize((320, 240))  # Resize if needed
    tk_img = ImageTk.PhotoImage(img)

    label = tk.Label(popup, text="Match this image!", font=("Arial", 14), bg="white")
    label.pack(pady=5)
    panel = tk.Label(popup, image=tk_img)
    panel.image = tk_img  # Keep reference
    panel.pack()

    popup.after(4000, popup.destroy)  # Auto-close after 4 seconds

def trigger(alarm_data, root, go_back_callback):
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()

    mode = alarm_data["config"].get("mode")
    userId = alarm_data.get("userId")
    start_time = time.time()

    label = tk.Label(root, text="Waking you up...", font=("Arial", 16), bg="white")
    label.pack(pady=20)

    play_alarm_sound()

    def run_check():
        success = False
        try:
            if mode == "reference":
                label.config(text="Match the reference image. Press the button when ready.")
                ref_path = f"data/references/{userId}_ref.jpg"
                show_reference_popup(ref_path)
                preview = preview_camera()
                wait_for_button()
                comp_path = f"/tmp/{userId}_compare.jpg"
                capture_image(comp_path, preview)
                score = compute_similarity(ref_path, comp_path)
                success = score >= 0.75

            elif mode == "category":
                selected_category = alarm_data["config"].get("category")
                target_objects = CATEGORIES.get(selected_category, [])

                if not target_objects:
                    label.config(text=f"No objects defined for category: {selected_category}", fg="red")
                    return

                target_object = random.choice(target_objects)
                alarm_data["config"]["target_object"] = target_object  # store for logging

                # Display instructions first
                label.config(
                    text=f"📸 Show me a '{target_object}' from category '{selected_category}'.\n\nPress the button when ready.",
                    font=("Arial", 14),
                    wraplength=500,
                    justify="center"
                )
                root.update_idletasks()     # Force GUI to update
                time.sleep(1.0)             # Give user a second to read

                # Now launch the preview and capture
                preview = preview_camera()
                wait_for_button()
                image_path = f"/tmp/{userId}_category.jpg"
                capture_image(image_path, preview)
                
                detected = detect_objects(image_path)
                print("Detected:", detected)

                success = target_object in detected

        except Exception as e:
            label.config(text=f"Error: {e}", fg="red")

        if success:
            stop_alarm_sound()
            end_time = time.time()
            label.config(text="✅ Alarm passed! Good morning!", fg="green")
            payload = {
                "userId": userId,
                "alarmType": "Image Recognition",
                "alarmTime": time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(start_time)),
                "resolvedTime": time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(end_time)),
                "mode": mode,
                "category": alarm_data["config"].get("category", None)
            }
            # post_alarm_history(payload)
            print(payload)
            tk.Button(root, text="Back", command=go_back_callback, bg="white").pack(pady=10)
            GPIO.cleanup()
        else:
            label.config(text="❌ Try again! Press the button when ready.", fg="red")
            root.after(1000, run_check)

    run_check()
