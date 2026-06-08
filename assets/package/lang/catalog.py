# -*- coding: utf-8 -*-
"""Language registry and the Traduction holder (replaces game_lang.py).

Each language lives in its own ``lang/<code>.py`` module as a ``STRINGS`` dict.
``Traduction.apply(code)`` copies that language's strings onto the instance, so
reading ``lang.play_button`` etc. behaves exactly as in the original code where a
``french()`` / ``english()`` method set the attributes.
"""
from importlib import import_module

# Ordered list used to cycle languages in the settings menu.
LANGUAGES = ["fr", "en", "es", "it", "pt", "de", "ru", "zh_TW", "zh_CN", "jp", "ko", "ar"]

# Code -> display name (the old Traduction.selection dict).
DISPLAY_NAMES = {
    "fr": "Français",
    "en": "English",
    "es": "Español",
    "it": "Italiano",
    "pt": "Português",
    "de": "Deutsch",
    "ru": "Pусский",
    "zh_TW": "繁體中文",
    "zh_CN": "简体中文",
    "jp": "日本語",
    "ko": "한국어",
    "ar": "العربية",
}

# Code -> module name (filenames must be valid lowercase identifiers).
_MODULES = {
    "fr": "fr", "en": "en", "es": "es", "it": "it", "pt": "pt", "de": "de",
    "ru": "ru", "zh_TW": "zh_tw", "zh_CN": "zh_cn", "jp": "jp", "ko": "ko", "ar": "ar",
}


class Traduction:
    def __init__(self):
        self.selection = dict(DISPLAY_NAMES)

    def apply(self, code):
        """Load ``code``'s strings onto this instance."""
        assert code in LANGUAGES
        module = import_module(f"{__package__}.{_MODULES[code]}")
        self.__dict__.update(module.STRINGS)
