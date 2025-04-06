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
from services.cloudinary_uploader import upload_image_to_cloudinary
import datetime
from services.sleep_detection.sleep_detection import checks_if_user_is_awake

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

def capture_image_with_preview(path):
    cap = cv2.VideoCapture(0)  # USB webcam usually shows up as /dev/video0
    if not cap.isOpened():
        raise RuntimeError("Cannot open USB webcam")

    cv2.namedWindow("Camera Preview", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera Preview", 640, 480)

    print("Showing preview... Press the button to capture.")
    captured_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow("Camera Preview", frame)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed! Capturing image...")
            captured_frame = frame
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Optional escape
            print("Preview canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()

    if captured_frame is not None:
        cv2.imwrite(path, captured_frame)
        print(f"Image saved to {path}")
        return True
    else:
        return False

def compute_similarity(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    return ssim(img1, img2)

def detect_objects(image_path):
    image = cv2.imread(image_path)
    results = model(image)
    return [model.names[int(obj[5])] for obj in results[0].boxes.data.cpu().numpy()]

def poll_user_awake_status(root, label, alarm_data, go_back_callback):
    countdown_seconds = 15  # Set to 300 for 5 minutes in real usage

    def update_countdown(time_left):
        if time_left > 0:
            label.config(
                text=f"⏳ Checking if you're still awake in {time_left} seconds...",
                fg="blue"
            )
            root.update()
            root.after(1000, update_countdown, time_left - 1)
        else:
            check_awake_status()

    def check_awake_status():
        label.config(text="Checking if you're awake using AI...", fg="blue")
        root.update()

        if checks_if_user_is_awake():
            label.config(text="You're awake! Alarm complete.", fg="green")
            root.update()
            GPIO.cleanup()
            root.after(3000, root.quit)  # Quit after 3s
        else:
            label.config(text="Still sleepy... Let's play again!", fg="orange")
            root.update()
            root.after(2000, lambda: trigger(alarm_data, root, go_back_callback))

    update_countdown(countdown_seconds)



def handle_alarm_result(success, mode, refImageUrl, imageUrl, target_object, start_time, alarm_data, root, go_back_callback, label):


    if success:
        stop_alarm_sound()
        end_time = datetime.datetime.now()



        payload = {
            "userId": alarm_data.get("userId"),
            "alarmTime": start_time.isoformat(),
            "resolvedTime": end_time.isoformat(),
            "alarmType": "Image Recognition",
            "mode": mode,
            "imageUrl": imageUrl,
            "refImageUrl": refImageUrl,
            "target object": target_object,
            "category": alarm_data["config"].get("category", "")
        }

        post_alarm_history(payload)

        label.config(text="Alarm passed! Good morning!", fg="green")
        root.update()

        # After 2 seconds, update message and start countdown
        def start_awake_check():
            label.config(text="Now checking if you're awake...", fg="green")
            root.update()
            poll_user_awake_status(root, label, alarm_data, go_back_callback)

        root.after(2000, start_awake_check)


    else:
        label.config(text="Try again! Press the button when ready.", fg="red")
        tk.Button(
            root,
            text="Retry",
            command=lambda: trigger(alarm_data, root, go_back_callback),
            bg="white"
        ).pack(pady=10)

        tk.Button(
            root,
            text="Back",
            command=go_back_callback,
            bg="white"
        ).pack(pady=5)


def trigger(alarm_data, root, go_back_callback):
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()

    mode = alarm_data["config"].get("mode")

    label = tk.Label(root, text="Waking you up...", font=("Arial", 16), bg="white")
    label.pack(pady=20)

    start_time = datetime.datetime.now()
    play_alarm_sound()

    target_object = None
    success = False

    try:
        if mode == "reference":
            label.config(text="Match the reference image. Press the button when ready.")
            ref_path = f"data/references/ref.jpg"
            img = Image.open(ref_path)
            img = img.resize((320, 240))
            tk_img = ImageTk.PhotoImage(img)

            image_label = tk.Label(root, image=tk_img, bg="white")
            image_label.image = tk_img  # Prevent GC
            image_label.pack(pady=5)

            root.update()  # ✅ Force UI to render before continuing

            refImageUrl = upload_image_to_cloudinary(ref_path)


            comp_path = f"/tmp/compare.jpg"

            success = capture_image_with_preview(comp_path)

            image_label.destroy()


            if not success:
                raise RuntimeError("Image capture failed or was cancelled.")
            
            imageUrl = upload_image_to_cloudinary(comp_path)
            score = compute_similarity(ref_path, comp_path)
            success = score >= 0.75

            handle_alarm_result(
            success=success,
            mode=mode,
            refImageUrl = refImageUrl,
            imageUrl = imageUrl,
            target_object="",
            start_time=start_time,
            alarm_data=alarm_data,
            root=root,
            go_back_callback=go_back_callback,
            label=label
            )


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
                text=f"Show me a '{target_object}' from category '{selected_category}'.\n\nPress the button when ready.",
                font=("Arial", 14),
                wraplength=500,
                justify="center"
            )
            root.update_idletasks()     # Force GUI to update
            time.sleep(1.0)             # Give user a second to read

            image_path = f"/tmp/category.jpg"
    
            success = capture_image_with_preview(image_path)

            imageUrl = upload_image_to_cloudinary(image_path)

            detected = detect_objects(image_path)
            print("Detected:", detected)

            success = target_object in detected

            handle_alarm_result(
            success=success,
            mode=mode,
            refImageUrl = "",
            imageUrl=imageUrl,
            target_object=target_object,
            start_time=start_time,
            alarm_data=alarm_data,
            root=root,
            go_back_callback=go_back_callback,
            label=label
            )


    except Exception as e:
        label.config(text=f"Error: {e}", fg="red")

   
