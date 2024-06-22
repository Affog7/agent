import pygame
import random
from detecteur import DetectorAgent
from settings import *
from grid import Grid
from Hostage import Hostage
from demineur import Demineur

# Boucle principale du jeu
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue Mission")
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

grid = Grid(GRID_SIZE, MINES_COUNT)

# Liste partagée pour suivre les positions des mines assignées
assigned_mines = []

# Initialisation des démineurs avec une vision radius de 5 par exemple
vision_radius = 5

hostages = [Hostage(0, 0, grid),Hostage(0, 1, grid)]


demineurs = [Demineur(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), grid, vision_radius, 30, hostages) for _ in range(3)]

detector_agents = [DetectorAgent(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), grid, demineurs+hostages) for _ in range(3)]

grid.setDemineurs(demineurs)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill(GRAY)
    grid.draw(SCREEN, font)

    for detector_agent in detector_agents:
        detector_agent.update()
        detector_agent.sendMessage() 

    for demineur in demineurs:
        demineur.update()
            
    for detector_agent in detector_agents:
        detector_agent.draw(SCREEN)
   
    for hostage in hostages:
        hostage.move()

    for hostage in hostages:
        hostage.draw(SCREEN)
    
    for demineur in demineurs:
        demineur.draw(SCREEN)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
