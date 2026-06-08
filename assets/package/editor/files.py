# -*- coding: utf-8 -*-
"""New / open / save / save-as, the close guard and the level validator."""
import json
from tkinter import filedialog, messagebox

from . import context as ectx
from . import render
from ..audio import music


def new_level():
    """Start a blank level (prompting if there are unsaved changes)."""
    lang = ectx.lang
    # Vérifie si les modifications ont été enregistrées
    if ectx.unsaved_changes:
        if messagebox.askyesno(lang.unsaved_title, lang.unsaved, icon="warning"):
            ectx.unsaved_changes = False
            new_level()
            return
        else:
            return
    ectx.plateau = [[[0] * 4 for _ in range(16)] for _ in range(12)]
    ectx.unsaved_changes = False

    # Titre du niveau
    ectx.file_opened = lang.editor_new_file
    ectx.filepath = ""
    ectx.window.title(f"{lang.editor_title} - {ectx.file_opened}")
    render.affiche_plateau_canvas()


def open_level():
    """Open a level JSON (prompting if there are unsaved changes)."""
    lang = ectx.lang
    # Vérifie si les modifications ont été enregistrées
    if ectx.unsaved_changes:
        if messagebox.askyesno(lang.unsaved_title, lang.unsaved, icon="warning"):
            ectx.unsaved_changes = False
            open_level()
            return
        else:
            return
    ectx.filepath = filedialog.askopenfilename(title=lang.open_file, filetypes=[("JSON files", "*.json")])
    if not ectx.filepath:  # L'utilisateur n'a rien choisi
        return
    try:
        with open(ectx.filepath, 'r') as infile:
            loaded_data = json.load(infile)
            ectx.plateau = loaded_data
            ectx.unsaved_changes = False

            # Titre du niveau
            ectx.file_opened = ectx.filepath.split("/")[-1]
            ectx.window.title(f"{lang.editor_title} - {ectx.file_opened}")

            render.affiche_plateau_canvas()
    except Exception:
        messagebox.showerror(lang.error, lang.corrupted)
        new_level()


def save():
    """Save to the current file, asking for a name on first save."""
    lang = ectx.lang
    if not_valid():
        return
    if not ectx.filepath:  # Regarde si l'utilisateur a choisi un nom de fichier
        ectx.filepath = filedialog.asksaveasfilename(initialfile=ectx.file_opened, defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if ectx.filepath:
        try:
            with open(ectx.filepath, 'w') as outfile:
                json.dump(ectx.plateau, outfile)
            ectx.unsaved_changes = False

            # Titre du niveau
            ectx.file_opened = ectx.filepath.split("/")[-1]
            ectx.window.title(f"{lang.editor_title} - {ectx.file_opened}")
        except Exception as e:
            messagebox.showerror(lang.error, lang.error_opening + str(e))


def save_as():
    """Save to a newly chosen file."""
    lang = ectx.lang
    if not_valid():
        return
    filepath2 = filedialog.asksaveasfilename(initialfile=ectx.file_opened, defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if filepath2:  # Regarde si l'utilisateur a choisi un nom de fichier
        try:
            ectx.filepath = filepath2
            with open(ectx.filepath, 'w') as outfile:
                json.dump(ectx.plateau, outfile)
            ectx.unsaved_changes = False

            # Titre du niveau
            ectx.file_opened = ectx.filepath.split("/")[-1]
            ectx.window.title(f"{lang.editor_title} - {ectx.file_opened}")
        except Exception as e:
            messagebox.showerror(lang.error, lang.error_opening + str(e))


def confirm_close():
    """Close the editor, warning if there are unsaved changes."""
    lang = ectx.lang
    if ectx.unsaved_changes:
        if messagebox.askyesno(lang.unsaved_title, lang.unsaved, icon="warning"):
            music.stop_music()
            ectx.window.destroy()
    else:
        music.stop_music()
        ectx.window.destroy()


def not_valid():
    """Validate the level before saving. Returns True if invalid."""
    lang = ectx.lang
    plateau = ectx.plateau
    error = ""

    # Met des variables pour chaque type d'objet à vérifier
    player = False
    portal_blue = False
    portal_red = False
    door = False
    trapdoor = False
    button = 0
    crate = 0

    # Boucle qui compte les différents objets obligatoires
    for i in range(12):
        for j in range(16):
            if plateau[i][j][1] == 1:
                player = True
            elif plateau[i][j][1] == 2:
                portal_blue = True
            elif plateau[i][j][2] == 2:
                portal_red = True
            elif plateau[i][j][1] == 3:
                door = True
            elif plateau[i][j][2] == 3:
                trapdoor = True
            elif plateau[i][j][2] == 1:
                crate += 1
            elif plateau[i][j][3] == 1:
                button += 1

    # Met un message d'erreur si l'une des conditions n'est pas remplie
    if player == False:
        error = lang.error_player
    elif button == 0 or crate == 0 or button > crate:
        error = lang.error_boulder
    elif portal_blue == True and portal_red == False or portal_blue == False and portal_red == True:
        error = lang.error_portal
    elif door == True and trapdoor == False or door == False and trapdoor == True:
        error = lang.error_door

    if error != "":
        messagebox.showerror(lang.error, lang.error_not_valid + str(error))
        return True
    return False
