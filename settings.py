# Couleurs
WHITE = (255, 255, 255)  # Blanc
BLACK = (0, 0, 0)  # Noir
GRAY = (200, 200, 200)  # Gris
RED = (255, 0, 0)  # Rouge
PURPLE = (128, 0, 128)  # Violet
GREEN = (0, 255, 0)  # Vert
BLUE = (0, 0, 255)  # Bleu
ORANGE = (100, 150, 155)  # Orange (teinte spécifique)

# Les dimensions de la grille
GRID_SIZE = 30  # Taille de la grille (nombre de cellules par côté)
CELL_SIZE = 20  # Taille d'une cellule en pixels
MINES_COUNT = 50  # Nombre de mines dans la grille

START_PLACE = (0, 1, 2)  # Positions de départ possibles (indices de cellules)

# États possibles d'une cellule de la grille concernant les mines
POSITION_MINEE = -1  # La cellule contient une mine
POSITION_A_DEMINEE = -2  # La cellule est marquée pour être déminée
POSITION_DEMINEE = 3  # La cellule est déjà déminée

# Taille de l'écran
WIDTH = GRID_SIZE * CELL_SIZE  # Largeur de l'écran en pixels
HEIGHT = GRID_SIZE * CELL_SIZE  # Hauteur de l'écran en pixels
