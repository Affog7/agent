class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = []
        self.obstacles = set()

    def add_agent(self, agent):
        self.agents.append(agent)
        agent.env = self

    def add_obstacle(self, x, y):
        if self.is_within_bounds(x, y):
            self.obstacles.add((x, y))

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_occupied(self, x, y):
        if (x, y) in self.obstacles:
            return True
        for agent in self.agents:
            if agent.x == x and agent.y == y:
                return True
        return False

    def step(self):
        for agent in self.agents:
            agent.step()

    def __str__(self):
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        for agent in self.agents:
            grid[agent.y][agent.x] = agent.symbol
        return '\n'.join(' '.join(row) for row in grid)
    

    def update(frame_num, env, scatters):
            env.step()
            agent_positions = [(agent.x, agent.y) for agent in env.agents]
            for scatter, (x, y) in zip(scatters, agent_positions):
                scatter.set_offsets((x, y))
            return scatters
    

    