import threading
import time
import json
import os
from datetime import datetime
from alarm import math_alarm
# import nothing_alarm
# import shake_it_alarm
# import speech_alarm
# import image_recognition_alarm

alarms_file = "alarms.json"

class AlarmManager:
    def __init__(self):
        self.alarms = []
        self.load_alarms()
        self.running = True
        self.thread = threading.Thread(target=self.check_alarms)
        self.thread.daemon = True
        self.thread.start()

    def load_alarms(self):
        if os.path.exists(alarms_file):
            with open(alarms_file, "r") as f:
                self.alarms = json.load(f)
        else:
            self.alarms = []

    def save_alarms(self):
        with open(alarms_file, "w") as f:
            json.dump(self.alarms, f)

    def add_alarm(self, alarm):
        self.alarms.append(alarm)
        self.save_alarms()

    def check_alarms(self):
        while self.running:
            now = datetime.now().strftime("%H:%M")
            for alarm in self.alarms:
                if not alarm.get("triggered") and alarm["time"] == now:
                    alarm["triggered"] = True
                    self.trigger_alarm(alarm)
                    self.save_alarms()
            time.sleep(30)

    def trigger_alarm(self, alarm):
        t = alarm["type"]
        if t == "Math":
            math_alarm.trigger(alarm)
        # elif t == "Nothing":
        #     nothing_alarm.trigger(alarm)
        # elif t == "Shake It":
        #     shake_it_alarm.trigger(alarm)
        # elif t == "Speech":
        #     speech_alarm.trigger(alarm)
        # elif t == "Image Recognition":
        #     image_recognition_alarm.trigger(alarm)