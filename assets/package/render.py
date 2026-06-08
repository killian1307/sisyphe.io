# -*- coding: utf-8 -*-
"""Drawing the board, HUD and in-game hint/tutorial icons, plus the refresh loop."""
import time

from . import context
from . import board
from . import level_flow
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
    if not jeu.fini:
        context.canvas.delete('all')
        affiche_plateau_canvas()
        jeu.fps += 1
        # Limiteur de FPS si la fenêtre n'a pas le focus
        if context.window.focus_displayof() is not None:
            context.window.after(jeu.mode_fps, periodic_canvas_update)
        else:
            context.window.after(100, periodic_canvas_update)


def affiche_plateau_canvas():
    """Draw the whole board, the player, HUD counters and hint/tutorial icons."""
    Canevas = context.canvas
    plateau = context.plateau
    jeu = context.game
    game_images = context.images
    lang = context.lang
    parametres = context.params
    for i in range(12):
        for j in range(16):
            if (plateau[i][j][0] == 0):
                # affichage case vide
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.ground_texture, anchor='center')
            if (plateau[i][j][0] == 1):
                # affichage mur
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.wall_texture, anchor='center')

            if plateau[i][j][2] == 3:
                # affichage portal bleu
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.blue_portal_texture, anchor='center')
            elif plateau[i][j][2] == 4:
                # affichage portal rouge
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.red_portal_texture, anchor='center')

            # affiche plaque de pression
            if plateau[i][j][3] == 8:
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.Trapdoor_texture, anchor='center')
            # affiche porte fermée
            elif plateau[i][j][3] == 9:
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.Door_closed_texture, anchor='center')
            # affiche porte ouverte
            elif plateau[i][j][3] == 10:
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.Door_open_texture, anchor='center')

            # affichache marteau
            if plateau[i][j][3] == 5:
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.hammer_on_texture, anchor='center')

            # affichage mur fissuré
            if plateau[i][j][0] == 2:
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.wall_cracked_texture, anchor='center')

            # affichage corde
            if plateau[i][j][3] == 6:
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.rope_on_texture, anchor='center')

            # affichage boite
            if plateau[i][j][2] == 2:
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.box_texture, anchor='center')

            # affichage rocher dans un trou
            if plateau[i][j][2] == 1 and plateau[i][j][3] == 1:
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.crate_hole_texture, anchor='center')

            elif (plateau[i][j][1] == 1):
                # affichage joueur
                if jeu.haut >= 1:
                    if jeu.haut == 1:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['haut'][1], anchor='center')
                    elif jeu.haut == 2:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['haut'][0], anchor='center')
                    elif jeu.haut == 3:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['haut'][2], anchor='center')
                    elif jeu.haut == 4:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['haut'][0], anchor='center')
                    else:
                        jeu.haut = 1
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['haut'][1], anchor='center')

                elif jeu.bas >= 1:
                    if jeu.bas == 1:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['bas'][1], anchor='center')
                    elif jeu.bas == 2:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['bas'][0], anchor='center')
                    elif jeu.bas == 3:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['bas'][2], anchor='center')
                    elif jeu.bas == 4:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['bas'][0], anchor='center')
                    else:
                        jeu.bas = 1
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['bas'][1], anchor='center')
                elif jeu.gauche >= 1:
                    if jeu.gauche == 1:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['gauche'][1], anchor='center')
                    elif jeu.gauche == 2:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['gauche'][0], anchor='center')
                    elif jeu.gauche == 3:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['gauche'][2], anchor='center')
                    elif jeu.gauche == 4:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['gauche'][0], anchor='center')
                    else:
                        jeu.gauche = 1
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['gauche'][1], anchor='center')
                elif jeu.droite >= 1:
                    if jeu.droite == 1:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['droite'][1], anchor='center')
                    elif jeu.droite == 2:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['droite'][0], anchor='center')
                    elif jeu.droite == 3:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['droite'][2], anchor='center')
                    elif jeu.droite == 4:
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['droite'][0], anchor='center')
                    else:
                        jeu.droite = 1
                        Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['droite'][1], anchor='center')
                else:
                    Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.sisyphe_images['bas'][0], anchor='center')
            elif (plateau[i][j][2] == 1):
                # affichage rocher
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.crate_texture, anchor='center')
            elif (plateau[i][j][3] == 1):
                # affichage trou
                Canevas.create_image(50 * j + 25, 50 * i + 25, image=game_images.button_texture, anchor='center')

    # Afficher le niveau
    if jeu.custom > 0:
        pass
    else:
        Canevas.create_text(402, 24, fill='black', font=(context.FONT, "20"), text=lang.level + f"{jeu.numero_monde} - {jeu.niveau}", anchor='center')  # Affiche le niveau
        Canevas.create_text(400, 22, fill='white', font=(context.FONT, "20"), text=lang.level + f"{jeu.numero_monde} - {jeu.niveau}", anchor='center')

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
        Canevas.create_image(75, 575, image=hammer_texture, anchor='center')

        # Met à jour le texte avec le nombre d'utilisations du marteau
        total_hammers_display = full_hammers + 1 if remaining_uses > 0 else full_hammers  # + le marteau actuel s'il lui reste de la durabilité

        # Affiche le texte
        Canevas.create_text(92, 590, fill='black', font=(context.FONT, "15"), text=total_hammers_display, anchor='center')
        Canevas.create_text(90, 588, fill='white', font=(context.FONT, "15"), text=total_hammers_display, anchor='center')

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
        Canevas.create_image(25, 575, image=rope_texture, anchor='center')

        # Met à jour le texte avec le nombre d'utilisations de la corde
        total_ropes_display = full_ropes + 1 if remaining_uses_2 > 0 else full_ropes  # + la corde actuelle s'il lui reste de la durabilité

        # Affiche le texte
        Canevas.create_text(42, 590, fill='black', font=(context.FONT, "15"), text=total_ropes_display, anchor='center')
        Canevas.create_text(40, 588, fill='white', font=(context.FONT, "15"), text=total_ropes_display, anchor='center')

    # Afficher le compteur de déplacements
    Canevas.create_text(792, 24, fill='black', font=(context.FONT, "20"), text=lang.moves + str(jeu.deplacements), anchor='e')
    Canevas.create_text(790, 22, fill='white', font=(context.FONT, "20"), text=lang.moves + str(jeu.deplacements), anchor='e')  # Affiche le nombre de déplacements
    if jeu.niveau == 'FIN':
        Canevas.create_text(402, 277, fill="black", font=(context.FONT, "30", "bold"), text=lang.congrats_1, anchor='center')
        Canevas.create_text(400, 275, fill="white", font=(context.FONT, "30", "bold"), text=lang.congrats_1, anchor='center')
        Canevas.create_text(402, 327, fill="black", font=(context.FONT, "30", "bold"), text=lang.congrats_2 + str(jeu.numero_monde) + lang.congrats_3, anchor='center')
        Canevas.create_text(400, 325, fill="white", font=(context.FONT, "30", "bold"), text=lang.congrats_2 + str(jeu.numero_monde) + lang.congrats_3, anchor='center')
    # Afficher le temps écoulé
    temps_ecoule = round(time.time() - jeu.temps_debut_niveau)
    minutes = temps_ecoule // 60
    secondes = temps_ecoule % 60  # Pour convertir en Minutes les secondes
    Canevas.create_text(12, 24, fill='black', font=(context.FONT, "20"), text=lang.time + f'{minutes}min {secondes}s', anchor='w')
    Canevas.create_text(10, 22, fill='white', font=(context.FONT, "20"), text=lang.time + f'{minutes}min {secondes}s', anchor='w')  # Affiche le temps écoulé à chaque déplacement
    if parametres["fps"]["show"]:
        Canevas.create_text(794, 584, fill='black', font=(context.FONT, "15"), text=lang.fps + str(jeu.fps_print), anchor='e')
        Canevas.create_text(792, 582, fill='white', font=(context.FONT, "15"), text=lang.fps + str(jeu.fps_print), anchor='e')  # Affiche le niveau

    # Afficher les icones d'indice/de tuto
    if context.tutorial_bool == True:
        tutorial_icon = Canevas.create_image(775, 175, image=game_images.lightbulb_texture, anchor='center')
        # Pour les boutons tuto/indice en jeu
        Canevas.tag_bind(tutorial_icon, "<Button-1>", lambda event=None: level_flow.open_world_tutorial())
    if context.hint_bool == True:
        hint_icon = Canevas.create_image(775, 125, image=game_images.info_texture, anchor='center')
        Canevas.tag_bind(hint_icon, "<Button-1>", lambda event=None: dialogs.show_dialog_bottom_screen(jeu.numero_monde))
