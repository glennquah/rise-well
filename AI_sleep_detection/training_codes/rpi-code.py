import os
import time
import serial
import cv2
import mediapipe as mp
import pandas as pd

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

# CSV File to store data
csv_filename = "pose_sleep_data.csv"
buffer = []  # Buffer to store records before saving

# Set up Serial Connection with Microbit
try:
    microbit_serial = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    microbit_serial.flush()  # Flush serial buffer
except serial.serialutil.SerialException:
    print("Error: Could not open serial port. Microbit might be disconnected.")
    microbit_serial = None  # Prevent crashes


def extract_landmarks(image_path):
    """Extracts pose landmarks from an image file."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return None

    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.pose_landmarks:
        return None  # No landmarks detected

    # Extract (x, y, z) coordinates for all 33 landmarks
    landmarks = []
    print(results.pose_world_landmarks)
    for lm in results.pose_world_landmarks.landmark:
        landmarks.extend([lm.x, lm.y, lm.z])

    return landmarks


def capture_image():
    """Captures an image using ffmpeg and saves it."""
    image_path = "../../../GroupProject/ML-train/image.jpg"
    os.system(f"ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 {image_path} -y -loglevel quiet")
    return image_path


def save_data():
    """Saves buffered data to CSV every 10 records."""
    global buffer
    if len(buffer) >= 10:  # Save every 10 records
        columns = [f"landmark_{i}" for i in range(len(buffer[0]) - 1)] + ["label"]

        file_exists = os.path.isfile(csv_filename)

        df = pd.DataFrame(buffer, columns=columns)

        df.to_csv(csv_filename, mode='a', header=not file_exists, index=False)

        print(f"Saved {len(buffer)} records to CSV.")
        buffer.clear()  # Clear the buffer


while True:
    try:
        # Flush the buffer before reading
        microbit_serial.flushInput()

        # Read data from Microbit Serial
        try:
            data = microbit_serial.readline().decode('utf-8').strip()
            if not data:  # If no data is received, set label to -1
                data = "-1"
        except (serial.serialutil.SerialException, AttributeError):
            print("Warning: Microbit disconnected or Serial port busy.")
            data = "-1"

        label = -1 if data == "-1" else (1 if data == "SLEEP" else 0)
        print(f"Received from Microbit: {data}")

        # Capture Image
        image_path = capture_image()
        if not image_path:
            continue

        # Extract Pose Landmarks
        landmarks = extract_landmarks(image_path)
        if landmarks is None:
            print("No pose detected. Skipping entry.")
            continue

        # Store Data in Buffer
        buffer.append(landmarks + [label])
        print(f"Buffered {len(buffer)}/10 records.")

        # Save Data Every 10 Records
        save_data()

        # Reduce sleep time for faster updates
        time.sleep(1)

    except KeyboardInterrupt:
        print("Stopping data collection...")

        if buffer:
            save_data()  # Save remaining data

        break

# Close Serial Connection
if microbit_serial:
    microbit_serial.close()
