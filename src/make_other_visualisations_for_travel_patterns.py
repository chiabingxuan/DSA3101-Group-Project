import os
import pandas as pd
import datetime

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
    

def main():
    make_and_save_line_graph(trip_data_path="../data/train_trip_data_after_sdv.csv", save_path="../visualisations/num_of_trips_throughout_day.png")


if __name__ == "__main__":
    main()