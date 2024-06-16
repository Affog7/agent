import pygame
import random
from settings import *

class Grid:
    def __init__(self, size, mines_count):
        self.size = size
        self.mines_count = mines_count
        self.grid = self.create_grid()
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.verified = [[False for _ in range(size)] for _ in range(size)]
        self.flags = [[False for _ in range(size)] for _ in range(size)]
        self.load_images()
        

    def create_grid(self):
        grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        mines = set()
        while len(mines) < self.mines_count:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if (x, y) not in mines:
                mines.add((x, y))
                grid[y][x] = -1

        for y in range(self.size):
            for x in range(self.size):
                if grid[y][x] == -1:
                    continue
                count = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size and grid[ny][nx] == -1:
                            count += 1
                grid[y][x] = count
        return grid

    def draw(self, screen, font):
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.revealed[y][x]:
                    if self.grid[y][x] == -2:  
                        #pygame.draw.ellipse(screen, RED, rect)
                        screen.blit(self.demi_image, rect)

                    else:
                        pygame.draw.rect(screen, WHITE, rect)
                        if self.grid[y][x] > 0:
                            text = font.render(str(self.grid[y][x]), True, WHITE)
                            screen.blit(text, (x * CELL_SIZE + 5, y * CELL_SIZE + 5))
                
                elif self.grid[y][x] == -2:
                    pygame.draw.ellipse(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect)
                    if self.flags[y][x]:
                        pygame.draw.rect(screen, BLUE, rect, 2)
                    elif self.verified[y][x]:
                        pygame.draw.rect(screen, GREEN, rect, 1)
                    if self.grid[y][x] == -1:  
                        #pygame.draw.ellipse(screen, BLACK, rect)
                        screen.blit(self.r_image, rect)
                        #screen.blit(pygame.image.load("R.png"), rect)
                pygame.draw.rect(screen, GRAY, rect, 1)

    def reveal_cell(self, x, y):
        if self.revealed[y][x] or self.flags[y][x]:
            return
        self.revealed[y][x] = True
        self.verified[y][x] = True
        if self.grid[y][x] == 0:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        self.reveal_cell(nx, ny)



    def load_images(self):
            self.demi_image = pygame.image.load("demi.png")
            self.demi_image = pygame.transform.scale(self.demi_image, (CELL_SIZE, CELL_SIZE))
            self.r_image = pygame.image.load("R.png")
            self.r_image = pygame.transform.scale(self.r_image, (CELL_SIZE, CELL_SIZE))
