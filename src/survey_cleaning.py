import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime
import major_mappings

def reshape(survey_data):
    df_first_trip = survey_data.iloc[:, 1:22].copy()  # contains rows corresponding to first trip
    df_second_trip = survey_data.iloc[:, np.r_[1:9, 22:35]].copy()    # contains rows corresponding to second trip
    other_feedback_data = survey_data.iloc[:, np.r_[1:9, 35]].copy()   # contains rows corresponding to other feedback, which are responses to the last question
    df_second_trip.rename(columns=lambda name: name[:-2] if name[-2:] == ".1" else name, inplace=True)  # changing column names of df_second_trip to match those of df_first_trip
    trip_data = pd.concat([df_first_trip, df_second_trip], ignore_index=True)   # stacking df_first_trip and df_second_trip on top of each other
    return trip_data, other_feedback_data


def rename_columns(data, new_col_names):
    data.columns = new_col_names
    print(f"Renamed columns: New column names are {new_col_names}")


def trim_whitespace(data, col_names):
    for col_name in col_names:
        data[col_name] = data[col_name].str.strip()
    print(f"Completed trimming of whitespace for {col_names}")


def choose_first_int_only(entry):
    entry_chosen = str()
    for char in entry:
        if not char.isdigit():
            break
        entry_chosen += char
    if not entry_chosen:
        entry_chosen = "0"      # if first char of entry is not a digit, we just treat the entry as 0 (eg. if num_people_at_bus_stop is "-3" or "a12", treat as 0)
    return entry_chosen


def convert_columns_to_int(data, col_names):
    for col_name in col_names:
        data[col_name] = data[col_name].astype(str)   # convert column to str
        modified_col = data[col_name].map(choose_first_int_only)    # choose the first number in the entry (removes all other characters that follow)
        num_entries_changed = (data[col_name] != modified_col).sum()    # compare original column (str data type) with the modified column and count the differences
        data[col_name] = modified_col.astype(int)   # convert modified column to int and use it to replace the original column in data
        print(f"Converted columns to int data type: Number of entries modified for {col_name} is {num_entries_changed}")


def format_dates(data, col_names):  # col_names: names of all columns with dates
    for col_name in col_names:
        data[col_name] = pd.to_datetime(data[col_name]) # convert to datetime


def correct_indiv_time(trip_time):
    time_only = trip_time.time()    # get only the timestamp from datetime
    FIRST_BUS_TIME, LAST_BUS_TIME = datetime.time(hour=7, minute=0), datetime.time(hour=23, minute=0) # just general operating hours for now (7 am - 11 pm), we can change this in the future if we want
    if time_only < FIRST_BUS_TIME:
        trip_time += datetime.timedelta(hours=12)   # change invalid AMs to PMs
    elif time_only > LAST_BUS_TIME:
        trip_time -= datetime.timedelta(hours=12)   # change invalid PMs to AMs
    return trip_time


def format_and_correct_times(data, col_names):  # col_names: names of all columns with times
    for col_name in col_names:
        data[col_name] = pd.to_datetime(data[col_name], format="%I:%M:%S %p")   # convert to datetime
        modified_col = data[col_name].map(correct_indiv_time) # correct any invalid times
        num_entries_changed = (data[col_name] != modified_col).sum()    # compare original column (datetime data type) with the modified column and count the differences
        data[col_name] = modified_col
        print(f"Formatted and corrected invalid times: Number of entries modified for {col_name} is {num_entries_changed}")

def correct_individual_major(major):
    # Step 1: Dictionary to get the mappings
    MAPPINGS = major_mappings.MAJOR_MAPPING

    # Step 2: Convert major to lowercase
    lower_major = major.lower()

    # Step 3: Replace using the mapping dictionary, if applicable
    cleaned_major = MAPPINGS.get(lower_major, lower_major)  # Use the original field if not found in mapping

    return cleaned_major


