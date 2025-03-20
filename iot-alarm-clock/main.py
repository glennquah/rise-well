import tkinter as tk
from alarm.alarm_manager import AlarmManager
from gui.start_window import start_window

alarm_manager = AlarmManager()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("White.TRadiobutton", background="white", foreground="black")
    rb = ttk.Radiobutton(root, text="Option", variable=tk.StringVar(), value="1", style="White.TRadiobutton")
    start_window(root, alarm_manager)
    root.mainloop()