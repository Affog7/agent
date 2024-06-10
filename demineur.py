import pygame
import random
from settings import *

class Demineur:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.move_count = 0

    def move(self):
        if self.move_count % 5 == 0:  # Move every 5 frames
            dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                self.x = new_x
                self.y = new_y
        self.move_count += 1

    def reveal_mine(self):
        if self.grid.grid[self.y][self.x] == -1:
            self.grid.revealed[self.y][self.x] = True
            self.grid.flags[self.y][self.x] = True            
        else:
            self.grid.verified[self.y][self.x] = True

    def update(self):
        self.move()
        self.reveal_mine()

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

    def notify(self):
        return self.x