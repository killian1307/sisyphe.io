# -*- coding: utf-8 -*-
"""Shared runtime state for the level editor (the former module globals)."""

# --- window / canvas ---
window = None        # was Mafenetre
canvas = None        # was Canevas
frame_elements = None

# --- config / paths ---
base_path = None     # the assets directory (where img/, sfx/, mus/ live)
params = None        # settings dict

# --- managers ---
sounds = None        # SoundManager
lang = None          # Traduction
tex = {}             # name -> PhotoImage (real block textures)

# What to do when the editor is left (set by the launcher):
#   standalone -> destroy the window ; embedded -> return to the game's main menu.
on_exit = None

# --- document state ---
plateau = None       # the level grid (reassigned by new_level/open_level)
show_textures = False  # was the ``textures`` flag (show real textures vs shapes)
unsaved_changes = False
file_opened = ""
filepath = ""

# --- tool selection (tk.IntVar, created by tools.init) ---
element_type = None
wall_selected = None
boulder_selected = None
hole_selected = None
player_selected = None
blue_portal_selected = None
red_portal_selected = None
door_selected = None
trapdoor_selected = None
fwall_selected = None
hammer_selected = None
rope_selected = None
box_selected = None
delete_selected = None
