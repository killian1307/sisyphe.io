# -*- coding: utf-8 -*-
"""The main menu, the scrolling story text, the editor-launch logic and quit."""
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox

from .. import context
from .. import settings
from . import widgets
from . import world_select
from . import settings_menu
from . import credits
from . import dialogs
from .. import level_flow
from ..audio import music


# --- editor subprocess (kept tracked via threading, as in the original) ---
def monitor_subprocess(process):
    """Watch the editor process; when it closes, restore menu music + story."""
    process.wait()  # Attend la fin du sous-processus
    context.game.process_launched = False
    try:
        histoire_sisyphe = context.lang.story + "  —  "
        cycle(context.story, histoire_sisyphe)
        context.window.after(200, lambda: music.play_music(os.path.join(context.assets_dir, 'assets', 'mus', 'menu_main.ogg')))
    except Exception:
        print("Le jeu est fermé")


def open_external_app():
    """Launch the level editor as a separate process."""
    context.sounds.play_sound('button')
    if context.game.process_launched == False:
        if context.fichier_exe == True:
            proc = subprocess.Popen([os.path.join(context.assets_dir, 'assets', 'editor.exe')])
        else:
            proc = subprocess.Popen([sys.executable, os.path.join(context.assets_dir, 'assets', 'editor.py')])
        context.game.process_launched = True
        monitor_thread = threading.Thread(target=monitor_subprocess, args=(proc,))
        monitor_thread.start()
        music.stop_music()


def show_popup():
    """Windows-style 'access denied' message when a feature is locked."""
    context.sounds.play_sound('button')
    if context.game.process_launched == True:
        return
    if messagebox.showinfo(context.lang.no_access_title, context.lang.no_access, icon="warning") == 'ok':
        context.sounds.play_sound('button')


def quitter(croix=False):
    """Close the program. ``croix`` is True for an ALT+F4 / window-close."""
    if context.game.process_launched == True:
        if croix == False:
            context.sounds.play_sound('button')
            return
    elif croix == False:
        context.sounds.play_sound('button')
    # Arrête la musique à la fermeture du jeu
    music.stop_music()
    context.window.destroy()


def button_world():
    """Main-menu Play button: play the click then open world selection."""
    context.sounds.play_sound('button')
    world_select.create_world_selection_menu()


def button_settings():
    """Main-menu Settings button: play the click then open the settings menu."""
    context.sounds.play_sound('button')
    settings_menu.create_settings_menu()


