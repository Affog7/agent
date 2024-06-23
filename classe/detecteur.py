import random 
from classe.agent import Agent  
from utils.settings import CELL_SIZE, ORANGE, POSITION_A_DEMINEE, POSITION_MINEE 

class DetectorAgent(Agent):
    def __init__(self, x, y, grid, agents):
        super().__init__(x, y, grid, ORANGE, 2)
        self.radius = self.move_interval  # Rayon de détection
        self.agents = agents  # Liste des autres agents
        self.communication_system = []  # Système de communication pour stocker les messages

    def detect_mines(self):
        detected_positions = []  # Liste pour stocker les positions détectées

        # Vérifier d'abord les positions non encore révélées dans le rayon de détection
        for dx in range(-self.radius, self.radius + 1):
            for dy in range(-self.radius, self.radius + 1):
                if 0 <= self.x + dx < self.grid.size and 0 <= self.y + dy < self.grid.size:
                    if not self.grid.verified[self.y + dy][self.x + dx] or not self.grid.revealed[self.y + dy][self.x + dx]:
                        # Vérifier si la position contient une mine
                        if self.grid.grid[self.y + dy][self.x + dx] == POSITION_MINEE:
                            detected_positions.append((self.x + dx, self.y + dy, False))
                            self.grid.grid[self.y + dy][self.x + dx] = POSITION_A_DEMINEE  # Marquer la position
                        else:
                            self.grid.verified[self.y + dy][self.x + dx] = True  # Marquer comme vérifiée

        return detected_positions


    def distance(self, agent):
        return abs(self.x - agent.x) + abs(self.y - agent.y)  # Calcul de la distance de Manhattan à un autre agent

    def sendMessage(self):
        mine_positions = self.detect_mines()  # prendre les mines detectées
        if not mine_positions:
            return  # Si aucune mine détectée, sortir de la fonction
        for agent in self.agents:
            agent.receiveMessage(mine_positions)  # Envoi des positions détectées aux autres agents

    def move(self):
            if self.move_count % self.move_interval == 0:
                # Obtenir les positions adjacentes non vérifiées
                unchecked_positions = self.get_unchecked_positions()

                if unchecked_positions:
                    # Choisir une position non vérifiée de manière aléatoire
                    new_x, new_y = random.choice(unchecked_positions)
                else:
                    # Si toutes les positions adjacentes sont vérifiées, se déplacer de manière aléatoire
                    dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
                    new_x = self.x + dx
                    new_y = self.y + dy

                # Mettre à jour la position de l'agent
                if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size:
                    self.x = new_x
                    self.y = new_y

            self.move_count += 1  # Incrémentation du compteur de mouvements

    # trouver des positions non verifiees
    def get_unchecked_positions(self):
        unchecked_positions = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Directions adjacentes
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size:
                if not self.grid.verified[new_y][new_x]:  # Vérifier si la position n'est pas vérifiée
                    unchecked_positions.append((new_x, new_y))
        return unchecked_positions

    def update(self):
        self.move()  
        self.sendMessage()  # Envoie un message aux autres agents

    def draw(self, screen):
        super().draw(screen)  # Dessine l'agent sur l'écran
    
    def drop_pos_of_mine(self, pos):
        self.communication_system.pop(self.communication_system.index(pos))  # Retire une position de la liste du système de communication des postion
