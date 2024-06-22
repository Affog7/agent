import pygame
import random
from agent import Agent
from settings import *

class Demineur(Agent):
    def __init__(self, x, y, grid, vision_radius=5, move_interval=30, agents_otages=None):
        super().__init__(x, y, grid, GREEN, move_interval)  # Initialisation de la classe parente Agent avec des paramètres spécifiques
        self.isBusy = False  # Indique si le démineur est occupé
        self.target = None  # Cible actuelle du démineur
        self.current_agent = None  # Agent actuel attribué
        self.assigned_mines = []  # Liste des mines assignées
        self.agents_otages = agents_otages  # Liste des agents otages
        self.vision_radius = vision_radius  # Rayon de vision du démineur
        self.move_delay = 0  # Délai de mouvement
        self.mine_positions = []  # Liste des positions des mines

    def receiveMessage(self, mine_positions):
        print(f"moi demineur je suis notifie de : {mine_positions}")
        self.mine_positions.extend(mine_positions)  # Ajoute les positions des mines reçues à la liste

    def find_mines_in_vision(self):
        mines_in_vision = []  # Liste des mines dans le champ de vision
        for position in self.mine_positions:
            if not position[2] and (position[0], position[1]) not in self.assigned_mines:  # Si la mine n'est pas désamorcée et n'est pas déjà assignée
                dist = ((position[0] - self.x) ** 2 + (position[1] - self.y) ** 2) ** 0.5  # Calcul de la distance entre le démineur et la mine
                if dist <= self.vision_radius:  # Si la mine est dans le champ de vision
                    mines_in_vision.append((position, None, dist))  # Ajoute la mine à la liste des mines dans le champ de vision
        return mines_in_vision

    def find_closest_mine(self):
        mines_in_vision = self.find_mines_in_vision()  # Trouve les mines dans le champ de vision
        if mines_in_vision:
            mines_in_vision.sort(key=lambda x: (self.grid.verified[x[0][1]][x[0][0]], x[2]))  # Trie les mines par vérification et distance
            closest_mine = mines_in_vision[0]  # Trouve la mine la plus proche
            self.assigned_mines.append((closest_mine[0][0], closest_mine[0][1]))  # Assigne cette mine au démineur
            return closest_mine[0], closest_mine[1]
        return None

    def find_random_verified_position(self):
        verified_positions = []  # Liste des positions vérifiées
        for dy in range(-self.vision_radius, self.vision_radius + 1):
            for dx in range(-self.vision_radius, self.vision_radius + 1):
                new_x = self.x + dx
                new_y = self.y + dy
                if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size:  # Vérifie si la nouvelle position est dans les limites de la grille
                    dist = (dx ** 2 + dy ** 2) ** 0.5  # Calcul de la distance entre le démineur et la nouvelle position
                    if dist <= self.vision_radius and (self.grid.verified[new_y][new_x] or self.grid.verified[new_y][new_x] == POSITION_A_DEMINEE):
                        verified_positions.append((new_x, new_y))  # Ajoute la position vérifiée à la liste
        if verified_positions:
            return random.choice(verified_positions)  # Retourne une position vérifiée aléatoire
        return None

    def move(self):
        if self.move_delay > 0:  # Si le délai de mouvement est supérieur à zéro
            self.move_delay -= 1
            return

        if self.target:
            target_x, target_y = self.target[0], self.target[1]  # Utilise la cible actuelle
        else:
            random_position = self.find_random_verified_position()  # Trouve une position vérifiée aléatoire
            if random_position:
                target_x, target_y = random_position
            else:
                return

        dx = 1 if target_x > self.x else -1 if target_x < self.x else 0  # Détermine la direction du mouvement en x
        dy = 1 if target_y > self.y else -1 if target_y < self.y else 0  # Détermine la direction du mouvement en y
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size:  # Vérifie si la nouvelle position est dans les limites de la grille
            if self.grid.verified[new_y][new_x] and not self.is_position_in_radius_of_other_agents(new_x, new_y):  # Si la position est vérifiée et qu'elle n'est pas dans le rayon d'un autre agent
                self.x = new_x
                self.y = new_y
                if self.target and self.x == target_x and self.y == target_y:  # Si le démineur atteint sa cible
                    self.reveal_mine()  # Révèle la mine
                    self.isBusy = False
                    self.target = None
                    self.assigned_mines.remove((target_x, target_y))  # Enlève la mine de la liste des mines assignées
            else:
                closest_mineur, closest_distance = self.find_closest_mineur_to_target(target_x, target_y)  # Trouve le démineur le plus proche de la cible
                if closest_mineur == self:
                    self.x = new_x
                    self.y = new_y
                    if self.target and self.x == target_x and self.y == target_y:  # Si le démineur atteint sa cible
                        self.reveal_mine()  # Révèle la mine
                        self.isBusy = False
                        self.target = None
                        self.assigned_mines.remove((target_x, target_y))  # Enlève la mine de la liste des mines assignées
                else:
                    self.change_position()  # Change de position

        self.move_delay = self.move_interval  # Réinitialise le délai de mouvement

    def is_position_in_radius_of_other_agents(self, x, y):
        for agent in self.grid.demineurs:
            if agent != self:
                dist = ((agent.x - x) ** 2 + (agent.y - y) ** 2) ** 0.5  # Calcul de la distance entre le démineur et l'autre agent
                if dist <= agent.vision_radius:  # Si l'autre agent est dans le rayon de vision
                    return True
        return False

    def find_closest_mineur_to_target(self, target_x, target_y):
        closest_mineur = None
        closest_distance = float('inf')
        for agent in self.grid.demineurs:
            if agent != self:
                dist = ((agent.x - target_x) ** 2 + (agent.y - target_y) ** 2) ** 0.5  # Calcul de la distance entre l'agent et la cible
                if dist < closest_distance:  # Si la distance est inférieure à la distance actuelle la plus proche
                    closest_mineur = agent
                    closest_distance = dist
        return closest_mineur, closest_distance

    def change_position(self):
        new_position = self.find_random_verified_position()  # Trouve une position vérifiée aléatoire
        if new_position:
            self.x, self.y = new_position  # Change la position du démineur

    def notifyOthers(self, pos):
        for agent in self.grid.demineurs:
            agent.update_inbox_me(pos)  # Notifie les autres démineurs de la position de la mine

    def update_inbox_me(self, pos):
        try:
            self.mine_positions.remove(pos)  # Enlève la position de la mine de la liste
        except Exception:
            print("pos not found")

    def reveal_mine(self):
        if self.grid.grid[self.y][self.x] == POSITION_A_DEMINEE:  # Si la position actuelle est une position à déminer
            self.grid.revealed[self.y][self.x] = True
            self.grid.verified[self.y][self.x] = True
            self.grid.flags[self.y][self.x] = True
            self.grid.grid[self.y][self.x] = POSITION_DEMINEE  # Marque la position comme démine
            self.notifyOthers((self.x, self.y, False))
            self.sendMessage()
        elif self.grid.grid[self.y][self.x] == POSITION_MINEE:  # Si la position actuelle est une mine
            print("morrrt")
        else:
            self.grid.verified[self.y][self.x] = True

    def update(self):
        if not self.isBusy:  # Si le démineur n'est pas occupé
            find = self.find_closest_mine()  # Cherche la mine la plus proche
            if find:
                self.target, self.current_agent = find
                self.isBusy = True
        self.move()  # Effectue un mouvement

    def draw(self, screen):
        super().draw(screen)  # Dessine le démineur sur l'écran
        pygame.draw.circle(screen, (0, 255, 0, 100), (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), self.vision_radius * CELL_SIZE, 1)  # Dessine le rayon de vision

    def sendMessage(self):
        for agent in self.agents_otages:
            agent.receiveMessage((self.x, self.y), type="SAFE")  # Envoie un message aux agents otages pour indiquer que la position est sûre
