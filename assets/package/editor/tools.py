# -*- coding: utf-8 -*-
"""Tool selection: the IntVars, the uncheck helper and the per-tool selectors.

``element_type`` holds the active tool's code (0 = delete, 1..12 = blocks),
matching the original numbering.
"""
import tkinter as tk

from . import context as ectx

# Selection IntVar attribute name on the context -> active element_type code.
_TOOLS = {
    'wall_selected': 1,
    'boulder_selected': 2,
    'hole_selected': 3,
    'player_selected': 4,
    'blue_portal_selected': 5,
    'red_portal_selected': 6,
    'door_selected': 7,
    'trapdoor_selected': 8,
    'fwall_selected': 9,
    'hammer_selected': 10,
    'rope_selected': 11,
    'box_selected': 12,
    'delete_selected': 0,
}


def init():
    """Create every tool IntVar (must run after the Tk root exists)."""
    ectx.element_type = tk.IntVar()
    for name in _TOOLS:
        setattr(ectx, name, tk.IntVar())


def uncheck_all():
    """Deselect every tool checkbutton."""
    for name in _TOOLS:
        getattr(ectx, name).set(0)


def _make_selector(name, code):
    def select(event=None):
        uncheck_all()
        getattr(ectx, name).set(1)
        ectx.element_type.set(code)
    return select


select_wall = _make_selector('wall_selected', 1)
select_boulder = _make_selector('boulder_selected', 2)
select_hole = _make_selector('hole_selected', 3)
select_player = _make_selector('player_selected', 4)
select_portal_blue = _make_selector('blue_portal_selected', 5)
select_portal_red = _make_selector('red_portal_selected', 6)
select_door = _make_selector('door_selected', 7)
select_trapdoor = _make_selector('trapdoor_selected', 8)
select_fwall = _make_selector('fwall_selected', 9)
select_hammer = _make_selector('hammer_selected', 10)
select_rope = _make_selector('rope_selected', 11)
select_box = _make_selector('box_selected', 12)
select_delete = _make_selector('delete_selected', 0)
