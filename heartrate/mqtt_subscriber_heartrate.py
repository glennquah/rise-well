import os
import paho.mqtt.client as mqtt
import time
import pymongo
from dotenv import load_dotenv

load_dotenv()

# =============================================
# ================== MONGODB ==================
# =============================================

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")#"mongodb://localhost:27017/"
DB_NAME = os.getenv("MONGO_DB", "rise-well")#"mqtt_data"
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "heartrate")#"heartrate"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
print("Connected to MongoDB...")
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# =============================================
# =================== MQTT ====================
# =============================================

BROKER = os.getenv("MQTT_BROKER", "127.0.0.1")#"127.0.0.1"
PORT = int(os.getenv("MQTT_PORT", 1883))# 1883
TOPIC = os.getenv("MQTT_TOPIC", "sensors/heartrate")#"sensors/heartrate"

def on_connect(client, userdata, flags, rc):
    if not rc:
        print("Connected to MQTT Broker...")
    else:
        print("An error has occured")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection {rc}")

def on_message(client, userdata, message):
    message = message.payload.decode("utf-8")

    # Set data
    data = {
        "timestamp": time.time(),
        "heartrate": message
    }

    # Store data in MongoDB
    collection.insert_one(data)

    print(f"Value {message} added to MongoDB")

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(BROKER, PORT)
client.subscribe(TOPIC)
client.loop_forever()



