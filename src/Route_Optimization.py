def main():
    """
    **1. Data Cleaning & Preprocessing**
    """

    # Import the necessary libraries and packages
    import pandas as pd
    import warnings
    from sklearn.preprocessing import MinMaxScaler

    # Suppress warnings for a more user friendly experience
    warnings.filterwarnings("ignore")

    # Read in the dataset
    df = pd.read_csv(r'C:\Users\user\OneDrive - National University of Singapore\Uni\2425 SEM 1\DSA3101\Project\DSA3101-Group-Project\data\train_trip_data_after_sdv.csv')

    # Reformat the time, so that the hour can be extracted
    df['time'] = pd.to_datetime(df['time']).dt.strftime('%H:%M:%S')
    df['hour'] = pd.to_datetime(df['time']).dt.hour

    # Feature Engineering a new column to denote the day of the week
    df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek + 1


    # Remove irrelevant features
    df2 = df.drop(columns=['time', 'major', 'date', 'year', 'on_campus',
                            'main_reason_for_taking_isb', 'trips_per_day',
                            'duration_per_day', 'waiting_time',
                            'waiting_time_satisfaction',
                            'crowdedness_satisfaction', 'overall_satisfaction'])

    # Encode the 'has_exam' column so that we can perform mathematical operations on this column
    df2['has_exam'] = df2['has_exam'].map({'No': 0, 'Yes': 1})

    # Encode the 'weather' column using map so that we can perform mathematical operations on this column
    df2['weather'] = df2['weather'].map({'Sunny': 0, 'Rainy': 1})

    # Display the first few rows of dataframe
    print(df2.head())

    # Store all unique bus number
    unique_bus_numbers = df['bus_num'].unique().tolist()

    # Define the bus numbers and their respective stops present in our survey questions though not all will be used as it depends on whether respondents chose them
    bus_stops = {
        'A1': ['LT13 / Ventus', 'BIZ2 / Opp HSSML', 'PGP', 'Kent Ridge MRT / Opp Kent Ridge MRT', 'LT27 / S17', 'UHC / Opp UHC', 'IT / CLB'],
        'A2': ['IT / CLB', 'UHC / Opp UHC', 'LT27 / S17', 'Kent Ridge MRT / Opp Kent Ridge MRT', 'PGP', 'BIZ2 / Opp HSSML', 'LT13 / Ventus'],
        'D1': ['COM3', 'BIZ2 / Opp HSSML', 'LT13 / Ventus', 'IT / CLB', 'UTown', 'IT / CLB', 'LT13 / Ventus', 'BIZ2 / Opp HSSML', 'COM3'],
        'D2': ['COM3', 'PGP', 'Kent Ridge MRT / Opp Kent Ridge MRT', 'LT27 / S17', 'UHC / Opp UHC', 'UTown', 'UHC / Opp UHC', 'LT27 / S17', 'Kent Ridge MRT / Opp Kent Ridge MRT', 'PGP', 'COM3'],
        'E': ['Utown', 'IT / CLB', 'UTown']
    }

    print(unique_bus_numbers)
    print(bus_stops)

    # Check if user filled in starting bus stops that does not exist for that particular bus number, remove such rows as these scenarios are not valid
    for bus_num in unique_bus_numbers:
        stops = bus_stops.get(bus_num, [])
        df2 = df2[df2['start'].isin(stops) | (df2['bus_num'] != bus_num)]

    # Check if user filled in ending bus stops that does not exist for that particular bus number, remove such rows as these scenarios are not valid
    for bus_num in unique_bus_numbers:
        stops = bus_stops.get(bus_num, [])
        df2 = df2[df2['end'].isin(stops) | (df2['bus_num'] != bus_num)]

    # Display the final processed dataframe
    print("Final Dataframe:")
    print(df2)

    """
    **2. Bus Stop Prioritization and Sorting Algorithm Based on Survey Data**
    """

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

    # Print the dictionary containing the possible scenarios based on our survey data
    for key, value in sorted_bus_route_priorities.items():
        print(f"Bus: {key[0]}, Day: {key[1]}, Hour: {key[2]}, Weather: {key[3]}, Has Exam: {key[4]} - Bus Stops Order: {value}")

    """
    **3. User Customization Algorithm**
    """

    # To map numerical days to their proper names
    days_of_week = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }

    # To map 24H time to their ranges
    time_ranges = {hour: f"{hour:02d}00H - {hour:02d}59H" for hour in range(1, 24)}

    # To map weather conditions from binary back to their categorical name
    weather_conditions = {
        0: "Sunny",
        1: "Rainy"
    }

    # To map exam statuses from binary back to their categorical name
    exam_statuses = {
        0: "No",
        1: "Yes"
    }

    # Extract all unique bus numbers from the sorted_bus_route_priorities
    unique_bus_numbers = sorted(set([key[0] for key in sorted_bus_route_priorities.keys()]))

    def run_algorithm():
        # Yield all available bus numbers
        yield "Available Bus Numbers:"
        for bus_num in unique_bus_numbers:
            yield str(bus_num)

        # Ask the user to pick a bus number
        selected_bus_num = input("Please pick a bus number from the list above: ")
        yield "-------------------------------------------------------------------------------------------------------------"

        terminate_algorithm = 0

        if selected_bus_num in unique_bus_numbers:
            # Extract unique days available for the selected bus
            unique_days = sorted(set([key[1] for key in sorted_bus_route_priorities.keys() if key[0] == selected_bus_num]))

            # Yield available unique days for the selected bus
            yield f"Available Days of the week for Bus {selected_bus_num}:"
            for day in unique_days:
                yield str(day)

            selected_day = int(input("Please pick a day from the list above (e.g., 1 for Monday): "))
            yield "-------------------------------------------------------------------------------------------------------------"

            if selected_day in unique_days:
                # Extract unique hours available for the selected bus and day
                unique_hours = sorted(set([key[2] for key in sorted_bus_route_priorities.keys() if key[0] == selected_bus_num and key[1] == selected_day]))

                day_name = days_of_week.get(selected_day)
                yield f"Available Hours for Bus {selected_bus_num} on {day_name}:"
                for hour in unique_hours:
                    yield str(hour)

                selected_hour = int(input("Please pick an hour from the list above (e.g, 8 for 0800H - 0859H): "))
                yield "-------------------------------------------------------------------------------------------------------------"

                if selected_hour in unique_hours:
                    # Extract unique weather conditions available for the selected bus, day, and hour
                    unique_weathers = sorted(set([key[3] for key in sorted_bus_route_priorities.keys() if key[0] == selected_bus_num and key[1] == selected_day and key[2] == selected_hour]))

                    time_range = time_ranges.get(selected_hour)
                    yield f"Available Weather for Bus {selected_bus_num} on {day_name} between {time_range}:"
                    for weather in unique_weathers:
                        yield str(weather)

                    selected_weather = int(input("Please pick a weather condition from the list above (0 for sunny, 1 for rainy): "))
                    yield "-------------------------------------------------------------------------------------------------------------"

                    if selected_weather in unique_weathers:
                        # Extract unique exam statuses available for the selected bus, day, hour, and weather
                        unique_exams = sorted(set([key[4] for key in sorted_bus_route_priorities.keys() if key[0] == selected_bus_num and key[1] == selected_day and key[2] == selected_hour and key[3] == selected_weather]))

                        weather_name = weather_conditions.get(selected_weather)
                        yield f"Available Exam Status for Bus {selected_bus_num} on {day_name} between {time_range} with {weather_name} weather:"
                        for exam in unique_exams:
                            yield str(exam)

                        selected_exam = int(input("Please pick an exam status from the list above (0 for no exam, 1 for exam): "))
                        yield "-------------------------------------------------------------------------------------------------------------"

                        if selected_exam in unique_exams:
                            final_tuple = (selected_bus_num, selected_day, selected_hour, selected_weather, selected_exam)
                        else:
                            yield "Invalid exam status. Please select a valid exam status from the list."
                            terminate_algorithm = 1
                    else:
                        yield "Invalid weather condition. Please select a valid weather condition from the list."
                        terminate_algorithm = 1
                else:
                    yield "Invalid hour. Please select a valid hour from the list."
                    terminate_algorithm = 1
            else:
                yield "Invalid day. Please select a valid day from the list."
                terminate_algorithm = 1
        else:
            yield "Invalid bus number. Please select a valid bus number from the list."
            terminate_algorithm = 1

        if terminate_algorithm != 1:
            bus_route = bus_route_priorities.get(final_tuple, [])
            all_routes = bus_stops.get(selected_bus_num, [])

            prioritized_stops = []
            non_prioritized_stops = []

            for stop in bus_route:
                if stop in all_routes:
                    prioritized_stops.append(stop)

            non_prioritized_stops = [stop for stop in all_routes if stop not in prioritized_stops]

            final_routes = prioritized_stops + non_prioritized_stops

            got_exam = exam_statuses.get(selected_exam)
            yield f"User Selection: \nBus - {selected_bus_num} \nDay - {day_name} \nTime - {time_range} \nWeather - {weather_name} \nExam - {got_exam}"
            yield "-------------------------------------------------------------------------------------------------------------"
            yield f"Required Priority for Certain Bus Stops:"
            for index, stop in enumerate(bus_route):
                yield f"{index+1}: {stop}"
            yield "-------------------------------------------------------------------------------------------------------------"
            yield "Final Optimized Order of Bus Stops to visit:"
            for index, stop in enumerate(final_routes):
                yield f"{index+1}: {stop}"
            yield "------------------------------------------------------END----------------------------------------------------"
        else:
            yield "Algorithm terminated due to invalid input."
        
    def process_algorithm():
            for output in run_algorithm():
                print(output)

        # Call the function
    process_algorithm()
    return

main()
