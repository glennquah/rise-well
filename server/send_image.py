import os
import time
import paho.mqtt.client as mqtt
import base64

# RabbitMQ Server Details
BROKER = "192.168.50.83"  # Change to your RabbitMQ server IP
PORT = 1883
TOPIC = "image_data"


# Function to capture image using FFmpeg
def capture_image():
    image_path = "image.jpg"
    os.system(f"ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 {image_path} -y")
    return image_path


# Function to send image data via MQTT
def send_image():
    image_path = capture_image()

    # Convert image to Base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Publish to RabbitMQ
    client.publish(TOPIC, encoded_string)

    print("Image sent successfully!")


# Capture and send an image every 10 seconds
client = mqtt.Client()
client.connect(BROKER, PORT)
while True:
    send_image()
    time.sleep(10)
