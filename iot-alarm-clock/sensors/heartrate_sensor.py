import os
import time
import paho.mqtt.client as mqtt
import pymongo
import serial
import platform
import glob
import sys

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

def upload_to_mongo(data):
    # message = message.payload.decode("utf-8")

    # Set data
    data_encapsulated = {
        "timestamp": time.time(),
        "heartrate": data
    }

    # Store data in MongoDB
    collection.insert_one(data_encapsulated)

    print(f"Value {data} added to MongoDB")

# =============================================
# ============= AUTO-DETECT SERIAL ============
# =============================================

def get_serial_ports():
    """
    Detects available serial ports based on the operating system.

    Returns:
        str: The first available serial port or None if none found.
    """
    system_os = platform.system()

    if system_os == "Windows":
        ports = [f'COM{i}' for i in range(1, 257)]
    elif system_os == "Linux":
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        raise SystemError(f"Unsupported OS: {system_os}")

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            return port  # Return first available port
        except (OSError, serial.SerialException):
            pass
    return None

SERIAL_PORT = get_serial_ports()
if not SERIAL_PORT:
    print("No serial ports found. Check your connection.")
    sys.exit(1)

BAUD_RATE = 115200
TIMEOUT = 1

print(f"Using serial port: {SERIAL_PORT}")

# =============================================
# ================== SERIAL ===================
# =============================================

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            #send data to database
            #client.publish(TOPIC, data)
            upload_to_mongo(data)
            print(f"Uploaded: {data}")
except serial.SerialException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("User interrupted")
finally:
    if ser.is_open:
        ser.close()
    print("Serial port closed")

client.loop_stop()
client.disconnect()
