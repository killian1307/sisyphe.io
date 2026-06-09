# -*- coding: utf-8 -*-
"""In-window editor toolbar overlay.

Replaces the native menu bar (which jumps to the OS top bar — bad in fullscreen)
with an on-screen toolbar drawn inside the game window: a top strip of file /
toggle actions + Back, and a bottom strip of tool icons with the active tool
highlighted. All keyboard shortcuts are unchanged (see editor/menu.bind_keys).

The toolbar sits over the top/bottom border rows (always auto-walls), so it never
covers an editable interior cell. It scales with :mod:`view` like everything else.
"""
from .. import view
from .. import tooltip
from ..ui import widgets
from . import context as ectx
from . import textures
from . import tools
from . import files
from . import toggles

ICON_LOGICAL = 38  # tool-icon size in logical px (scaled by view)

_widgets = []
_tool_buttons = {}   # element_type code -> button
_trace_name = None

# (element_type code, texture key or None=delete, lang attr for the tooltip)
_TOOL_DEFS = [
    (1, 'wall', 'select_wall'),
    (2, 'crate', 'select_boulder'),
    (3, 'button', 'select_hole'),
    (12, 'box', 'select_box'),
    (4, 'sisyphe', 'select_player'),
    (5, 'bportal', 'select_portal1'),
    (6, 'rportal', 'select_portal2'),
    (7, 'door', 'select_door'),
    (8, 'trapdoor', 'select_pressure_plate'),
    (9, 'fwall', 'select_cracked_wall'),
    (10, 'hammer', 'select_hammer'),
    (11, 'rope', 'select_rope'),
    (0, None, 'delete_mode'),
]
_SELECT = {
    1: tools.select_wall, 2: tools.select_boulder, 3: tools.select_hole,
    12: tools.select_box, 4: tools.select_player, 5: tools.select_portal_blue,
    6: tools.select_portal_red, 7: tools.select_door, 8: tools.select_trapdoor,
    9: tools.select_fwall, 10: tools.select_hammer, 11: tools.select_rope,
    0: tools.select_delete,
}


def build():
    """Create (or rebuild) the toolbar overlay at the current scale."""
    teardown()
    lang = ectx.lang
    icons = textures.load(ectx.base_path, max(1, round(view.S(ICON_LOGICAL))))

    # --- top strip: Back, file actions, toggles ---
    top = [
        (lang.back_button, files.confirm_close, None),
        (lang.new_button, files.new_level, None),
        (lang.open_button, files.open_level, None),
        (lang.save_button, files.save, None),
        (lang.save_as_button, files.save_as, None),
        ("Tex", toggles.toggle_textures, lang.toggle_textures_button),
        ("Mus", toggles.toggle_music, lang.toggle_music_button),
        ("SFX", toggles.toggle_sounds, lang.toggle_sounds_button),
    ]
    top_buttons = []
    for label, cmd, tip in top:
        b = widgets.styled_button(ectx.window, label, cmd, bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
                                  width=None, border=2, font_size=10)
        if tip:
            tooltip.ToolTip(b, tip)
        top_buttons.append(b)
        _widgets.append(b)
    # measure then lay out left-to-right in logical space
    ectx.window.update_idletasks()
    x = 6
    for b in top_buttons:
        view.place(b, x, 6)
        x += b.winfo_reqwidth() / view.scale + 4

    # --- bottom strip: tool icons (centred) ---
    _tool_buttons.clear()
    step = 46  # logical spacing per tool button
    x = (800 - len(_TOOL_DEFS) * step) / 2
    for code, key, tip_attr in _TOOL_DEFS:
        img = icons.get(key) if key else None
        b = widgets.styled_button(ectx.window, '' if img else '✕', lambda c=code: _pick(c),
                                  bg=widgets.PANEL, active_bg=widgets.PANEL_ACTIVE,
                                  width=None, border=2, font_size=12, image=img)
        view.place(b, x, 556)
        tooltip.ToolTip(b, getattr(lang, tip_attr))
        _widgets.append(b)
        _tool_buttons[code] = b
        x += step

    # keep the highlight in sync with keyboard shortcuts too
    global _trace_name
    _trace_name = ectx.element_type.trace_add('write', lambda *a: _refresh())
    _refresh()


def _pick(code):
    _SELECT[code]()  # sets element_type -> trace -> _refresh()


def _refresh():
    selected = ectx.element_type.get()
    for code, btn in _tool_buttons.items():
        btn.configure(highlightbackground=('white' if code == selected else widgets.PANEL))


def teardown():
    """Destroy the overlay widgets and detach the selection trace."""
    global _trace_name
    if _trace_name is not None:
        try:
            ectx.element_type.trace_remove('write', _trace_name)
        except Exception:
            pass
        _trace_name = None
    for w in _widgets:
        w.destroy()
    _widgets.clear()
    _tool_buttons.clear()
