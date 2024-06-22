import random 
from agent import Agent  
from settings import CELL_SIZE, ORANGE, POSITION_A_DEMINEE, POSITION_MINEE  # Importation des paramètres nécessaires

class DetectorAgent(Agent):
    def __init__(self, x, y, grid, agents):
        super().__init__(x, y, grid, ORANGE, 3)  # Initialisation de la classe parente avec des paramètres spécifiques
        self.radius = 2  # Rayon de détection
        self.agents = agents  # Liste des autres agents
        self.communication_system = []  # Système de communication pour stocker les messages

    def detect_mines(self):
        detected_positions = []  # Liste pour stocker les positions détectées
        if self.grid.grid[self.y][self.x] == POSITION_MINEE and not self.grid.revealed[self.y][self.x]:
            detected_positions.append((self.x, self.y, False))  # Ajout de la position de la mine détectée
            print(f"position de {self.x} et {self.y} detectee")
            self.grid.grid[self.y][self.x] = POSITION_A_DEMINEE  # Mise à jour de la grille pour marquer la position détectée
        else:
            self.grid.verified[self.y][self.x] = True  # Marquage de la position comme vérifiée
        return detected_positions

    def distance(self, agent):
        return abs(self.x - agent.x) + abs(self.y - agent.y)  # Calcul de la distance de Manhattan à un autre agent

    def sendMessage(self):
        mine_positions = self.detect_mines()  # Détecte les mines
        if not mine_positions:
            return  # Si aucune mine détectée, sortir de la fonction
        for agent in self.agents:
            agent.receiveMessage(mine_positions)  # Envoi des positions détectées aux autres agents

    def move(self):
        if self.move_count % self.move_interval == 0:
            dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])  # Choix aléatoire d'une direction
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < self.grid.size and 0 <= new_y < self.grid.size:
                self.x = new_x  # Mise à jour de la position x
                self.y = new_y  # Mise à jour de la position y
        self.move_count += 1  # Incrémentation du compteur de mouvements

    def update(self):
        self.move()  # Déplace l'agent
        self.sendMessage()  # Envoie un message aux autres agents

    def draw(self, screen):
        super().draw(screen)  # Dessine l'agent sur l'écran
    
    def drop_pos_of_mine(self, pos):
        self.communication_system.pop(self.communication_system.index(pos))  # Retire une position de la liste du système de communication
