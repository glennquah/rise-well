import base64

import paho.mqtt.client as mqtt


BROKER = "192.168.50.83"
PORT = 1883
TOPIC = "image_data"


def on_message(client, userdata, msg):
    print("Image data received!")
    prediction = base64.b64decode(msg.payload)
    #
    # decoded_list = [json.loads(json_data)]

    # process json_data
    # print(decoded_list)

    print("sleep" if prediction[0] == 0 else "awake")

# Send to on_message
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_forever()