def clean_majors(data, col_name):   # col_name: name of columns with major
    modified_col = data[col_name].map(correct_individual_major)
    num_entries_changed = (data[col_name] != modified_col).sum()    # compare original column with the modified column and count the differences
    data[col_name] = modified_col
    print(f"Standardised majors: Number of entries modified for {col_name} is {num_entries_changed}")


def check_start_end_has_bus_num(start, end, bus_num):
    # Dictionary of bus services for each of our target bus stops
    # Since we are grouping bus stops in pairs, there is a potential issue here. For example, Kent Ridge MRT services A1 but Opp Kent Ridge MRT does not
    BUS_NUMS_OF_BUS_STOPS = {
        "Kent Ridge MRT / Opp Kent Ridge MRT": ["A1", "A2", "D2"],
        "LT27 / S17": ["A1", "A2", "D2"],
        "UHC / Opp UHC": ["A1", "A2", "D2"],
        "UTown": ["D1", "D2", "E"],
        "COM3": ["D1", "D2"],
        "BIZ2 / Opp HSSML": ["A1", "A2", "D1"],
        "LT13 / Ventus": ["A1", "A2", "D1"],
        "IT / CLB": ["A1", "A2", "D1", "E"],
        "PGP": ["A1", "A2", "D2"]
    }

    return (bus_num in BUS_NUMS_OF_BUS_STOPS[start]) and (bus_num in BUS_NUMS_OF_BUS_STOPS[end])    # check if bus_num is serviced in both starting and ending bus-stops


def remove_invalid_trips(data, start, end, bus_num):
    # Starting and ending bus stops cannot be the same
    are_start_end_the_same = data[start] == data[end]
    num_trips_with_start_end_the_same = are_start_end_the_same.sum()    # count number of trips with start == end
    data.drop(data[are_start_end_the_same].index, inplace=True)
    print(f"Removed invalid bus trips: Number of rows where starting and ending bus stops are the same is {num_trips_with_start_end_the_same}")

    # bus_num must be serviced in both starting and ending bus stops
    do_trips_not_have_bus_num_in_start_end = data.apply(lambda row: not check_start_end_has_bus_num(row[start], row[end], row[bus_num]), axis=1)
    num_trips_not_have_bus_num_in_start_end = do_trips_not_have_bus_num_in_start_end.sum()      # count number of trips where bus_num is not serviced in both start and end
    data.drop(data[do_trips_not_have_bus_num_in_start_end].index, inplace=True)
    print(f"Removed invalid bus trips: Number of rows where bus number is not serviced in both starting and ending bus stops is {num_trips_not_have_bus_num_in_start_end}")


def clean_feedback(data, col_name):
    data[col_name] = data[col_name].map(lambda feedback: feedback.lower())  # convert feedback to lowercase


def clean_trip_data(trip_data):
    print("Cleaning trip data...")

    # Rename columns
    rename_columns(trip_data, ["year", "major", "on_campus", "main_reason_for_taking_isb", "trips_per_day", "duration_per_day", "date", "has_exam", "start", "end", "bus_num", "time", "weather", "num_people_at_bus_stop", "waiting_time", "waiting_time_satisfaction", "crowdedness", "crowdedness_satisfaction", "comfort", "safety", "overall_satisfaction"])

    # Trim whitespace
    trim_whitespace(trip_data, ["major", "main_reason_for_taking_isb", "trips_per_day", "duration_per_day", "num_people_at_bus_stop", "waiting_time"])

    # Convert some columns to int data type
    convert_columns_to_int(trip_data, ["trips_per_day", "duration_per_day", "num_people_at_bus_stop", "waiting_time"])

    # Clean date and time data
    format_dates(trip_data, ["date"])
    format_and_correct_times(trip_data, ["time"])

    # Clean major data
    clean_majors(trip_data, "major")

    # Remove trips that don't make sense
    remove_invalid_trips(trip_data, "start", "end", "bus_num")

    print("Trip data cleaned!\n")


