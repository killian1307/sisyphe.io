# -*- coding: utf-8 -*-
"""The per-world tutorial dialog box shown at the bottom of the screen."""
import tkinter as tk
from tkinter import ttk

from .. import context
from .. import settings


def show_dialog_bottom_screen(world_number):
    """Show the tutorial/end message for ``world_number`` (6 = game finished)."""
    def close_tutorial():
        """Close the open dialog box."""
        context.sounds.play_sound('button')
        context.canvas.focus_force()
        text_widget.unbind('<Return>')
        dialog_frame.destroy()
        border_frame.destroy()
        if world_number == 6:
            overlay.destroy()
        context.dialog_opened = False

    if context.dialog_opened == False:
        context.sounds.play_sound('popup')

        lang = context.lang
        parametres = context.params

        # Crée un label qui va recouvrir le menu principal
        if world_number == 6:
            overlay = tk.Label(context.window, image=context.images.world_menu_texture)
            overlay.place(x=0, y=0, relwidth=1, relheight=1)
            overlay.bind("<Button-1>", lambda event: "break")  # Empêche d'intéragir avec le label

        # Tous les textes de Tutoriels
        tuto_monde = {
            1: lang.w1_tutorial_1 + f"[ {parametres['controles']['reset'].upper()} ]" + lang.w1_tutorial_2 + f"[ {parametres['controles']['menu'].upper()} ].",
            2: lang.w2_tutorial,
            3: lang.w3_tutorial_1 + f"[ {parametres['controles']['interact'].upper()} ]" + lang.w3_tutorial_2,
            4: lang.w4_tutorial,
            5: lang.w5_tutorial + f"[ {parametres['controles']['interact'].upper()} ].",
            6: lang.finished
        }

        dialog_text = tuto_monde[world_number]
        bg_color = '#998070'
        fg_color = 'WHITE'
        font_style = ('Small Fonts', 15)

        # Bordure de la boîte
        border_frame = tk.Frame(context.window, background='#433632')

        # Boîte de dialogue
        dialog_frame = tk.Frame(context.window, bg=bg_color)
        dialog_frame.pack_propagate(False)  # Taille fixe pour la boîte

        # Texte à afficher
        text_widget = tk.Text(dialog_frame, wrap='word', font=font_style, borderwidth=0, bg=bg_color, fg=fg_color, height=4)
        text_widget.insert('1.0', dialog_text)
        text_widget.configure(state='disabled', padx=10, pady=10, cursor=context.cursor_spec, takefocus=0)
        text_widget.tag_configure("centre_texte", justify='center')
        text_widget.tag_add("centre_texte", "1.0", "end")
        text_widget.focus_set()

        text_widget.bind("<Button-1>", lambda event: "break")
        text_widget.bind("<Button-2>", lambda event: "break")
        text_widget.bind("<Button-3>", lambda event: "break")
        text_widget.bind('<B1-Motion>', lambda event: "break")
        text_widget.bind("<FocusIn>", lambda event: "break")
        text_widget.bind('<Return>', lambda event=None: close_tutorial())

        scrollbar = ttk.Scrollbar(dialog_frame, orient="vertical", style='Vertical.TScrollbar', command=text_widget.yview)
        text_widget['yscrollcommand'] = scrollbar.set

        scrollbar.pack(side='right', fill='y')

        # Bouton fermer
        close_button = tk.Button(dialog_frame, text=lang.popup_close_button, font=font_style, bg='#bea48e', border=2, fg=fg_color, activebackground='#7c645c', activeforeground='white', command=close_tutorial)

        # Met le bouton et le texte dans la boîte de dialogue
        text_widget.pack(side='top', fill='x', expand=True)
        close_button.pack(side='bottom', pady=10)

        # Calcule la taille du texte
        text_widget.update_idletasks()
        text_height = text_widget.winfo_reqheight()

        # Calcule la hauteur de la boîte
        button_height = close_button.winfo_reqheight()
        dialog_frame_height = text_height + button_height + 20

        # Centrer la boîte de dialogue sur l'écran
        window_width = context.window.winfo_width()
        dialog_frame_width = window_width * 0.8  # 80% de la taille de la fenêtre

        # Met la boîte de dialogue au centre de la fenêtre
        border_frame.place(in_=context.window, anchor='center', relx=0.5, rely=0.5, width=dialog_frame_width + 10, height=dialog_frame_height + 10)
        dialog_frame.place(in_=context.window, anchor='center', relx=0.5, rely=0.5, width=dialog_frame_width, height=dialog_frame_height)

        # Empêche le tutoriel de se montrer plusieurs fois
        parametres["tutoriels"][f"tutoriel_{world_number}_termine"] = True
        settings.save(parametres)

        context.dialog_opened = True
