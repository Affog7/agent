import pygame
import random
from settings import *

class Agent:
    def __init__(self, x, y, grid, color, move_interval):
        self.x = x
        self.y = y
        self.grid = grid
        self.color = color
        self.move_count = 0
        self.move_interval = move_interval

    def move(self):
        raise NotImplementedError("La méthode move doit être implémentée par les sous-classes")

    def update(self):
        raise NotImplementedError("La méthode update doit être implémentée par les sous-classes")

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
