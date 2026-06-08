# -*- coding: utf-8 -*-
"""Sisyphe.io — entry point.

This used to be a single 2810-line file. It is now a thin launcher: it builds the
window, wires up the shared runtime state in ``assets.package.context`` and starts
the game. All behavior lives in the small modules under ``assets/package``.

Run with:  python3 app.py
"""
import os
import tkinter as tk
from tkinter import ttk

from assets.package import context
from assets.package import paths
from assets.package import settings
from assets.package import platform_utils
from assets.package import fonts
from assets.package import images
from assets.package import game_state
from assets.package import db
from assets.package import board
from assets.package import movement
from assets.package.audio import music
from assets.package.audio import sounds
from assets.package.lang import catalog
from assets.package.ui import intro

# METTRE À TRUE POUR COMPILER LE JEU EN .EXE (see exe.txt)
fichier_exe = False

# VERSION DU JEU
version = "beta v1.0"


def build_window():
    """Create the main window, apply icon/cursor and the scrollbar style."""
    window = tk.Tk()
    window.geometry("800x600")
    window.title(version)
    platform_utils.set_window_icon(
        window,
        os.path.join(context.assets_dir, 'assets', 'img', 'icons', 'game_tskbr.ico'),
    )
    window.resizable(False, False)
    window['cursor'] = context.cursor_spec

    # Style pour la barre latérale des tutoriels
    style = ttk.Style()
    style.theme_use('clam')
    color_1 = "#bea48e"
    color_2 = '#7c645c'
    style.configure('Vertical.TScrollbar', relief='flat', background=color_1,
                    lightcolor=color_1, darkcolor=color_1, bordercolor=color_2,
                    troughcolor=color_2, arrowcolor=color_2)
    context.style = style
    return window


def build_canvas():
    """Create the game canvas and bind the keyboard."""
    canvas = tk.Canvas(context.window, width=context.WIDTH, height=context.HEIGHT, bg='black')
    canvas.configure(highlightthickness=0)
    canvas.grid(row=0, column=0)
    canvas.focus_set()

    # Pour les events Clavier
    canvas.bind('<Key>', movement.Clavier)

    # Pour changer l'orientation du joueur sans se déplacer
    canvas.bind('<Shift_L>', movement.on_shift_press)
    canvas.bind('<Shift_R>', movement.on_shift_press)
    canvas.bind('<KeyRelease-Shift_L>', movement.on_shift_release)
    canvas.bind('<KeyRelease-Shift_R>', movement.on_shift_release)
    canvas.bind('<Control_L>', movement.on_shift_press)
    canvas.bind('<Control_R>', movement.on_shift_press)
    canvas.bind('<KeyRelease-Control_L>', movement.on_shift_release)
    canvas.bind('<KeyRelease-Control_R>', movement.on_shift_release)

    # Désactive le tab pour éviter des problèmes de focus
    context.window.bind("<Tab>", lambda event: "break")
    context.window.bind("<Shift-Tab>", lambda event: "break")
    return canvas


def main():
    """Set up the runtime state and start the game loop."""
    # --- config / paths ---
    context.fichier_exe = fichier_exe
    context.version = version
    context.assets_dir = paths.asset_root(fichier_exe)
    context.settings_dir = settings.ensure_user_copy(context.assets_dir)
    context.cursor_spec = platform_utils.cursor_spec(context.assets_dir)

    # --- fonts: register bundled fonts BEFORE the Tk root so Tk can see them ---
    bundled_fonts = fonts.register(context.assets_dir)

    # --- window + canvas ---
    context.window = build_window()
    context.canvas = build_canvas()

    # resolve the family now that the Tk root exists (bundled fonts win)
    context.FONT = fonts.resolve(bundled_fonts)

    # --- managers / singletons ---
    context.images = images.GameImages(context.assets_dir)
    context.game = game_state.GameDeroulement()
    context.sounds = sounds.SoundManager()
    context.lang = catalog.Traduction()

    # base de données des scores
    db.init_database()

    # tous les sons du jeu
    sounds.load_all_sounds(context.sounds, context.assets_dir)

    # --- settings ---
    context.params = settings.load()
    for key in settings.REQUIRED_KEYS:
        assert key in context.params, f"Valeur manquante : {key}"

    # tables de langues
    context.languages = catalog.LANGUAGES
    context.languages_dic = catalog.DISPLAY_NAMES
    context.lang.apply(context.params["language"])

    # volume initial
    music.set_volume(context.params["volume"]["musique"])
    context.sounds.set_volume(context.params["volume"]["sons"])

    # --- board ---
    context.plateau = board.new_board()

    # --- window close + intro ---
    context.window.protocol("WM_DELETE_WINDOW", lambda croix=True: _on_close(croix))
    intro.start()

    context.window.mainloop()


def _on_close(croix):
    """Window-close handler (deferred import to avoid an import cycle at startup)."""
    from assets.package.ui import main_menu
    main_menu.quitter(croix)


if __name__ == "__main__":
    main()
