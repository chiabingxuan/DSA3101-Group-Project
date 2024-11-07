##Simulation Of System Efficiency and User Satisfaction
import pandas as pd
import numpy as np
import warnings
import simpy
import random
from sklearn.linear_model import LinearRegression
warnings.filterwarnings("ignore")
##Data
train = pd.read_csv('train_trip_data_after_sdv.csv')

## Cleaning
# Group by 'bus_num' and 'time' and calculate the mean of 'crowdedness' and 'num_of_waiting_people'
average_df = t.groupby(['bus_num', 'hour', 'start'])[['crowdedness', 'num_people_at_bus_stop']].mean().reset_index()
# Rename columns if desired
average_df.columns = ['bus_num', 'hour', 'start', 'average_crowdedness', 'average_num_of_waiting_people']

## Creating the each bus route and distance
# Define bus stops and distances
A1_bus_stops = ["KR BI", "LT13 / Ventus", "BIZ2 / Opp HSSML", "PGP", "Kent Ridge MRT / Opp Kent Ridge MRT", "LT27 / S17", "UHC / Opp UHC", "IT / CLB", "KR BI"]
A1_distances = [0.5, 0.7, 0.7, 0.9, 0.5, 0.7, 0.5, 0.6]  # Distances between consecutive stops
A2_bus_stops = ["KR BI", "IT / CLB", "UHC / Opp UHC", "LT27 / S17", "Kent Ridge MRT / Opp Kent Ridge MRT", "PGP", "BIZ2 / Opp HSSML", "LT13 / Ventus", "KR BI"]
A2_distances = [0.6, 0.5, 0.7, 0.5, 0.9, 0.7, 0.7, 0.5]  # Distances between consecutive stops
D1_bus_stops = ["COM3", "BIZ2 / Opp HSSML", "LT13 / Ventus", "IT / CLB", "UTown", "IT / CLB", "LT13 / Ventus", "BIZ2 / Opp HSSML", "COM3_2"]
D1_distances = [0.3, 0.7, 0.4, 0.9, 1.0, 0.4, 0.7, 0.3]  # Distances between consecutive stops
D2_bus_stops = ["COM3", "PGP", "Kent Ridge MRT / Opp Kent Ridge MRT", "LT27 / S17", "UHC / Opp UHC", "UTown", "UHC / Opp UHC", "LT27 / S17", "Kent Ridge MRT / Opp Kent Ridge MRT", "PGP", "COM3_2"]
D2_distances = [0.8, 0.9, 0.5, 0.7, 0.7, 0.8, 0.7, 0.5, 0.9, 0.8]  # Distances between consecutive stops

# Initialize dictionary
A1_bus_stop_distances = {}
A2_bus_stop_distances = {}
D1_bus_stop_distances = {}
D2_bus_stop_distances = {}

# Populate the dictionaries

for i, stop in enumerate(A1_bus_stops):
    A1_bus_stop_distances[stop] = {}
    for j in range(i+1, len(A1_bus_stops)):
        # Accumulate distance for each subsequent stop
        A1_bus_stop_distances[stop][A1_bus_stops[j]] = round(sum(A1_distances[i:j]), 2)
for i, stop in enumerate(A2_bus_stops):
    A2_bus_stop_distances[stop] = {}
    for j in range(i+1, len(A2_bus_stops)):
        # Accumulate distance for each subsequent stop
        A2_bus_stop_distances[stop][A2_bus_stops[j]] = round(sum(A2_distances[i:j]), 2)
for i, stop in enumerate(D1_bus_stops):
    D1_bus_stop_distances[stop] = {}
    for j in range(i+1, len(D1_bus_stops)):
        # Accumulate distance for each subsequent stop
        D1_bus_stop_distances[stop][D1_bus_stops[j]] = round(sum(D1_distances[i:j]), 2)
for i, stop in enumerate(D2_bus_stops):
    D2_bus_stop_distances[stop] = {}
    for j in range(i+1, len(D2_bus_stops)):
        # Accumulate distance for each subsequent stop
        D2_bus_stop_distances[stop][D2_bus_stops[j]] = round(sum(D2_distances[i:j]), 2)
        
# Example crowd level and satisfaction data for training
crowd_data = train[['crowdedness', 'overall_satisfaction']]

# Train a linear regression model for satisfaction prediction
def train_satisfaction_model(data):
    model = LinearRegression()
    model.fit(data[['crowdedness']], data['overall_satisfaction'])
    return model

satisfaction_model = train_satisfaction_model(crowd_data)

# Function to predict satisfaction using the model
def predict_satisfaction(crowd_level):
    return satisfaction_model.predict([[crowd_level]])[0]

class Bus:
    def __init__(self, env, name, stops, distances, crowd_df):
        self.env = env
        self.name = name
        self.stops = stops
        self.distances = distances
        self.capacity = MAX_BUS_CAPACITY
        self.passengers = []  # List to hold current passengers
        self.crowd_df = crowd_df  # DataFrame showing crowd levels at stops and times
        self.satisfaction_levels = []

    def run_hourly_schedule(self, start_hour, end_hour):
        # Loop through each hour from start_hour to end_hour
        for hour in range(start_hour, end_hour + 1):
            print(f"\n--- Hour {hour}:00 ---")
            yield self.env.process(self.run_for_hour(hour))
            yield self.env.timeout(60)  # Move to the next hour (60 minutes)

        mean_satisfaction = np.mean(self.satisfaction_levels) if self.satisfaction_levels else 0
        print(f"\nMean Satisfaction Level for {self.name}: {mean_satisfaction:.2f}")

    def run_for_hour(self, hour):
        for i, stop in enumerate(self.stops):
            travel_time = self.get_travel_time(i)
            yield self.env.timeout(travel_time)  # Travel to the next stop
            print(f"{self.name} arrived at {stop}")
            self.board_passengers(stop, hour)

            # Wait before starting next trip based on bus frequency
            yield self.env.timeout(get_bus_frequency(hour))

    def get_travel_time(self, stop_index):
        if stop_index < len(self.distances):
            distance = self.distances[stop_index]
            speed = random.uniform(*BUS_SPEED_RANGE)
            return round(distance / speed, 2)
        return 0

    def board_passengers(self, stop, hour):
        # Retrieve crowd level for current stop and time
        hour = int(self.env.now // 60) % 24  # Get the current hour
        crowd_level = self.get_crowd_level(stop, hour)
        
        # Predict satisfaction using crowd level
        satisfaction = predict_satisfaction(crowd_level)

        self.satisfaction_levels.append(satisfaction)
        
        # Log satisfaction or assign it to passengers
        print(f"{self.name} boarding passengers at {stop} with crowd level {crowd_level} -> Predicted Satisfaction: {satisfaction:.2f}")

    def get_crowd_level(self, stop, hour):
        # Retrieve crowd level from DataFrame for the given stop and hour
        crowd_level = self.crowd_df[(self.crowd_df['start'] == stop) & (self.crowd_df['hour'] == hour)]['average_crowdedness']
        if not crowd_level.empty:
            return crowd_level.values[0]
        return 0  # Default if no data for the stop and hour

# Example DataFrame showing crowd levels at stops and times
crowd_df = average_df

# Example environment setup and bus creation
env = simpy.Environment()
bus = Bus(env, 'A1', A1_bus_stops, A1_distances, crowd_df)
env.process(bus.run_hourly_schedule(start_hour=7, end_hour=23))
env.run()  # Run for a short duration for testing     