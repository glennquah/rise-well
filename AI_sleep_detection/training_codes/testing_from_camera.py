import json
import joblib
import numpy as np
import paho.mqtt.client as mqtt
import base64
import cv2
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import mediapipe as mp

BROKER = "192.168.50.83"
PORT = 1883
TOPIC = "image_data"
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)


def load_model():
    loaded_model = joblib.load('pose_sleep_model.sav')
    scalar = joblib.load('pose_sleep_scaler.sav')
    return loaded_model, scalar




def predict(data):
    global model
    # Get the model's predictions
    prediction = model.predict(data)

    return prediction


def on_message(client, userdata, msg):
    print("Image data received!")
    # json_data = base64.b64decode(msg.payload).decode('utf-8')
    #
    # decoded_list = [json.loads(json_data)]

    # process json_data
    # print(decoded_list)

    df = pd.DataFrame([msg])
    df_scaled = scaler.fit_transform(df)

    result = predict(df_scaled)

    print(result)


def take_picture():
    # Open the USB camera (camera 0 is the default)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
    else:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # If the frame was successfully captured
        if ret:
            # Save the frame as an image file
            cv2.imwrite('captured_image.jpg', frame)
            print("Image saved as 'captured_image.jpg'")

    # Release the camera
    cap.release()


def extract_landmarks(image_path):
    """Extracts pose landmarks from an image file."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not load image.")
        return None

    # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # value = 42  # whatever value you want to add
    # hsv[:, :, 2] = cv2.add(hsv[:, :, 2], value)
    # image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    image_resized = cv2.resize(image, (640, 640))
    image_rgb = cv2.cvtColor(image_resized, cv2.COLOR_BGR2RGB)

    results = pose.process(image_rgb)

    if not results.pose_world_landmarks:
        return None  # No landmarks detected

    # Extract (x, y, z) coordinates for all 33 landmarks
    landmarks = []
    for lm in results.pose_world_landmarks.landmark:
        landmarks.extend([lm.x, lm.y, lm.visibility])
    print(landmarks)
    return landmarks


model, scaler = load_model()
# Take a picture,
take_picture()
# mediapipe pose it
landmarks = extract_landmarks('captured_image.jpg')
landmarks = scaler.transform([landmarks])
prediction = predict(landmarks)
print("sleep" if prediction[0] == 0 else "awake")

# if landmarks:
#     # Draw the landmarks on the image
#     draw_landmarks('captured_image.jpg', landmarks)

# Send to on_message
# on_message(None, None, landmarks)

# client = mqtt.Client()
# client.on_message = on_message
# client.connect(BROKER, PORT)
# client.subscribe(TOPIC)
# client.loop_forever()
