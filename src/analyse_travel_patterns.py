import folium
from folium import plugins
import os
import pandas as pd
import numpy as np
import datetime
import config

def approx_indiv_time_within_half_hour_range(dt): # dt: datetime object from "time" column
    if dt.minute < 30:  # first half of the hour - interpolate to 15 minutes
        approx_time = datetime.time(dt.hour, 15, 0)
    else:   # second half of the hour - interpolate to 45 minutes
        approx_time = datetime.time(dt.hour, 45, 0)
    return approx_time


def approx_times_within_half_hour_range(data, time):
    # Convert to datetime
    data[time] = pd.to_datetime(data[time], format="%Y-%m-%d %H:%M:%S")

    # For each datetime, approximate the time (within a half-hour range)
    data[time] = data[time].map(approx_indiv_time_within_half_hour_range)


def make_and_save_line_graph(trip_data_path, save_path):
    # Read trip_data
    trip_data = pd.read_csv(os.path.join(os.path.dirname(__file__), trip_data_path), keep_default_na=False)

    # Convert each time to an approximate time, within a half-hour range
    approx_times_within_half_hour_range(trip_data, "time")

    # Count each of these approximate times
    half_hour_time_interval_counts = trip_data.groupby("time").size().to_frame("num_of_trips").reset_index()

    # Plot line graph of number of trips throughout the day
    fig = half_hour_time_interval_counts.plot.line("time", "num_of_trips", figsize=(12,6), title="Line graph of number of trips against time", xlabel="Time", ylabel="Number of trips", xticks=[datetime.time(hour, 0, 0) for hour in range(7, 24)]).get_figure()
    fig.savefig(os.path.join(os.path.dirname(__file__), save_path))


def format_time_and_add_iso_time(data, time):
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
        noises = np.random.normal(0, 0.0001, 4) # add some normal noise to prevent all points (of the same bus stop) from falling on the same coordinate
        shift = 0.0003  # use shift to separate start and end markers
        iso_time_str = row["iso_time"]
        bus_num = row["bus_num"]
        start_long, start_lat, end_long, end_lat = row["start_long"] + noises[0], row["start_lat"] + noises[1] + shift, row["end_long"] + noises[2], row["end_lat"] + noises[3] - shift
        feature_start = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [start_long, start_lat]
            },
            "properties": {
                "times": [iso_time_str],
                "icon": "circle",
                "iconstyle": {"color": "green", "fillColor": "green", "fillOpacity": 0.6}
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
                "iconstyle": {"color": "red", "fillColor": "red", "fillOpacity": 0.6}
            }
        }

        feature_line = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[start_long, start_lat], [end_long, end_lat]]
            },
            "properties": {
                "times": [iso_time_str, iso_time_str],
                "style": {
                    "color": config.BUS_NUM_COLOURS[bus_num],
                    "weight": 1,
                    "opacity": 0.8
                }
            }
        }

        features.extend([feature_start, feature_end, feature_line])
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson_data


def make_and_save_timelapse(trip_data_path, save_path, scenario):
    # Read trip_data
    trip_data = pd.read_csv(os.path.join(os.path.dirname(__file__), trip_data_path), keep_default_na=False)

    # Raise exception if KeyError
    if "want_overall" not in scenario:
        raise Exception("Please specify 'want_overall' parameter")
    
    # Filter according to selected scenario
    if not scenario["want_overall"]:
        # Filter using want_exam_day
        if "want_exam_day" in scenario:
            if scenario["want_exam_day"]:
                trip_data = trip_data[trip_data["has_exam"] == "Yes"]
            else:
                trip_data = trip_data[trip_data["has_exam"] == "No"]

        # Filter using bus_num
        if "bus_num" in scenario:
            bus_num = scenario["bus_num"]
            trip_data = trip_data[trip_data["bus_num"] == bus_num]

    # Get iso format from "time" column of trip_data
    format_time_and_add_iso_time(trip_data, "time")

    # To the trip_data, we add coordinates of starting and ending bus stops
    add_coordinates_to_data(trip_data, "start", "end")

    geojson_data = get_geojson_for_timelapse(trip_data)

    # Generate NUS map and apply the TimestampedGeoJson timelapse to it
    map = folium.Map(location=config.NUS_COORDINATES, tiles="Cartodb dark_matter", zoom_start=15)
    plugins.TimestampedGeoJson(geojson_data, transition_time=200, period="PT10M", duration="PT10M", date_options="HH:mm:ss", loop=True, auto_play=True, add_last_point=False).add_to(map)
    map.save(os.path.join(os.path.dirname(__file__), save_path))
    

def main(save_path, scenario):
    make_and_save_line_graph(trip_data_path="../data/train_trip_data_after_sdv.csv", save_path=save_path)
    # make_and_save_timelapse(trip_data_path="../data/train_trip_data_after_sdv.csv", save_path=save_path, scenario=scenario)


if __name__ == "__main__":
    main(save_path="../visualisations/num_of_trips_throughout_day.png", scenario={"want_overall": False, "bus_num": "D2"})