from agent import Agent


class Otage(Agent):
    def __init__(self, position, vision_range, goal_position):
        super().__init__(position)
        self.vision_range = vision_range
        self.goal_position = goal_position
        self.mines_info = []
        self.chemin_actuel = []

    def update_path(self, nouvelles_mines_info):
        self.mines_info = nouvelles_mines_info
        self.planifier_chemin()

    def planifier_chemin(self):
        # Implémenter un algorithme de pathfinding (par exemple A* ou Dijkstra) pour trouver un chemin sûr
        pass

    def deplacer(self):
        if self.chemin_actuel:
            self.position = self.chemin_actuel.pop(0)

    def update(self, terrain):
        self.deplacer()

    def get_color(self):
        return (96,44,88)  # Exemple de couleur pour le démineur