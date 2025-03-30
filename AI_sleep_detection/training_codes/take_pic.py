import cv2
import os
import time

def take_pictures(sleep_mode=True):
    # Create 'image' folder if it doesn't exist
    if not os.path.exists('image'):
        os.makedirs('image')

    # Open the USB camera (camera 0 is the default)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture 50 pictures
    for i in range(50):
        # Capture a frame from the camera
        ret, frame = cap.read()

        # If the frame was successfully captured
        if ret:
            # Get current timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())

            # Set the file name based on sleep or awake mode
            if sleep_mode:
                filename = f"image/image_sleep_{timestamp}.jpg"
            else:
                filename = f"image/image_awake_{timestamp}.jpg"

            # Save the frame as an image file
            cv2.imwrite(filename, frame)
            print(f"Image saved as '{filename}'")

        # Wait for a short moment before taking the next picture
        time.sleep(4)

    # Release the camera
    cap.release()

# Call the function with sleep_mode=True (or False for awake)
take_pictures(sleep_mode=True)
