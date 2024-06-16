from agent import Agent


class Detecteur(Agent):
    def __init__(self, position, range_detection):
        super().__init__(position)
        self.range_detection = range_detection
        self.mines_detectees = []

    def detecter_mines(self, terrain):
        x, y = self.position
        for i in range(x - self.range_detection, x + self.range_detection + 1):
            for j in range(y - self.range_detection, y + self.range_detection + 1):
                if 0 <= i < len(terrain) and 0 <= j < len(terrain[0]) and terrain[i][j] == 1:
                    self.mines_detectees.append((i, j))

    def notifier_demineurs(self, demineurs):
        for demineur in demineurs:
            demineur.recevoir_info_mines(self.mines_detectees)

    def update(self, terrain, demineurs=None, otages=None):
        self.detecter_mines(terrain)
        if demineurs:
            self.notifier_demineurs(demineurs)
    def get_color(self):
        return (100,75,0)  # Exemple de couleur pour le démineur

