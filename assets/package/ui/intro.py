# -*- coding: utf-8 -*-
"""The opening fade-in/fade-out of the welcome text, then the main menu."""
import tkinter as tk

from .. import context
from . import main_menu

_FADE = ["#000000", "#2b2b2b", "#808080", "#c0c0c0", "#ffffff"]


def start():
    """Hide the cursor and kick off the welcome-text fade sequence."""
    context.canvas.configure(cursor='none')
    label = tk.Label(context.window, text=context.lang.welcome, fg="black", bg="black",
                     font=('Small Fonts', 30, 'bold'), cursor='none')
    label.place(relx=0.5, rely=0.5, anchor="center")
    context.window.after(500, fade_in_text, label)


def fade_in_text(label, fade=1):
    """Fade the welcome text in, then schedule the fade-out."""
    if fade < 5:
        label.config(fg=_FADE[fade])
        context.window.after(300, fade_in_text, label, fade + 1)
    else:
        context.window.after(3000, fade_out_text, label)


def fade_out_text(label, fade=4):
    """Fade the welcome text out, then open the main menu."""
    if fade >= 0:
        label.config(fg=_FADE[fade])
        context.window.after(300, fade_out_text, label, fade - 1)
    else:
        label.destroy()
        context.window.after(500, main_menu.create_main_menu)
