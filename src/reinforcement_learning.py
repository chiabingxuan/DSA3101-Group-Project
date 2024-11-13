import gym
from gym import spaces
import numpy as np

class ShuttleBusEnv(gym.Env):
    def __init__(self):
        super(ShuttleBusEnv, self).__init__()

        # Define action and observation space
        self.action_space = spaces.Discrete(3)  # Example actions: 0 - do nothing, 1 - add bus, 2 - reroute bus
        self.observation_space = spaces.Box(
            low=0, high=100, shape=(8,), dtype=np.float32)  # State: waiting time, crowdedness, etc.

        # Initialize state
        self.state = self._get_initial_state()
        self.done = False

    def _get_initial_state(self):
        # Start with an initial state vector (e.g., waiting time, satisfaction, crowdedness, etc.)
        # This will depend on your dataset's features
        initial_state = np.random.rand(8) * 100  # Example: Random initialization
        return initial_state

    def step(self, action):
        # Apply action and update the state
        reward = self._calculate_reward(action)
        self.state = self._next_state(action)

        # Define a condition for episode termination
        self.done = bool(self.state[0] < 5)  # For example, end if waiting time is very low

        return self.state, reward, self.done, {}

    def _calculate_reward(self, action):
        # Reward calculation (penalize waiting time, incentivize satisfaction)
        waiting_time = self.state[0]
        crowdedness = self.state[1]
        overall_satisfaction = self.state[6]

        # Reward function based on action impact
        reward = -waiting_time * 0.1 + crowdedness * -0.05 + overall_satisfaction * 0.2
        if action == 1:  # Adding bus
            reward += 1
        elif action == 2:  # Rerouting bus
            reward += 0.5

        return reward

    def _next_state(self, action):
        # Transition to next state
        new_state = self.state + np.random.rand(8) - 0.5  # Random next state for demo
        return new_state

    def reset(self):
        self.state = self._get_initial_state()
        self.done = False
        return self.state
