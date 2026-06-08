# -*- coding: utf-8 -*-
"""Looping background music via pygame.mixer (top half of the old game_music.py)."""
import pygame

pygame.mixer.init()

# Path of the track currently playing, so we don't restart the same one.
current_music_path = None


def play_music(path):
    """Play ``path`` on infinite loop, unless it is already the active track."""
    global current_music_path
    if path != current_music_path:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)  # Boucle infinie
        current_music_path = path


def stop_music():
    """Stop the current track (if any)."""
    global current_music_path
    if current_music_path is not None:
        pygame.mixer.music.stop()
        current_music_path = None


def set_volume(volume):
    """Set music volume from the 0..20 settings scale (0 = 0%, 20 = 100%)."""
    volume = volume * 5    # 0..20 -> percentage
    volume = volume / 100  # percentage -> pygame's 0.0..1.0
    pygame.mixer.music.set_volume(volume)


def get_volume():
    """Return pygame's current music volume (0.0..1.0)."""
    return pygame.mixer.music.get_volume()
