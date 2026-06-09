# -*- coding: utf-8 -*-
"""The game board: creation, helpers, win-test, entity lookups and level loading.

Each cell is ``[wall, player, crate/portal, hole/door/item]`` exactly as in the
original code; the integer codes are unchanged.
"""
import json
import os
import time
from tkinter import messagebox

from . import context

# Modules referenced at call time only (imported as modules to avoid cycles).
from . import level_flow
from .ui import main_menu


def new_board():
    """Return a fresh 12x16 board of empty cells (was the module-level loop)."""
    plateau = []
    for i in range(12):
        plateau.append([])
        for j in range(16):
            plateau[i].append([0, 0, 0, 0])  # Case vide par défaut
    return plateau


def murs_de_base():
    """Surround the playfield with walls (used by the end-of-world screen)."""
    plateau = context.plateau
    clear_canvas()
    for i in range(12):
        plateau[i][0][0] = 1
        plateau[i][1][0] = 1
        plateau[i][14][0] = 1
        plateau[i][15][0] = 1

    for j in range(16):
        plateau[0][j][0] = 1
        plateau[1][j][0] = 1
        plateau[10][j][0] = 1
        plateau[11][j][0] = 1


def clear_canvas():
    """Remove every item drawn on the game canvas."""
    context.canvas.delete("all")


def test_victoire():
    """Return True when every hole is filled by a crate."""
    plateau = context.plateau
    for i in range(12):
        for j in range(16):
            if plateau[i][j][3] == 1 and plateau[i][j][2] == 0:
                return False
    return True


def find_portal(plateau, portal_type):
    """Return the (i, j) of the portal of ``portal_type`` (3=blue, 4=red), or None."""
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j][2] == portal_type:
                return (i, j)
    return None


def find_door(plateau):
    """Return [i, j] of the door (open or closed), or None."""
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j][3] == 9 or plateau[i][j][3] == 10:
                return [i, j]
    return None


def find_trapdoor(plateau):
    """Return [i, j] of the pressure plate, or None."""
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            if plateau[i][j][3] == 8:
                return [i, j]
    return None


def genere_niveau(numero_niveau=1, numero_monde=1, mode="Normal", diff=1):
    """Load an official or custom level into the board.

    ``mode`` is "Normal" (official world levels) or "Custom" (a chosen JSON file,
    path read from :data:`context.filepath`). ``diff`` feeds the scoring formula.
    """
    jeu = context.game
    plateau = context.plateau
    jeu.difficulte = diff
    jeu.niveau = numero_niveau
    jeu.deplacements = 0
    jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 0, 0
    jeu.marteau = 0
    jeu.corde = 0
    for i in range(12):
        for j in range(16):
            plateau[i][j][0] = 0
            plateau[i][j][1] = 0
            plateau[i][j][2] = 0
            plateau[i][j][3] = 0
    if mode == "Normal":
        jeu.custom = 0
        if numero_niveau == 6:  # Remplacer cette valeur par 1 pour finir le monde instantanément
            level_flow.affiche_ecran_fin(numero_monde)
            return
        try:
            with open(os.path.join(context.assets_dir, 'assets', 'niveaux', f'monde{numero_monde}', f'monde{numero_monde}_niveau{numero_niveau}.json'), 'r') as fichier:
                grille_chargee = json.load(fichier)
            context.window.title(f'{context.lang.game_name} - {context.lang.level}{numero_monde}-{numero_niveau}')
            if context.hint_timer is None:
                context.hint_timer = context.window.after(5000, level_flow.show_hint_icon)
        except Exception:
            jeu.fini = True
            main_menu.create_main_menu()
            messagebox.showerror(context.lang.error, context.lang.error_opening)
            return
    else:
        jeu.custom = 1
        jeu.temps_debut_niveau = time.time()
        with open(context.filepath, 'r') as fichier:
            grille_chargee = json.load(fichier)
    marteau = 0
    corde = 0
    for i in range(12):
        for j in range(16):
            if grille_chargee[i][j] == [1, 0, 0, 0]:
                plateau[i][j][0] = 1
            elif grille_chargee[i][j] == [0, 0, 1, 0]:
                plateau[i][j][2] = 1
            elif grille_chargee[i][j] == [0, 0, 0, 1]:
                plateau[i][j][3] = 1
            elif grille_chargee[i][j] == [0, 1, 0, 0]:
                plateau[i][j][1] = 1
            elif grille_chargee[i][j] == [0, 2, 0, 0]:
                plateau[i][j][2] = 3
            elif grille_chargee[i][j] == [0, 0, 2, 0]:
                plateau[i][j][2] = 4
            elif grille_chargee[i][j] == [0, 3, 0, 0]:
                plateau[i][j][3] = 9
            elif grille_chargee[i][j] == [0, 0, 3, 0]:
                plateau[i][j][3] = 8
            elif grille_chargee[i][j] == [0, 4, 0, 0]:
                plateau[i][j][0] = 2
            elif grille_chargee[i][j] == [0, 0, 4, 0]:
                plateau[i][j][3] = 5
                marteau += 1
            elif grille_chargee[i][j] == [0, 5, 0, 0]:
                plateau[i][j][3] = 6
                corde += 1
            elif grille_chargee[i][j] == [0, 0, 5, 0]:
                plateau[i][j][2] = 2

            # Check s'il faut afficher l'image de la corde/du marteau en bas à gauche
            if corde > 0:
                jeu.corde_present = True
            else:
                jeu.corde_present = False
            if marteau > 0:
                jeu.marteau_present = True
            else:
                jeu.marteau_present = False
    context.needs_redraw = True  # a fresh level was loaded -> repaint
