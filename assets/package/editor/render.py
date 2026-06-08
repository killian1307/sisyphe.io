# -*- coding: utf-8 -*-
"""Draws the editor grid after each click (real textures or placeholder shapes)."""
from . import context as ectx
from . import placement


def affiche_plateau_canvas():
    """Redraw the whole editor canvas."""
    Canevas = ectx.canvas
    plateau = ectx.plateau
    textures = ectx.show_textures
    tex = ectx.tex
    Canevas.delete('all')
    for i in range(12):
        Canevas.create_line(0, 50 * i, 800, 50 * i, width=0.5)
    for j in range(16):
        Canevas.create_line(50 * j, 0, 50 * j, 600, width=0.5)
    placement.initialize_walls()
    for row in range(12):
        for col in range(16):
            # Sol
            if plateau[row][col][0] == 0 and textures == True:
                Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['ground'], anchor='center')
            # Mur
            if plateau[row][col][0] == 1:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['wall'], anchor='center')
                else:
                    Canevas.create_rectangle(50 * col, 50 * row, 50 * col + 50, 50 * row + 50, fill='blue')
            # Joueur
            elif plateau[row][col][1] == 1:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['sisyphe'], anchor='center')
                else:
                    Canevas.create_oval(50 * col, 50 * row, 50 * col + 50, 50 * row + 50, fill='yellow')
            # Rocher
            elif plateau[row][col][2] == 1:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['crate'], anchor='center')
                else:
                    Canevas.create_oval(50 * col, 50 * row, 50 * col + 50, 50 * row + 50, fill='#804000')
            # Trou
            elif plateau[row][col][3] == 1:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['button'], anchor='center')
                else:
                    y = 50 * row + 25
                    x = 50 * col + 25
                    couleur = 'black'         # CHANGEZ MOI pour modifier la couleur du trou dans l'editeur de lvl
                    epaisseur = 3                 # CHANGEZ MOI pour l'eapissseur des fleches
                    # rond central
                    Canevas.create_oval(x - 13, y - 13, x + 13, y + 13, fill=couleur)

                    # fleche haut droite
                    Canevas.create_line(x + 24, y - 24, x + 12, y - 12, fill=couleur, width=epaisseur)
                    Canevas.create_line(x + 12, y - 12, x + 19, y - 12, fill=couleur, width=epaisseur)
                    Canevas.create_line(x + 12, y - 12, x + 12, y - 19, fill=couleur, width=epaisseur)
                    # Flèche haut gauche
                    Canevas.create_line(x - 24, y - 24, x - 12, y - 12, fill=couleur, width=epaisseur)
                    Canevas.create_line(x - 12, y - 12, x - 19, y - 12, fill=couleur, width=epaisseur)
                    Canevas.create_line(x - 12, y - 12, x - 12, y - 19, fill=couleur, width=epaisseur)

                    # Fleche bas droite
                    Canevas.create_line(x + 24, y + 24, x + 12, y + 12, fill=couleur, width=epaisseur)
                    Canevas.create_line(x + 12, y + 12, x + 19, y + 12, fill=couleur, width=epaisseur)
                    Canevas.create_line(x + 12, y + 12, x + 12, y + 19, fill=couleur, width=epaisseur)

                    # Fleche bas gauche
                    Canevas.create_line(x - 24, y + 24, x - 12, y + 12, fill=couleur, width=epaisseur)
                    Canevas.create_line(x - 12, y + 12, x - 19, y + 12, fill=couleur, width=epaisseur)
                    Canevas.create_line(x - 12, y + 12, x - 12, y + 19, fill=couleur, width=epaisseur)
            # Portail Bleu
            elif plateau[row][col][1] == 2:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['bportal'], anchor='center')
                else:
                    Canevas.create_oval(50 * col + 5, 50 * row, 50 * col + 45, 50 * row + 50, fill='cyan')
            # Portail Rouge
            elif plateau[row][col][2] == 2:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['rportal'], anchor='center')
                else:
                    Canevas.create_oval(50 * col + 5, 50 * row, 50 * col + 45, 50 * row + 50, fill='#ff3333')
            # Porte
            elif plateau[row][col][1] == 3:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['door'], anchor='center')
                else:
                    Canevas.create_rectangle(50 * col, 50 * row, 50 * col + 50, 50 * row + 50, fill='lime')
            # Plaque de pression
            elif plateau[row][col][2] == 3:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['trapdoor'], anchor='center')
                else:
                    Canevas.create_oval(50 * col, 50 * row, 50 * col + 50, 50 * row + 50, fill='lime')
            # Mur Fragile
            elif plateau[row][col][1] == 4:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['fwall'], anchor='center')
                else:
                    Canevas.create_rectangle(50 * col, 50 * row, 50 * col + 50, 50 * row + 50, fill='magenta')
            # Marteau
            elif plateau[row][col][2] == 4:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['hammer'], anchor='center')
                else:
                    y = 50 * row + 43
                    x = 50 * col + 25

                    handle_length = 30
                    handle_thickness = 2
                    head_width = 20
                    head_height = 10
                    couleur = '#804000'

                    # Base du marteau
                    Canevas.create_line(x, y, x, y - handle_length, fill=couleur, width=handle_thickness)

                    # Tête du marteau
                    head_start_x = x - head_width // 2
                    head_start_y = y - handle_length - head_height // 2
                    head_end_x = head_start_x + head_width
                    head_end_y = head_start_y + head_height
                    Canevas.create_rectangle(head_start_x, head_start_y, head_end_x, head_end_y, fill=couleur)
                    Canevas.create_rectangle(head_start_x, head_start_y, head_end_x, head_end_y, fill=couleur)
            # Corde
            elif plateau[row][col][1] == 5:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['rope'], anchor='center')
                else:
                    y = 50 * row + 25
                    x = 50 * col + 25
                    Canevas.create_line(x - 20, y - 20, x + 20, y + 20, fill='#804000', width=5)
            # Caisse
            elif plateau[row][col][2] == 5:
                if textures == True:
                    Canevas.create_image(50 * col + 25, 50 * row + 25, image=tex['box'], anchor='center')
                else:
                    y = 50 * row + 25
                    x = 50 * col + 25
                    Canevas.create_rectangle(50 * col, 50 * row, 50 * col + 50, 50 * row + 50, fill='#804000')
                    Canevas.create_line(x - 25, y - 25, x + 25, y + 25, fill='black', width=3)
                    Canevas.create_line(x + 25, y - 25, x - 25, y + 25, fill='black', width=3)
    if ectx.unsaved_changes == True:
        fenetre_title = f"{ectx.lang.editor_title} - {ectx.file_opened}"
        ectx.window.title(fenetre_title + "*")
