# -*- coding: utf-8 -*-
"""Loads the editor's block textures (collapses the repeated Image.open blocks).

The cell size is a parameter so the editor can rebuild crisp textures when the
window is scaled (fullscreen).
"""
import os

from PIL import Image, ImageTk


def _load(path, cell):
    image = Image.open(path)
    resample = Image.NEAREST if (cell >= image.width and cell >= image.height) else Image.LANCZOS
    image = image.resize((cell, cell), resample)
    return ImageTk.PhotoImage(image)


def load(base_path, cell=50):
    """Return a name -> PhotoImage dict for every editor texture at ``cell`` px."""
    def blocs(name):
        return os.path.join(base_path, 'img', 'blocs', name)

    def char(name):
        return os.path.join(base_path, 'img', 'char', name)

    return {
        'sisyphe': _load(char('sisyphe_bas_1.png'), cell),
        'ground': _load(blocs('ground.png'), cell),
        'wall': _load(blocs('wall.png'), cell),
        'crate': _load(blocs('crate.png'), cell),
        'button': _load(blocs('button.png'), cell),
        'bportal': _load(blocs('blue_portal.png'), cell),
        'rportal': _load(blocs('red_portal.png'), cell),
        'door': _load(blocs('door_closed.png'), cell),
        'trapdoor': _load(blocs('trapdoor.png'), cell),
        'fwall': _load(blocs('wall_cracked.png'), cell),
        'hammer': _load(blocs('hammer_on.png'), cell),
        'rope': _load(blocs('rope_on.png'), cell),
        'box': _load(blocs('box.png'), cell),
    }
