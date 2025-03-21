import paho.mqtt.client as mqtt
import serial
import platform
import glob
import sys

# =============================================
# ================== MQTT =====================
# =============================================

BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "sensors/heartrate"

def on_connect(client, userdata, flags, rc):
    if not rc:
        print("Connected to MQTT Broker...")
    else:
        print("An error has occurred")

def on_publish(client, userdata, mid):
    print(f'{mid} published')

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect

client.connect(BROKER, PORT)
client.loop_start()

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
            client.publish(TOPIC, data)
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
