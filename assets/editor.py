# -*- coding: utf-8 -*-
"""Thin entry point for the Sisyphe.io level editor.

Launched as a separate process by the game (ui/main_menu.open_external_app) or
directly with ``python3 assets/editor.py``. All editor logic lives under
``assets/package/editor``.
"""
import os
import sys

# The assets directory (where img/, sfx/, mus/ live) — same value the original
# editor used as ``base_path``. Putting it on sys.path makes ``package`` importable.
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

from package.editor import app

if __name__ == "__main__":
    app.main(base_path)
