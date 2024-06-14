import pygame
import random
from detecteur import DetectorAgent
from settings import *
from grid import Grid
from agent import Hostage
from demineur import Demineur

# Boucle principale du jeu
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue Mission")
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

grid = Grid(GRID_SIZE, MINES_COUNT)
hostages = [Hostage(0, 0, grid)]
detector_agent = DetectorAgent(1, 1, grid)
demineurs = [Demineur(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), grid, detector_agent) for _ in range(3)]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill(GRAY)
    grid.draw(SCREEN, font)

    detector_agent.communicate_mine_positions()

    detector_agent.update()
    for demineur in demineurs:
        demineur.update()

    detector_agent.draw(SCREEN)  # Dessiner le détecteur sur l'écran

    for hostage in hostages:
        hostage.draw(SCREEN)
    for demineur in demineurs:
        demineur.draw(SCREEN)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
