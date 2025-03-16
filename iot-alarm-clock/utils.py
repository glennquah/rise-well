import pygame
import os

def init_sound():
    pygame.mixer.init()

def play_alarm_sound():
    if not pygame.mixer.get_init():
        init_sound()
    sound_file = os.path.join(os.path.dirname(__file__), "ringtones", "alarm1.wav")
    if os.path.exists(sound_file):
        sound = pygame.mixer.Sound(sound_file)
        sound.play()