def clean_other_feedback_data(other_feedback_data):
    print("Cleaning other feedback data...")

    # Rename columns
    rename_columns(other_feedback_data, ["year", "major", "on_campus", "main_reason_for_taking_isb", "trips_per_day", "duration_per_day", "date", "has_exam", "feedback"])

    # Trim whitespace
    trim_whitespace(other_feedback_data, ["major", "main_reason_for_taking_isb", "trips_per_day", "duration_per_day", "feedback"])

    # Convert some columns to int data type
    convert_columns_to_int(other_feedback_data, ["trips_per_day", "duration_per_day"])

    # Clean date data
    format_dates(other_feedback_data, ["date"])

    # Clean major data
    clean_majors(other_feedback_data, "major")

    # Clean feedback data
    clean_feedback(other_feedback_data, "feedback")

    print("Other feedback data cleaned!\n")


def visualise_data(data, categorical_vars, continuous_vars):
    for var_index in categorical_vars:
        var_name = data.columns[var_index]
        plt.figure(figsize=(12,6))
        data.iloc[:, var_index].value_counts().plot(kind="barh")
        plt.title(f"Bar chart for {var_name}")
        plt.xlabel("Count")
        plt.ylabel(var_name)
        plt.tight_layout()
        plt.show()
    for var_index in continuous_vars:
        var_name = data.columns[var_index]
        data.iloc[:, var_index].plot(kind="hist")
        plt.title(f"Histogram for {data.columns[var_index]}")
        plt.xlabel(var_name)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.show()


def remove_outliers(data, year_of_study, num_people_at_bus_stop=None):
    if num_people_at_bus_stop is not None:  # means that data provided is trip_data
        print("Removing outliers for trip data...")
    else:
        print("Removing outliers for other feedback data...")

    # Remove rows that correspond to Year 5 or Masters / PhD
    is_year_5_and_above = data[year_of_study].map(lambda year: year in ["Year 5", "Masters / PhD"])
    num_is_year_5_and_above = is_year_5_and_above.sum()    # count number of rows with year being Year 5 and above
    data.drop(data[is_year_5_and_above].index, inplace=True)
    print(f"Removed outliers for {year_of_study}: Number of rows that are either 'Year 5' or 'Masters / PhD' is {num_is_year_5_and_above}")

    # Remove rows that have unrealistically large num_people_at_bus_stop
    if num_people_at_bus_stop is not None:  # means that data provided is trip_data
        has_large_num_people_at_bus_stop = data[num_people_at_bus_stop] >= 80   # set upper limit at 80
        num_has_large_num_people_at_bus_stop = has_large_num_people_at_bus_stop.sum()   # count number of rows with unrealistically large num_people_at_bus_stop
        data.drop(data[has_large_num_people_at_bus_stop].index, inplace=True)
        print(f"Removed outliers for {num_people_at_bus_stop}: Number of rows that have unrealistically large {num_people_at_bus_stop} is {num_has_large_num_people_at_bus_stop}")
    
    print("Outliers removed!\n")


if __name__ == "__main__":
    # Read in data
    survey_data = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/survey.csv"), keep_default_na=False))

    # Initial reshaping and cleaning of data
    trip_data, other_feedback_data = reshape(survey_data)
    clean_trip_data(trip_data)
    clean_other_feedback_data(other_feedback_data)

    # Conduct preliminary data exploration
    # visualise_data(trip_data, categorical_vars=[0, 1, 2, 3, 7, 8, 9, 10, 12], continuous_vars=[4, 5, 13, 14, 15, 16, 17, 18, 19, 20])    # omit date and time column
    # visualise_data(other_feedback_data, categorical_vars=[0, 1, 2, 3, 7], continuous_vars=[4, 5])    # omit date column

    # Remove outliers
    remove_outliers(trip_data, "year", num_people_at_bus_stop="num_people_at_bus_stop")
    remove_outliers(other_feedback_data, "year")

    # Save cleaned data frames
    trip_data.to_csv(os.path.join(os.path.dirname(__file__), "../data/cleaned_trip_data.csv"), index=False)
    other_feedback_data.to_csv(os.path.join(os.path.dirname(__file__), "../data/cleaned_other_feedback_data.csv"), index=False)
