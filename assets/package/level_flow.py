# -*- coding: utf-8 -*-
"""Flow around levels: start, between-level transitions, custom levels, the
end-of-world screen, return-to-menu, and the in-game hint/tutorial timers."""
import os
import time
from tkinter import filedialog, messagebox

from . import context
from . import db
from . import platform_utils
from . import settings
from . import board
from . import render
from . import view
from .audio import music
from .ui import main_menu
from .ui import widgets


def demarrer_niveau():
    """Reset the per-run counters at the start of a world."""
    jeu = context.game
    jeu.temps_debut_niveau = time.time()
    jeu.niveau = 1
    jeu.deplacements = 0
    jeu.deplacements_tot = 0
    jeu.score = 0


# --- 3 functions of the post-level sequence ---
def attente_post_niveau():
    """Freeze the game then schedule the transition screen (half-second pause)."""
    context.game.fini = True
    context.canvas.after(500, affichage_ecran_transition)


def affichage_ecran_transition():
    """Black screen showing the score and the upcoming level."""
    board.clear_canvas()
    context.canvas.configure(bg="black")
    jeu = context.game
    lang = context.lang
    score_1 = round(jeu.score)
    if jeu.niveau == 5:
        level = lang.end
    else:
        level = jeu.niveau + 1
    context.canvas.create_text(view.X(context.WIDTH / 2), view.Y(context.HEIGHT / 2 - 30), text=lang.score + str(score_1), fill="white", font=view.font("30", "bold"))
    context.canvas.create_text(view.X(context.WIDTH / 2), view.Y(context.HEIGHT / 2 + 30), text=lang.next_level + f"{jeu.numero_monde} - {level}", fill="white", font=view.font("30", "bold"))
    context.canvas.after(2000, mise_en_place_nouveau_niveau)


def mise_en_place_nouveau_niveau():
    """Reset state and load the next level."""
    board.clear_canvas()
    context.canvas.configure(bg='#9b6b53')
    jeu = context.game
    jeu.fini = False
    jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 0, 0
    jeu.niveau = jeu.niveau + 1
    jeu.marteau = 0
    jeu.corde = 0
    board.genere_niveau(jeu.niveau, jeu.numero_monde)
    render.periodic_canvas_update(True)


def start_game_custom():
    """Pick a JSON file and start it as a custom level."""
    jeu = context.game
    lang = context.lang
    context.sounds.play_sound('button')
    if jeu.process_launched == True:
        return

    # Remet le jeu à zéro
    jeu.fini = False
    context.filepath = filedialog.askopenfilename(title=lang.open_file, filetypes=[("JSON files", "*.json")])
    if not context.filepath:  # Regarde si l'utilisateur n'a pas choisi de fichier
        jeu.fini = True
        main_menu.create_main_menu()
        return
    # Détruit le bouton et cache le fond d'écran
    widgets.clear_bg()
    widgets.clear_buttons_1()
    context.window.title(f'{lang.game_name} - {context.filepath.split("/")[-1]}')
    try:
        board.genere_niveau(mode="Custom")
        render.periodic_canvas_update(True)
        context.window.after(200, lambda: music.play_music(os.path.join(context.assets_dir, 'assets', 'mus', 'world_custom.ogg')))
    except Exception:
        jeu.fini = True
        main_menu.create_main_menu()
        messagebox.showerror(lang.error, lang.corrupted)
        return


def loop_back_to_menu(gamemode="Normal"):
    """Draw the final board then return to the main menu after a delay."""
    render.affiche_plateau_canvas()
    widgets.clear_buttons_1()
    if gamemode == "Custom":
        ms_time = 500
    else:
        ms_time = 3000
    context.window.after(ms_time, main_menu.create_main_menu)  # Revient au menu principal après une attente


