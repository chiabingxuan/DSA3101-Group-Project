import pandas as pd
import os

def filter_route_counts(trip_data, output_file_name, top_n):

    # Load data
    data = trip_data

    # Convert string to datetime type
    data['time'] = pd.to_datetime(data['time'])

    # Ceiling the time to the nearest 10th minute   
    data['time_ceiling'] = data['time'].dt.ceil('10min')

    # Combine 'start' and 'end' so that it we can group them for counting
    data['route'] = data['start'] + ' - ' + data['end']

    # Group by 'route', 'bus_num' and 'time_ceiling' for counting
    route_time_counts = data.groupby(['route', 'bus_num', 'time_ceiling']).size().reset_index(name='count')

    # Count based on grouping above
    filtered_counts = route_time_counts.sort_values('count', ascending=False).head(top_n)

    # Split 'route' back into 'start' and 'end'
    filtered_counts[['start', 'end']] = filtered_counts['route'].str.split(' - ', expand=True)

    # Choose only columns required
    filtered_counts = filtered_counts[['start', 'end', 'bus_num', 'time_ceiling', 'count']]

    # Save data as name provided in the argument: output_file_name
    filtered_counts.to_csv(os.path.join(os.path.dirname(__file__), f"../data/timelapse_popular_trips/{output_file_name}.csv"), index=False)