import time
from bluetooth import ble
from sensors.bleuartlib import BleUartDevice

stop_flag = False 

def uart_callback(data):
    global stop_flag
    if data:
        print(data)
        if "Game Over" in data:
            print("********** GAME OVER **********")
            stop_flag = True

def game_selection(bleUartDevice1):
    global stop_flag
    stop_flag = False
    print("Select difficulty: easy(5 shakes), medium(10 shakes), hard(15 shakes)")
    difficulty = input("Enter Difficulty: ").lower()
    levels = ['easy', 'medium', 'hard']
    while difficulty not in levels: 
        print("Try again")
        difficulty = input("Enter Difficulty: ").lower()
    send_difficulty(difficulty, bleUartDevice1)

def send_difficulty(difficulty, bleUartDevice1): 
    bleUartDevice1.send(difficulty)

def shake_game(): 
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
            print('Connected to micro:bit device')

            # Enable UART receiving with callback function
            bleUartDevice1.enable_uart_receive(uart_callback)

            game_selection(bleUartDevice1)
            while not stop_flag:
                time.sleep(1)  # Keep the script alive to process callbacks

    except KeyboardInterrupt:
        print('********** END **********')

    except Exception as e:
        print(f'********** UNKNOWN ERROR: {e}')

    finally:
        if bleUartDevice1:
            bleUartDevice1.disconnect()
            print('Disconnected from micro:bit device')

