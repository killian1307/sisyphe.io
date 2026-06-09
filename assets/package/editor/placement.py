# -*- coding: utf-8 -*-
"""Placing, deleting and validating cells on the editor grid.

Cell encoding (unchanged from the original editor): for layer ``[a, b, c, d]``
the editor stores walls in ``a``; player/blue-portal/door/cracked-wall/rope in
``b`` (1..5); crate/red-portal/pressure-plate/hammer/box in ``c`` (1..5);
hole in ``d``.
"""
from . import context as ectx
from . import render
from .. import view


def initialize_walls():
    """Force walls on the left/right columns and top/bottom rows."""
    plateau = ectx.plateau
    for i in range(12):
        plateau[i][0][0] = 1
        # plateau[i][1][0] = 1
        # plateau[i][14][0] = 1
        plateau[i][15][0] = 1

    for j in range(16):
        plateau[0][j][0] = 1
        # plateau[1][j][0] = 1
        # plateau[10][j][0] = 1
        plateau[11][j][0] = 1


def get_selected_cell(event):
    """Return the (row, col) of the clicked cell (accounts for fullscreen scale)."""
    x = ectx.canvas.canvasx(event.x)
    y = ectx.canvas.canvasy(event.y)
    row = int((y - view.off_y) / view.cell)
    col = int((x - view.off_x) / view.cell)
    return row, col


def _empty(row, col):
    plateau = ectx.plateau
    return plateau[row][col][0] == 0 and plateau[row][col][1] == 0 and plateau[row][col][2] == 0 and plateau[row][col][3] == 0


def place_element(event):
    """Place the active tool's element on the clicked cell (if allowed)."""
    row, col = get_selected_cell(event)
    if not (0 <= row < 12 and 0 <= col < 16):
        return  # click landed in the fullscreen letterbox margin
    code = ectx.element_type.get()
    if code == 0:
        delete(row, col)
    if code == 1 and _empty(row, col):
        place_wall(row, col)
    elif code == 2 and _empty(row, col):
        place_boulder(row, col)
    elif code == 3 and _empty(row, col):
        place_switch(row, col)
    elif code == 4 and _empty(row, col):
        place_player(row, col)
    elif code == 5 and _empty(row, col):
        place_portal_blue(row, col)
    elif code == 6 and _empty(row, col):
        place_portal_red(row, col)
    elif code == 7 and _empty(row, col):
        place_door(row, col)
    elif code == 8 and _empty(row, col):
        place_trapdoor(row, col)
    elif code == 9 and _empty(row, col):
        place_fwall(row, col)
    elif code == 10 and _empty(row, col):
        place_hammer(row, col)
    elif code == 11 and _empty(row, col):
        place_rope(row, col)
    elif code == 12 and _empty(row, col):
        place_box(row, col)
    ectx.unsaved_changes = True
    render.affiche_plateau_canvas()


def delete(row, col):
    """Clear the clicked cell."""
    plateau = ectx.plateau
    if plateau[row][col][0] != 0 or plateau[row][col][1] != 0 or plateau[row][col][2] != 0 or plateau[row][col][3] != 0:
        ectx.sounds.play_sound('reset')
        plateau[row][col][0] = 0
        plateau[row][col][1] = 0
        plateau[row][col][2] = 0
        plateau[row][col][3] = 0


def place_wall(row, col):
    ectx.sounds.play_sound('button')
    ectx.plateau[row][col][0] = 1


def place_boulder(row, col):
    ectx.sounds.play_sound('steps1')
    ectx.plateau[row][col][2] = 1


def place_switch(row, col):
    ectx.sounds.play_sound('hole_filled')
    ectx.plateau[row][col][3] = 1


def place_portal_blue(row, col):
    already = False
    for i in range(12):
        for j in range(16):
            if ectx.plateau[i][j][1] == 2:
                already = True
    if already == False:
        ectx.sounds.play_sound('portal')
        ectx.plateau[row][col][1] = 2


def place_portal_red(row, col):
    already = False
    for i in range(12):
        for j in range(16):
            if ectx.plateau[i][j][2] == 2:
                already = True
    if already == False:
        ectx.sounds.play_sound('portal')
        ectx.plateau[row][col][2] = 2


def place_door(row, col):
    already = False
    for i in range(12):
        for j in range(16):
            if ectx.plateau[i][j][1] == 3:
                already = True
    if already == False:
        ectx.sounds.play_sound('door')
        ectx.plateau[row][col][1] = 3


def place_trapdoor(row, col):
    already = False
    for i in range(12):
        for j in range(16):
            if ectx.plateau[i][j][2] == 3:
                already = True
    if already == False:
        ectx.sounds.play_sound('door')
        ectx.plateau[row][col][2] = 3


def place_fwall(row, col):
    ectx.sounds.play_sound('break')
    ectx.plateau[row][col][1] = 4


def place_hammer(row, col):
    ectx.sounds.play_sound('powerup')
    ectx.plateau[row][col][2] = 4


def place_rope(row, col):
    ectx.sounds.play_sound('powerup')
    ectx.plateau[row][col][1] = 5


def place_box(row, col):
    ectx.sounds.play_sound('steps2')
    ectx.plateau[row][col][2] = 5


def place_player(row, col):
    already = False
    for i in range(12):
        for j in range(16):
            if ectx.plateau[i][j][1] == 1:
                already = True
    if already == False:
        ectx.sounds.play_sound('small_win')
        ectx.plateau[row][col][1] = 1
