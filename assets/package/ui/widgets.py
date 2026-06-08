# -*- coding: utf-8 -*-
"""Shared UI helpers: the styled-button factory, the return-to-menu handler and
the widget-cleanup routines used when switching screens.

Every button is rendered from a ``tk.Label`` (not ``tk.Button``) with hover/press
bindings, so the look is *identical on every platform*. This is required because
macOS's native Aqua ``tk.Button`` ignores ``bg``/``relief``/``borderwidth`` and
draws its own button, whereas a ``tk.Label`` honors them everywhere.
"""
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


class _StyledButton(tk.Label):
    """A button drawn from a Label so the custom styling renders the same on
    Windows, macOS and Linux."""

    def __init__(self, parent, *, text, command, bg, active_bg, fg, active_fg,
                 font, width, border, height=None, state=None, highlight_bg=None,
                 disabledforeground=None, anchor='center', **_ignore):
        opts = dict(
            text=text, background=bg, foreground=fg, font=font,
            borderwidth=border, relief='raised',
            highlightthickness=2, highlightbackground=highlight_bg or bg,
            highlightcolor='WHITE', anchor=anchor,
        )
        if width is not None:
            opts['width'] = width
        if height is not None:
            opts['height'] = height
        super().__init__(parent, **opts)
        self._bg, self._active_bg = bg, active_bg
        self._fg, self._active_fg = fg, active_fg
        self._command = command
        if state == 'disabled':
            self.configure(foreground=disabledforeground or fg, relief='groove')
        else:
            self.bind('<Enter>', self._on_enter, add='+')
            self.bind('<Leave>', self._on_leave, add='+')
            self.bind('<ButtonPress-1>', self._on_press, add='+')
            self.bind('<ButtonRelease-1>', self._on_release, add='+')

    def _on_enter(self, _event):
        self.configure(background=self._active_bg, foreground=self._active_fg)

    def _on_leave(self, _event):
        self.configure(background=self._bg, foreground=self._fg, relief='raised')

    def _on_press(self, _event):
        self.configure(relief='sunken', background=self._active_bg, foreground=self._active_fg)

    def _on_release(self, event):
        self.configure(relief='raised', background=self._bg, foreground=self._fg)
        inside = 0 <= event.x < self.winfo_width() and 0 <= event.y < self.winfo_height()
        if self._command is not None and inside:
            self._command()


def styled_button(parent, text, command, *, bg, active_bg, fg='WHITE', active_fg='WHITE',
                  width=10, border=5, font_size=20, height=None, state=None,
                  highlight_bg=None, **extra):
    """Create a button with the project's recurring styling.

    Rendered identically on every platform via :class:`_StyledButton`.
    ``width`` may be ``None`` to auto-size to the text.
    """
    font = (context.FONT, font_size, 'bold')
    return _StyledButton(parent, text=text, command=command, bg=bg, active_bg=active_bg,
                         fg=fg, active_fg=active_fg, font=font, width=width, border=border,
                         height=height, state=state, highlight_bg=highlight_bg, **extra)


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
