# -*- coding: utf-8 -*-
"""Run the level editor inside the game's main window (no separate process).

The home-screen 'Editor' button calls :func:`open_editor`. The on-screen toolbar
overlay's Back button — and File -> Leave — call :func:`close_editor` (via the
unsaved-changes guard) to return to the home screen.

The editor modules all operate on ``editor.context`` (``ectx``); here we simply
point that context at the game's existing window, canvas and shared managers
instead of creating a second window. Controls are an in-window overlay (see
``editor/overlay.py``) rather than a native menu bar, so they stay inside the
window and scale in fullscreen.
"""
import os
from tkinter import messagebox

from .. import context
from .. import settings
from .. import view
from ..audio import music
from ..ui import widgets
from ..ui import main_menu
from . import context as ectx
from . import textures
from . import tools
from . import placement
from . import render
from . import menu
from . import overlay


def _rebuild():
    """Reload textures + toolbar at the current scale and redraw (called on F1)."""
    ectx.tex = textures.load(ectx.base_path, view.cell)
    render.affiche_plateau_canvas()
    overlay.build()


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
    context.rebuild_screen = _rebuild   # so F1 rescales the editor

    ectx.tex = textures.load(base_path, view.cell)

    # Fresh document.
    ectx.plateau = [[[0] * 4 for _ in range(16)] for _ in range(12)]
    ectx.show_textures = False
    ectx.unsaved_changes = False
    ectx.file_opened = ectx.lang.editor_new_file
    ectx.filepath = ""

    context.canvas.configure(bg='grey', cursor='')
    context.window.title(f"{ectx.lang.editor_title} - {ectx.file_opened}")

    # Tools, in-window toolbar overlay, keyboard shortcuts, click binding.
    tools.init()
    overlay.build()
    menu.bind_keys()
    context.canvas.bind('<Button-1>', placement.place_element)
    context.canvas.focus_set()

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


def close_editor():
    """Tear the editor down and return to the home screen."""
    music.stop_music()
    overlay.teardown()
    menu.unbind_keys()
    context.canvas.unbind('<Button-1>')
    # Restore the shared audio volumes (the editor's mute toggles change them).
    music.set_volume(context.params["volume"]["musique"])
    context.sounds.set_volume(context.params["volume"]["sons"])
    main_menu.create_main_menu()
