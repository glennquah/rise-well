import tkinter as tk
from tkinter import ttk
from bluetooth import ble
from bleuartlib import BleUartDevice
import time
import datetime
import threading
from utils import stop_alarm_sound
from apis.api_client import post_alarm_history

stop_flag = False 
start_time = datetime.datetime.now()
total_score = 0
message = ''

def trigger(alarm, root: tk.Tk, go_back_callback): 
    root.configure(bg="white")
    for widget in root.winfo_children():
        widget.destroy()
    root.title("Shake It Alarm")

    config = alarm.get("config", {})
    difficulty = config.get("difficulty", "Easy")

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
            print(f"updating{total_score}")
            message = "\n".join([
                "Challenge completed!",
                f"Shake it count: {total_score}",
                f"Time taken: {str(time_taken).split('.')[0]}"
            ])
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
            score = int(cleaned_data)
            print(f"score:{score} ")
            total_score = score
            update_display()
        except Exception as e:
            print(f"Error: {e}")

    def shake_game(difficulty): 
        global stop_flag
        global start_time
        stop_flag = False 
        display_label.config(text=f"Shake it level: {difficulty}\n Initiating shake...")

        try:
            bleUartDevice1 = None
            found_microbit = False

            service = ble.DiscoveryService()
            devices = service.discover(5)

            print('********** Initiating device discovery......')

            for address, name in devices.items():
                if address == 'E5:AA:61:83:73:1F':  # Ensure this matches your micro:bit's address
                    print(f'Found BBC micro:bit [vavet]: {address}')
                    found_microbit = True
                    break

            if found_microbit:
                bleUartDevice1 = BleUartDevice(address)
                bleUartDevice1.connect()
                print('connected to micro:bit')
                display_label.config(text="Start shaking!")
                start_time = datetime.datetime.now()

                # Enable UART receiving with callback function
                bleUartDevice1.enable_uart_receive(uart_callback)

                # Send difficulty directly
                bleUartDevice1.send(difficulty)

                while not stop_flag:
                    time.sleep(1)  # Keep script alive to process callbacks

        except KeyboardInterrupt:
            print('********** END **********')

        except Exception as e:
            print(f'********** UNKNOWN ERROR: {e}')

        finally:
            if bleUartDevice1:
                bleUartDevice1.disconnect()
                display_label.config(text=message)
                back_button = tk.Button(root, text="Back", command=go_back_callback, bg="white")
                back_button.pack(pady=10)

    def run_game(): 
        shake_game(difficulty) 

    threading.Thread(target=run_game, daemon=True).start()

