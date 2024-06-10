import pygame
import random

# Initialiser Pygame
pygame.init()

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 255, 0)

# Définir les dimensions de la grille
GRID_SIZE = 30
CELL_SIZE = 20
MINES_COUNT = 8

# Définir la taille de l'écran
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Démineur")

# Créer la grille avec des mines aléatoires
def create_grid():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = set()
    while len(mines) < MINES_COUNT:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            grid[y][x] = -1

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == -1:
                continue
            count = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[ny][nx] == -1:
                        count += 1
            grid[y][x] = count
    return grid

grid = create_grid()
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Classe Agent (otage)
class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = []

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x = new_x
            self.y = new_y
            self.path.append((self.x, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

# Classe Demineur
class Demineur:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x = new_x
            self.y = new_y

    def reveal_mine(self):
        if grid[self.y][self.x] == -1:
            revealed[self.y][self.x] = True

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

# Fonction pour dessiner la grille
def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if revealed[y][x]:
                if grid[y][x] == -1:
                    pygame.draw.rect(SCREEN, RED, rect)
                else:
                    pygame.draw.rect(SCREEN, WHITE, rect)
                    if grid[y][x] > 0:
                        text = font.render(str(grid[y][x]), True, BLACK)
                        SCREEN.blit(text, (x * CELL_SIZE + 5, y * CELL_SIZE + 5))
            else:
                pygame.draw.rect(SCREEN, GRAY, rect)
                if flags[y][x]:
                    pygame.draw.rect(SCREEN, BLACK, rect, 2)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)

# Fonction pour révéler les cellules
def reveal_cell(x, y):
    if revealed[y][x] or flags[y][x]:
        return
    revealed[y][x] = True
    if grid[y][x] == 0:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    reveal_cell(nx, ny)

# Pygame setup pour le cercle
clock = pygame.time.Clock()
running = True
dt = 0

# Position initiale des agents
agents = [Agent(0, 0)]
demineurs = [Demineur(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)) for _ in range(3)]

# Boucle principale du jeu
font = pygame.font.SysFont(None, 30)

while running:
    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran
    SCREEN.fill(PURPLE)

    # Dessiner la grille
    draw_grid()

    # Déplacer les démineurs et révéler les mines
    for demineur in demineurs:
        demineur.move()
        demineur.reveal_mine()

    # Déplacer les agents
    for agent in agents:
        if agent.x < GRID_SIZE - 1:
            agent.move(1, 0)
        elif agent.y < GRID_SIZE - 1:
            agent.move(0, 1)

    # Dessiner les agents et les démineurs
    for agent in agents:
        agent.draw(SCREEN)
    for demineur in demineurs:
        demineur.draw(SCREEN)

    # Afficher à l'écran
    pygame.display.flip()

    # Limiter à 60 FPS
    dt = clock.tick(60) / 1000

pygame.quit()
