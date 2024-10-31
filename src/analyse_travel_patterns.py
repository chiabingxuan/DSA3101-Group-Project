import folium
from folium import plugins
from shapely.geometry import LineString
import os
import pandas as pd
import numpy as np
import datetime
import config

def extract_hour(data, time):
    # Convert "time" column to datetime 
    data[time] = pd.to_datetime(data[time])

    # Replace year with "2024" - TimestampedGeoJson cannot handle dates before epoch
    data[time] = data[time].map(lambda dt: dt.replace(year=2024))

    # Subtract 8 hours from each datetime (SGT: GMT+8)
    data[time] = data[time].map(lambda dt: dt - datetime.timedelta(hours=8))

    # Create new column storing ISO format of "time" column
    data["iso_time"] = data[time].dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def add_coordinates_to_data(data, start, end):      # start and end both in the form (lat, long)
    BUS_STOP_COORDINATES = config.BUS_STOP_COORDINATES
    data["start_lat"] = data[start].map(lambda start: BUS_STOP_COORDINATES[start][0])
    data["start_long"] = data[start].map(lambda start: BUS_STOP_COORDINATES[start][1])
    data["end_lat"] = data[end].map(lambda end: BUS_STOP_COORDINATES[end][0])
    data["end_long"] = data[end].map(lambda end: BUS_STOP_COORDINATES[end][1])


def get_geojson_for_timelapse(data):
    features = list()
    for _, row in data.iterrows():
        noises = np.random.normal(0, 0.0002, 4)
        iso_time_str = row["iso_time"]
        start_long, start_lat, end_long, end_lat = row["start_long"] + noises[0], row["start_lat"] + noises[1], row["end_long"] + noises[2], row["end_lat"] + noises[3]     # add some normal noise to prevent all points (of the same bus stop) from falling on the same coordinate
        feature_start = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [start_long, start_lat]
            },
            "properties": {
                "times": [iso_time_str],
                "icon": "circle",
                "iconstyle": {"color": "green"}
            }
        }

        feature_end = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [end_long, end_lat]
            },
            "properties": {
                "times": [iso_time_str],
                "icon": "circle",
                "iconstyle": {"color": "red"}
            }
        }

        features.extend([feature_start, feature_end])
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson_data
    

if __name__ == "__main__":
    # Read trip_data
    trip_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False)

    # Extract hour only from "time" column of trip_data
    extract_hour(trip_data, "time")

    # To the trip_data, we add coordinates of starting and ending bus stops
    add_coordinates_to_data(trip_data, "start", "end")

    geojson_data = get_geojson_for_timelapse(trip_data)

    # Generate NUS map and apply the TimestampedGeoJson timelapse to it
    map = folium.Map(location=config.NUS_COORDINATES, zoom_start=15)
    plugins.TimestampedGeoJson(geojson_data, transition_time=200, period="PT10M", duration="PT10M", loop=True, auto_play=True, add_last_point=True).add_to(map)
    map.save(os.path.join(os.path.dirname(__file__), "../visualisations/nus_trip_markers_timelapse.html"))
