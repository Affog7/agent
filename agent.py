import pygame
from settings import *

class Hostage:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.path = []

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            if self.grid.revealed[new_y][new_x] and self.grid.verified[new_y][new_x]:
                self.x = new_x
                self.y = new_y
                self.path.append((self.x, self.y))

    def update(self):
        if self.x < GRID_SIZE - 1 and self.grid.revealed[self.y][self.x + 1] and self.grid.verified[self.y][self.x + 1]:
            self.move(1, 0)
        elif self.y < GRID_SIZE - 1 and self.grid.revealed[self.y + 1][self.x] and self.grid.verified[self.y + 1][self.x]:
            self.move(0, 1)

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

    def isFinal(self):
        if self.x == GRID_SIZE-1 and self.y == GRID_SIZE-1:
            return True
        else :
            return False