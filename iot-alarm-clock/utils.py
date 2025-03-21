import os
import pygame
import threading

pygame.mixer.init()
playing_thread = None

def play_alarm_sound():
    global playing_thread

    sound_file = os.path.join(os.path.dirname(__file__), "ringtones", "alarm1.wav")

    if not os.path.exists(sound_file):
        print("Sound file not found!")
        return

    def play_audio():
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play(loops=-1)

    playing_thread = threading.Thread(target=play_audio, daemon=True)
    playing_thread.start()
    print("Sound started...")

def stop_alarm_sound():
    pygame.mixer.music.stop()
    print("Sound stopped.")