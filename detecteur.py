import random
import pygame
from settings import CELL_SIZE, ORANGE


class DetectorAgent:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.radius = 2  # Rayon de détection
        self.communication_system = []  # Liste pour stocker les positions des mines détectées
        self.color = ORANGE  # Couleur pour représenter le détecteur
        self.move_count = 0
        self.move_interval = 3  # Déplacer le détecteur tous les 3 frames

    def detect_mines(self):
        detected_positions = []
        for y in range(self.grid.size):
            for x in range(self.grid.size):
                if self.grid.grid[y][x] == -1 and not self.grid.revealed[y][x]:
                    detected_positions.append((x, y))
        return detected_positions

    def communicate_mine_positions(self):
        mine_positions = self.detect_mines()
        self.communication_system.extend(mine_positions)

    def get_communicated_mines(self):
        return self.communication_system

    def move(self):
        if self.move_count % self.move_interval == 0:  # Déplacer le détecteur à chaque `move_interval` frames
            dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size:
                self.x = new_x
                self.y = new_y
        self.move_count += 1

    def update(self):
        self.move()
        self.communicate_mine_positions()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
