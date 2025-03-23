import speech_recognition as sr
from difflib import SequenceMatcher

class AudioSensor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    @staticmethod
    def calculate_similarity(expected_sentence, user_sentence):
        return SequenceMatcher(None, expected_sentence.lower(), user_sentence.lower()).ratio() * 100