def affiche_ecran_fin(numero_monde):
    """End-of-world screen: mark the world complete, save the score, congratulate."""
    jeu = context.game
    plateau = context.plateau
    jeu.fini = True
    reset_hint_tutorial()
    jeu.niveau = "FIN"
    board.murs_de_base()
    jeu.deplacements = jeu.deplacements_tot  # remets les déplacements à 0 pour chaque niveau

    context.params["mondes"][f"monde_{numero_monde}_termine"] = True
    settings.save(context.params)

    # Écrit le score dans la base SQL
    db.save_value_to_database(jeu.score, numero_monde)

    # on efface le tableau
    for i in range(2, 10):
        for j in range(2, 14):
            plateau[i][j][0] = 0
            plateau[i][j][1] = 0
            plateau[i][j][2] = 0
            plateau[i][j][3] = 0
    music.stop_music()
    context.sounds.play_sound('big_win')
    loop_back_to_menu()


# --- in-game hint / tutorial icons ---
def show_hint_icon():
    """After 5s, allow re-showing the world's dialog via the info icon."""
    if context.game.fini == False:
        context.hint_bool = True
        context.needs_redraw = True  # repaint so the icon appears
        context.tutorial_timer = context.window.after(115000, show_tutorial_icon)


def show_tutorial_icon():
    """After ~2min, allow accessing the world's solution video via the bulb icon."""
    if context.game.fini == False:
        context.tutorial_bool = True
        context.needs_redraw = True  # repaint so the icon appears


def reset_hint_tutorial():
    """Cancel the hint/tutorial timers when leaving the current world."""
    context.tutorial_bool = False
    context.hint_bool = False
    if context.hint_timer is not None:
        context.window.after_cancel(context.hint_timer)
        context.hint_timer = None
    if context.tutorial_timer is not None:
        context.window.after_cancel(context.tutorial_timer)
        context.tutorial_timer = None


def open_world_tutorial():
    """Open the YouTube solution for the current level at the right timecode."""
    jeu = context.game
    context.sounds.play_sound('button')
    # Liste des url des vidéos
    videos = [
        # Premier indice vide pour commencer au niveau 1
        '',
        # Monde 1
        'https://youtu.be/4m1SeLQ5XLU?t=8',
        'https://youtu.be/4m1SeLQ5XLU?t=30',
        'https://youtu.be/4m1SeLQ5XLU?t=52',
        'https://youtu.be/4m1SeLQ5XLU?t=68',
        'https://youtu.be/4m1SeLQ5XLU?t=95',
        # Monde 2
        'https://youtu.be/AW5Uu3fqxHU?t=5',
        'https://youtu.be/AW5Uu3fqxHU?t=40',
        'https://youtu.be/AW5Uu3fqxHU?t=61',
        'https://youtu.be/AW5Uu3fqxHU?t=93',
        'https://youtu.be/AW5Uu3fqxHU?t=119',
        # Monde 3
        'https://youtu.be/BVKllKNNQPc?t=9',
        'https://youtu.be/BVKllKNNQPc?t=56',
        'https://youtu.be/BVKllKNNQPc?t=79',
        'https://youtu.be/BVKllKNNQPc?t=118',
        'https://youtu.be/BVKllKNNQPc?t=175',
        # Monde 4
        'https://youtu.be/CpCTv19n780?t=10',
        'https://youtu.be/CpCTv19n780?t=40',
        'https://youtu.be/CpCTv19n780?t=106',
        'https://youtu.be/CpCTv19n780?t=163',
        'https://youtu.be/CpCTv19n780?t=232',
        # Monde 5
        'https://youtu.be/qf5C5179S10?t=8',
        'https://youtu.be/qf5C5179S10?t=53',
        'https://youtu.be/qf5C5179S10?t=111',
        'https://youtu.be/qf5C5179S10?t=155',
        'https://youtu.be/qf5C5179S10?t=206'
    ]

    # Trouve le timecode correspondant au niveau
    platform_utils.open_url(videos[(jeu.numero_monde - 1) * 5 + jeu.niveau])
