import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import gym
from gym import spaces


# has_exam
# start
# end
# time
# weather
# num_people_at_bus_stop
# waiting_time
# crowdedness
# overall_satisfaction

# Load data
data = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False))

# Preprocess categorical columns using OneHotEncoder
encoder = OneHotEncoder(sparse=False)
start_end_weather = encoder.fit_transform(data[['start', 'end', 'weather']])

# Normalize numerical columns
scaler = MinMaxScaler()
numerical_features = data[['num_people_at_bus_stop', 'waiting_time', 'crowdedness', 'overall_satisfaction']].values
normalized_numerical = scaler.fit_transform(numerical_features)

# Combine the processed data
processed_data = np.hstack([start_end_weather, normalized_numerical])

# Add a column for has_exam (1 for 'Yes', 0 for 'No')
data['has_exam'] = data['has_exam'].map({'Yes': 1, 'No': 0}).values
processed_data = np.hstack([processed_data, data[['has_exam']].values])

# Check the processed data
print(processed_data.shape)


class BusAllocationEnv(gym.Env):
    def __init__(self, features):
        super(BusAllocationEnv, self).__init__()
        self.features = features
        self.num_bus_stops = len(features)
        
        # Action space: number of buses to deploy (e.g., 0 to 5 buses)
        self.action_space = spaces.Discrete(6)  # Actions: [0, 1, 2, 3, 4, 5]
        
        # State space: the features we processed earlier
        self.observation_space = spaces.Box(low=0, high=1, shape=(features.shape[1],), dtype=np.float32)
        
        # Initialize the environment state
        self.current_step = 0
    
    def reset(self):
        # Reset the environment to the initial state (first row of features)
        self.current_step = 0
        return self.features[self.current_step]
    
    def step(self, action):
        # Get the current state
        state = self.features[self.current_step]
        
        # Extract relevant values
        waiting_time = state[6]
        crowdedness = state[7]
        satisfaction = state[8]
        
        # Simple reward function
        reward = 0
        if waiting_time < 5 and crowdedness < 5:
            reward += 10  # Good service (low waiting time and crowdedness)
        if satisfaction > 7:
            reward += 5   # High satisfaction
        
        # Update step counter
        self.current_step += 1
        done = self.current_step >= self.num_bus_stops
        
        # Return the next state and whether the episode is done
        next_state = self.features[self.current_step] if not done else None
        return next_state, reward, done, {}

# Initialize the environment with the processed data
env = BusAllocationEnv(processed_data)



# Wrap the environment to support vectorized environments (required by Stable-Baselines3)
env = DummyVecEnv([lambda: env])

# Initialize the PPO model
model = PPO("MlpPolicy", env, verbose=1)

# Train the model for a certain number of timesteps
model.learn(total_timesteps=10000)

# Save the trained model
model.save("bus_allocation_model")

# To load the model later
# model = PPO.load("bus_allocation_model")


# Run the model on the environment
state = env.reset()
done = False
total_reward = 0

while not done:
    action, _states = model.predict(state)
    next_state, reward, done, _ = env.step(action)
    total_reward += reward
    state = next_state

print("Total reward:", total_reward)
