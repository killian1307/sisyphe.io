# -*- coding: utf-8 -*-
"""Loads the editor's block textures (collapses the repeated Image.open blocks)."""
import os

from PIL import Image, ImageTk


def _load(path):
    image = Image.open(path)
    image = image.resize((50, 50), Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def load(base_path):
    """Return a name -> PhotoImage dict for every editor texture."""
    def blocs(name):
        return os.path.join(base_path, 'img', 'blocs', name)

    return {
        'sisyphe': _load(os.path.join(base_path, 'img', 'char', 'sisyphe_bas_1.png')),
        'ground': _load(blocs('ground.png')),
        'wall': _load(blocs('wall.png')),
        'crate': _load(blocs('crate.png')),
        'button': _load(blocs('button.png')),
        'bportal': _load(blocs('blue_portal.png')),
        'rportal': _load(blocs('red_portal.png')),
        'door': _load(blocs('door_closed.png')),
        'trapdoor': _load(blocs('trapdoor.png')),
        'fwall': _load(blocs('wall_cracked.png')),
        'hammer': _load(blocs('hammer_on.png')),
        'rope': _load(blocs('rope_on.png')),
        'box': _load(blocs('box.png')),
    }
