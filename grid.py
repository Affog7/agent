import pygame   
import random   
from utils.settings import *   
from utils.utils import dernieres_coordonnees  

class Grid:
    def __init__(self, size, mines_count):
        """
        Initialise la grille avec une taille et un nombre de mines spécifiés.

        :size: Taille de la grille (nombre de cellules par côté)
        :mines_count: Nombre de mines dans la grille
        """
        self.size = size
        self.mines_count = mines_count
        self.grid = self.create_grid()  # Création de la grille
        self.revealed = [[False for _ in range(size)] for _ in range(size)]  # Statut de révélation des cellules
        self.verified = [[False for _ in range(size)] for _ in range(size)]  # Statut de vérification des cellules
        self.flags = [[False for _ in range(size)] for _ in range(size)]  # Statut de drapeau des cellules
        self.load_images()  # Chargement des images nécessaires
        self.demineurs = None  # Initialisation de la liste ds démineurs à None
        self.mark_safe_positions()  # Marquer les positions initiales des agents otages comme sûres

    def setDemineurs(self, demineurs): # setters pour prendre les autres demineurs
        self.demineurs = demineurs

    def create_grid(self):
        """
        Crée la grille en plaçant les mines et en calculant le nombre de mines voisines pour chaque cellule.

        :return: La grille créée
        """
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]  # Initialisation de la grille
        mines = set()  # Ensemble pour stocker les positions des mines
        safe_positions = dernieres_coordonnees()  # Positions sûres ==>(à ne pas minier)

        while len(mines) < self.mines_count:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if (x, y) not in mines and (x, y) not in safe_positions:
                mines.add((x, y))
                grid[y][x] = -1  # Zone minée

        for y in range(self.size):
            for x in range(self.size):
                if grid[y][x] == -1:
                    continue
                count = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size and grid[ny][nx] == -1:
                            count += 1
                grid[y][x] = count  # Nombre de mines voisines
        return grid

    def draw(self, screen, font):
        """
        Dessine la grille à l'écran.
        """
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.revealed[y][x]:
                    if self.grid[y][x] == POSITION_DEMINEE:  # Position déminée
                        screen.blit(self.demi_image, rect)
                    else:
                        pygame.draw.rect(screen, WHITE, rect)
                        if self.grid[y][x] > 0:
                            text = font.render(str(self.grid[y][x]), True, WHITE)
                            screen.blit(text, (x * CELL_SIZE + 5, y * CELL_SIZE + 5))
                elif   (x, y) in dernieres_coordonnees():
                    pygame.draw.rect(screen, BLACK, rect)
                elif self.grid[y][x] == POSITION_A_DEMINEE:  # Position marquée pour être déminée
                    pygame.draw.ellipse(screen, RED, rect)
                else:
                    if self.grid[y][x] == POSITION_MINEE:  # Position d'une mine
                        screen.blit(self.r_image, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)  # Bordure de la cellule

    def reveal_cell(self, x, y):
        """
        Révèle une cellule et, si elle est vide, révèle également ses voisines.

        :x: Coordonnée x de la cellule
        :y: Coordonnée y de la cellule
        """
        if self.revealed[y][x] or self.flags[y][x]:
            return
        self.revealed[y][x] = True
        self.verified[y][x] = True
        if self.grid[y][x] == 0:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        self.reveal_cell(nx, ny)

    def load_images(self):
        """
        Charge les images nécessaires pour le jeu et les redimensionne.
        """
        self.demi_image = pygame.image.load("image/demi.png")
        self.demi_image = pygame.transform.scale(self.demi_image, (CELL_SIZE, CELL_SIZE))
        self.r_image = pygame.image.load("image/R.png")
        self.r_image = pygame.transform.scale(self.r_image, (CELL_SIZE, CELL_SIZE))

    # del
    def mark_safe_positions(self):
        """
        Marque les positions initiales des agents otages comme sûres (révélées et vérifiées).
        """        
        for (x, y) in dernieres_coordonnees():
            self.revealed[y][x] = True
            self.verified[y][x] = True
