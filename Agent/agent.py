class Agent:
    def __init__(self, position):
        self.position = position

    def move(self, new_position):
        self.position = new_position

    def get_position(self):
        return self.position
