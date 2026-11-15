# serial_reader.py
import os
import time
import pymongo
import serial
import platform
import glob
import sys

# Configure a database you control; never commit credentials.
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DEVICE_USER_ID = os.environ["RISEWELL_USER_ID"]

DB_NAME = os.getenv("MONGO_DB", "rise-well")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "heartrate")#heartrate

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def upload_to_mongo(data):
    data_encapsulated = {
        "timestamp": time.time(),
        "heartrate": data,
        "userId": DEVICE_USER_ID,
    }
    collection.insert_one(data_encapsulated)
    print(f"Value {data_encapsulated} added to MongoDB2")

def get_serial_ports():
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
            return port
        except (OSError, serial.SerialException):
            pass
    return None

def start_serial_listener():
    # SERIAL_PORT = get_serial_ports()
    SERIAL_PORT = "/dev/ttyACM0"
    if not SERIAL_PORT:
        print("No serial ports found. Check your connection.")
        return

    print(f"Using serial port: {SERIAL_PORT}")

    BAUD_RATE = 115200
    TIMEOUT = 1

    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
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
