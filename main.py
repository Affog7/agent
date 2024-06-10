import pygame
import random
from settings import *
from grid import Grid
from agent import Hostage
from demineur import Demineur

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue Mission")
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

grid = Grid(GRID_SIZE, MINES_COUNT)
hostages = [Hostage(0, 0, grid)]
demineurs = [Demineur(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1), grid) for _ in range(3)]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill(PURPLE)
    grid.draw(SCREEN, font)

    for demineur in demineurs:
        demineur.update()
        for hostage in hostages:
            hostage.move(5,5)

    for hostage in hostages:
        hostage.update()

    for hostage in hostages:
        hostage.draw(SCREEN)
    for demineur in demineurs:
        demineur.draw(SCREEN)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
