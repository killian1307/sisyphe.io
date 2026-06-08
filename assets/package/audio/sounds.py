# -*- coding: utf-8 -*-
"""One-shot sound effects (the SoundManager class from the old game_music.py),
plus the table that loads every game sound from the assets folder."""
import os

import pygame

# Logical name -> file inside assets/sfx (was the 14 load_sound calls in app.py).
SOUND_FILES = {
    'steps1': 'footsteps1.wav',
    'steps2': 'footsteps2.wav',
    'small_win': 'level_completed.wav',
    'big_win': 'world_completed.wav',
    'hole_filled': 'hole_filled.wav',
    'portal': 'portal_entered.wav',
    'powerup': 'powerup_taken.wav',
    'break': 'wall_broken.wav',
    'door': 'door_opened.wav',
    'door2': 'door_closed.wav',
    'button': 'button_pressed.wav',
    'reset': 'reset_level.wav',
    'menu': 'return_menu.wav',
    'popup': 'popup_menu.wav',
}


class SoundManager:
    def __init__(self):
        self.sounds = {}

    def load_sound(self, name, path):
        self.sounds[name] = pygame.mixer.Sound(path)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def set_volume(self, volume):
        # 0..20 settings scale -> pygame's 0.0..1.0
        volume = volume * 5
        volume = volume / 100
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def get_volume(self, name):
        assert name in self.sounds.keys(), "Le son rentré n'est pas valide"
        return self.sounds[name].get_volume()


def load_all_sounds(manager, assets_dir):
    """Load every game sound into ``manager`` from ``assets/sfx``."""
    for name, filename in SOUND_FILES.items():
        manager.load_sound(name, os.path.join(assets_dir, 'assets', 'sfx', filename))
