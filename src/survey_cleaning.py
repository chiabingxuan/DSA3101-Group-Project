import pandas as pd
import numpy as np
import os
import datetime
import chatgpt_major_groupings


def reshape(survey_data):
    df_first_trip = survey_data.iloc[:, 1:22].copy()  # contains rows corresponding to first trip
    df_second_trip = survey_data.iloc[:, np.r_[1:9, 22:35]].copy()    # contains rows corresponding to second trip
    other_feedback_data = survey_data.iloc[:, np.r_[1:9, 35]].copy()   # contains rows corresponding to other feedback, which are responses to the last question
    df_second_trip.rename(columns=lambda name: name[:-2] if name[-2:] == ".1" else name, inplace=True)  # changing column names of df_second_trip to match those of df_first_trip
    trip_data = pd.concat([df_first_trip, df_second_trip], ignore_index=True)   # stacking df_first_trip and df_second_trip on top of each other
    return trip_data, other_feedback_data


def rename_columns(data, new_col_names):
    data.columns = new_col_names


def trim_whitespace(data, col_names):
    for col_name in col_names:
        data[col_name] = data[col_name].str.strip()


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
        data[col_name] = data[col_name].map(choose_first_int_only)    # choose the first number in the entry (removes all other characters that follow)
        data[col_name] = data[col_name].astype(int)   # convert column to int


def format_dates(data, col_names):  # col_names: names of all columns with dates
    for col_name in col_names:
        data[col_name] = pd.to_datetime(data[col_name]) # convert to datetime


def correct_indiv_time(trip_time):
    time_only = trip_time.time()    # get only the timestamp from datetime
    first_bus_time, last_bus_time = datetime.time(hour=7, minute=0), datetime.time(hour=23, minute=0) # just general operating hours for now (7 am - 11 pm), we can change this in the future if we want
    if time_only < first_bus_time:
        trip_time += datetime.timedelta(hours=12)   # change invalid AMs to PMs
    elif time_only > last_bus_time:
        trip_time -= datetime.timedelta(hours=12)   # change invalid PMs to AMs
    return trip_time.time() # get only the timestamp from corrected datetime


def format_and_correct_times(data, col_names):  # col_names: names of all columns with times
    for col_name in col_names:
        data[col_name] = pd.to_datetime(data[col_name], format="%I:%M:%S %p")   # convert to datetime
        data[col_name] = data[col_name].map(correct_indiv_time) # correct any invalid times


def clean_majors(data, col_name, is_trip_data):   # col_name: name of columns with major
    if is_trip_data:
        data[col_name] = np.array(chatgpt_major_groupings.cleaned_majors * 2)   # cleaned_majors are based on the major column in other_feedback_data. For trip_data, need to double the cleaned_majors list
    else:
        data[col_name] = np.array(chatgpt_major_groupings.cleaned_majors)


def clean_trip_data(trip_data):
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
    clean_majors(trip_data, "major", is_trip_data=True)


def clean_other_feedback_data(other_feedback_data):
    # Rename columns
    rename_columns(other_feedback_data, ["year", "major", "on_campus", "main_reason_for_taking_isb", "trips_per_day", "duration_per_day", "date", "has_exam", "feedback"])

    # Trim whitespace
    trim_whitespace(other_feedback_data, ["major", "main_reason_for_taking_isb", "trips_per_day", "duration_per_day", "feedback"])

    # Convert some columns to int data type
    convert_columns_to_int(other_feedback_data, ["trips_per_day", "duration_per_day"])

    # Clean date data
    format_dates(other_feedback_data, ["date"])

    # Clean major data
    clean_majors(other_feedback_data, "major", is_trip_data=False)


if __name__ == "__main__":
    survey_data = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/survey.csv"), keep_default_na=False))
    trip_data, other_feedback_data = reshape(survey_data)
    clean_trip_data(trip_data)
    clean_other_feedback_data(other_feedback_data)
    trip_data.to_csv(os.path.join(os.path.dirname(__file__), "../data/cleaned_survey_trip_data.csv"))
    other_feedback_data.to_csv(os.path.join(os.path.dirname(__file__), "../data/cleaned_survey_other_feedback_data.csv"))