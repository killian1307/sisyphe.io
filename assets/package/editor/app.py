# -*- coding: utf-8 -*-
"""Editor entry point: wires the runtime state together and starts the loop."""
import os
import tkinter as tk
from tkinter import messagebox

from .. import settings
from .. import platform_utils
from ..audio import music
from ..audio import sounds as sounds_mod
from ..lang import catalog
from . import context as ectx
from . import textures
from . import tools
from . import placement
from . import render
from . import menu

# Logical name -> file in <assets>/sfx (the editor uses a subset of the sounds).
EDITOR_SOUNDS = {
    'steps1': 'footsteps1.wav',
    'steps2': 'footsteps2.wav',
    'small_win': 'level_completed.wav',
    'hole_filled': 'hole_filled.wav',
    'portal': 'portal_entered.wav',
    'powerup': 'powerup_taken.wav',
    'break': 'wall_broken.wav',
    'door': 'door_opened.wav',
    'button': 'button_pressed.wav',
    'reset': 'reset_level.wav',
}


def main(base_path):
    """Build the editor window and run it. ``base_path`` is the assets directory."""
    ectx.base_path = base_path

    # --- settings + language ---
    ectx.params = settings.load()
    for key in settings.REQUIRED_KEYS:
        assert key in ectx.params, f"Valeur manquante : {key}"
    ectx.lang = catalog.Traduction()
    ectx.lang.apply(ectx.params["language"])

    # --- window ---
    window = tk.Tk()
    ectx.window = window
    ectx.file_opened = ectx.lang.editor_new_file
    ectx.filepath = ""
    window.title(f"{ectx.lang.editor_title} - {ectx.file_opened}")
    platform_utils.set_window_icon(
        window,
        os.path.join(base_path, 'img', 'icons', 'editor_tskbr.ico'),
    )
    window.resizable(False, False)

    # --- sounds + textures ---
    ectx.sounds = sounds_mod.SoundManager()
    for name, filename in EDITOR_SOUNDS.items():
        ectx.sounds.load_sound(name, os.path.join(base_path, 'sfx', filename))
    ectx.tex = textures.load(base_path)

    # --- board + canvas ---
    ectx.plateau = [[[0] * 4 for _ in range(16)] for _ in range(12)]
    ectx.show_textures = False
    canvas = tk.Canvas(window, width=800, height=600, bg='grey')
    canvas.grid(row=0, column=0)
    ectx.canvas = canvas
    ectx.frame_elements = tk.Frame(window)
    ectx.frame_elements.grid(row=0, column=1)

    # --- tools, menu, bindings ---
    tools.init()
    menu.build()
    menu.bind_keys()
    canvas.bind('<Button-1>', placement.place_element)

    # --- launch ---
    tools.select_wall()
    render.affiche_plateau_canvas()

    # Met le volume du son/de la musique par défaut
    music.set_volume(ectx.params["volume"]["musique"])
    ectx.sounds.set_volume(ectx.params["volume"]["sons"])

    # Lance la musique de l'éditeur
    window.after(200, lambda: music.play_music(os.path.join(base_path, 'mus', 'editor.ogg')))

    # Affiche le tutoriel de l'éditeur si nécessaire
    if not ectx.params["tutoriels"]["tutoriel_editeur_termine"]:
        messagebox.showinfo(ectx.lang.editor_tutorial_title, ectx.lang.editor_tutorial)
        ectx.params["tutoriels"]["tutoriel_editeur_termine"] = True
        settings.save(ectx.params)

    window.mainloop()
