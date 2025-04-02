import tkinter as tk
from tkinter import ttk
from gui.start_window import start_window
import threading
from sensors import serial_heartrate_reader  # 👈 import your function

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("White.TRadiobutton", background="white", foreground="black")
    rb = ttk.Radiobutton(root, text="Option", variable=tk.StringVar(), value="1", style="White.TRadiobutton")

    

    Start serial listener in background thread
    serial_thread = threading.Thread(target=serial_heartrate_reader.start_serial_listener, daemon=True)
    serial_thread.start()


    
    start_window(root)
    root.mainloop()
