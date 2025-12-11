"""Playing .wav voice or sound"""

import winsound

def play_sound(path:str):
    winsound.PlaySound(path, winsound.SND_FILENAME)