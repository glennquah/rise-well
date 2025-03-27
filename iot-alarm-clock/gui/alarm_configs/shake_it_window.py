import tkinter as tk
from tkinter import ttk
# import threading
# import time
# from bluetooth import ble
# from bleuartlib import BleUartDevice
from gui.count_down_window import count_down_window


# stop_flag = False 

# def uart_callback(data):
#     global stop_flag
#     if data:
#         print(data)
#         if "Game Over" in data:
#             print("********** GAME OVER **********")
#             stop_flag = True

# def send_difficulty(difficulty, bleUartDevice1): 
#     bleUartDevice1.send(difficulty)

# def shake_game(difficulty): 
#     global stop_flag
#     stop_flag = False  # Reset stop flag

#     try:
#         bleUartDevice1 = None
#         found_microbit = False

#         service = ble.DiscoveryService()
#         devices = service.discover(5)

#         print('********** Initiating device discovery......')

#         for address, name in devices.items():
#             if address == 'E5:AA:61:83:73:1F':  # Ensure this matches your micro:bit's address
#                 print(f'Found BBC micro:bit [vavet]: {address}')
#                 found_microbit = True
#                 break

#         if found_microbit:
#             bleUartDevice1 = BleUartDevice(address)
#             bleUartDevice1.connect()
#             print('Connected to micro:bit device')

#             # Enable UART receiving with callback function
#             bleUartDevice1.enable_uart_receive(uart_callback)

#             # Send difficulty directly
#             send_difficulty(difficulty, bleUartDevice1)

#             while not stop_flag:
#                 time.sleep(1)  # Keep script alive to process callbacks

#     except KeyboardInterrupt:
#         print('********** END **********')

#     except Exception as e:
#         print(f'********** UNKNOWN ERROR: {e}')

#     finally:
#         if bleUartDevice1:
#             bleUartDevice1.disconnect()
#             print('Disconnected from micro:bit device')


def shake_it_window(root: tk.Tk, alarm_data, go_back_callback):
    """GUI for selecting shake difficulty"""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Shake Game Configuration")
    alarm_data["config"] = {}

    tk.Label(root, text="Select Difficulty", bg="white").pack(pady=5)
    difficulty = tk.StringVar(value="easy")  # Set default to "easy"
    
    ttk.Radiobutton(root, text="Easy", variable=difficulty, value="easy", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Medium", variable=difficulty, value="medium", style="White.TRadiobutton").pack()
    ttk.Radiobutton(root, text="Hard", variable=difficulty, value="hard", style="White.TRadiobutton").pack()

    def next_action():
        alarm_data["config"]["difficulty"] = difficulty.get()
        count_down_window(root,alarm_data, go_back_callback)

    ttk.Button(root, text="Submit Alarm", command=next_action).pack(pady=10)
    ttk.Button(root, text="Back", command=go_back_callback).pack(pady=5)
