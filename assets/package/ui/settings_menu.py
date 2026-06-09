# -*- coding: utf-8 -*-
"""The settings menu: key rebinding, FPS, language, volumes and reset."""
import os
import tkinter as tk
from tkinter import messagebox

from .. import context
from .. import settings
from .. import board
from .. import view
from . import widgets
from ..audio import music

VALID_KEYS = ["a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "d", "f", "g",
              "h", "j", "k", "l", "m", "w", "x", "c", "v", "b", "n",
              "Up", "Left", "Down", "Right", "space"]


def show_listening_popup(action):
    """Open the popup that listens for the next key to bind to ``action``."""
    context.sounds.play_sound('button')
    popup = tk.Toplevel(context.window)
    context.popup = popup
    popup.title("En attente...")
    popup.configure(bg='#9b6b53')  # Couleur du fond
    popup.geometry("450x100")
    popup.resizable(False, False)
    # Met à jour le label de la popup
    tk.Label(popup, text="Veuillez appuyer sur une touche...", bg='#9b6b53', fg='white',
             font=(context.FONT, "20")).pack(pady=20)
    # Commence à écouter les touches du clavier
    popup.bind('<Key>', lambda event: save_key_press(event, action))
    # La popup prend le focus
    popup.grab_set()
    popup.focus_set()
    # Pour fermer la popup
    popup.protocol("WM_DELETE_WINDOW", lambda: on_popup_close(action))
    # mettre la popup au centre
    window_width, window_height = 200, 100
    position_right = int(popup.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(popup.winfo_screenheight() / 2 - window_height / 2)
    popup.geometry("+{}+{}".format(position_right, position_down))


def on_popup_close(filename):
    """Close the key-listening popup and rebuild the settings menu."""
    if context.popup:
        # Arrête d'écouter les touches du clavier
        context.popup.unbind('<Key>')
        context.popup.destroy()
        context.popup = None
        create_settings_menu()


def save_key_press(event, action):
    """Validate the pressed key and bind it to ``action`` if it is free."""
    touche = event.keysym
    if touche == "Up" or touche == "Left" or touche == "Right" or touche == "Down":
        pass
    else:
        touche = touche.lower()
    if not touche in VALID_KEYS:
        return
    # Vérifie si la touche que l'utilisateur veut utiliser est déjà assingée à une autre touche
    for key, value in context.params["controles"].items():
        if touche == value and key != action:
            return  # La touche est déjà utilisée, ne rien faire
    # Change la touche correspondante au bouton appuyé
    context.params["controles"][action] = touche

    # Sauvegarde les changements dans le fichier JSON
    settings.save(context.params)

    if context.popup:
        on_popup_close(action)  # Ferme la popup


def handle_button_click(action):
    """Return a click handler that opens the key-listening popup for ``action``."""
    def on_click():
        # Affiche la popup et continue le déroulement des actions
        show_listening_popup(action)
    return on_click


def create_direction_button(text, x, y, filename):
    """Create one of the seven control-rebinding buttons."""
    button = widgets.styled_button(
        context.window, text, handle_button_click(filename),
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=10, border=3, font_size=15, anchor="center",
    )
    view.place(button, x, y)
    context.button_widgets.append(button)


def create_settings_menu():
    """Build the settings screen."""
    if context.game.process_launched == True:
        return
    context.rebuild_screen = create_settings_menu  # so F1 rescales this screen
    board.clear_canvas()
    widgets.clear_buttons_1()
    if context.monde_buttons is not None:
        widgets.clear_buttons_2()
    widgets.clear_bg()
    widgets.clear_canvas_and_buttons()

    # rafraîchissement des paramètres
    context.params = settings.load()
    parametres = context.params
    Canevas = context.canvas
    lang = context.lang
    game_images = context.images

    Canevas.create_image(view.X(400), view.Y(300), image=game_images.settings_menu_texture, anchor="center")
    Canevas.create_image(view.X(400), view.Y(60), anchor="center", image=game_images.logo_texture)
    # Titre, sous-titre et textes à gauche des boutons
    Canevas.create_text(view.X(192), view.Y(182), fill='black', font=view.font("20"), text=lang.up, anchor='e')
    Canevas.create_text(view.X(190), view.Y(180), fill='white', font=view.font("20"), text=lang.up, anchor='e')

    Canevas.create_text(view.X(532), view.Y(282), fill='black', font=view.font("20"), text=lang.music, anchor='e')
    Canevas.create_text(view.X(530), view.Y(280), fill='white', font=view.font("20"), text=lang.music, anchor='e')

    Canevas.create_text(view.X(642), view.Y(282), fill='black', font=view.font("20"), text=f"{parametres['volume']['musique']*5} %", anchor='center')
    Canevas.create_text(view.X(640), view.Y(280), fill='white', font=view.font("20"), text=f"{parametres['volume']['musique']*5} %", anchor='center')

    Canevas.create_text(view.X(532), view.Y(182), fill='black', font=view.font("20"), text=lang.fps, anchor='e')
    Canevas.create_text(view.X(530), view.Y(180), fill='white', font=view.font("20"), text=lang.fps, anchor='e')

    Canevas.create_text(view.X(192), view.Y(232), fill='black', font=view.font("20"), text=lang.left, anchor='e')
    Canevas.create_text(view.X(190), view.Y(230), fill='white', font=view.font("20"), text=lang.left, anchor='e')

    Canevas.create_text(view.X(192), view.Y(282), fill='black', font=view.font("20"), text=lang.down, anchor='e')
    Canevas.create_text(view.X(190), view.Y(280), fill='white', font=view.font("20"), text=lang.down, anchor='e')

    Canevas.create_text(view.X(532), view.Y(332), fill='black', font=view.font("20"), text=lang.sounds, anchor='e')
    Canevas.create_text(view.X(530), view.Y(330), fill='white', font=view.font("20"), text=lang.sounds, anchor='e')

    Canevas.create_text(view.X(642), view.Y(332), fill='black', font=view.font("20"), text=f"{parametres['volume']['sons']*5} %", anchor='center')
    Canevas.create_text(view.X(640), view.Y(330), fill='white', font=view.font("20"), text=f"{parametres['volume']['sons']*5} %", anchor='center')

    Canevas.create_text(view.X(192), view.Y(332), fill='black', font=view.font("20"), text=lang.right, anchor='e')
    Canevas.create_text(view.X(190), view.Y(330), fill='white', font=view.font("20"), text=lang.right, anchor='e')

    Canevas.create_text(view.X(532), view.Y(232), fill='black', font=view.font("20"), text=lang.language, anchor='e')
    Canevas.create_text(view.X(530), view.Y(230), fill='white', font=view.font("20"), text=lang.language, anchor='e')

    Canevas.create_text(view.X(192), view.Y(382), fill='black', font=view.font("20"), text=lang.interact, anchor='e')
    Canevas.create_text(view.X(190), view.Y(380), fill='white', font=view.font("20"), text=lang.interact, anchor='e')

    Canevas.create_text(view.X(192), view.Y(432), fill='black', font=view.font("20"), text=lang.restart, anchor='e')
    Canevas.create_text(view.X(190), view.Y(430), fill='white', font=view.font("20"), text=lang.restart, anchor='e')

    Canevas.create_text(view.X(192), view.Y(482), fill='black', font=view.font("20"), text=lang.menu, anchor='e')
    Canevas.create_text(view.X(190), view.Y(480), fill='white', font=view.font("20"), text=lang.menu, anchor='e')

    Canevas.create_text(view.X(402), view.Y(122), fill='black', font=view.font("25"), text=lang.settings, anchor='center')
    Canevas.create_text(view.X(400), view.Y(120), fill='white', font=view.font("25"), text=lang.settings, anchor='center')

    # Boutons pour afficher et changer les contrôles
    create_direction_button(f'{parametres["controles"]["up"].upper()}', 230, 160, 'up')
    create_direction_button(f'{parametres["controles"]["left"].upper()}', 230, 210, 'left')
    create_direction_button(f'{parametres["controles"]["down"].upper()}', 230, 260, 'down')
    create_direction_button(f'{parametres["controles"]["right"].upper()}', 230, 310, 'right')
    create_direction_button(f'{parametres["controles"]["interact"].upper()}', 230, 360, 'interact')
    create_direction_button(f'{parametres["controles"]["reset"].upper()}', 230, 410, 'reset')
    create_direction_button(f'{parametres["controles"]["menu"].upper()}', 230, 460, 'menu')

    button = widgets.styled_button(
        context.window, lang.reset_button, reset_settings,
        bg=widgets.DANGER, active_bg=widgets.DANGER_ACTIVE,
        width=15, border=5, font_size=15, anchor="center",
    )
    button_width_pixels = 214
    window_width = 800
    x_position = (window_width - button_width_pixels) / 2
    view.place(button, x_position, 525)
    context.button_widgets.append(button)

    return_button = widgets.make_return_button()
    view.place(return_button, 625, 525)
    context.button_widgets.append(return_button)

    if parametres["fps"]["mode"] == 1:
        fps = 10
    else:
        fps = 30
    if parametres["fps"]["show"]:
        fps_state = lang.fps_show
    else:
        fps_state = lang.fps_hide

    fps_button = widgets.styled_button(
        context.window, fps, change_fps,
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=3, height=1, border=3, font_size=15,
    )
    view.place(fps_button, 570, 160)
    context.button_widgets.append(fps_button)

    fps_show = widgets.styled_button(
        context.window, fps_state[0].upper() + fps_state[1:].lower(), change_show_fps,
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=6, height=1, border=3, font_size=15,
    )
    view.place(fps_show, 622, 160)
    context.button_widgets.append(fps_show)

    music_button_minus = widgets.styled_button(
        context.window, "-", lambda: change_volume_musique("down"),
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=1, border=3, font_size=15,
    )
    view.place(music_button_minus, 570, 260)
    context.button_widgets.append(music_button_minus)

    music_button_plus = widgets.styled_button(
        context.window, "+", lambda: change_volume_musique("up"),
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=1, border=3, font_size=15,
    )
    view.place(music_button_plus, 687, 260)
    context.button_widgets.append(music_button_plus)

    sound_button_minus = widgets.styled_button(
        context.window, "-", lambda: change_volume_sons("down"),
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=1, border=3, font_size=15,
    )
    view.place(sound_button_minus, 570, 310)
    context.button_widgets.append(sound_button_minus)

    sound_button_plus = widgets.styled_button(
        context.window, "+", lambda: change_volume_sons("up"),
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=1, border=3, font_size=15,
    )
    view.place(sound_button_plus, 687, 310)
    context.button_widgets.append(sound_button_plus)

    language_button = widgets.styled_button(
        context.window, context.languages_dic[parametres["language"]], change_language,
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=10, height=1, border=3, font_size=15,
    )
    view.place(language_button, 570, 210)
    context.button_widgets.append(language_button)

    context.window.after(200, lambda: music.play_music(os.path.join(context.assets_dir, 'assets', 'mus', 'menu_settings.ogg')))


def change_fps():
    """Toggle between the two FPS modes (10/30)."""
    context.sounds.play_sound('button')
    if context.params["fps"]["mode"] == 2:
        context.params["fps"]["mode"] = 1
    else:
        context.params["fps"]["mode"] = 2
    settings.save(context.params)
    create_settings_menu()


def change_language():
    """Cycle to the next language in the catalog order."""
    context.sounds.play_sound('button')
    assert context.params["language"] in context.languages
    index_language = context.languages.index(context.params["language"])
    if index_language < len(context.languages) - 1:
        index_language += 1
    else:
        index_language = 0
    context.params["language"] = context.languages[index_language]
    settings.save(context.params)
    context.lang.apply(context.params["language"])
    create_settings_menu()


def change_volume_musique(direction):
    """Raise/lower the music volume by one step (0..20)."""
    context.sounds.play_sound('button')
    if context.params["volume"]['musique'] < 20 and direction == "up":
        context.params["volume"]['musique'] += 1
    elif context.params["volume"]['musique'] > 0 and direction == "down":
        context.params["volume"]['musique'] -= 1
    settings.save(context.params)
    music.set_volume(context.params["volume"]['musique'])
    create_settings_menu()


def change_volume_sons(direction):
    """Raise/lower the sound-effects volume by one step (0..20)."""
    context.sounds.play_sound('button')
    if context.params["volume"]['sons'] < 20 and direction == "up":
        context.params["volume"]['sons'] += 1
    elif context.params["volume"]['sons'] > 0 and direction == "down":
        context.params["volume"]['sons'] -= 1
    settings.save(context.params)
    context.sounds.set_volume(context.params["volume"]["sons"])
    create_settings_menu()


def change_show_fps():
    """Toggle whether the FPS counter is shown in-game."""
    context.sounds.play_sound('button')
    context.params["fps"]["show"] = not context.params["fps"]["show"]
    settings.save(context.params)
    create_settings_menu()


def reset_settings():
    """Restore every setting to its default after confirmation."""
    context.sounds.play_sound('button')
    if messagebox.askyesno(context.lang.confirm, context.lang.reset_lang_confirm, icon="warning"):
        context.sounds.play_sound('button')
        context.params["controles"]["up"] = "Up"
        context.params["controles"]["left"] = "Left"
        context.params["controles"]["down"] = "Down"
        context.params["controles"]["right"] = "Right"
        context.params["controles"]["interact"] = "e"
        context.params["controles"]["reset"] = "r"
        context.params["controles"]["menu"] = "m"
        context.params["fps"]["mode"] = 2
        context.params["fps"]["show"] = True
        context.params["volume"]['musique'] = 10
        context.params["volume"]['sons'] = 10
        context.params["language"] = "fr"
        settings.save(context.params)
        music.set_volume(context.params["volume"]['musique'])
        context.sounds.set_volume(context.params["volume"]["sons"])
        context.lang.apply(context.params["language"])
        create_settings_menu()
    else:
        context.sounds.play_sound('button')
