# -*- coding: utf-8 -*-
"""The world-selection menu (unlocking, best-score tooltips) and save reset."""
import os
import tkinter as tk
from tkinter import messagebox

from .. import context
from .. import settings
from .. import db
from .. import tooltip
from .. import board
from .. import level_flow
from .. import render
from .. import view
from . import widgets
from . import dialogs
from ..audio import music


def create_world_selection_menu():
    """Build the world picker; worlds unlock once the previous one is finished."""
    if context.game.process_launched == True:
        return
    context.rebuild_screen = create_world_selection_menu  # so F1 rescales this screen
    board.clear_canvas()
    widgets.clear_buttons_1()
    if context.monde_buttons is not None:
        widgets.clear_buttons_2()
    widgets.clear_bg()

    if context.background_label is None:
        background_image = context.images.world_menu_texture
        context.background_label = tk.Label(context.window, image=background_image)
        view.place(context.background_label, 0, 0, width=800, height=600)

    jeu = context.game

    def start_monde(monde):
        """Start the chosen world from level 1."""
        context.sounds.play_sound('button')
        widgets.clear_bg()
        widgets.clear_buttons_2()
        jeu.custom = 0
        board.clear_canvas()
        jeu.fini = False

        jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 0, 0
        jeu.difficulte = monde
        level_flow.demarrer_niveau()
        jeu.niveau = 1
        jeu.numero_monde = monde
        jeu.deplacements = 0

        board.genere_niveau(jeu.niveau, jeu.numero_monde, diff=jeu.difficulte)
        render.periodic_canvas_update(True)

        if context.params["tutoriels"][f"tutoriel_{jeu.numero_monde}_termine"] == False:
            dialogs.show_dialog_bottom_screen(jeu.numero_monde)
        context.window.after(200, lambda: music.play_music(os.path.join(context.assets_dir, 'assets', 'mus', f'world_{monde}.ogg')))

    button_pos = {
        1: [-250, 250],
        2: [-125, 375],
        3: [0, 250],
        4: [125, 375],
        5: [250, 250],
    }

    # refresh les parametres du jeu
    context.params = settings.load()

    if context.params["fps"]["mode"] == 2:
        jeu.mode_fps = 33
    else:
        jeu.mode_fps = 100

    # Crée un bouton pour chaque monde
    context.monde_buttons = []
    for i in range(1, 6):
        if i == 1:
            commande = lambda i=i: start_monde(i)
            color2 = '#bea48e'
            color3 = '#7c645c'
            color4 = 'WHITE'
            states = 'normal'
        elif context.params["mondes"][f"monde_{i - 1}_termine"] == True:
            commande = lambda i=i: start_monde(i)
            color2 = '#bea48e'
            color3 = '#7c645c'
            color4 = 'WHITE'
            states = 'normal'
        else:
            commande = None
            color2 = '#656565'
            color3 = color2
            color4 = '#a9a9a9'
            states = "disabled"

        monde_button = widgets.styled_button(
            context.window, context.lang.world + str(i), commande,
            bg=color2, active_bg=color3, fg=color4, active_fg=color4,
            width=10, height=1, border=5, font_size=20, state=states,
            disabledforeground=color4,
        )
        view.place(monde_button, 400 - (monde_button.winfo_reqwidth() / view.scale) / 2 + button_pos[i][0], button_pos[i][1])
        context.monde_buttons.append(monde_button)

        meilleur_score = db.get_highest_score_and_date(i)
        if meilleur_score == (None, None):
            tooltip.ToolTip(monde_button, context.lang.no_score)
        else:
            # Affichage du meilleur score
            tooltip.ToolTip(monde_button, f"{context.lang.best_score_1} {meilleur_score[0]} {context.lang.best_score_2} {meilleur_score[1].split(' ')[0]} {context.lang.best_score_3} {meilleur_score[1].split(' ')[1]} {context.lang.best_score_4}")

    return_button = widgets.make_return_button()
    view.place(return_button, 625, 525)
    context.monde_buttons.append(return_button)

    reset_save_button = widgets.styled_button(
        context.window, context.lang.reset_button, reset_save,
        bg=widgets.DANGER, active_bg=widgets.DANGER_ACTIVE,
        width=15, border=5, font_size=15, anchor="center",
    )
    view.place(reset_save_button, 25, 525)
    context.monde_buttons.append(reset_save_button)

    context.window.after(200, lambda: music.play_music(os.path.join(context.assets_dir, 'assets', 'mus', 'menu_world.ogg')))


def reset_save():
    """Reset world/tutorial progress and wipe the scores after confirmation."""
    context.sounds.play_sound('button')
    if messagebox.askyesno(context.lang.confirm, context.lang.reset_save_confirm, icon="warning"):
        context.sounds.play_sound('button')
        for i in range(1, 6):
            context.params["mondes"][f"monde_{i}_termine"] = False
            context.params["tutoriels"][f"tutoriel_{i}_termine"] = False
        # Pour le message de fin du jeu
        context.params["tutoriels"]["tutoriel_6_termine"] = False
        context.params["tutoriels"]["tutoriel_editeur_termine"] = False
        settings.save(context.params)

        db.wipe_table_contents()
        create_world_selection_menu()
    else:
        context.sounds.play_sound('button')
