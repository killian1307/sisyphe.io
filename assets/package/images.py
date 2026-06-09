# -*- coding: utf-8 -*-
"""Loads and holds every Tk image used by the game (was game_images.py).

Images are loaded from their source PNGs and (re)built at the current scale via
:meth:`GameImages.rescale`, so fullscreen can upscale them crisply
(nearest-neighbour when enlarging, Lanczos when shrinking) without blur. The
attribute names are stable, so callers don't change when the scale does.
"""
import os

from PIL import Image, ImageTk

BASE_CELL = 50  # logical cell size (windowed)


class GameImages:
    def __init__(self, base_path=''):
        self.base_path = base_path
        self.rescale(1.0)

    def rescale(self, scale):
        """Rebuild every texture at ``scale`` (1.0 = windowed 50px cells)."""
        b = self.base_path
        cell = max(1, round(BASE_CELL * scale))
        menu_w, menu_h = round(800 * scale), round(600 * scale)
        logo_w, logo_h = round(300 * scale), round(64 * scale)

        def blocs(name):
            return os.path.join(b, 'assets', 'img', 'blocs', name)

        def menus(name):
            return os.path.join(b, 'assets', 'img', 'menus', name)

        self.sisyphe_images = self._load_character('sisyphe', ['bas', 'haut', 'gauche', 'droite'], 3, cell)

        self.ground_texture = self._load(blocs('ground.png'), cell, cell)
        self.wall_texture = self._load(blocs('wall.png'), cell, cell)
        self.crate_texture = self._load(blocs('crate.png'), cell, cell)
        self.button_texture = self._load(blocs('button.png'), cell, cell)
        self.blue_portal_texture = self._load(blocs('blue_portal.png'), cell, cell)
        self.red_portal_texture = self._load(blocs('red_portal.png'), cell, cell)

        self.main_menu_texture = self._load(menus('bg.png'), menu_w, menu_h)
        self.world_menu_texture = self._load(menus('bg_world.png'), menu_w, menu_h)
        self.settings_menu_texture = self._load(menus('bg_settings.png'), menu_w, menu_h)
        self.logo_texture = self._load(menus('sisyphe.png'), logo_w, logo_h)

        self.Trapdoor_texture = self._load(blocs('trapdoor.png'), cell, cell)
        self.Door_closed_texture = self._load(blocs('door_closed.png'), cell, cell)
        self.Door_open_texture = self._load(blocs('door_open.png'), cell, cell)
        self.crate_hole_texture = self._load(blocs('crate_hole.png'), cell, cell)
        self.wall_cracked_texture = self._load(blocs('wall_cracked.png'), cell, cell)
        self.box_texture = self._load(blocs('box.png'), cell, cell)

        self.hammer_off_texture = self._load(blocs('hammer_off.png'), cell, cell)
        self.hammer_on_texture = self._load(blocs('hammer_on.png'), cell, cell)
        self.hammer_on_1_texture = self._load(blocs('hammer_on_1.png'), cell, cell)
        self.hammer_on_2_texture = self._load(blocs('hammer_on_2.png'), cell, cell)
        self.hammer_on_3_texture = self._load(blocs('hammer_on_3.png'), cell, cell)

        self.rope_on_1_texture = self._load(blocs('rope_on_1.png'), cell, cell)
        self.rope_on_2_texture = self._load(blocs('rope_on_2.png'), cell, cell)
        self.rope_on_3_texture = self._load(blocs('rope_on_3.png'), cell, cell)
        self.rope_off_texture = self._load(blocs('rope_off.png'), cell, cell)
        self.rope_on_texture = self._load(blocs('rope_on.png'), cell, cell)

        self.lightbulb_texture = self._load(blocs('lightbulb.png'), cell, cell)
        self.info_texture = self._load(blocs('info.png'), cell, cell)

    def _load(self, path, w, h):
        image = Image.open(path)
        # Crisp upscaling for the pixel art; smooth shrink for the few big sources.
        resample = Image.NEAREST if (w >= image.width and h >= image.height) else Image.LANCZOS
        image = image.resize((w, h), resample)
        return ImageTk.PhotoImage(image)

    def _load_character(self, character_name, directions, count, cell):
        textures = {}
        for direction in directions:
            textures[direction] = []
            for i in range(1, count + 1):
                path = os.path.join(self.base_path, 'assets', 'img', 'char', f'{character_name}_{direction}_{i}.png')
                textures[direction].append(self._load(path, cell, cell))
        return textures
