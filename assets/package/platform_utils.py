# -*- coding: utf-8 -*-
"""Small cross-platform helpers for the bits that were Windows-only.

Windows behavior is preserved; on macOS/Linux these degrade gracefully instead
of raising. Uses the standard library only (no new dependencies).
"""
import os
import sys
import webbrowser


def open_url(url):
    """Open a URL in the default browser (replaces ``os.system('start "" url')``)."""
    webbrowser.open(url)


def set_window_icon(window, ico_path, png_path):
    """Set the window/taskbar icon.

    Windows uses the original ``.ico`` via ``iconbitmap``; elsewhere we fall back
    to a PNG via ``iconphoto`` (``.ico`` + ``iconbitmap`` is Windows-only in Tk).
    """
    try:
        if sys.platform == 'win32':
            window.iconbitmap(ico_path)
        else:
            from PIL import Image, ImageTk
            icon = ImageTk.PhotoImage(Image.open(png_path))
            window._icon_ref = icon  # keep a reference so Tk doesn't garbage-collect it
            window.iconphoto(True, icon)
    except Exception:
        pass


def cursor_spec(assets_dir):
    """Return a Tk cursor spec for the custom ``.cur`` cursor, or '' for default.

    The ``@file.cur`` syntax is only supported on Windows; macOS Aqua rejects it,
    so everywhere else we return '' (the default arrow).
    """
    if sys.platform != 'win32':
        return ''
    path = os.path.join(assets_dir, 'assets', 'img', 'cur', 'normal.cur').replace('\\', '/')
    return f'@{path}'
