# -*- coding: utf-8 -*-
"""Run the level editor inside the game's main window (no separate process).

The home-screen 'Editor' button calls :func:`open_editor`. A small floating Back
button — and the editor's File -> Leave menu item — call :func:`close_editor`
(via the unsaved-changes guard) to return to the home screen.

The editor modules all operate on ``editor.context`` (``ectx``); here we simply
point that context at the game's existing window, canvas and shared managers
instead of creating a second window.
"""
import os
from tkinter import messagebox

from .. import context
from .. import settings
from ..audio import music
from ..ui import widgets
from ..ui import main_menu
from . import context as ectx
from . import textures
from . import tools
from . import placement
from . import render
from . import menu
from . import files

_back_button = None
_tex_cache = None


def open_editor():
    """Replace the home screen with the embedded level editor."""
    context.sounds.play_sound('button')

    # Leave the menu screen.
    widgets.clear_buttons_1()
    if context.monde_buttons is not None:
        widgets.clear_buttons_2()
    widgets.clear_bg()
    widgets.clear_canvas_and_buttons()

    # Point the editor context at the game's window/canvas and shared managers.
    base_path = os.path.join(context.assets_dir, 'assets')
    ectx.base_path = base_path
    ectx.window = context.window
    ectx.canvas = context.canvas
    ectx.params = context.params
    ectx.sounds = context.sounds       # the game already loaded every sound the editor uses
    ectx.lang = context.lang
    ectx.on_exit = close_editor

    global _tex_cache
    if _tex_cache is None:
        _tex_cache = textures.load(base_path)
    ectx.tex = _tex_cache

    # Fresh document.
    ectx.plateau = [[[0] * 4 for _ in range(16)] for _ in range(12)]
    ectx.show_textures = False
    ectx.unsaved_changes = False
    ectx.file_opened = ectx.lang.editor_new_file
    ectx.filepath = ""

    context.canvas.configure(bg='grey', cursor='')
    context.window.title(f"{ectx.lang.editor_title} - {ectx.file_opened}")

    # Tools, menu bar, key + click bindings.
    tools.init()
    menu.build()
    menu.bind_keys()
    context.canvas.bind('<Button-1>', placement.place_element)
    context.canvas.focus_set()

    # Small floating Back button. It's a placed widget so it survives the
    # canvas redraws, and it sits over the top-left border cell (always a wall).
    global _back_button
    _back_button = widgets.styled_button(
        context.window, ectx.lang.back_button, _back,
        bg=widgets.ACCENT, active_bg=widgets.ACCENT_ACTIVE, width=None, border=2, font_size=12,
    )
    _back_button.place(x=2, y=2)

    tools.select_wall()
    render.affiche_plateau_canvas()

    music.set_volume(context.params["volume"]["musique"])
    context.sounds.set_volume(context.params["volume"]["sons"])
    context.window.after(200, lambda: music.play_music(os.path.join(base_path, 'mus', 'editor.ogg')))

    # First-time editor tutorial.
    if not context.params["tutoriels"]["tutoriel_editeur_termine"]:
        messagebox.showinfo(ectx.lang.editor_tutorial_title, ectx.lang.editor_tutorial)
        context.params["tutoriels"]["tutoriel_editeur_termine"] = True
        settings.save(context.params)


def _back():
    """Back button handler: click sound then the unsaved-changes guard."""
    context.sounds.play_sound('button')
    files.confirm_close()


def close_editor():
    """Tear the editor down and return to the home screen."""
    global _back_button
    music.stop_music()
    menu.teardown()
    if _back_button is not None:
        _back_button.destroy()
        _back_button = None
    # Restore the shared audio volumes (the editor's mute toggles change them).
    music.set_volume(context.params["volume"]["musique"])
    context.sounds.set_volume(context.params["volume"]["sons"])
    main_menu.create_main_menu()
