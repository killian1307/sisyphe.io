# -*- coding: utf-8 -*-
"""Uniform scaling transform between the game's logical 800x600 layout and the
actual (possibly fullscreen) window.

Every draw/place site maps logical coordinates through :func:`X`/:func:`Y`, sizes
through :func:`S`, and fonts through :func:`F`/:func:`font`. In windowed mode the
factor is 1 and the offset 0, so the transform is the identity and rendering is
unchanged. Fullscreen picks an integer-snapped cell size (crisp pixels) and
centres the 4:3 content, leaving margins that gameplay fills with tiled wall.
"""
from . import context

LOGICAL_W = 800
LOGICAL_H = 600
BASE_CELL = 50

# Current transform state.
scale = 1.0
off_x = 0.0
off_y = 0.0
cell = BASE_CELL
screen_w = LOGICAL_W
screen_h = LOGICAL_H


def configure(win_w, win_h):
    """Fit the 800x600 layout into ``win_w`` x ``win_h``, centred, integer cell."""
    global scale, off_x, off_y, cell, screen_w, screen_h
    screen_w, screen_h = win_w, win_h
    factor = min(win_w / LOGICAL_W, win_h / LOGICAL_H)
    cell = max(1, int(BASE_CELL * factor))   # integer cell -> crisp board
    scale = cell / BASE_CELL
    off_x = (win_w - LOGICAL_W * scale) / 2.0
    off_y = (win_h - LOGICAL_H * scale) / 2.0


def reset():
    """Back to the 1:1 windowed transform (identity)."""
    global scale, off_x, off_y, cell, screen_w, screen_h
    scale, off_x, off_y, cell = 1.0, 0.0, 0.0, BASE_CELL
    screen_w, screen_h = LOGICAL_W, LOGICAL_H


def X(v):
    """Logical x -> screen x."""
    return off_x + v * scale


def Y(v):
    """Logical y -> screen y."""
    return off_y + v * scale


def S(v):
    """Scale a logical length to screen pixels."""
    return v * scale


def F(size):
    """Scale a font point size (kept >= 1)."""
    return max(1, round(float(size) * scale))


def font(size, *style):
    """Build a scaled font tuple, e.g. ``font(20, 'bold')``."""
    return (context.FONT, F(size)) + style


def place(widget, x, y, anchor=None, width=None, height=None):
    """``widget.place`` with logical coordinates/sizes transformed to screen."""
    kwargs = {'x': X(x), 'y': Y(y)}
    if anchor is not None:
        kwargs['anchor'] = anchor
    if width is not None:
        kwargs['width'] = S(width)
    if height is not None:
        kwargs['height'] = S(height)
    widget.place(**kwargs)


def has_margins():
    """True when there are letterbox margins to fill (fullscreen)."""
    return off_x > 0.5 or off_y > 0.5
