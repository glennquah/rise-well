import tkinter as tk
from tkinter import ttk
from alarm.alarm_manager import AlarmManager
from gui.add_alarm_window import add_alarm_window

alarm_manager = AlarmManager()

root = tk.Tk()
root.title("RiseWell")
tk.Label(root, text="Welcome to RiseWell, add your alarm now").pack()
tk.Button(root, text="Add Alarm", command=add_alarm_window).pack()
root.mainloop()