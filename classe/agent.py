import pygame
from utils.settings import *

class Agent:
    def __init__(self, x, y, grid, color, move_interval=2):
        """
        Initialise un agent avec une position (x, y), une grille de référence,
        une couleur et un intervalle de déplacement.

        :param x: Position x de l'agent sur la grille
        :param y: Position y de l'agent sur la grille
        :param grid: Référence à la grille sur laquelle l'agent se déplace
        :param color: Couleur de l'agent pour l'affichage
        :param move_interval: Intervalle de temps entre les déplacements de l'agent
        """
        self.x = x
        self.y = y
        self.grid = grid
        self.color = color
        self.move_count = 0  # Compteur de déplacements pour gérer l'intervalle de mouvement
        self.move_interval = move_interval  # Intervalle de temps entre les déplacements


    def move(self):
        """
        Méthode à implémenter par les sous-classes pour définir le comportement
        de déplacement de l'agent.
        """
        raise NotImplementedError("La méthode move doit être implémentée par les sous-classes")

    def receiveMessage(self, message=None, type=None):
        """
        Méthode à implémenter par les sous-classes pour définir le comportement
        de réception de message de l'agent.

        :param message: Le message reçu par l'agent
        :param type: Le type de message reçu
        """
        raise NotImplementedError("La méthode receiveMessage doit être implémentée par les sous-classes")

    def sendMessage(self):
        """
        Méthode à implémenter par les sous-classes pour définir le comportement
        d'envoi de message de l'agent.
        """
        raise NotImplementedError("La méthode sendMessage doit être implémentée par les sous-classes")

    def update(self):
        """
        Méthode à implémenter par les sous-classes pour mettre à jour l'état
        de l'agent.
        """
        raise NotImplementedError("La méthode update doit être implémentée par les sous-classes")

    def draw(self, screen):
        """
        Dessine l'agent à l'écran sous forme de cercle.

        :param screen: L'écran sur lequel dessiner l'agent
        """
        pygame.draw.circle(
            screen, 
            self.color, 
            (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), 
            CELL_SIZE // 2
        )