def create_main_menu():
    """Build (and refresh) the main menu."""
    # Pour bouton reset/menu
    widgets.clear_canvas_and_buttons()
    widgets.clear_buttons_1()
    widgets.clear_bg()

    context.canvas.configure(bg='#9b6b53')

    # Titre de la fenêtre
    context.window.title(context.lang.game_name)

    # Image en fond d'écran
    if context.background_label is None:
        background_image = context.images.world_menu_texture
        context.background_label = tk.Label(context.window, image=background_image)
        context.background_label.place(x=0, y=0, width=800, height=600)

    if context.monde_buttons is not None:
        widgets.clear_buttons_2()
    # couleurs pour le bouton
    color2 = '#bb7e4b'
    color3 = '#714e31'
    color4 = 'WHITE'

    # refresh les paramètres du jeu
    context.params = settings.load()

    # Bouton Démarrer
    context.start_button = widgets.styled_button(
        context.window, context.lang.play_button, button_world,
        bg=color2, active_bg=color3, fg=color4, active_fg=color4,
        width=10, height=1, border=5, font_size=20,
    )

    if context.params["mondes"]["monde_1_termine"] == True:
        # Bouton Niveaux Custom
        context.menu_button = widgets.styled_button(
            context.window, context.lang.open_button, level_flow.start_game_custom,
            bg=color2, active_bg=color3, fg=color4, active_fg=color4,
            width=10, height=1, border=5, font_size=20,
        )
        # Bouton Editeur de niveaux
        context.edit_button = widgets.styled_button(
            context.window, context.lang.editor_button, open_external_app,
            bg=color2, active_bg=color3, fg=color4, active_fg=color4,
            width=10, height=1, border=5, font_size=20,
        )
    else:
        # Bouton Niveaux Custom grisé
        context.menu_button = widgets.styled_button(
            context.window, context.lang.open_button, show_popup,
            bg='#656565', active_bg='#656565', fg='#a9a9a9', active_fg='#a9a9a9',
            width=10, height=1, border=5, font_size=20,
        )
        # Bouton Editeur de niveaux grisé
        context.edit_button = widgets.styled_button(
            context.window, context.lang.editor_button, show_popup,
            bg='#656565', active_bg='#656565', fg='#a9a9a9', active_fg='#a9a9a9',
            width=10, height=1, border=5, font_size=20,
        )

    # Bouton Commandes du jeu
    context.command_button = widgets.styled_button(
        context.window, context.lang.settings, button_settings,
        bg=color2, active_bg=color3, fg=color4, active_fg=color4,
        width=10, height=1, border=5, font_size=20,
    )

    context.credits_button = widgets.styled_button(
        context.window, context.lang.credits_button, credits.credits_menu,
        bg=color2, active_bg=color3, fg=color4, active_fg=color4,
        width=10, height=1, border=5, font_size=20,
    )

    context.leave_button = widgets.styled_button(
        context.window, context.lang.leave_button, quitter,
        bg=color2, active_bg=color3, fg=color4, active_fg=color4,
        width=10, height=1, border=5, font_size=20,
    )

    # calcul du milieu de l'écran où placer le bouton
    button_width = context.start_button.winfo_reqwidth()
    button_height = context.start_button.winfo_reqheight()
    window_width = 800
    window_height = 600

    x = window_width / 2 - button_width - 10
    y = window_height / 2 - button_height - 10
    context.start_button.place(x=x, y=y)

    x = window_width / 2 - button_width - 10
    y = window_height / 2 + 10
    context.command_button.place(x=x, y=y)

    x = window_width / 2 + 10
    y = window_height / 2 - button_height - 10
    context.menu_button.place(x=x, y=y)

    x = window_width / 2 + 10
    y = window_height / 2 + 10
    context.edit_button.place(x=x, y=y)

    x = window_width / 2 - button_width - 10
    y = window_height / 2 + button_height + 30
    context.credits_button.place(x=x, y=y)

    x = window_width / 2 + 10
    y = window_height / 2 + button_height + 30
    context.leave_button.place(x=x, y=y)

    # Variable pour le texte qui défile
    histoire_sisyphe = context.lang.story + "  —  "

    context.story = tk.Label(context.window, text=histoire_sisyphe, fg="white", bg='black', font=(context.FONT, 15, 'bold'))

    y = window_height / 2 + button_height * 3 + 30
    context.story.place(x=400, y=y, anchor="center")

    # Boucle de l'histoire
    cycle(context.story, histoire_sisyphe)

    # Montre le curseur à nouveau après le jeu (pour le menu paramètres)
    context.canvas.configure(cursor=context.cursor_spec)
    context.window.after(200, lambda: music.play_music(os.path.join(context.assets_dir, 'assets', 'mus', 'menu_main.ogg')))

    if context.params["mondes"]["monde_5_termine"] == True and context.params["tutoriels"]["tutoriel_6_termine"] == False:
        dialogs.show_dialog_bottom_screen(6)


def cycle(label, text):
    """Recursively rotate the scrolling story text under the menu."""
    # Regarde si le label existe
    if label.winfo_exists() and context.game.process_launched == False:
        # Met une largeur définie pour le label
        label.config(width=50)
        # Met à jour le label
        label.configure(text=text)
        # Effectue la rotation des lettres du texte
        text = text[1:] + text[0]
        # Appelle la fonction récursivement
        context.window.after(300, cycle, label, text)
