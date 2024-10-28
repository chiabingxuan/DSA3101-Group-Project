import folium
from folium import plugins
from shapely.geometry import LineString
import geopandas as gpd
from collections import defaultdict
import os
import pandas as pd
import numpy as np
import config

def extract_time(data, time):
    # Convert to datetime
    data[time] = pd.to_datetime(data[time], format="%Y-%m-%d %H:%M:%S")

    # Extract time
    data[time] = data[time].map(lambda dt: dt.time())


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


def get_heat_data(data, num_points_sampled_per_line):
    # Get gdf
    data["line_geometry"] = data.apply(lambda row: LineString([(row["start_long"], row["start_lat"]), (row["end_long"], row["end_lat"])]), axis=1)
    gdf = gpd.GeoDataFrame(data, geometry="line_geometry")

    # Initialise storage for points grouped by time
    heat_data_dict = defaultdict(list)

    # Get heat data and time indices
    for _, row in gdf.iterrows():
        time, line = row["time"], row["line_geometry"]
        proportions_of_length = generate_proportions_concentrated_at_0_and_1(num_points_sampled_per_line)

        # For each proportion, which represents how far along the line with must go, the corresponding point is sampled. Proportions are concentrated at 0 and 1, since buses are more likely to accumulate at the bus stops themselves
        points = [line.interpolate(proportion * line.length) for proportion in proportions_of_length]

        # Add the sampled points to the heat data
        heat_data_dict[time].extend([[point.y, point.x] for point in points]) # (lat, long) format for folium
    
    # Convert dictionary to sorted lists by time
    time_indices = sorted(heat_data_dict.keys())    # time_indices: all times in ascending order
    heat_data = [heat_data_dict[time_index] for time_index in time_indices]     # heat_data: list of coordinates (coordinates represented as a list of length 2) for each time_index
    return heat_data, time_indices


if __name__ == "__main__":
    # Read trip_data
    trip_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False)

    # Extract time only from "time" column of trip_data
    extract_time(trip_data, "time")

    # To the trip_data, we add coordinates of starting and ending bus stops
    add_coordinates_to_data(trip_data, "start", "end")
    heat_data, time_indices = get_heat_data(trip_data, num_points_sampled_per_line=50)

    # Generate NUS map and apply the heat map timelapse to it
    map = folium.Map(location=config.NUS_COORDINATES, zoom_start=16)
    plugins.HeatMapWithTime(heat_data, index=[str(time_index) for time_index in time_indices], radius=8, auto_play=True, display_index=True, max_opacity=0.8).add_to(map)

    # Save map
    map.save(os.path.join(os.path.dirname(__file__), "../visualisations/nus_heat_map_timelapse.html"))