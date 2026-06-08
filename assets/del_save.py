# -*- coding: utf-8 -*-
"""Delete the per-user save directory (settings.json + scores.db).

Run with:  python3 assets/del_save.py
Uses the same cross-platform location as the game (see package/paths.py).
"""
import os
import shutil
import sys

# Make the 'package' importable so we reuse the game's path resolution.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from package import paths

target_dir = paths.user_data_dir()

if os.path.exists(target_dir):
    shutil.rmtree(target_dir)
