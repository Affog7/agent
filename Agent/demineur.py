import pygame
from agent import Agent
from settings import CELL_SIZE, GREEN, GRID_SIZE


class Demineur:
    def __init__(self, x, y, grid, detector_agent):
        self.x = x
        self.y = y
        self.grid = grid
        self.detector_agent = detector_agent
        self.move_count = 0
        self.color = GREEN  # Couleur pour représenter le démineur

    def move(self):
        if self.move_count % 5 == 0:  # Se déplacer toutes les 5 images
            communicated_mines = self.detector_agent.get_communicated_mines()
            if communicated_mines:
                mine_x, mine_y = communicated_mines[0]  # On suppose la première mine communiquée
                dx = 1 if mine_x > self.x else -1 if mine_x < self.x else 0
                dy = 1 if mine_y > self.y else -1 if mine_y < self.y else 0
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    self.x = new_x
                    self.y = new_y
        self.move_count += 1

    def update(self):
        self.move()
        self.reveal_mine()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)