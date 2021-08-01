import os
import pygame as pg

import src.config as cfg


class Sound:
    """Class for handling all sounds in the game."""
    def __init__(self):
        """Loads all sounds and stores them."""
        self._sfx = {}
        print("Loading all sounds...")
        for filename in os.listdir(cfg.SND_DIR):
            if filename.endswith(".wav"):
                filepath = os.path.join(cfg.SND_DIR, filename)
                self._sfx[filename] = pg.mixer.Sound(filepath)

    def play_sfx(self, filename: str) -> None:
        """Plays a sound effect whose name is indicated by the provided filename."""
        self._sfx[filename].play()

    @staticmethod
    def play_music(filename: str, loops=0) -> None:
        pg.mixer.music.load(os.path.join(cfg.SND_DIR, filename))
        pg.mixer.music.play(loops)

    @staticmethod
    def stop_music() -> None:
        pg.mixer.music.stop()


# Global sound class.
_sound_loader = Sound()
# Interface methods for the global class.
play_sfx = _sound_loader.play_sfx
play_music = Sound.play_music
stop_music = Sound.stop_music
