# -*- coding: utf-8 -*-
"""The keyboard / movement engine: walking, pushing crates, portals, doors,
pressure plates, hammer (break cracked walls) and rope (pull crates), plus
reset/menu keys and per-level win detection."""
from . import context
from . import board
from . import level_flow
from . import render
from .audio import music
from .ui import main_menu


def on_shift_press(event):
    """Hold Shift/Ctrl to turn in place without moving (press)."""
    context.game.wait_next_key = True


def on_shift_release(event):
    """Release Shift/Ctrl to resume moving (release)."""
    context.game.wait_next_key = False


def Clavier(event):
    """Handle a key press during play."""
    jeu = context.game
    plateau = context.plateau
    parametres = context.params
    sound_manager = context.sounds
    if jeu.fini == False:  # quand le jeu est fini on ne peux plus se deplacer
        # a key was pressed during play: the board may change -> request a repaint
        context.needs_redraw = True

        mvt_poss = True
        touche = event.keysym
        if touche == "Up" or touche == "Left" or touche == "Right" or touche == "Down":
            pass
        else:
            touche = touche.lower()

        for i in range(12):
            for j in range(16):
                if (plateau[i][j][1] == 1) and mvt_poss == True:
                    # Pour touche shift/controle
                    if jeu.wait_next_key:
                        if touche in [parametres["controles"]["up"], "Up"]:
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 2, 0, 0, 0
                        elif touche in [parametres["controles"]["down"], "Down"]:
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 2, 0, 0
                        elif touche in [parametres["controles"]["left"], "Left"]:
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 2, 0
                        elif touche in [parametres["controles"]["right"], "Right"]:
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 0, 2
                        return

                    direction = None
                    if touche in [parametres["controles"]["up"], "Up"]:
                        direction = (-1, 0)
                    elif touche in [parametres["controles"]["down"], "Down"]:
                        direction = (1, 0)
                    elif touche in [parametres["controles"]["left"], "Left"]:
                        direction = (0, -1)
                    elif touche in [parametres["controles"]["right"], "Right"]:
                        direction = (0, 1)

                    # Si une direction de mouvement est définie
                    if direction:
                        new_i, new_j = i + direction[0], j + direction[1]

                    # Vérification et ramassage de la corde
                        if plateau[new_i][new_j][3] == 6:  # Si la case de destination contient une corde
                            jeu.corde += 3  # Incrémente le nombre de cordes
                            plateau[new_i][new_j][3] = 0  # Retire la corde de la case
                            sound_manager.play_sound('powerup')

                             # Tirage de rocher/boite
                    # si joueur va vers en haut
                    if touche == parametres["controles"]["interact"] and (plateau[i - 1][j][2] == 1 or plateau[i - 1][j][2] == 2) and jeu.corde > 0 and plateau[i + 1][j][2] != 2 and plateau[i + 1][j][2] != 1 and plateau[i + 1][j][0] != 2 and plateau[i + 1][j][3] != 9 and plateau[i + 1][j][0] != 1 and (plateau[i + 1][j][2] != 3 and plateau[i + 1][j][2] != 4) and plateau[i + 1][j][3] != 1 and plateau[i][j][2] != 3 and plateau[i][j][2] != 4 and jeu.haut > 0:
                        if plateau[i - 1][j][2] == 1:
                            plateau[i - 1][j][2] = 0
                            plateau[i][j][2] = 1
                            plateau[i][j][1] = 0
                            plateau[i + 1][j][1] = 1
                        else:
                            plateau[i - 1][j][2] = 0
                            plateau[i][j][2] = 2
                            plateau[i][j][1] = 0
                            plateau[i + 1][j][1] = 1
                        sound_manager.play_sound('steps1')
                        jeu.corde -= 1
                        jeu.deplacements += 1
                        direction = (1, 0)
                    # si joueur va vers en bas
                    if touche == parametres["controles"]["interact"] and (plateau[i + 1][j][2] == 1 or plateau[i + 1][j][2] == 2) and jeu.corde > 0 and plateau[i - 1][j][2] != 2 and plateau[i - 1][j][2] != 1 and plateau[i - 1][j][0] != 2 and plateau[i - 1][j][3] != 9 and plateau[i - 1][j][0] != 1 and (plateau[i - 1][j][2] != 3 and plateau[i - 1][j][2] != 4) and plateau[i - 1][j][3] != 1 and plateau[i][j][2] != 3 and plateau[i][j][2] != 4 and jeu.bas > 0:
                        if plateau[i + 1][j][2] == 1:
                            plateau[i + 1][j][2] = 0
                            plateau[i][j][2] = 1
                            plateau[i][j][1] = 0
                            plateau[i - 1][j][1] = 1
                        else:
                            plateau[i + 1][j][2] = 0
                            plateau[i][j][2] = 2
                            plateau[i][j][1] = 0
                            plateau[i - 1][j][1] = 1
                        sound_manager.play_sound('steps1')
                        jeu.corde -= 1
                        jeu.deplacements += 1
                        direction = (-1, 0)
                    # si joueur va vers la gauche
                    if touche == parametres["controles"]["interact"] and (plateau[i][j - 1][2] == 1 or plateau[i][j - 1][2] == 2) and jeu.corde > 0 and plateau[i][j + 1][2] != 2 and plateau[i][j + 1][2] != 1 and plateau[i][j + 1][0] != 2 and plateau[i][j + 1][3] != 9 and plateau[i][j + 1][0] != 1 and (plateau[i][j + 1][2] != 3 and plateau[i][j + 1][2] != 4) and plateau[i][j + 1][3] != 1 and plateau[i][j][2] != 3 and plateau[i][j][2] != 4 and jeu.gauche > 0:
                        if plateau[i][j - 1][2] == 1:
                            plateau[i][j - 1][2] = 0
                            plateau[i][j][2] = 1
                            plateau[i][j][1] = 0
                            plateau[i][j + 1][1] = 1
                        else:
                            plateau[i][j - 1][2] = 0
                            plateau[i][j][2] = 2
                            plateau[i][j][1] = 0
                            plateau[i][j + 1][1] = 1
                        sound_manager.play_sound('steps1')
                        jeu.corde -= 1
                        jeu.deplacements += 1
                        direction = (0, 1)
                    # si joueur va vers la droite
                    if touche == parametres["controles"]["interact"] and (plateau[i][j + 1][2] == 1 or plateau[i][j + 1][2] == 2) and jeu.corde > 0 and plateau[i][j - 1][2] != 2 and plateau[i][j - 1][2] != 1 and plateau[i][j - 1][0] != 2 and plateau[i][j - 1][3] != 9 and plateau[i][j - 1][0] != 1 and (plateau[i][j - 1][2] != 3 and plateau[i][j - 1][2] != 4) and plateau[i][j - 1][3] != 1 and plateau[i][j][2] != 3 and plateau[i][j][2] != 4 and jeu.droite > 0:
                        if plateau[i][j + 1][2] == 1:
                            plateau[i][j + 1][2] = 0
                            plateau[i][j][2] = 1
                            plateau[i][j][1] = 0
                            plateau[i][j - 1][1] = 1
                        else:
                            plateau[i][j + 1][2] = 0
                            plateau[i][j][2] = 2
                            plateau[i][j][1] = 0
                            plateau[i][j - 1][1] = 1
                        sound_manager.play_sound('steps1')
                        jeu.corde -= 1
                        jeu.deplacements += 1
                        direction = (0, -1)

                    # Si une direction de mouvement est définie
                    if direction:
                        new_i, new_j = i + direction[0], j + direction[1]

                        # Vérification et ramassage du marteau
                        if plateau[new_i][new_j][3] == 5:  # Si la case de destination contient un marteau
                            jeu.marteau += 3  # Incrémente le nombre de marteaux
                            plateau[new_i][new_j][3] = 0  # Retire le marteau de la case
                            sound_manager.play_sound('powerup')

                        # Destruction mur fissuré
                    # si joueur va vers en haut
                    if touche == parametres["controles"]["interact"] and plateau[i - 1][j][0] == 2 and jeu.marteau > 0 and jeu.haut > 0:
                        plateau[i - 1][j][0] = 0
                        jeu.marteau -= 1
                        sound_manager.play_sound('break')
                    # si joueur va vers en bas
                    if touche == parametres["controles"]["interact"] and plateau[i + 1][j][0] == 2 and jeu.marteau > 0 and jeu.bas > 0:
                        plateau[i + 1][j][0] = 0
                        jeu.marteau -= 1
                        sound_manager.play_sound('break')
                    # si joueur va vers la gauche
                    if touche == parametres["controles"]["interact"] and plateau[i][j - 1][0] == 2 and jeu.marteau > 0 and jeu.gauche > 0:
                        plateau[i][j - 1][0] = 0
                        jeu.marteau -= 1
                        sound_manager.play_sound('break')
                    # si joueur va vers la droite
                    if touche == parametres["controles"]["interact"] and plateau[i][j + 1][0] == 2 and jeu.marteau > 0 and jeu.droite > 0:
                        plateau[i][j + 1][0] = 0
                        jeu.marteau -= 1
                        sound_manager.play_sound('break')

                    # Si le joueur est sur le point de rentrer dans un portail
                    if touche in [parametres["controles"]["up"], parametres["controles"]["left"], parametres["controles"]["right"], parametres["controles"]["down"]]:
                        # Détermine la direction basée sur la touche pressée
                        destination_i, destination_j = i, j
                        if touche == parametres["controles"]["up"]:
                            destination_i -= 1
                        elif touche == parametres["controles"]["down"]:
                            destination_i += 1
                        elif touche == parametres["controles"]["left"]:
                            destination_j -= 1
                        elif touche == parametres["controles"]["right"]:
                            destination_j += 1

                        # Regarde si la destination du joueur est un portail
                        if plateau[destination_i][destination_j][2] in [3, 4]:  # Portail détecté
                            portal_type = plateau[destination_i][destination_j][2]
                            other_portal_type = 4 if portal_type == 3 else 3  # Détermine l'autre portail
                            other_portal_coords = board.find_portal(plateau, other_portal_type)  # Trouve l'autre portail

                            if other_portal_coords:
                                # Téléporte le joueur
                                plateau[i][j][1] = 0
                                i, j = other_portal_coords
                                plateau[i][j][1] = 1
                                jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 0, 0
                                sound_manager.play_sound('portal')
                                return

                    if touche == parametres["controles"]["up"]:
                        if plateau[i - 1][j][0] != 2 and plateau[i - 1][j][3] != 9 and plateau[i - 1][j][2] != 2 and plateau[i - 1][j][0] != 1 and (plateau[i - 1][j][2] != 3 and plateau[i - 1][j][2] != 4) and plateau[i - 1][j][3] != 1 and not (plateau[i - 1][j][2] == 1 and (plateau[i - 2][j][2] == 1 or plateau[i - 2][j][0] == 1 or plateau[i - 2][j][2] == 3 or plateau[i - 2][j][2] == 4 or plateau[i - 2][j][3] == 9 or plateau[i - 2][j][0] == 2 or plateau[i - 2][j][2] == 2)):
                            if plateau[i - 1][j][2] == 1:
                                plateau[i - 2][j][2] = 1
                                plateau[i - 1][j][2] = 0
                                if plateau[i - 2][j][3] == 1 and not (board.test_victoire() == True):
                                    sound_manager.play_sound('hole_filled')
                            plateau[i][j][1] = 0
                            plateau[i - 1][j][1] = 1
                            jeu.deplacements += 1  # Incrémentation du compteur de déplacements
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = jeu.haut + 1, 0, 0, 0
                            if jeu.haut % 2 == 0:
                                sound_manager.play_sound('steps2')
                            else:
                                sound_manager.play_sound('steps1')
                        else:
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 2, 0, 0, 0
                    elif touche == parametres["controles"]["left"]:
                        if plateau[i][j - 1][0] != 2 and plateau[i][j - 1][3] != 9 and plateau[i][j - 1][2] != 2 and plateau[i][j - 1][0] != 1 and (plateau[i][j - 1][2] != 3 and plateau[i][j - 1][2] != 4) and plateau[i][j - 1][3] != 1 and not (plateau[i][j - 1][2] == 1 and (plateau[i][j - 2][2] == 1 or plateau[i][j - 2][0] == 1 or plateau[i][j - 2][2] == 3 or plateau[i][j - 2][2] == 4 or plateau[i][j - 2][3] == 9 or plateau[i][j - 2][0] == 2 or plateau[i][j - 2][2] == 2)):
                            if plateau[i][j - 1][2] == 1:
                                plateau[i][j - 2][2] = 1
                                plateau[i][j - 1][2] = 0
                                if plateau[i][j - 2][3] == 1 and not (board.test_victoire() == True):
                                    sound_manager.play_sound('hole_filled')
                            plateau[i][j][1] = 0
                            plateau[i][j - 1][1] = 1
                            jeu.deplacements += 1  # Incrémentation du compteur de déplacements
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, jeu.gauche + 1, 0
                            if jeu.gauche % 2 == 0:
                                sound_manager.play_sound('steps2')
                            else:
                                sound_manager.play_sound('steps1')
                        else:
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 2, 0
                    elif touche == parametres["controles"]["right"]:
                        if plateau[i][j + 1][0] != 2 and plateau[i][j + 1][3] != 9 and plateau[i][j + 1][2] != 2 and plateau[i][j + 1][0] != 1 and (plateau[i][j + 1][2] != 3 and plateau[i][j + 1][2] != 4) and plateau[i][j + 1][3] != 1 and not (plateau[i][j + 1][2] == 1 and (plateau[i][j + 2][2] == 1 or plateau[i][j + 2][0] == 1 or plateau[i][j + 2][2] == 3 or plateau[i][j + 2][2] == 4 or plateau[i][j + 2][3] == 9 or plateau[i][j + 2][0] == 2 or plateau[i][j + 2][2] == 2)):
                            if plateau[i][j + 1][2] == 1:
                                plateau[i][j + 2][2] = 1
                                plateau[i][j + 1][2] = 0
                                if plateau[i][j + 2][3] == 1 and not (board.test_victoire() == True):
                                    sound_manager.play_sound('hole_filled')
                            plateau[i][j][1] = 0
                            plateau[i][j + 1][1] = 1
                            jeu.deplacements += 1  # Incrémentation du compteur de déplacements
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 0, jeu.droite + 1
                            if jeu.droite % 2 == 0:
                                sound_manager.play_sound('steps1')
                            else:
                                sound_manager.play_sound('steps2')
                        else:
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 0, 2
                    elif touche == parametres["controles"]["down"]:
                        if plateau[i + 1][j][0] != 2 and plateau[i + 1][j][3] != 9 and plateau[i + 1][j][2] != 2 and plateau[i + 1][j][0] != 1 and (plateau[i + 1][j][2] != 3 and plateau[i + 1][j][2] != 4) and plateau[i + 1][j][3] != 1 and not (plateau[i + 1][j][2] == 1 and (plateau[i + 2][j][2] == 1 or plateau[i + 2][j][0] == 1 or plateau[i + 2][j][2] == 3 or plateau[i + 2][j][2] == 4 or plateau[i + 2][j][3] == 9 or plateau[i + 2][j][0] == 2 or plateau[i + 2][j][2] == 2)):
                            if plateau[i + 1][j][2] == 1:
                                plateau[i + 2][j][2] = 1
                                plateau[i + 1][j][2] = 0
                                if plateau[i + 2][j][3] == 1 and not (board.test_victoire() == True):
                                    sound_manager.play_sound('hole_filled')
                            jeu.deplacements += 1  # Incrémentation du compteur de déplacements
                            plateau[i][j][1] = 0
                            plateau[i + 1][j][1] = 1
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, jeu.bas + 1, 0, 0
                            if jeu.bas % 2 == 0:
                                sound_manager.play_sound('steps1')
                            else:
                                sound_manager.play_sound('steps2')
                        else:
                            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 2, 0, 0
                        # deplacements vers plaque de pression / porte
                    # si rocher sur la plaque
                    trapdoor_pos = board.find_trapdoor(plateau)
                    door_pos = board.find_door(plateau)
                    if trapdoor_pos != None and door_pos != None:
                        if plateau[trapdoor_pos[0]][trapdoor_pos[1]][3] == 8 and plateau[trapdoor_pos[0]][trapdoor_pos[1]][2] == 1:
                            plateau[door_pos[0]][door_pos[1]][3] = 10
                            if context.door_opened == 0:
                                sound_manager.play_sound('door')
                                context.door_opened += 1
                        # si rien sur la plaque
                        else:
                            trapdoor_pos = board.find_trapdoor(plateau)
                            door_pos = board.find_door(plateau)
                            plateau[door_pos[0]][door_pos[1]][3] = 9
                            if context.door_opened > 0:
                                sound_manager.play_sound('door2')
                                context.door_opened = 0
                    # si rocher sur la porte fermée
                    trapdoor_pos = board.find_trapdoor(plateau)
                    door_pos = board.find_door(plateau)
                    if trapdoor_pos != None and door_pos != None:
                        if plateau[door_pos[0]][door_pos[1]][3] == 9 and (plateau[door_pos[0]][door_pos[1]][2] == 1 or plateau[door_pos[0]][door_pos[1]][2] == 2):
                            plateau[door_pos[0]][door_pos[1]][2] = 0
                    mvt_poss = False  # pour ne pas se déplacer plusieurs cases à la fois
        if touche == parametres["controles"]["reset"]:
            sound_manager.play_sound('reset')
            jeu.haut, jeu.bas, jeu.gauche, jeu.droite = 0, 0, 0, 0
            jeu.marteau = 0
            jeu.corde = 0
            context.door_opened = 0
            if jeu.custom > 0:
                board.genere_niveau(mode="Custom")
            else:
                board.genere_niveau(jeu.niveau, jeu.numero_monde)
        elif touche == parametres["controles"]["menu"]:
            sound_manager.play_sound('menu')
            jeu.marteau = 0
            jeu.corde = 0
            context.door_opened = 0
            jeu.fini = True
            level_flow.reset_hint_tutorial()
            music.stop_music()
            main_menu.create_main_menu()
        # le cas échéant on change de niveau:
        if (board.test_victoire() == True):
            if jeu.custom > 0:
                jeu.fini = True
                music.stop_music()
                sound_manager.play_sound('small_win')
                level_flow.loop_back_to_menu("Custom")
            else:
                jeu.deplacements_tot += jeu.deplacements
                jeu.score += ((1500 * jeu.difficulte / 10) // ((jeu.deplacements // 10) + 1)) * 10
                context.door_opened = 0
                level_flow.reset_hint_tutorial()
                sound_manager.play_sound('small_win')
                render.affiche_plateau_canvas()
                level_flow.attente_post_niveau()
