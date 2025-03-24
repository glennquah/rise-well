from time import sleep

import cv2
import joblib
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)


def __capture_image__():
    """Captures an image using the Raspberry Pi camera and saves it."""
    image_path = "./image.jpg"

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


def __load_model__():
    loaded_model = joblib.load('pose_sleep_model.sav')
    scalar = joblib.load('pose_sleep_scaler.sav')
    return loaded_model, scalar


def __predict__(data):
    global model
    # Get the model's predictions
    prediction = model.predict(data)

    return prediction


def __extract_landmarks__(image_path):
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
            landmarks.extend([landmark.x, landmark.y, landmark.visibility])

        return landmarks
    return None


def __ai_predict__():
    """
    Takes a picture and predict if someone is sleeping or not.
    :return:
    -1 : should try again
    AWAKE: person is awake
    SLEEP: person is sleeping
    """
    image_path = __capture_image__()
    model, scaler = __load_model__()

    if not image_path:
        print("Failed to capture image.")
        return -1

    # Extract Pose Landmarks
    landmarks = __extract_landmarks__(image_path)
    if landmarks is None:
        print("No pose detected. Skipping entry.")
        return -1

    landmarks = scaler.transform([landmarks])
    prediction = __predict__(landmarks)

    return "SLEEP" if prediction[0] == 0 else "AWAKE"


def checks_if_user_is_awake():
    detection = __ai_predict__()
    while detection != "AWAKE":
        if detection == -1:
            checks_if_user_is_awake()
            return
        else:
            print("User not awake. Sleeping for 5 minutes...")
            sleep(300) # 5 mins
            detection = __ai_predict__()

