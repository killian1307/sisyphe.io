# -*- coding: utf-8 -*-
"""Drawing the board, HUD and in-game hint/tutorial icons, plus the refresh loop.

All coordinates/sizes/fonts go through :mod:`view`, so the board scales crisply in
fullscreen. In windowed mode the transform is the identity (unchanged output).
"""
import math
import time

from . import context
from . import board
from . import level_flow
from . import view
from .ui import dialogs


def periodic_canvas_update(FirstTime=False):
    """Recursive canvas refresh loop. On the first call it starts the FPS counter."""
    jeu = context.game

    def count_fps():
        if not jeu.fini:
            jeu.fps_print = jeu.fps
            jeu.fps = 0
            context.window.after(1000, count_fps)

    if FirstTime:
        count_fps()
        context.rebuild_screen = redraw  # so F1 rescales the board immediately
        context.needs_redraw = True
    if not jeu.fini:
        # Repaint only when the board changed or the displayed second ticked over,
        # instead of redrawing the whole (possibly fullscreen) canvas every frame.
        elapsed = int(time.time() - jeu.temps_debut_niveau)
        if context.needs_redraw or elapsed != context.last_drawn_sec:
            context.canvas.delete('all')
            affiche_plateau_canvas()
            context.needs_redraw = False
            context.last_drawn_sec = elapsed
        jeu.fps += 1
        # Limiteur de FPS si la fenêtre n'a pas le focus
        if context.window.focus_displayof() is not None:
            context.window.after(jeu.mode_fps, periodic_canvas_update)
        else:
            context.window.after(100, periodic_canvas_update)


def redraw():
    """Clear and redraw the board (used to refresh after a fullscreen rescale)."""
    context.canvas.delete('all')
    affiche_plateau_canvas()


def _draw_wall_margins(Canevas, wall):
    """Tile the wall texture over the letterbox margins (fullscreen gameplay)."""
    cell = view.cell
    first_col = -math.ceil(view.off_x / cell)
    last_col = 16 + math.ceil((view.screen_w - (view.off_x + 16 * cell)) / cell)
    first_row = -math.ceil(view.off_y / cell)
    last_row = 12 + math.ceil((view.screen_h - (view.off_y + 12 * cell)) / cell)
    for col in range(first_col, last_col):
        for row in range(first_row, last_row):
            if 0 <= col < 16 and 0 <= row < 12:
                continue  # the board itself is drawn below
            Canevas.create_image(view.X(50 * col + 25), view.Y(50 * row + 25), image=wall, anchor='center')


