# Takes pictures
# mediapipe to get the world landmarks
# Send to the rabbitmq
import base64
import json
import os
import time

import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)


def capture_image():
    """Captures an image using ffmpeg and saves it."""
    image_path = "./image.jpg"
    os.system(f"ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 {image_path} -y -loglevel quiet")
    return image_path


def send_data(data):
    # Publish to RabbitMQ
    client.publish(TOPIC, data)

    print("Image sent successfully!")

# RabbitMQ Server Details
BROKER = "192.168.50.83"  # Change to your RabbitMQ server IP
PORT = 1883
TOPIC = "image_data"

# Capture and send an image every 10 seconds
client = mqtt.Client()
client.connect(BROKER, PORT)

while True:
    image_path = capture_image()

    if not image_path:
        continue

    # Extract Pose Landmarks
    landmarks = extract_landmarks(image_path)
    if landmarks is None:
        print("No pose detected. Skipping entry.")
        continue
    json_encoded_landmarks = json.dumps(landmarks)
    send_data(base64.b64encode(json_encoded_landmarks.encode('utf-8')))
    time.sleep(2)

