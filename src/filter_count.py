import pandas as pd
import os

def filter_route_counts(trip_data, output_file_name, top_n):
    data = trip_data

    data['time'] = pd.to_datetime(data['time'])
    
    data['time_ceiling'] = data['time'].dt.ceil('10min')

    data['route'] = data['start'] + ' - ' + data['end']

    route_time_counts = data.groupby(['route', 'bus_num', 'time_ceiling']).size().reset_index(name='count')

    filtered_counts = route_time_counts.sort_values('count', ascending=False).head(top_n)

    filtered_counts[['start', 'end']] = filtered_counts['route'].str.split(' - ', expand=True)

    filtered_counts = filtered_counts[['start', 'end', 'bus_num', 'time_ceiling', 'count']]

    filtered_counts.to_csv(os.path.join(os.path.dirname(__file__), f"../data/timelapse_popular_trips/{output_file_name}.csv"), index=False)