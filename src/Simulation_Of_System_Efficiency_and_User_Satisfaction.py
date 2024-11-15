def main():

    import pandas as pd
    import numpy as np
    import warnings
    import simpy
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import MinMaxScaler
    
    # Suppress warnings for a more user friendly experience
    warnings.filterwarnings("ignore")
    
    ###############################################################################################
    ### Objective of model: Simulate the optimised bus route based on different scenarios       ###
    ###############################################################################################
    
    '''Preparing Data'''
    train = pd.read_csv('train_trip_data_after_sdv.csv')
    
    #Choosing the important columns and reformating the time and other variables into integers
    t = train[['bus_num', 'start', 'end','weather','has_exam', 'num_people_at_bus_stop', 'date', 'time', 'waiting_time','crowdedness', 'comfort', 'safety', 'overall_satisfaction']]
    t['day_of_week'] = pd.to_datetime(t['date']).dt.dayofweek + 1
    t['time'] = pd.to_datetime(t['time']).dt.strftime('%H:%M:%S')
    t['hour'] = pd.to_datetime(t['time']).dt.hour
    t = t.drop(columns = ['time'])
    t['end'] = t['end'].replace('COM3', 'COM3_2')
    t['weather'] = t['weather'].map({'Sunny': 0, 'Rainy': 1})
    t['has_exam'] = t['has_exam'].map({'No': 0, 'Yes': 1})
    
    ### Dictionaries needed for simulation of the optimised route
    
    ## Creating a dictionary to stall the average number of people at each bus stop during each different scenario
    
    # Calculate the mean of 'num_of_people_at_bus_stop'
    average_waiting_passengers = t.groupby(['bus_num', 'day_of_week', 'hour', 'weather', 'has_exam', 'start'])[['num_people_at_bus_stop']].mean().reset_index()
    
    # Rename columns if desired
    average_waiting_passengers.columns = ['bus_num','day_of_week', 'hour', 'weather', 'has_exam', 'start','average_num_of_waiting_people']
    people_at_the_bus_stop = {}
    # Iterate through each row to construct the dictionary
    for _, row in average_waiting_passengers.iterrows():
        # Create the tuple key from the first five columns
        tuple_key = (row["bus_num"], row["day_of_week"], row["hour"], row["weather"], row["has_exam"])
        
        # Initialize the main key if not already present
        if tuple_key not in people_at_the_bus_stop:
            people_at_the_bus_stop[tuple_key] = {}
        
        # Assign the 'start' value as a key and 'average_num_of_waiting_people' as the nested value
        people_at_the_bus_stop[tuple_key][row["start"]] = row["average_num_of_waiting_people"]
    
    
    ## Creating a dictionary to stall the number of people getting off the bus at each bus stop during each different scenario

    # Calculate the mean alighting passengers
    total_disembark = t.groupby(['bus_num', 'day_of_week','hour', 'weather', 'has_exam', 'end']).size().reset_index(name='alighting_passengers')
    people_getting_off = {}
    # Iterate through each row to construct the dictionary
    for _, row in total_disembark.iterrows():
        # Create the tuple key from the first five columns
        tuple_key = (row["bus_num"], row["day_of_week"], row["hour"], row["weather"], row["has_exam"])
        
        # Initialize the main key if not already present
        if tuple_key not in people_getting_off:
            people_getting_off[tuple_key] = {}
        
        # Assign the 'start' value as a key and 'average_num_of_waiting_people' as the nested value
        people_getting_off[tuple_key][row["end"]] = row["alighting_passengers"]
        
    
    ## Creating a dictionary to stall the mean waiting time of passengers at each bus stop during each different scenario
    
    # Calculate the mean of 'waiting_time'
    average_waiting_times = t.groupby(['bus_num', 'day_of_week', 'hour', 'weather', 'has_exam', 'start'])[['waiting_time']].mean().reset_index()
    
    # Rename columns if desired
    average_waiting_times.columns = ['bus_num','day_of_week', 'hour', 'weather', 'has_exam', 'start','average_waiting_time']
    
    waiting_times = {}
    
    # Iterate through each row to construct the dictionary
    for _, row in average_waiting_times.iterrows():
        # Create the tuple key from the first five columns
        tuple_key = (row["bus_num"], row["day_of_week"], row["hour"], row["weather"], row["has_exam"])
        
        # Initialize the main key if not already present
        if tuple_key not in waiting_times:
            waiting_times[tuple_key] = {}
        
        # Assign the 'start' value as a key and 'average_waiting_time' as the nested value
        waiting_times[tuple_key][row["start"]] = row["average_waiting_time"]

    ### To get the average crowdedness, waiting time and satisfaction level of the original route at each different scenarios

    ## Creating a dictionary to stall average crowdedness level of the original route
    
    # Calculate the mean of 'crowdedness'
    original_crowdedness = t.groupby(['bus_num', 'day_of_week', 'hour', 'weather', 'has_exam'])[['crowdedness']].mean().reset_index()
    
    # Rename columns if desired
    original_crowdedness.columns = ['bus_num','day_of_week', 'hour', 'weather', 'has_exam','average_crowdedness']
    
    original_crowdedness_levels = {}
    
    # Iterate through each row to construct the dictionary
    for _, row in original_crowdedness.iterrows():
        # Create the tuple key from the first five columns
        tuple_key = (row["bus_num"], row["day_of_week"], row["hour"], row["weather"], row["has_exam"])
        
        # Initialize the main key if not already present
        if tuple_key not in original_crowdedness_levels:
            original_crowdedness_levels[tuple_key] = {}
        
        # Assign the 'average_crowdedness' as the value
        original_crowdedness_levels[tuple_key] = row["average_crowdedness"]

    ## Creating a dictionary to stall average waiting time of the original route

    # Calculate the mean of 'waiting_time'
    original_waiting_time = t.groupby(['bus_num', 'day_of_week', 'hour', 'weather', 'has_exam'])[['waiting_time']].mean().reset_index()
    
    # Rename columns if desired
    original_waiting_time.columns = ['bus_num','day_of_week', 'hour', 'weather', 'has_exam','average_waiting_time']
    
    original_waiting_times = {}
    
    # Iterate through each row to construct the dictionary
    for _, row in original_waiting_time.iterrows():
        # Create the tuple key from the first five columns
        tuple_key = (row["bus_num"], row["day_of_week"], row["hour"], row["weather"], row["has_exam"])
        
        # Initialize the main key if not already present
        if tuple_key not in original_waiting_times:
            original_waiting_times[tuple_key] = {}
        
        # Assign the 'average_waiting_time' as the value
        original_waiting_times[tuple_key] = row["average_waiting_time"]

    ## Creating a dictionary to stall average overall satisfaction level of the original route

    # Calculate the mean of 'overall_satisfaction'
    original_satisfaction = t.groupby(['bus_num', 'day_of_week', 'hour', 'weather', 'has_exam'])[['overall_satisfaction']].mean().reset_index()
    
    # Rename columns if desired
    original_satisfaction.columns = ['bus_num','day_of_week', 'hour', 'weather', 'has_exam','average_satisfaction']
    
    original_satisfactions = {}
    
    # Iterate through each row to construct the dictionary
    for _, row in original_satisfaction.iterrows():
        # Create the tuple key from the first five columns
        tuple_key = (row["bus_num"], row["day_of_week"], row["hour"], row["weather"], row["has_exam"])
        
        # Initialize the main key if not already present
        if tuple_key not in original_satisfactions:
            original_satisfactions[tuple_key] = {}
        
        # Assign the 'average_satisfaction' as the value
        original_satisfactions[tuple_key] = row["average_satisfaction"]
    
    '''Calculation of priority scores'''
    ### From Route_Optimisation.py to calculate the priority score ###
    unique_bus_numbers = train['bus_num'].unique().tolist()
    
    # Define the bus numbers and their respective stops present in our survey questions though not all will be used as it depends on whether respondents chose them
    bus_stops = {
        'A1': ['LT13 / Ventus', 'BIZ2 / Opp HSSML', 'PGP', 'Kent Ridge MRT / Opp Kent Ridge MRT', 'LT27 / S17', 'UHC / Opp UHC', 'IT / CLB'],
        'A2': ['IT / CLB', 'UHC / Opp UHC', 'LT27 / S17', 'Kent Ridge MRT / Opp Kent Ridge MRT', 'PGP', 'BIZ2 / Opp HSSML', 'LT13 / Ventus'],
        'D1': ['COM3', 'BIZ2 / Opp HSSML', 'LT13 / Ventus', 'IT / CLB', 'UTown', 'IT / CLB', 'LT13 / Ventus', 'BIZ2 / Opp HSSML', 'COM3'],
        'D2': ['COM3', 'PGP', 'Kent Ridge MRT / Opp Kent Ridge MRT', 'LT27 / S17', 'UHC / Opp UHC', 'UTown', 'UHC / Opp UHC', 'LT27 / S17', 'Kent Ridge MRT / Opp Kent Ridge MRT', 'PGP', 'COM3']
    }
    
    print(unique_bus_numbers)
    print(bus_stops)
    
    # Check if user filled in starting bus stops that does not exist for that particular bus number, remove such rows as these scenarios are not valid
    for bus_num in unique_bus_numbers:
        stops = bus_stops.get(bus_num, [])
        df2 = t[t['start'].isin(stops) | (t['bus_num'] != bus_num)]
    
    # Check if user filled in ending bus stops that does not exist for that particular bus number, remove such rows as these scenarios are not valid
    for bus_num in unique_bus_numbers:
        stops = bus_stops.get(bus_num, [])
        df2= t[t['end'].isin(stops) | (t['bus_num'] != bus_num)]
    
    # Initialize the MinMaxScaler
    scaler = MinMaxScaler()
    
    # Define a function to apply normalization for each bus stop group
    def normalize_group(group):
        # Normalize only the numerical columns, excluding categorical columns like 'weather' and 'has_exam'
        group[['num_people_at_bus_stop', 'crowdedness', 'comfort', 'safety']] = scaler.fit_transform(
            group[['num_people_at_bus_stop', 'crowdedness', 'comfort', 'safety']])
        return group
    
    # Create an empty dictionary to store priority orders for each bus, day, hour, weather, and exam status
    bus_route_priorities = {}
    
    # Loop through each bus
    for bus_num in unique_bus_numbers:
            # Filter data for the specific bus
            bus_df = df2[df2['bus_num'] == bus_num]
    
            # Loop through each unique day of the week
            for day in bus_df['day_of_week'].unique():
                # Filter data for the specific day
                bus_day_df = bus_df[bus_df['day_of_week'] == day]
    
                # Loop through each unique hour
                for hour in bus_day_df['hour'].unique():
                    # Filter data for the specific hour
                    bus_hour_df = bus_day_df[bus_day_df['hour'] == hour]
    
                    # Loop through each unique weather condition
                    for weather in bus_hour_df['weather'].unique():
                        # Filter data for the specific weather condition
                        bus_weather_df = bus_hour_df[bus_hour_df['weather'] == weather]
    
                        # Loop through each unique exam status
                        for has_exam in bus_weather_df['has_exam'].unique():
                            # Filter data for the specific exam status
                            bus_exam_df = bus_weather_df[bus_weather_df['has_exam'] == has_exam]
    
                            # Copy the DataFrame to avoid modifying the original one
                            df_hour = bus_exam_df.copy()
    
                            # Apply the normalization group-wise for each unique bus stop (start), excluding 'start'
                            df_hour_normalized = df_hour.groupby('start', group_keys=False).apply(normalize_group)
                            # Calculate the average stats by bus stop, taking into account normalized demand (num_people_at_bus_stop) and user preferences (crowdedness, comfort, safety)
                            # These user preferences (crowdedness, comfort, safety) are the 3 most strongly correlated factors to overall_satisfaction score as shown in our "Enhanced Visualization - Overall Satisfaction Score against Factors" Tableau Dashboard, under the visualisations folder of our repository
                            average_stats_by_start = df_hour_normalized.groupby('start')[['num_people_at_bus_stop', 'crowdedness', 'comfort', 'safety']].mean()
    
                            # Priority score will take into account normalized demand (num_people_at_bus_stop) and user preferences (crowdedness, comfort, safety)
                            average_stats_by_start['priority_score'] = average_stats_by_start['num_people_at_bus_stop'] - average_stats_by_start['crowdedness'] - average_stats_by_start['comfort'] - average_stats_by_start['safety']
    
                            # Sort the bus stops by the priority score in descending order
                            average_stats_by_start_sorted = average_stats_by_start.sort_values(by='priority_score', ascending=False)
    
                            # Store the sorted bus stop priority for this bus, day, hour, weather, and exam status
                            bus_route_priorities[(bus_num, day, hour, weather, has_exam)] = average_stats_by_start_sorted.index.tolist()
    
    # Sort the bus_route_priorities based on bus, day of the week, hour, weather, and exam status (all in ascending order)
    sorted_bus_route_priorities = dict(sorted(bus_route_priorities.items(), key=lambda x: (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4])))
    
    
    '''Simulation'''
    # Parameters
    BUS_SPEED = 0.4  # Assumption of average bus speed in NUS in km/min 
    MAX_BUS_CAPACITY = 50  # Max number of people on the bus
    
    # Define bus stops and distances
    stop_distances = {
        "A1": {
            "LT13 / Ventus": 0.5,
            "BIZ2 / Opp HSSML": 1.2,
            "PGP": 1.9,
            "Kent Ridge MRT / Opp Kent Ridge MRT": 2.8,
            "LT27 / S17": 3.3,
            "UHC / Opp UHC": 4.0,
            "IT / CLB": 4.5
        },
        "A2": {
            "IT / CLB": 0.6,
            "UHC / Opp UHC": 1.1,
            "LT27 / S17": 1.8,
            "Kent Ridge MRT / Opp Kent Ridge MRT": 2.3,
            "PGP": 3.2,
            "BIZ2 / Opp HSSML": 3.9,
            "LT13 / Ventus": 4.6
        },
        "D1": {
            "COM3": 0.0,
            "BIZ2 / Opp HSSML": 0.3,
            "LT13 / Ventus": 1.0,
            "IT / CLB": 1.4,
            "UTown": 2.3
        },
        "D2": {
            "COM3": 0.0,
            "PGP": 0.8,
            "Kent Ridge MRT / Opp Kent Ridge MRT": 1.7,
            "LT27 / S17": 2.2,
            "UHC / Opp UHC": 2.9,
            "UTown": 3.6
        }
    }
    
    
    def get_condition():
        try:
            # Ask the user for input to form the tuple key
            print("Please input the values for the route selection.")
            
            # Get inputs and validate their types
            selected_bus_num = str(input("Bus Number (A1 or A2 or D1 or D2): "))
            if selected_bus_num not in ['A1', 'A2', 'D1', 'D2']:
                raise ValueError("Invalid bus number. Choose from 'A1', 'A2', 'D1', 'D2'.")
            selected_day = int(input("Please pick a day from 1 to 7 (e.g., 1 for Monday): "))
            if selected_day not in [1, 2, 3, 4, 5, 6, 7]:
                raise ValueError("Invalid day. Choose a number between 1 and 7.")
    
            selected_hour = int(input("Please pick an hour from 7 to 23 (e.g, 8 for 0800H - 0859H): "))
            if selected_hour not in range(7, 24):
                raise ValueError("Invalid hour. Choose an hour between 7 and 23.")
    
            selected_weather = int(input("Please pick a weather condition (0 for Sunny, 1 for Rainy): "))
            if selected_weather not in [0, 1]:
                raise ValueError("Invalid weather condition. Choose 0 for Sunny or 1 for Rainy.")
    
            selected_exam = int(input("Please pick an exam status (0 for No, 1 for Yes): "))
            if selected_exam not in [0, 1]:
                raise ValueError("Invalid exam status. Choose 0 for No or 1 for Yes.")
    
        except ValueError as e:
            print(f"Error: {e}")
            return None  # Or you could use a loop to ask again until valid input is given
    
        # Form the tuple if all inputs are valid
        route_key = (selected_bus_num, selected_day, selected_hour, selected_weather, selected_exam)
        return route_key
    
    def get_route(route_key):
    
        # Retrieve the route based on the tuple key
        route = sorted_bus_route_priorities.get(route_key, [])
        if not route:
            print("No optimised route found for this combination.") # Due to lack of data, some scenarios are not included so when it is not in the dictionary keys, this will be printed.
            return []
        return route
    
    def get_route_distances(route_key, route): # To get the distances between 2 consecutive bus stops for the suggested route
        distances = []
        distances.append(stop_distances[route_key[0]][route[0]])
        for i in range(1,len(route)):
            distances.append(round(abs(stop_distances[route_key[0]][route[i-1]] - stop_distances[route_key[0]][route[i]]),2)
            )
        return distances
    
    def get_boarding_passengers(route_key, route): # To get the number of passengers boarding
        boarding_passengers = []
        for i in range(len(route)):
            boarding_passengers.append(people_at_the_bus_stop[route_key][route[i]])
        boarding_passengers = [people // 2 for people in boarding_passengers] # There are 2 buses at each bus stop so assumption made is that probability that the waiting passengers get on the bus is 0.5.
        return boarding_passengers
    
    def get_alighting_passengers(route_key, route): # To get the number of passengers alighting
        alighting_passengers = []
        for i in range(len(route)):
            if not route[i] in people_getting_off[route_key]:
                alighting_passengers.append(0)
            else:
                alighting_passengers.append(people_getting_off[route_key][route[i]])
        alighting_passengers = [people * 2 for people in alighting_passengers]
        return alighting_passengers
    
    def get_crowdedness(boarding_passengers, alighting_passengers): # To calculate crowdedness; crowdedness level is 0 to 10 so the formula for this is no. of passengers in the bus / max capacity * 10
        crowdedness = []
        for i in range(len(boarding_passengers)):
            if i == 0:
              crowdedness.append(min(round((boarding_passengers[i] - alighting_passengers[i]) / MAX_BUS_CAPACITY * 10, 1), 10))
            else: 
              crowdedness.append(min(round((boarding_passengers[i] - alighting_passengers[i])/ MAX_BUS_CAPACITY * 10 + crowdedness[i-1], 1), 10))
        return crowdedness
    
    def get_waiting_time(route_key, route, distances): # To get the waiting time of the passengers at the bus stop
        waiting_time = []
        for i in range(len(route)):
            if i == 0:
                waiting_time.append(min(round(waiting_times[route_key][route[i]]), round(distances[i]/ BUS_SPEED, 2))) # either the mean waiting time of the original route or the shortened waiting time due to the new route
            else:
                waiting_time.append(min(round(waiting_times[route_key][route[i]]), round((distances[i] + distances[i-1])/ BUS_SPEED, 2)))
        return waiting_time
    
    # Train a linear regression model for satisfaction prediction
    def train_satisfaction_model(data):
        model = LinearRegression()
        # Pass both columns as a list inside a single set of brackets
        model.fit(data[['crowdedness', 'waiting_time']], data['overall_satisfaction'])
        return model
    
    satisfaction_model = train_satisfaction_model(t)
    
    # Function to predict satisfaction using the model
    def predict_satisfaction(crowdedness, waiting_time):
        satisfaction_list = []
        for i in range(len(crowdedness)):
            # Make sure to pass both crowdedness and waiting_time as a single row
            satisfaction_list.append(round(satisfaction_model.predict([[crowdedness[i], waiting_time[i]]])[0], 2))
    
        return satisfaction_list
    # Functions to get the crowdedness, waiting time and satisfaction level of the original route
    def get_original_crowdedness(route_key):
        return original_crowdedness_levels[route_key]
    
    def get_original_waiting_time(route_key):
        return original_waiting_times[route_key]
    
    def get_original_satisfaction(route_key):
        return original_satisfactions[route_key]
    
    # Function to simulate the bus route and can see the difference of systen efficiency and user satisfaction levle between the optimised route and original route
    def simulate_bus_route(env, route_key, route, passengers_up, passengers_down, crowdedness, waiting_time, satisfaction, original_crowdedness, original_waiting_time, original_satisfaction):
        print(f"Starting bus route simulation with stops: {route}")
        print("---------------------------------------------------------")
        for i in range(len(route)):
            print(f"Bus arrived at {route[i]}")
            print(f"{passengers_up[i]} passengers have boarded the bus")
            print(f"{passengers_down[i]} passengers have got off the bus")
            print(f"Crowdedness level: {crowdedness[i]}")
            print(f"Waiting time: {waiting_time[i]} minutes")
            print(f"Overall Satisfaction: {satisfaction[i]}")
            print("---------------------------------------------------------")
            yield env.timeout(1)  # Simulating time spent at each stop
        print(f"Average crowdedness level of optimised route: {round(sum(crowdedness)/len(crowdedness), 2)}")
        print(f"Average crowdedness level of original route: {round(original_crowdedness, 2)}")
        print("")
        print(f"Average waiting time of optimised route: {round(sum(waiting_time)/len(waiting_time), 2)} minutes")
        print(f"Original waiting time of original route: {round(original_waiting_time, 2)} minutes")
        print("")
        print(f"Average overall satisfaction of optimised route: {round(sum(satisfaction)/len(satisfaction), 2)}")
        print(f"Original overall satisfaction of original route: {round(original_satisfaction, 2)}")
        print("---------------------------------------------------------")
        print("Bus route simulation completed.")
    
    # Set up the SimPy environment and run the simulation
    env = simpy.Environment()
    selected_condition = get_condition()
    selected_route = get_route(selected_condition)
    if selected_route != []:
        distances = get_route_distances(selected_condition, selected_route)
        boarding_passengers = get_boarding_passengers(selected_condition, selected_route)
        alighting_passengers = get_alighting_passengers(selected_condition, selected_route)
        crowdedness = get_crowdedness(boarding_passengers, alighting_passengers)
        waiting_time = get_waiting_time(selected_condition, selected_route, distances)
        satisfaction = predict_satisfaction(crowdedness, waiting_time)
        original_crowdedness = get_original_crowdedness(selected_condition)
        original_waiting_time = get_original_waiting_time(selected_condition)
        original_satisfaction = get_original_satisfaction(selected_condition)
        env.process(simulate_bus_route(env, selected_condition, selected_route, boarding_passengers, alighting_passengers, crowdedness, waiting_time, satisfaction, original_crowdedness, original_waiting_time, original_satisfaction))
        env.run()  
