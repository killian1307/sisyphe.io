# -*- coding: utf-8 -*-
"""Toggle real textures, editor music and editor sound effects."""
from . import context as ectx
from . import render
from ..audio import music


def toggle_textures():
    """Switch between real block textures and placeholder shapes."""
    ectx.show_textures = not ectx.show_textures
    render.affiche_plateau_canvas()


def toggle_music():
    """Mute / unmute the editor music."""
    if music.get_volume() != 0:
        music.set_volume(0)
    else:
        music.set_volume(ectx.params["volume"]["musique"])


def toggle_sounds():
    """Mute / unmute the editor sound effects."""
    if ectx.sounds.get_volume("button") != 0:
        ectx.sounds.set_volume(0)
    else:
        ectx.sounds.set_volume(ectx.params["volume"]["sons"])
