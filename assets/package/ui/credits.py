# -*- coding: utf-8 -*-
"""The credits screen and the website button."""
import tkinter as tk

from .. import context
from .. import platform_utils
from .. import tooltip
from .. import board
from . import widgets


def _author_button(text, x, y, role):
    """A non-clickable label-style button naming a contributor, with a role tooltip."""
    btn = tk.Button(context.window, text=text, disabledforeground='WHITE', state="disabled",
                    font=('Small Fonts', 15, 'bold'), height=1, borderwidth=0, background="black")
    btn.place(x=x, y=y)
    context.monde_buttons.append(btn)
    tooltip.ToolTip(btn, role)


def credits_menu():
    """Build the credits screen."""
    context.sounds.play_sound('button')
    if context.game.process_launched == True:
        return
    board.clear_canvas()
    widgets.clear_buttons_1()
    widgets.clear_bg()

    if context.background_label is None:
        background_image = context.images.main_menu_texture
        context.background_label = tk.Label(context.window, image=background_image)
        context.background_label.place(x=0, y=0, width=800, height=600)

    context.monde_buttons = []
    return_button = widgets.make_return_button()
    return_button.place(x=625, y=525)
    context.monde_buttons.append(return_button)

    website_button = widgets.styled_button(
        context.window, "sisyphe.acciaw.me", open_website,
        bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
        width=18, height=1, border=5, font_size=15,
    )
    website_button.place(x=400 - website_button.winfo_reqwidth() // 2, y=525)
    context.monde_buttons.append(website_button)

    _author_button("Killian", 540, 265, "Developer, Lead Editor Developer, Game Designer, Web Developer, Level Designer")
    _author_button("Siméon", 350, 250, "Developer, Editor Developer, Lead Game Designer, Level Designer, Quality Assurance Tester")
    _author_button("Kylian", 175, 300, "Lead Developer, Game Designer, Translator, Pixel Artist, Level Designer")
    _author_button("Tristan", 85, 450, "Developer, Editor Developer, Lead Level Designer, Quality Assurance Tester")
    _author_button("Malik", 690, 450, "Developer, Game Designer, Lead Web Developer, Level Designer")


def open_website():
    """Open the project website in the default browser."""
    context.sounds.play_sound('button')
    platform_utils.open_url("https://sisyphe.acciaw.me/")
