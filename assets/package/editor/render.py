# -*- coding: utf-8 -*-
"""Draws the editor grid after each click (real textures or placeholder shapes).

Coordinates go through :mod:`view` so the grid scales in fullscreen; clicks are
mapped back in :func:`placement.get_selected_cell`. Windowed = identity.
"""
from . import context as ectx
from . import placement
from .. import view


def affiche_plateau_canvas():
    """Redraw the whole editor canvas."""
    Canevas = ectx.canvas
    plateau = ectx.plateau
    textures = ectx.show_textures
    tex = ectx.tex
    X, Y, S = view.X, view.Y, view.S
    Canevas.delete('all')
    for i in range(12):
        Canevas.create_line(X(0), Y(50 * i), X(800), Y(50 * i), width=0.5)
    for j in range(16):
        Canevas.create_line(X(50 * j), Y(0), X(50 * j), Y(600), width=0.5)
    placement.initialize_walls()
    for row in range(12):
        for col in range(16):
            cx, cy = X(50 * col + 25), Y(50 * row + 25)
            x0, y0 = X(50 * col), Y(50 * row)
            x1, y1 = X(50 * col + 50), Y(50 * row + 50)
            # Sol
            if plateau[row][col][0] == 0 and textures == True:
                Canevas.create_image(cx, cy, image=tex['ground'], anchor='center')
            # Mur
            if plateau[row][col][0] == 1:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['wall'], anchor='center')
                else:
                    Canevas.create_rectangle(x0, y0, x1, y1, fill='blue')
            # Joueur
            elif plateau[row][col][1] == 1:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['sisyphe'], anchor='center')
                else:
                    Canevas.create_oval(x0, y0, x1, y1, fill='yellow')
            # Rocher
            elif plateau[row][col][2] == 1:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['crate'], anchor='center')
                else:
                    Canevas.create_oval(x0, y0, x1, y1, fill='#804000')
            # Trou
            elif plateau[row][col][3] == 1:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['button'], anchor='center')
                else:
                    couleur = 'black'         # CHANGEZ MOI pour modifier la couleur du trou dans l'editeur de lvl
                    epaisseur = max(1, round(S(3)))  # CHANGEZ MOI pour l'eapissseur des fleches
                    # rond central
                    Canevas.create_oval(cx - S(13), cy - S(13), cx + S(13), cy + S(13), fill=couleur)

                    # fleche haut droite
                    Canevas.create_line(cx + S(24), cy - S(24), cx + S(12), cy - S(12), fill=couleur, width=epaisseur)
                    Canevas.create_line(cx + S(12), cy - S(12), cx + S(19), cy - S(12), fill=couleur, width=epaisseur)
                    Canevas.create_line(cx + S(12), cy - S(12), cx + S(12), cy - S(19), fill=couleur, width=epaisseur)
                    # Flèche haut gauche
                    Canevas.create_line(cx - S(24), cy - S(24), cx - S(12), cy - S(12), fill=couleur, width=epaisseur)
                    Canevas.create_line(cx - S(12), cy - S(12), cx - S(19), cy - S(12), fill=couleur, width=epaisseur)
                    Canevas.create_line(cx - S(12), cy - S(12), cx - S(12), cy - S(19), fill=couleur, width=epaisseur)

                    # Fleche bas droite
                    Canevas.create_line(cx + S(24), cy + S(24), cx + S(12), cy + S(12), fill=couleur, width=epaisseur)
                    Canevas.create_line(cx + S(12), cy + S(12), cx + S(19), cy + S(12), fill=couleur, width=epaisseur)
                    Canevas.create_line(cx + S(12), cy + S(12), cx + S(12), cy + S(19), fill=couleur, width=epaisseur)

                    # Fleche bas gauche
                    Canevas.create_line(cx - S(24), cy + S(24), cx - S(12), cy + S(12), fill=couleur, width=epaisseur)
                    Canevas.create_line(cx - S(12), cy + S(12), cx - S(19), cy + S(12), fill=couleur, width=epaisseur)
                    Canevas.create_line(cx - S(12), cy + S(12), cx - S(12), cy + S(19), fill=couleur, width=epaisseur)
            # Portail Bleu
            elif plateau[row][col][1] == 2:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['bportal'], anchor='center')
                else:
                    Canevas.create_oval(x0 + S(5), y0, x1 - S(5), y1, fill='cyan')
            # Portail Rouge
            elif plateau[row][col][2] == 2:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['rportal'], anchor='center')
                else:
                    Canevas.create_oval(x0 + S(5), y0, x1 - S(5), y1, fill='#ff3333')
            # Porte
            elif plateau[row][col][1] == 3:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['door'], anchor='center')
                else:
                    Canevas.create_rectangle(x0, y0, x1, y1, fill='lime')
            # Plaque de pression
            elif plateau[row][col][2] == 3:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['trapdoor'], anchor='center')
                else:
                    Canevas.create_oval(x0, y0, x1, y1, fill='lime')
            # Mur Fragile
            elif plateau[row][col][1] == 4:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['fwall'], anchor='center')
                else:
                    Canevas.create_rectangle(x0, y0, x1, y1, fill='magenta')
            # Marteau
            elif plateau[row][col][2] == 4:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['hammer'], anchor='center')
                else:
                    y = cy + S(18)   # logical 50*row+43
                    x = cx
                    handle_length = S(30)
                    handle_thickness = max(1, round(S(2)))
                    head_width = S(20)
                    head_height = S(10)
                    couleur = '#804000'

                    # Base du marteau
                    Canevas.create_line(x, y, x, y - handle_length, fill=couleur, width=handle_thickness)

                    # Tête du marteau
                    head_start_x = x - head_width / 2
                    head_start_y = y - handle_length - head_height / 2
                    head_end_x = head_start_x + head_width
                    head_end_y = head_start_y + head_height
                    Canevas.create_rectangle(head_start_x, head_start_y, head_end_x, head_end_y, fill=couleur)
                    Canevas.create_rectangle(head_start_x, head_start_y, head_end_x, head_end_y, fill=couleur)
            # Corde
            elif plateau[row][col][1] == 5:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['rope'], anchor='center')
                else:
                    Canevas.create_line(cx - S(20), cy - S(20), cx + S(20), cy + S(20), fill='#804000', width=max(1, round(S(5))))
            # Caisse
            elif plateau[row][col][2] == 5:
                if textures == True:
                    Canevas.create_image(cx, cy, image=tex['box'], anchor='center')
                else:
                    Canevas.create_rectangle(x0, y0, x1, y1, fill='#804000')
                    Canevas.create_line(cx - S(25), cy - S(25), cx + S(25), cy + S(25), fill='black', width=max(1, round(S(3))))
                    Canevas.create_line(cx + S(25), cy - S(25), cx - S(25), cy + S(25), fill='black', width=max(1, round(S(3))))
    if ectx.unsaved_changes == True:
        fenetre_title = f"{ectx.lang.editor_title} - {ectx.file_opened}"
        ectx.window.title(fenetre_title + "*")
