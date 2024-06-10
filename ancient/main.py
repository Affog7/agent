from env import Environment
from agent import RandomAgent
if __name__ == "__main__":
    env = Environment(10, 10)
    agent1 = RandomAgent(1, 1, 'A')
    agent2 = RandomAgent(8, 8, 'B')
    
    env.add_agent(agent1)
    env.add_agent(agent2)
    
    for _ in range(10):
        env.step()
        print(env)
        print()
