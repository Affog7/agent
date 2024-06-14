import pygame
from settings import *

class Hostage:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.path = []

    def move(self):

        old_x = self.x
        old_y = self.y
        
        if(self.x+1 > GRID_SIZE-1 or self.y+1 > GRID_SIZE-1  ) :
            return 
        
        if self.grid.revealed[self.x+1][self.y] or self.grid.verified[self.x+1][self.y]:
            print(1)            
            self.x +=1

        if self.grid.revealed[self.x][self.y+1] or self.grid.verified[self.x][self.y+1]:
            print(2)            
            self.y +=1

        if 0 <= self.x < GRID_SIZE and 0 <= self.y < GRID_SIZE:
            self.path.append((self.x, self.y))
        else :
            self.x = old_x
            self.y = old_x

        


    def update(self):
        if self.x < GRID_SIZE - 1 and self.grid.revealed[self.y][self.x + 1] and self.grid.verified[self.y][self.x + 1]:
            self.move(1, 0)
        elif self.y < GRID_SIZE - 1 and self.grid.revealed[self.y + 1][self.x] and self.grid.verified[self.y + 1][self.x]:
            self.move(0, 1)

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

    def isFinal(self):
        if self.x == GRID_SIZE-1 and self.y == GRID_SIZE-1:
            return True
        else :
            return False