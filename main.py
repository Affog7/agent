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

detector_agents = [DetectorAgent(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), grid) for _ in range(3)]

# Liste partagée pour suivre les positions des mines assignées
assigned_mines = []

# Initialisation des démineurs avec une vision radius de 5 par exemple
vision_radius = 5
demineurs = [Demineur(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), grid, detector_agents, assigned_mines, vision_radius) for _ in range(3)]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill(GRAY)
    grid.draw(SCREEN, font)

    for detector_agent in detector_agents:
        detector_agent.communicate_mine_positions()

    for detector_agent in detector_agents:
        detector_agent.update()

    for demineur in demineurs:
        demineur.update()
            
    for detector_agent in detector_agents:
        detector_agent.draw(SCREEN)
    for hostage in hostages:
        hostage.draw(SCREEN)
    for demineur in demineurs:
        demineur.draw(SCREEN)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
