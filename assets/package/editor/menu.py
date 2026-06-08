# -*- coding: utf-8 -*-
"""The editor menu bar and keyboard shortcuts."""
import sys
import tkinter as tk

from . import context as ectx
from . import tools
from . import files
from . import toggles

# macOS uses Command (⌘) where other platforms use Control.
_MOD = 'Command' if sys.platform == 'darwin' else 'Control'
_ACCEL = 'Cmd' if sys.platform == 'darwin' else 'Ctrl'


def _accel(combo):
    """Accelerator label, e.g. 'Cmd+N' on macOS, 'Ctrl+N' elsewhere."""
    return f"{_ACCEL}+{combo}"


def bind_keys():
    """Single-key tool shortcuts and Ctrl command shortcuts."""
    window = ectx.window

    window.bind('w', tools.select_wall)
    window.bind('W', tools.select_wall)
    window.bind('x', tools.select_boulder)
    window.bind('X', tools.select_boulder)
    window.bind('c', tools.select_hole)
    window.bind('C', tools.select_hole)
    window.bind('b', tools.select_player)
    window.bind('B', tools.select_player)
    window.bind('q', tools.select_portal_blue)
    window.bind('Q', tools.select_portal_blue)
    window.bind('s', tools.select_portal_red)
    window.bind('S', tools.select_portal_red)
    window.bind('d', tools.select_door)
    window.bind('D', tools.select_door)
    window.bind('f', tools.select_trapdoor)
    window.bind('F', tools.select_trapdoor)
    window.bind('g', tools.select_fwall)
    window.bind('G', tools.select_fwall)
    window.bind('h', tools.select_hammer)
    window.bind('H', tools.select_hammer)
    window.bind('j', tools.select_rope)
    window.bind('J', tools.select_rope)
    window.bind('v', tools.select_box)
    window.bind('V', tools.select_box)
    window.bind('<BackSpace>', tools.select_delete)

    window.bind_all(f'<{_MOD}-n>', lambda event: files.new_level())
    window.bind_all(f'<{_MOD}-o>', lambda event: files.open_level())
    window.bind_all(f'<{_MOD}-s>', lambda event: files.save())
    window.bind_all(f'<{_MOD}-Shift-s>', lambda event: files.save_as())
    window.bind_all(f'<{_MOD}-t>', lambda event: toggles.toggle_textures())
    window.bind_all(f'<{_MOD}-u>', lambda event: toggles.toggle_music())
    window.bind_all(f'<{_MOD}-i>', lambda event: toggles.toggle_sounds())

    window.bind_all(f'<{_MOD}-N>', lambda event: files.new_level())
    window.bind_all(f'<{_MOD}-O>', lambda event: files.open_level())
    window.bind_all(f'<{_MOD}-S>', lambda event: files.save())
    window.bind_all(f'<{_MOD}-Shift-S>', lambda event: files.save_as())
    window.bind_all(f'<{_MOD}-T>', lambda event: toggles.toggle_textures())
    window.bind_all(f'<{_MOD}-U>', lambda event: toggles.toggle_music())
    window.bind_all(f'<{_MOD}-I>', lambda event: toggles.toggle_sounds())


def build():
    """Create the menu bar, its commands and the window-close protocol."""
    window = ectx.window
    lang = ectx.lang

    # Création de la barre au dessus de l'éditeur
    menu_bar = tk.Menu(window)
    window.config(menu=menu_bar)
    window.protocol("WM_DELETE_WINDOW", files.confirm_close)

    # Création des cases de cette barre
    file_menu = tk.Menu(menu_bar, tearoff=0)
    edition_menu = tk.Menu(menu_bar, tearoff=0)
    textures_menu = tk.Menu(menu_bar, tearoff=0)
    music_menu = tk.Menu(menu_bar, tearoff=0)

    # Création des sous-menus d'Édition
    basic_objects_menu = tk.Menu(edition_menu, tearoff=0)
    special_objects_menu = tk.Menu(edition_menu, tearoff=0)

    menu_bar.add_cascade(label=lang.file_menu, menu=file_menu)
    menu_bar.add_cascade(label=lang.edition_menu, menu=edition_menu)
    menu_bar.add_cascade(label=lang.textures_menu, menu=textures_menu)
    menu_bar.add_cascade(label=lang.music_menu, menu=music_menu)

    # Création des options de la case "Fichier"
    file_menu.add_command(label=lang.new_button, command=files.new_level, accelerator=_accel("N"))
    file_menu.add_command(label=lang.open_button, command=lambda: files.open_level(), accelerator=_accel("O"))
    file_menu.add_command(label=lang.save_button, command=files.save, accelerator=_accel("S"))
    file_menu.add_command(label=lang.save_as_button, command=files.save_as, accelerator=_accel("Shift+S"))
    file_menu.add_command(label=lang.leave_button, command=files.confirm_close, accelerator="ALT+F4")

    # Création des options de la case "Textures"
    textures_menu.add_command(label=lang.toggle_textures_button, command=toggles.toggle_textures, accelerator=_accel("T"))

    # Création des options de la case "Musique & Sons"
    music_menu.add_command(label=lang.toggle_music_button, command=toggles.toggle_music, accelerator=_accel("U"))
    music_menu.add_command(label=lang.toggle_sounds_button, command=toggles.toggle_sounds, accelerator=_accel("I"))

    # Création des options de la case "Edition"
    # Menu Basique
    basic_objects_menu.add_checkbutton(label=lang.select_wall, variable=ectx.wall_selected, command=tools.select_wall, accelerator="W")
    basic_objects_menu.add_checkbutton(label=lang.select_boulder, variable=ectx.boulder_selected, command=tools.select_boulder, accelerator="X")
    basic_objects_menu.add_checkbutton(label=lang.select_hole, variable=ectx.hole_selected, command=tools.select_hole, accelerator="C")
    basic_objects_menu.add_checkbutton(label=lang.select_box, variable=ectx.box_selected, command=tools.select_box, accelerator="V")
    basic_objects_menu.add_checkbutton(label=lang.select_player, variable=ectx.player_selected, command=tools.select_player, accelerator="B")

    # Menu Spécial
    special_objects_menu.add_checkbutton(label=lang.select_portal1, variable=ectx.blue_portal_selected, command=tools.select_portal_blue, accelerator="Q")
    special_objects_menu.add_checkbutton(label=lang.select_portal2, variable=ectx.red_portal_selected, command=tools.select_portal_red, accelerator="S")
    special_objects_menu.add_checkbutton(label=lang.select_door, variable=ectx.door_selected, command=tools.select_door, accelerator="D")
    special_objects_menu.add_checkbutton(label=lang.select_pressure_plate, variable=ectx.trapdoor_selected, command=tools.select_trapdoor, accelerator="F")
    special_objects_menu.add_checkbutton(label=lang.select_cracked_wall, variable=ectx.fwall_selected, command=tools.select_fwall, accelerator="G")
    special_objects_menu.add_checkbutton(label=lang.select_hammer, variable=ectx.hammer_selected, command=tools.select_hammer, accelerator="H")
    special_objects_menu.add_checkbutton(label=lang.select_rope, variable=ectx.rope_selected, command=tools.select_rope, accelerator="J")

    # Ajout des sous-menus dans le menu Edition
    edition_menu.add_cascade(label=lang.base_objects, menu=basic_objects_menu)
    edition_menu.add_cascade(label=lang.special_objects, menu=special_objects_menu)

    # Ajout du mode suppression
    edition_menu.add_separator()
    edition_menu.add_checkbutton(label=lang.delete_mode, variable=ectx.delete_selected, command=tools.select_delete, accelerator=lang.return_key)
