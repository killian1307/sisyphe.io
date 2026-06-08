# -*- coding: utf-8 -*-
"""Cross-platform path resolution for bundled assets and per-user save data.

Replaces the original Windows-only ``os.environ['LOCALAPPDATA']`` lookups so the
game runs on Windows, macOS and Linux while keeping the Windows location
identical to before.
"""
import os
import sys

APP_NAME = 'Sisyphe.io'


def asset_root(fichier_exe=False):
    """Base path that the ``assets`` folder lives under.

    In development this is ``''`` (assets resolved relative to the CWD, exactly
    like the original code). When compiled to a .exe with PyInstaller the data is
    unpacked to ``sys._MEIPASS``.
    """
    if fichier_exe:
        return sys._MEIPASS
    return ''


def asset(asset_root_path, *parts):
    """Build a path inside the bundled ``assets`` folder."""
    return os.path.join(asset_root_path, 'assets', *parts)


def user_data_dir(app_name=APP_NAME):
    """Per-user writable directory for settings.json and scores.db.

    Windows : ``%LOCALAPPDATA%/<app>``  (unchanged from the original)
    macOS   : ``~/Library/Application Support/<app>``
    Linux   : ``$XDG_DATA_HOME/<app>`` or ``~/.local/share/<app>``
    """
    if sys.platform == 'win32':
        base = os.environ.get('LOCALAPPDATA') or os.path.expanduser(r'~\AppData\Local')
    elif sys.platform == 'darwin':
        base = os.path.expanduser('~/Library/Application Support')
    else:
        base = os.environ.get('XDG_DATA_HOME') or os.path.expanduser('~/.local/share')
    return os.path.join(base, app_name)
