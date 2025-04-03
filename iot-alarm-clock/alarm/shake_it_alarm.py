import tkinter as tk
from tkinter import ttk
import time
import datetime
import threading
from utils import stop_alarm_sound
from apis.api_client import post_alarm_history
import serial  


stop_flag = False 
start_time = datetime.datetime.now()
total_score = 0
message = ''

#TODO: Change serial port accordingly (use command: `ls /dev/ttyUSB* /dev/ttyACM* /dev/serial/by-id/` )
ser = serial.Serial(port='/dev/ttyACM1', baudrate=115200, timeout=1)

def trigger(alarm, root: tk.Tk, go_back_callback): 
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Shake It Alarm")

    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")
    print(f"difficulty: {difficulty}")

    display_label = tk.Label(root, text="", font=("Arial", 14), bg="white")
    display_label.pack(pady=10)

    def uart_callback(data):
        global start_time
        global total_score

        def update_display():
            global stop_flag
            global message
            end_time = datetime.datetime.now()
            time_taken = end_time - start_time
            print("ending")
            message = "\n".join([
                "Challenge completed!",
                f"Shake it count: {total_score}",
                f"Time taken: {str(time_taken).split('.')[0]}"
            ])
            display_label.after(0, lambda: display_label.config(text=message))
            back_button = tk.Button(root, text="Back", command=go_back_callback, bg="white")
            back_button.pack(pady=10)
            stop_alarm_sound()
            payload = {
                "userId": alarm.get("userId"),
                "alarmType": "Shake It",
                "alarmTime": start_time.isoformat(),
                "difficulty": difficulty,
                "resolvedTime": end_time.isoformat(),
                "shakeCount": total_score,
            }
            post_alarm_history(payload)
            stop_flag = True

        try:
            cleaned_data = data.strip().replace('\x00', '')
            if cleaned_data != 'm2':
                print(f"shake count: {cleaned_data}")
                score = int(cleaned_data)
                total_score = score
                update_display()
        except Exception as e:
            print(f"Error: {e}")

    def shake_game(difficulty): 
        global stop_flag
        global start_time
        stop_flag = False 
        print(f"Shake it level: {difficulty}\n Initiating shake...")
        
        try:
            ser.write(difficulty.encode() + b"\n")
            
            display_label.config(text="Start shaking!")
            start_time = datetime.datetime.now()

            while not stop_flag:
                if ser.in_waiting > 0:
                    data = ser.readline().decode().strip()
                    if data:
                        uart_callback(data)
                time.sleep(0.1)

        except serial.SerialException as e:
            print(f"Serial connection error: {e}")
            display_label.config(text="Failed to connect via USB.")

    def run_game(): 
        shake_game(difficulty) 
    
    threading.Thread(target=run_game, daemon=True).start()

