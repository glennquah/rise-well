import speech_recognition as sr
from difflib import SequenceMatcher

class AudioSensor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.collected_transcripts = []
        self.stop_listening = None

    def start_listening(self, callback):
        # Adjust for ambient noise and start background listening.
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        self.stop_listening = self.recognizer.listen_in_background(self.mic, callback)

    def stop_listening_func(self):
        if self.stop_listening:
            self.stop_listening(wait_for_stop=False)

    @staticmethod
    def calculate_similarity(expected_sentence, user_sentence):
        # Calculate similarity as a percentage.
        return SequenceMatcher(None, expected_sentence.lower(), user_sentence.lower()).ratio() * 100