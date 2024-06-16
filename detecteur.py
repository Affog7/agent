import random
import pygame
from agent import Agent
from settings import CELL_SIZE, ORANGE

class DetectorAgent(Agent):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid, ORANGE, 3)
        self.radius = 2
        self.communication_system = []

    def detect_mines(self):
        detected_positions = []
        if self.grid.grid[self.y][self.x] == -1 and not self.grid.revealed[self.y][self.x]:
            detected_positions.append((self.x, self.y, False))
            print(f"position de {self.x}  et {self.y} detectee")
            self.grid.grid[self.y][self.x] = -2
        self.grid.verified[self.y][self.x] = True
        return detected_positions

    def communicate_mine_positions(self):
        mine_positions = self.detect_mines()
        self.communication_system.extend(mine_positions)

    def get_communicated_mines(self):
        return self.communication_system

    def move(self):
        if self.move_count % self.move_interval == 0:
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
        super().draw(screen)
    
    def drop_pos_of_mine(self, pos):
        self.communication_system.pop(self.communication_system.index(pos))
