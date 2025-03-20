import tkinter as tk
from alarm.alarm_manager import AlarmManager
from gui.start_window import start_window

alarm_manager = AlarmManager()

if __name__ == "__main__":
    root = tk.Tk()
    start_window(root, alarm_manager)
    root.mainloop()