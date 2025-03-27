import speech_recognition as sr
from difflib import SequenceMatcher

class AudioSensor:
    def __init__(self, device_index=None):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=device_index)
        self.collected_transcripts = []
        self.stop_listening = None

    def start_listening(self, callback):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        self.stop_listening = self.recognizer.listen_in_background(self.mic, callback)

    def stop_listening_func(self):
        if self.stop_listening:
            try:
                # Use wait_for_stop=False to avoid joining mid-callback.
                self.stop_listening(wait_for_stop=False)
            except Exception as e:
                print("Error in stop_listening_func:", e)
            self.stop_listening = None

    @staticmethod
    def calculate_similarity(expected_sentence, user_sentence):
        return SequenceMatcher(None, expected_sentence.lower(), user_sentence.lower()).ratio() * 100