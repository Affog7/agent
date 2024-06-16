import pygame
import random
from agent import Agent
from settings import *

class Demineur(Agent):
    def __init__(self, x, y, grid, detector_agents, assigned_mines, vision_radius=5, move_interval=30):
        super().__init__(x, y, grid, GREEN, move_interval)
        self.detector_agents = detector_agents
        self.isBusy = False
        self.target = None
        self.current_agent = None
        self.assigned_mines = assigned_mines
        self.vision_radius = vision_radius
        self.move_delay = 0

    def find_mines_in_vision(self):
        mines_in_vision = []
        for agent in self.detector_agents:
            communicated_mines = agent.get_communicated_mines()
            for position in communicated_mines:
                if not position[2] and (position[0], position[1]) not in self.assigned_mines:
                    dist = ((position[0] - self.x) ** 2 + (position[1] - self.y) ** 2) ** 0.5
                    if dist <= self.vision_radius:
                        mines_in_vision.append((position, agent, dist))
        return mines_in_vision

    def find_closest_mine(self):
        mines_in_vision = self.find_mines_in_vision()
        if mines_in_vision:
            mines_in_vision.sort(key=lambda x: (self.grid.verified[x[0][1]][x[0][0]], x[2]))
            closest_mine = mines_in_vision[0]
            self.assigned_mines.append((closest_mine[0][0], closest_mine[0][1]))
            return closest_mine[0], closest_mine[1]
        return None

    def find_random_verified_position(self):
        verified_positions = []
        for dy in range(-self.vision_radius, self.vision_radius + 1):
            for dx in range(-self.vision_radius, self.vision_radius + 1):
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size:
                    dist = (dx ** 2 + dy ** 2) ** 0.5
                    if dist <= self.vision_radius and self.grid.verified[new_y][new_x]:
                        verified_positions.append((new_x, new_y))
        if verified_positions:
            return random.choice(verified_positions)
        return None

    def move(self):
        if self.move_delay > 0:
            self.move_delay -= 1
            return
        
        if self.target:
            target_x, target_y = self.target[0], self.target[1]
        else:
            random_position = self.find_random_verified_position()
            if random_position:
                target_x, target_y = random_position
            else:
                return

        dx = 1 if target_x > self.x else -1 if target_x < self.x else 0
        dy = 1 if target_y > self.y else -1 if target_y < self.y else 0
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size:
            self.x = new_x
            self.y = new_y
            if self.target and self.x == target_x and self.y == target_y:
                self.reveal_mine()
                self.current_agent.drop_pos_of_mine(self.target)
                self.isBusy = False
                self.target = None
                self.assigned_mines.remove((target_x, target_y))
        self.move_delay = self.move_interval

    def reveal_mine(self):
        if self.grid.grid[self.y][self.x] == -2:
            self.grid.revealed[self.y][self.x] = True
            self.grid.flags[self.y][self.x] = True
        else:
            self.grid.verified[self.y][self.x] = True

    def update(self):
        if not self.isBusy:
            find = self.find_closest_mine()
            if find:
                self.target, self.current_agent = find
                self.isBusy = True
        self.move()
        
    def draw(self, screen):
        super().draw(screen)
        pygame.draw.circle(screen, (0, 255, 0, 100), (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), self.vision_radius * CELL_SIZE, 1)

    def notify(self):
        return self.x
