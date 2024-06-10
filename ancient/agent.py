import random

class Agent:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.env = None

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if self.env.is_within_bounds(new_x, new_y) and not self.env.is_occupied(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def step(self):
        raise NotImplementedError("This method should be overridden by subclasses")

class RandomAgent(Agent):
    def step(self):
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        self.move(dx, dy)


class GoalAgent(Agent):
    def step(self):
        if self in self.env.targets:
            target_x, target_y = self.env.targets[self]
            dx = target_x - self.x
            dy = target_y - self.y
            if abs(dx) > abs(dy):
                self.move(int(dx / abs(dx)), 0)
            else:
                self.move(0, int(dy / abs(dy)))

class AvoidingAgent(Agent):
    def step(self):
        # Basic logic to avoid other agents
        possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(possible_moves)
        for dx, dy in possible_moves:
            new_x = self.x + dx
            new_y = self.y + dy
            if self.env.is_within_bounds(new_x, new_y) and not self.env.is_occupied(new_x, new_y):
                self.move(dx, dy)
                break