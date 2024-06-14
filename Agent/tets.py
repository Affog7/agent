import pygame
import random
from detecteur import Detecteur 
from grid import Grid
from otage import Otage
from demineur import Demineur
from settings import GRID_SIZE, MINES_COUNT

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)  # Blanc
FPS = 60
VISION_RANGE = 5  # Example vision range in grid cells
RANGE_DETECTION = 3 
# Chargement des images (à adapter selon vos fichiers)
background_image = pygame.image.load('demi.png')

# Fonction principale
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simulation de déminage")

    clock = pygame.time.Clock()

    # Initialisation de la grille de déminage
    grid = Grid(GRID_SIZE, MINES_COUNT)

    # Initialisation des agents
    demineur = Demineur((10, 10), RANGE_DETECTION)
    detecteur = Detecteur((20, 20), RANGE_DETECTION)
    otage = Otage((5, 5), VISION_RANGE, (GRID_SIZE - 1, GRID_SIZE - 1))

    agents = [demineur, detecteur, otage]

    running = True
    # Boucle principale
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Logique de jeu
        terrain = grid.grid

        # Mise à jour des agents
        for agent in agents:
            if isinstance(agent, Detecteur):
                agent.update(terrain, demineurs=[demineur])
                print(4)
            elif isinstance(agent, Demineur):
                agent.update(terrain, otages=[otage])
                print(5)
            elif isinstance(agent, Otage):
                agent.update(terrain)
                print(6)

        # Dessin
        screen.fill(BACKGROUND_COLOR)
        # screen.blit(background_image, (0, 0))  # Affichage de l'image de fond

        grid.draw(screen, pygame.font.Font(None, 30))

        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()

if __name__ == '__main__':
    main()
