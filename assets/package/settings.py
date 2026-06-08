# -*- coding: utf-8 -*-
"""Loading, saving and seeding of the user settings.json file.

Centralizes the many ``open(.../settings.json)`` / ``json.dump`` call sites that
were scattered across the original app.py.
"""
import json
import os
import shutil

from . import paths

REQUIRED_KEYS = ["controles", "mondes", "tutoriels", "fps", "volume", "language"]


def settings_dir():
    """Per-user directory that holds settings.json (and scores.db)."""
    return paths.user_data_dir()


def settings_path():
    return os.path.join(settings_dir(), 'settings.json')


def ensure_user_copy(assets_dir):
    """Create the user data dir and seed settings.json from the bundled default.

    Mirrors the original ``extract_settings()`` and returns the directory path.
    """
    target = settings_dir()
    if not os.path.exists(target):
        os.makedirs(target, exist_ok=True)
    if not os.path.exists(os.path.join(target, 'settings.json')):
        default = paths.asset(assets_dir, 'settings.json')
        shutil.copy(default, target)
    return target


def load():
    """Read and return the settings dict."""
    with open(settings_path(), 'r') as fichier:
        return json.load(fichier)


def save(params):
    """Persist the settings dict (pretty-printed, like the original)."""
    with open(settings_path(), 'w') as fichier:
        json.dump(params, fichier, indent=4)
