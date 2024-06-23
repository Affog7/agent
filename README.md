# PROJET : Simulation d'un Terrain de Mines de Guerre avec une Architecture Multi-Agent

## Introduction
Ce projet simule un terrain de mines de guerre où des agents doivent traverser un champ miné en utilisant des algorithmes d'IA pour détecter, désamorcer des mines et trouver des chemins sûrs. L'objectif est de coordonner différents types d'agents pour réussir la mission de sauvetage.


### Contexte
Ce projet simule un terrain de mines de guerre, où des agents otages doivent traverser de manière sécurisée depuis une position initiale jusqu'à la position finale du terrain. Le terrain est parsemé de mines, et les agents détecteurs, démineurs et otages doivent coopérer pour garantir la sécurité des otages.

Les détecteurs, ne disposant pas de connaissances omniscientes, trouvent aléatoirement les positions des mines. Ils transmettent ces informations cruciales aux démineurs et aux otages. Les démineurs, opérant dans un rayon d'activité prédéfini, localisent et désamorcent les mines, puis communiquent les positions des mines désamorcées aux otages.

Les otages utilisent l'algorithme A* pour déterminer un chemin sûr, en considérant les positions des mines découvertes et non désamorcées comme des obstacles à éviter. Lorsqu'une mine est désamorcée, les otages recalculent leur chemin en intégrant les nouvelles informations de terrain. L'objectif global est de permettre aux otages de traverser intelligemment le terrain miné, en prenant en compte les changements dynamiques de l'environnement.

### Objectifs communs :
   - Les otages doivent traverser le terrain en toute sécurité.
   - Les détecteurs doivent localiser toutes les mines.
   - Les démineurs doivent désamorcer les mines dans leur rayon d'activité.

### Les rôles et les responsabilités :
   Dans le projet de simulation du terrain de mines de guerre avec une architecture multi-agent, les différents agents sont classés en trois types principaux : les otages, les détecteurs et les démineurs. Voici une description détaillée de chaque type d'agent, leur rôle et leur type selon les classifications des agents en intelligence artificielle :

#### 1. Otages  

**Type : Agents basés sur un but**

**Rôle :**
- Traverser le terrain de mines en toute sécurité.
- Utiliser l'algorithme A* pour trouver des chemins sûrs vers la destination finale.
- Prendre en compte les positions des mines détectées et désamorcées pour ajuster leur chemin.
- Recevoir des informations des démineurs et des détecteurs pour éviter les zones dangereuses.
    
#### 2. Détecteurs
**Type : Agents observateurs**

**Rôle :**
- Parcourir le terrain pour détecter les positions des mines.
- Transmettre les positions des mines découvertes aux démineurs et aux otages.
- Aider à cartographier le terrain pour faciliter les déplacements des autres agents.
- Jouer un rôle crucial dans l'identification des menaces avant qu'elles ne deviennent un danger pour les otages.

 #### 3. Démineurs
**Type : Agents réflexes et agents basés sur l’utilité**

**Rôle :**
- Désamorcer les mines trouvées par les détecteurs.
- Communiquer les positions des mines désamorcées aux otages pour indiquer que ces zones sont sûres.
- Déplacer stratégiquement sur le terrain pour maximiser leur efficacité dans le désamorçage des mines.
- Coopérer avec d'autres démineurs pour assurer une couverture maximale et minimiser les risques.
    
#### Résumé des rôles et types
- **Otages :** Agents basés sur un but. Leur objectif est de traverser le terrain de mines en utilisant des informations pour éviter les mines et trouver un chemin sûr.
- **Détecteurs :** Agents observateurs. Leur rôle est de détecter les mines et de communiquer ces informations aux autres agents pour assurer leur sécurité.
- **Démineurs :** Agents réflexes et basés sur l’utilité. Leur fonction principale est de désamorcer les mines et de signaler les zones sécurisées aux otages.

 

### Mécanismes de communication :
   - Utilisation des messages pour la communication des positions des mines entre les agents.
   - Mise en place un protocole pour la notification des positions désamorcées.

### Algorithmes de coordination :
   - Utilisation A* pour la recherche de chemin par les otages.
   - Implémentation un algorithme pour la détection et la désactivation des mines par les détecteurs et démineurs.
   - Mise à jour les chemins en fonction des changements de terrain.

## Code fourni
### Classe Hostage
La classe Hostage représente les otages qui doivent traverser le champ miné.

```python
import heapq
import pygame
import time
from agent import Agent
from settings import BLUE, GRID_SIZE, CELL_SIZE
from utils import dernieres_coordonnees

class Hostage(Agent):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid, BLUE, 10)
        self.path = []
        self.target_pos = dernieres_coordonnees()
        self.positions_safe = []
        self.mine_positions = []
        self.current_target_index = 0
        self.last_move_time = time.time()
        self.move_delay = 0.5

    def heuristic(self, a, b):
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
                    if (self.x, self.y) == self.target_pos[self.current_target_index]:
                        self.current_target_index += 1
                        self.path = []
            if self.path and not self.is_path_safe(self.path):
                self.path = self.a_star_search(start, goal)
            self.last_move_time = current_time

    def update(self):
        if not self.isFinal():
            self.move()

    def draw(self, screen):
        super().draw(screen)
        for pos in self.path:
            pygame.draw.circle(screen, BLUE, (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

    def inbox_mine_positions(self, mine_positions):
        print(f"moi otage je suis notifie du mine non_d: {mine_positions}")
        self.mine_positions.extend(mine_positions)
        self.path = []

    def receiveMessage(self, position, type=None):
        if type == "SAFE":
            print(f"moi otage je suis notifie du mine d: {position}")
            if (position[0], position[1], False) in self.mine_positions:
                self.mine_positions.remove((position[0], position[1], False))
            self.positions_safe.append(position)
            self.path = []
        else:
            self.inbox_mine_positions(position)

    def isFinal(self):
        return self.current_target_index >= len(self.target_pos) and (self.x, self.y) == self.target_pos[-1]
```

### Image de simulation
L'image fournie montre la simulation du terrain de mines. Les différents éléments représentés sont :

- Points jaunes : Mines détectées
- Points verts : Démineurs
- Points bleus : Chemin des otages
- Points rouges : Mines non désamorcées
- Points noirs : Mines désamorcées

## Conclusion
Cette simulation utilise une architecture multi-agent pour modéliser et résoudre le problème de traversée d'un champ de mines en coordonnant des agents avec des rôles spécifiques. Les algorithmes d'IA tels que A* sont utilisés pour la recherche de chemins sûrs, et les communications entre agents permettent de mettre à jour les informations critiques sur le terrain de manière dynamique.
