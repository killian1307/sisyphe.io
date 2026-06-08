# -*- coding: utf-8 -*-
"""Shared UI helpers: the styled-button factory, the return-to-menu handler and
the widget-cleanup routines used when switching screens."""
import tkinter as tk

from .. import context
from . import main_menu

# Recurring palette (from the original inline button definitions).
ACCENT = '#bb7e4b'          # primary action buttons (Play / Back / Quit ...)
ACCENT_ACTIVE = '#714e31'
PANEL = '#bea48e'           # secondary buttons (world tiles, settings rows)
PANEL_ACTIVE = '#7c645c'
DANGER = '#bb4b4b'          # reset buttons
DANGER_ACTIVE = '#713131'


def styled_button(parent, text, command, *, bg, active_bg, fg='WHITE', active_fg='WHITE',
                  width=10, border=5, font_size=20, height=None, state=None,
                  highlight_bg=None, **extra):
    """Create a tk.Button with the project's recurring styling.

    Only ``height``/``state`` are added when given, so callers reproduce the
    exact original widgets (some buttons omit ``height``).
    """
    kwargs = dict(
        background=bg, foreground=fg,
        activebackground=active_bg, activeforeground=active_fg,
        highlightthickness=2,
        highlightbackground=bg if highlight_bg is None else highlight_bg,
        highlightcolor='WHITE',
        width=width, border=border,
        font=('Small Fonts', font_size, 'bold'),
        text=text, command=command,
    )
    if height is not None:
        kwargs['height'] = height
    if state is not None:
        kwargs['state'] = state
    kwargs.update(extra)
    return tk.Button(parent, **kwargs)


def make_return_button(command=None):
    """The standard 'Go Back' button used by several menus."""
    return styled_button(
        context.window, context.lang.back_button, command or button_sound,
        bg=ACCENT, active_bg=ACCENT_ACTIVE, width=10, height=1, border=5, font_size=15,
    )


def button_sound():
    """Play the button click then return to the main menu (back-button handler)."""
    context.sounds.play_sound('button')
    main_menu.create_main_menu()


# --- screen-switch cleanup ---
def clear_buttons_1():
    """Destroy the main-menu widgets when changing screen."""
    for name in ('start_button', 'menu_button', 'edit_button', 'command_button',
                 'credits_button', 'leave_button', 'return_button', 'story'):
        widget = getattr(context, name)
        if widget is not None:
            widget.destroy()
            setattr(context, name, None)


def clear_buttons_2():
    """Destroy the world-selection / credits widgets when changing screen."""
    for elt in context.monde_buttons:
        if elt is not None:
            elt.destroy()
    context.monde_buttons = None
    if context.return_button is not None:
        context.return_button.destroy()
        context.return_button = None


def clear_bg():
    """Destroy the menu background image."""
    if context.background_label is not None:
        context.background_label.destroy()
        context.background_label = None


def clear_canvas_and_buttons():
    """Clear the canvas and destroy every tracked settings-menu button."""
    context.canvas.delete("all")
    for button in context.button_widgets:
        button.destroy()
    context.button_widgets.clear()
