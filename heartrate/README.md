# Heart Rate Monitoring System

This system reads heart rate data from a **BBC micro:bit**, sends it via **MQTT**, and stores it in **MongoDB**.

---

## 📌 How It Works
1. **Micro:bit** reads heart rate and sends it via **serial**.
2. **MQTT Publisher** reads serial data and **publishes** it.
3. **MQTT Subscriber** receives the data and **stores it in MongoDB**.

---

## 🔧 Setup

### 1️⃣ Install Dependencies
```sh
pip install paho-mqtt pymongo python-dotenv pyserial
```

### 2️⃣ Configure `.env`
Create a `.env` file:
```
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=mqtt_data
MONGO_COLLECTION=heartrate

MQTT_BROKER=127.0.0.1
MQTT_PORT=1883
MQTT_TOPIC=sensors/heartrate
```

### 3️⃣ Flash Micro:bit
2. **Flash** the hex file onto the Micro:bit.

### 4️⃣ Run the System
Start the **MQTT Publisher** (reads serial data and publishes to MQTT):
```sh
python mqtt_publisher_heartrate.py
```
Start the **MQTT Subscriber** (receives data and saves it to MongoDB):
```sh
python mqtt_subscriber_heartrate.py
```
