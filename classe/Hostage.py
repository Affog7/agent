import heapq
import pygame
import time
from classe.agent import Agent
from utils.settings import BLUE, GRID_SIZE, CELL_SIZE
from utils.utils import dernieres_coordonnees

class Hostage(Agent):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid, BLUE, 10)
        self.path = []
        self.target_pos = dernieres_coordonnees()  # Liste des positions cibles
        self.positions_safe = []
        self.mine_positions = []
        self.current_target_index = 0  # Index pour suivre la position cible actuelle
        self.last_move_time = time.time()  # Heure du dernier mouvement
        self.move_delay = 0.5  # Délai en secondes entre les mouvements
        self.grid.revealed[y][x] = True
        self.grid.verified[y][x] = True

        
    def heuristic(self, a, b):
        # Fonction heuristique pour A*
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_search(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append((current[0], current[1], False))
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                    if self.grid.verified[neighbor[1]][neighbor[0]] and (neighbor[0], neighbor[1], False) not in self.mine_positions:
                        tentative_g_score = g_score[current] + 1
                        if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                            came_from[neighbor] = current
                            g_score[neighbor] = tentative_g_score
                            f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def is_path_safe(self, path):
        # Vérifie si une position dans le chemin est une mine
        return any(position in self.mine_positions for position in path)

    def move(self):
        if self.current_target_index >= len(self.target_pos):
            return

        start = (self.x, self.y)
        goal = self.target_pos[self.current_target_index]
        current_time = time.time()
        
        if current_time - self.last_move_time >= self.move_delay:
            if not self.path:
                self.path = self.a_star_search(start, goal)

            if self.path:
                next_position = self.path.pop(0)
                if next_position not in self.mine_positions:
                    self.x, self.y, _ = next_position

                    # Si on atteint la position cible actuelle, passer à la suivante
                    if (self.x, self.y) == self.target_pos[self.current_target_index]:
                        self.current_target_index += 1
                        self.path = []  # Efface le chemin pour recalculer un nouveau chemin vers la prochaine cible

            # Recalculer le chemin si le chemin actuel n'est pas sûr
            if self.path and not self.is_path_safe(self.path):
                self.path = self.a_star_search(start, goal)

            self.last_move_time = current_time  # Met à jour l'heure du dernier mouvement

    def update(self):
        if not self.isFinal():
            self.move()

    def draw(self, screen):
        super().draw(screen)
        for pos in self.path:
            pygame.draw.circle(screen, BLUE, (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

    def inbox_mine_positions(self, mine_positions):
        print(f"moi otage je suis notifie du mine : {mine_positions}")
        self.mine_positions.extend(mine_positions)
        self.path = []  # Efface le chemin actuel pour recalculer

    def receiveMessage(self, position, type=None):
        if type == "SAFE":
            print(f"moi otage je suis notifie du mine désarmoçer: {position}")
            if (position[0], position[1], False) in self.mine_positions:
                self.mine_positions.remove((position[0], position[1], False))
            self.positions_safe.append(position)
            self.path = []  # Efface le chemin actuel pour recalculer
        else:
            self.inbox_mine_positions(position)

    def isFinal(self):
       
        return   (self.x, self.y) == self.target_pos[-1]
       
