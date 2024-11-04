import pandas as pd
import os

def filter_route_counts(trip_data, output_file_name, min_count):
    data = trip_data

    data['time'] = pd.to_datetime(data['time'])
    data['time_floored'] = data['time'].dt.floor('10T')

    data['route'] = data['start'] + ' - ' + data['end']

    route_time_counts = data.groupby(['route', 'bus_num', 'time_floored']).size().reset_index(name='count')

    filtered_counts = route_time_counts[route_time_counts['count'] > min_count]

    filtered_counts[['start', 'end']] = filtered_counts['route'].str.split(' - ', expand=True)

    filtered_counts = filtered_counts[['start', 'end', 'bus_num', 'time_floored', 'count']]

    filtered_counts.to_csv(os.path.join(os.path.dirname(__file__), f"../data/{output_file_name}.csv"), index=False)