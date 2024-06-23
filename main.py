import pygame
import random
from classe.Hostage import Hostage
from classe.demineur import Demineur
from classe.detecteur import DetectorAgent
from grid import Grid
from utils.settings import *

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre de jeu
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mission de sauvetage")

# Initialisation de la police pour les textes
font = pygame.font.SysFont(None, 25)

# Initialisation de l'horloge pour contrôler la vitesse de rafraîchissement
clock = pygame.time.Clock()

# Création de la grille de jeu avec une taille définie et un nombre de mines
grid = Grid(GRID_SIZE, MINES_COUNT)

# Initialisation des démineurs avec un rayon de vision de 5
vision_radius = 5

# Création d'une liste d'otages à des positions spécifiques sur la grille
hostages = [Hostage(0, 0, grid), Hostage(int(GRID_SIZE / 2), 0, grid)]

# Création d'une liste de démineurs placés aléatoirement sur la grille
# Chaque démineur a une position aléatoire, un rayon de vision, et connait les otages à sauver
demineurs = [Demineur(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1), grid, vision_radius, 30, hostages) for _ in range(3)]

# Création d'une liste d'agents détecteurs placés aléatoirement sur la grille
# Chaque détecteur connait les démineurs et les otagees
detector_agents = [DetectorAgent(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1), grid, demineurs + hostages) for _ in range(3)]

# Affectation des démineurs à la grille
grid.setDemineurs(demineurs)

# Variable pour contrôler la boucle principale du jeu
running = True

# Fonction pour vérifier si tous les otages ont atteint la destination finzle
def check_all_hostages_final():
    return all(hostage.isFinal() for hostage in hostages)

# Affichage  le nombre d'otages sauvés et restants
def showInfo() :    
    nb_sauv = sum(1 for hostage in hostages if hostage.isFinal())
    nb_restant = len(hostages) - nb_sauv

    # Création du texte à afficher
    info = f"Otages sauvés : {nb_sauv}  |  Otages restants : {nb_restant}"
    rendu = font.render(info, True, LIGHT_GRAY)
    text_rect = rendu.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    SCREEN.blit(rendu, text_rect)

# Boucle principale du jeu
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplissage de l'écran avec une couleur grise
    SCREEN.fill(GRAY) 

    # Dessin de la grille sur l'écran
    grid.draw(SCREEN, font)

    # Mise à jour et envoi de messages par les agents détecteurs
    for detector_agent in detector_agents:
        detector_agent.update()
        detector_agent.sendMessage()

    # Mise à jour de l'état de chaque démineur
    for demineur in demineurs:
        demineur.update()

    # Dessin des agents détecteurs sur l'écran
    for detector_agent in detector_agents:
        detector_agent.draw(SCREEN)

    # Mise à jour de l'état de chaque otage
    for hostage in hostages:
        hostage.update()

    # Dessin des otages sur l'écran
    for hostage in hostages:
        hostage.draw(SCREEN)

    # Dessin des démineurs sur l'écran
    for demineur in demineurs:
        demineur.draw(SCREEN)

    showInfo() # pour afficher le nombre de otages sauvés

    # Vérification si tous les otages ont atteint leur destination
    if check_all_hostages_final():
        # Affichage de la popup de fin
        SCREEN.fill(GRAY)
        end_text = font.render("Tous les otages sont en sécurité !", True, BLACK)
        SCREEN.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # Mise à jour de l'affichage
    pygame.display.flip()

    # Limitation du nombre d'images par seconde à 30
    clock.tick(30)

# Fermeture de Pygame
pygame.quit()
