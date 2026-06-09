# -*- coding: utf-8 -*-
"""Shared runtime state for the game.

This module is the single home for what used to be the module-level globals of
the monolithic app.py. Every screen/logic module reads and writes these
attributes (``context.window``, ``context.plateau``, ``context.params`` ...), so
reassignments stay visible everywhere exactly as the original ``global``
declarations made them.

It deliberately imports nothing heavy: ``app.py`` fills these in at startup.
"""

# --- Window / canvas ---
window = None        # tk.Tk root            (was Mafenetre)
canvas = None        # tk.Canvas             (was Canevas)
WIDTH = 800          # (was Largeur)
HEIGHT = 600         # (was Hauteur)
style = None         # ttk.Style

# --- Config / paths ---
version = "beta v1.0"
fichier_exe = False  # set True to compile to .exe (see exe.txt)
assets_dir = ''      # asset root ('' in dev, sys._MEIPASS when frozen)
settings_dir = None  # per-user data dir
cursor_spec = ''     # Tk cursor string (custom .cur on Windows, default elsewhere)
FONT = 'Small Fonts'  # UI font family, resolved per-platform at startup (see fonts.py)

# --- Managers / singletons ---
images = None        # GameImages       (was game_images)
game = None          # GameDeroulement  (was jeu)
sounds = None        # SoundManager     (was sound_manager)
lang = None          # Traduction       (was lang)

# --- Settings dict (reloaded frequently) ---
params = None        # (was parametres)

# --- Board ---
plateau = []

# --- Language tables ---
languages = []       # ordered list of language codes
languages_dic = {}   # code -> display name

# --- Main-menu widgets ---
start_button = None
menu_button = None
edit_button = None
command_button = None
credits_button = None
leave_button = None
story = None

# --- World / credits widgets ---
monde_buttons = None
return_button = None

# --- Popups / background / settings widgets ---
popup = None
background_label = None
button_widgets = []

# --- Flags / timers ---
dialog_opened = False
hint_bool = False
tutorial_bool = False
hint_timer = None
tutorial_timer = None
door_opened = 0

# --- Custom-level path & editor subprocess ---
filepath = ""

# --- Fullscreen (F1) ---
fullscreen = False       # current fullscreen state
rebuild_screen = None    # callable that redraws the active screen after a rescale

# --- Render-on-demand (the gameplay loop only repaints when this is set,
#     or when the on-screen second changes) ---
needs_redraw = True
last_drawn_sec = -1
