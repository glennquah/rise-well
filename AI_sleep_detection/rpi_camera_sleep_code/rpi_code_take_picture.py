import base64
import json
import os
import time

import cv2
import joblib
import mediapipe as mp
import paho.mqtt.client as mqtt

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)


# Function to capture an image using the Raspberry Pi camera
def capture_image():
    """Captures an image using the Raspberry Pi camera and saves it."""
    image_path = "/home/pi/image.jpg"

    # Initialize the camera (using OpenCV)
    cap = cv2.VideoCapture(0)  # 0 is typically the default camera
    ret, frame = cap.read()

    if ret:
        cv2.imwrite(image_path, frame)  # Save the captured image
        cap.release()
        return image_path
    else:
        cap.release()
        return None


# Function to extract pose landmarks
def extract_landmarks(image_path):
    """Extract pose landmarks from the image using mediapipe."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error reading image.")
        return None

    # Convert the image to RGB (as mediapipe uses RGB)
    image_resized = cv2.resize(image, (640, 640))
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

    # Process the image to get landmarks
    result = pose.process(image_rgb)

    if result.pose_world_landmarks:
        landmarks = []
        for landmark in result.pose_world_landmarks.landmark:
            landmarks.append({
                "x": landmark.x,
                "y": landmark.y,
                "visibility": landmark.visibility
            })
        return landmarks
    return None


# Function to send data to RabbitMQ
def send_data(data):
    """Publish image data to RabbitMQ."""
    client.publish(TOPIC, data)
    print("Image data sent successfully!")

def load_model():
    loaded_model = joblib.load('pose_sleep_model.sav')
    scalar = joblib.load('pose_sleep_scaler.sav')
    return loaded_model, scalar

def predict(data):
    global model
    # Get the model's predictions
    prediction = model.predict(data)

    return prediction

# RabbitMQ Server Details
BROKER = "192.168.50.83"  # Change to your RabbitMQ server IP
PORT = 1883
TOPIC = "image_data"

# Setup MQTT Client
client = mqtt.Client()
client.connect(BROKER, PORT)

while True:
    image_path = capture_image()
    model, scaler = load_model()

    if not image_path:
        print("Failed to capture image.")
        continue

    # Extract Pose Landmarks
    landmarks = extract_landmarks(image_path)
    if landmarks is None:
        print("No pose detected. Skipping entry.")
        continue

    landmarks = scaler.transform([landmarks])
    prediction = predict(landmarks)

    # Encode landmarks to JSON, then base64
    encoded_landmarks = base64.b64encode(prediction.encode('utf-8'))

    # Send encoded landmarks data over MQTT
    send_data(encoded_landmarks)

    time.sleep(10)  # Capture and send image every 10 seconds
