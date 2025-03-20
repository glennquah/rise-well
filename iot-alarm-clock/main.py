from alarm.alarm_manager import AlarmManager
from gui.start_window import start_window

alarm_manager = AlarmManager()

if __name__ == "__main__":
    start_window(alarm_manager)