import joblib
import paho.mqtt.client as mqtt
import base64

BROKER = "192.168.50.83"
PORT = 1883
TOPIC = "image_data"

def load_model():
    loaded_model = joblib.load('')


def on_message(client, userdata, msg):
    print("Image data received!")
    image_data = base64.b64decode(msg.payload)

    with open("received_image.jpg", "wb") as f:
        f.write(image_data)

    print("Image saved as received_image.jpg")


client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_forever()