def affiche_plateau_canvas():
    """Draw the whole board, the player, HUD counters and hint/tutorial icons."""
    Canevas = context.canvas
    plateau = context.plateau
    jeu = context.game
    game_images = context.images
    lang = context.lang
    parametres = context.params
    X, Y, fnt = view.X, view.Y, view.font

    # Fullscreen: fill the side/top/bottom bars with tiled wall texture.
    if view.has_margins():
        _draw_wall_margins(Canevas, game_images.wall_texture)

    for i in range(12):
        for j in range(16):
            cx = X(50 * j + 25)
            cy = Y(50 * i + 25)
            if (plateau[i][j][0] == 0):
                # affichage case vide
                Canevas.create_image(cx, cy, image=game_images.ground_texture, anchor='center')
            if (plateau[i][j][0] == 1):
                # affichage mur
                Canevas.create_image(cx, cy, image=game_images.wall_texture, anchor='center')

            if plateau[i][j][2] == 3:
                # affichage portal bleu
                Canevas.create_image(cx, cy, image=game_images.blue_portal_texture, anchor='center')
            elif plateau[i][j][2] == 4:
                # affichage portal rouge
                Canevas.create_image(cx, cy, image=game_images.red_portal_texture, anchor='center')

            # affiche plaque de pression
            if plateau[i][j][3] == 8:
                Canevas.create_image(cx, cy, image=game_images.Trapdoor_texture, anchor='center')
            # affiche porte fermée
            elif plateau[i][j][3] == 9:
                Canevas.create_image(cx, cy, image=game_images.Door_closed_texture, anchor='center')
            # affiche porte ouverte
            elif plateau[i][j][3] == 10:
                Canevas.create_image(cx, cy, image=game_images.Door_open_texture, anchor='center')

            # affichache marteau
            if plateau[i][j][3] == 5:
                Canevas.create_image(cx, cy, image=game_images.hammer_on_texture, anchor='center')

            # affichage mur fissuré
            if plateau[i][j][0] == 2:
                Canevas.create_image(cx, cy, image=game_images.wall_cracked_texture, anchor='center')

            # affichage corde
            if plateau[i][j][3] == 6:
                Canevas.create_image(cx, cy, image=game_images.rope_on_texture, anchor='center')

            # affichage boite
            if plateau[i][j][2] == 2:
                Canevas.create_image(cx, cy, image=game_images.box_texture, anchor='center')

            # affichage rocher dans un trou
            if plateau[i][j][2] == 1 and plateau[i][j][3] == 1:
                Canevas.create_image(cx, cy, image=game_images.crate_hole_texture, anchor='center')

            elif (plateau[i][j][1] == 1):
                # affichage joueur
                if jeu.haut >= 1:
                    if jeu.haut == 1:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['haut'][1], anchor='center')
                    elif jeu.haut == 2:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['haut'][0], anchor='center')
                    elif jeu.haut == 3:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['haut'][2], anchor='center')
                    elif jeu.haut == 4:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['haut'][0], anchor='center')
                    else:
                        jeu.haut = 1
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['haut'][1], anchor='center')

                elif jeu.bas >= 1:
                    if jeu.bas == 1:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['bas'][1], anchor='center')
                    elif jeu.bas == 2:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['bas'][0], anchor='center')
                    elif jeu.bas == 3:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['bas'][2], anchor='center')
                    elif jeu.bas == 4:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['bas'][0], anchor='center')
                    else:
                        jeu.bas = 1
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['bas'][1], anchor='center')
                elif jeu.gauche >= 1:
                    if jeu.gauche == 1:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['gauche'][1], anchor='center')
                    elif jeu.gauche == 2:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['gauche'][0], anchor='center')
                    elif jeu.gauche == 3:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['gauche'][2], anchor='center')
                    elif jeu.gauche == 4:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['gauche'][0], anchor='center')
                    else:
                        jeu.gauche = 1
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['gauche'][1], anchor='center')
                elif jeu.droite >= 1:
                    if jeu.droite == 1:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['droite'][1], anchor='center')
                    elif jeu.droite == 2:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['droite'][0], anchor='center')
                    elif jeu.droite == 3:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['droite'][2], anchor='center')
                    elif jeu.droite == 4:
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['droite'][0], anchor='center')
                    else:
                        jeu.droite = 1
                        Canevas.create_image(cx, cy, image=game_images.sisyphe_images['droite'][1], anchor='center')
                else:
                    Canevas.create_image(cx, cy, image=game_images.sisyphe_images['bas'][0], anchor='center')
            elif (plateau[i][j][2] == 1):
                # affichage rocher
                Canevas.create_image(cx, cy, image=game_images.crate_texture, anchor='center')
            elif (plateau[i][j][3] == 1):
                # affichage trou
                Canevas.create_image(cx, cy, image=game_images.button_texture, anchor='center')

    # Afficher le niveau
    if jeu.custom > 0:
        pass
    else:
        Canevas.create_text(X(402), Y(24), fill='black', font=fnt("20"), text=lang.level + f"{jeu.numero_monde} - {jeu.niveau}", anchor='center')  # Affiche le niveau
        Canevas.create_text(X(400), Y(22), fill='white', font=fnt("20"), text=lang.level + f"{jeu.numero_monde} - {jeu.niveau}", anchor='center')

    # affichage icone marteau
    if jeu.marteau_present == True:
        MAX_USES_PER_HAMMER = 3

        # Calcule le nombre d'utilisations restantes pour le marteau
        full_hammers, remaining_uses = divmod(jeu.marteau, MAX_USES_PER_HAMMER)

        # Détermine la texture à afficher en fonction de l'état de durabilité du marteau
        if jeu.marteau == 0:
            hammer_texture = game_images.hammer_off_texture
        elif remaining_uses == 1:
            hammer_texture = game_images.hammer_on_3_texture  # Texture pour 1 utilisation restante
        elif remaining_uses == 2:
            hammer_texture = game_images.hammer_on_2_texture  # Texture pour 2 utilisations restantes
        else:  # Cela veut dire que le marteau est neuf
            hammer_texture = game_images.hammer_on_1_texture  # Texture pour 3 utilisations restantes

        # Montre la texture du marteau
        Canevas.create_image(X(75), Y(575), image=hammer_texture, anchor='center')

        # Met à jour le texte avec le nombre d'utilisations du marteau
        total_hammers_display = full_hammers + 1 if remaining_uses > 0 else full_hammers  # + le marteau actuel s'il lui reste de la durabilité

        # Affiche le texte
        Canevas.create_text(X(92), Y(590), fill='black', font=fnt("15"), text=total_hammers_display, anchor='center')
        Canevas.create_text(X(90), Y(588), fill='white', font=fnt("15"), text=total_hammers_display, anchor='center')

    # affichage icone corde
    if jeu.corde_present == True:
        MAX_USES_PER_ROPE = 3

        # Calcule le nombre d'utilisations restantes pour la corde
        full_ropes, remaining_uses_2 = divmod(jeu.corde, MAX_USES_PER_ROPE)

        # Détermine la texture à afficher en fonction de l'état de durabilité de la corde
        if jeu.corde == 0:
            rope_texture = game_images.rope_off_texture
        elif remaining_uses_2 == 1:
            rope_texture = game_images.rope_on_3_texture  # Texture pour 1 utilisation restante
        elif remaining_uses_2 == 2:
            rope_texture = game_images.rope_on_2_texture  # Texture pour 2 utilisations restantes
        else:  # Cela veut dire que le marteau est neuf
            rope_texture = game_images.rope_on_1_texture  # Texture pour 3 utilisations restantes

        # Montre la texture de la corde
        Canevas.create_image(X(25), Y(575), image=rope_texture, anchor='center')

        # Met à jour le texte avec le nombre d'utilisations de la corde
        total_ropes_display = full_ropes + 1 if remaining_uses_2 > 0 else full_ropes  # + la corde actuelle s'il lui reste de la durabilité

        # Affiche le texte
        Canevas.create_text(X(42), Y(590), fill='black', font=fnt("15"), text=total_ropes_display, anchor='center')
        Canevas.create_text(X(40), Y(588), fill='white', font=fnt("15"), text=total_ropes_display, anchor='center')

    # Afficher le compteur de déplacements
    Canevas.create_text(X(792), Y(24), fill='black', font=fnt("20"), text=lang.moves + str(jeu.deplacements), anchor='e')
    Canevas.create_text(X(790), Y(22), fill='white', font=fnt("20"), text=lang.moves + str(jeu.deplacements), anchor='e')  # Affiche le nombre de déplacements
    if jeu.niveau == 'FIN':
        Canevas.create_text(X(402), Y(277), fill="black", font=fnt("30", "bold"), text=lang.congrats_1, anchor='center')
        Canevas.create_text(X(400), Y(275), fill="white", font=fnt("30", "bold"), text=lang.congrats_1, anchor='center')
        Canevas.create_text(X(402), Y(327), fill="black", font=fnt("30", "bold"), text=lang.congrats_2 + str(jeu.numero_monde) + lang.congrats_3, anchor='center')
        Canevas.create_text(X(400), Y(325), fill="white", font=fnt("30", "bold"), text=lang.congrats_2 + str(jeu.numero_monde) + lang.congrats_3, anchor='center')
    # Afficher le temps écoulé
    temps_ecoule = round(time.time() - jeu.temps_debut_niveau)
    minutes = temps_ecoule // 60
    secondes = temps_ecoule % 60  # Pour convertir en Minutes les secondes
    Canevas.create_text(X(12), Y(24), fill='black', font=fnt("20"), text=lang.time + f'{minutes}min {secondes}s', anchor='w')
    Canevas.create_text(X(10), Y(22), fill='white', font=fnt("20"), text=lang.time + f'{minutes}min {secondes}s', anchor='w')  # Affiche le temps écoulé à chaque déplacement
    if parametres["fps"]["show"]:
        Canevas.create_text(X(794), Y(584), fill='black', font=fnt("15"), text=lang.fps + str(jeu.fps_print), anchor='e')
        Canevas.create_text(X(792), Y(582), fill='white', font=fnt("15"), text=lang.fps + str(jeu.fps_print), anchor='e')  # Affiche le niveau

    # Afficher les icones d'indice/de tuto
    if context.tutorial_bool == True:
        tutorial_icon = Canevas.create_image(X(775), Y(175), image=game_images.lightbulb_texture, anchor='center')
        # Pour les boutons tuto/indice en jeu
        Canevas.tag_bind(tutorial_icon, "<Button-1>", lambda event=None: level_flow.open_world_tutorial())
    if context.hint_bool == True:
        hint_icon = Canevas.create_image(X(775), Y(125), image=game_images.info_texture, anchor='center')
        Canevas.tag_bind(hint_icon, "<Button-1>", lambda event=None: dialogs.show_dialog_bottom_screen(jeu.numero_monde))
