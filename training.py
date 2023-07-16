import random
from engine import MathemagixGame
from agent import MathemagixAgent

# Usage example
grid_size = 3  # Change this to match your grid size
env = MathemagixGame(grid_size, agent_player=1)  # Create an instance of the MathemagixGame
agent = MathemagixAgent(grid_size)  # Create an instance of the MathemagixAgent

num_episodes = 1000
max_steps = 100

for episode in range(num_episodes):
    state = env.reset()
    done = False
    total_reward = 0

    for step in range(max_steps):
        action = agent.select_action(state)
        next_state, reward, done = env.step(action)
        total_reward += reward

        agent.update_model(state, action, reward, next_state, done)

        if done:
            break

        state = next_state

    print("Episode:", episode + 1, "Total Reward:", total_reward)

print("Training completed.")
