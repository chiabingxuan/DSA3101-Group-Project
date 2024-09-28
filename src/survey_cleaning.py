import pandas as pd
import numpy as np
import os

def reshape(survey_data):
    df_first_trip = survey_data.iloc[:, 1:22].copy()  # contains rows corresponding to first trip
    df_second_trip = survey_data.iloc[:, np.r_[1:9, 22:35]].copy()    # contains rows corresponding to second trip
    other_feedback_data = survey_data.iloc[:, np.r_[1:9, 35]].copy()   # contains rows corresponding to other feedback, which are responses to the last question
    df_second_trip.rename(columns=lambda name: name[:-2] if name[-2:] == ".1" else name, inplace=True)  # changing column names of df_second_trip to match those of df_first_trip
    trip_data = pd.concat([df_first_trip, df_second_trip], ignore_index=True)   # stacking df_first_trip and df_second_trip on top of each other
    return trip_data, other_feedback_data

survey_data = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/survey.csv")))
trip_data, other_feedback_data = reshape(survey_data)