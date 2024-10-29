import folium
from folium import plugins
from shapely.geometry import LineString
import geopandas as gpd
from collections import defaultdict
import os
import pandas as pd
import numpy as np
import datetime
import config


def convert_to_one_hour_range(dt): # dt: datetime object from "time" column
    # Get start and end hours in str
    start_hour = str(dt.hour)
    end_hour = str((dt + datetime.timedelta(hours=1)).hour)

    # Pad hours with leading zeroes where necessary
    if len(start_hour) == 1:
        start_hour = "0" + start_hour
    if len(end_hour) == 1:
        end_hour = "0" + end_hour
    
    # Make range
    range_str = f"{start_hour}:00:00 - {end_hour}:00:00"
    return range_str


def extract_hour(data, time):
    # Convert to datetime
    data[time] = pd.to_datetime(data[time], format="%Y-%m-%d %H:%M:%S")

    # For each datetime, convert to a 1 hour range (str)
    data[time] = data[time].map(convert_to_one_hour_range)


def add_coordinates_to_data(data, start, end):      # start and end both in the form (lat, long)
    BUS_STOP_COORDINATES = config.BUS_STOP_COORDINATES
    data["start_lat"] = data[start].map(lambda start: BUS_STOP_COORDINATES[start][0])
    data["start_long"] = data[start].map(lambda start: BUS_STOP_COORDINATES[start][1])
    data["end_lat"] = data[end].map(lambda end: BUS_STOP_COORDINATES[end][0])
    data["end_long"] = data[end].map(lambda end: BUS_STOP_COORDINATES[end][1])


def generate_proportions_concentrated_at_0_and_1(num_points):
    # Consider the function y = 0.5(cos x + 1). If we have uniform x values between 0 and π, corresponding y values will be more concentrated at 0 and 1
    angles = np.linspace(0, np.pi, num_points)  # Uniformly generate values between 0 and π

    # Apply the function
    proportions = (1 + np.cos(angles)) / 2
    return proportions


def get_first_hour_from_time_range(time_range):     # time_range: string corresponding to 1 hour range
    first_hour_str = time_range.split()[0]
    first_hour = datetime.datetime.strptime(first_hour_str, "%H:%M:%S")
    return first_hour


def get_heat_data_for_overall_heat_map(data):
    # Get heat data
    heat_data = list()
    for _, row in data.iterrows():
        start_long, start_lat, end_long, end_lat = row["start_long"], row["start_lat"], row["end_long"], row["end_lat"]

        # Add the start and end coordinates to the heat data
        heat_data.extend([(start_lat, start_long), (end_lat, end_long)])  # (lat, long) format for folium

    return heat_data


def get_heat_data_and_time_indices_for_timelapse(data):
    # Initialise storage for points grouped by time
    heat_data_dict = defaultdict(list)

    # Get heat data and time indices
    for _, row in data.iterrows():
        time, start_long, start_lat, end_long, end_lat = row["time"], row["start_long"], row["start_lat"], row["end_long"], row["end_lat"]
        
        # Add the start and end coordinates to the heat data
        heat_data_dict[time].extend([[start_lat, start_long], [end_lat, end_long]]) # (lat, long) format for folium
    
    # Convert dictionary to sorted lists by time
    time_indices = sorted(heat_data_dict.keys(), key=get_first_hour_from_time_range)    # time_indices: all times in ascending order
    heat_data = [heat_data_dict[time_index] for time_index in time_indices]     # heat_data: list of coordinates (coordinates represented as a list of length 2) for each time_index
    return heat_data, time_indices


if __name__ == "__main__":
    # Read trip_data
    trip_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False)

    # Extract hour only from "time" column of trip_data
    extract_hour(trip_data, "time")

    # To the trip_data, we add coordinates of starting and ending bus stops
    add_coordinates_to_data(trip_data, "start", "end")
    
    heat_data_for_overall_heat_map = get_heat_data_for_overall_heat_map(trip_data)
    heat_data_for_timelapse, time_indices = get_heat_data_and_time_indices_for_timelapse(trip_data)

    # Generate NUS map and apply the overall heat map to it
    map = folium.Map(location=config.NUS_COORDINATES, zoom_start=15)
    plugins.HeatMap(heat_data_for_overall_heat_map, radius=30).add_to(map)
    map.save(os.path.join(os.path.dirname(__file__), "../visualisations/nus_heat_map.html"))

    # Generate NUS map and apply the heat map timelapse to it
    map = folium.Map(location=config.NUS_COORDINATES, zoom_start=15)
    plugins.HeatMapWithTime(heat_data_for_timelapse, index=[str(time_index) for time_index in time_indices], radius=30, auto_play=True, display_index=True).add_to(map)
    map.save(os.path.join(os.path.dirname(__file__), "../visualisations/nus_heat_map_timelapse.html"))
