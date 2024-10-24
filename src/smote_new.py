import pandas as pd
import numpy as np
import os
from imblearn.over_sampling import SMOTENC
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/cleaned_trip_data.csv"), keep_default_na=False)

X = data.drop(columns=['major'])  # Features
y = data['major']  # Target

# Split the data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)


# Functions
def combine_trip_columns(data):
    data['trip'] = data['start'] + ',' + data['end'] + ',' + data['bus_num']
    data.drop(['start', 'end', 'bus_num'], axis=1, inplace=True)
    return data

def extract_time_components(data):
    data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S') 
    data['hour'] = data['time'].dt.hour
    data['minute'] = data['time'].dt.minute
    data.drop(columns=['time'], inplace=True)
    return data

def clean(data):
    data['year'] = data['year'].str.replace('Year ', '').astype(int)
    return data

def encode_date(data):
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    data['yeardate'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['day_of_month'] = data['date'].dt.day
    return data

def drop_cols(data):
    data = data.drop(columns=['yeardate', 'date']) 
    return data

def transform_original_cols(data):
    data[['start', 'end', 'bus_num']] = data['trip'].str.split(',', expand=True)
    data['yeardate'] = '2024'
    data['date'] = pd.to_datetime(data[['yeardate', 'month', 'day_of_month']].astype(str).agg('-'.join, axis=1))
    data['time'] = pd.to_datetime('1900-01-01 ' + data['hour'].astype(str) + ':' + data['minute'].astype(str))

    original_cols = ['year', 'major', 'on_campus', 'main_reason_for_taking_isb', 'trips_per_day',
                    'duration_per_day', 'date', 'has_exam', 'start', 'end', 'bus_num', 
                    'time', 'weather', 'num_people_at_bus_stop', 'waiting_time', 
                    'waiting_time_satisfaction', 'crowdedness', 'crowdedness_satisfaction', 
                    'comfort', 'safety', 'overall_satisfaction']

    data = data[original_cols]

    return data

## Balance train set
# If "start", "end" and "bus_num" are in separate columns, synthesised data may have nonsensical data (eg. "start" and "end" being the same). So we need to combine these 3 columns into one single column, "trip"
X_train = combine_trip_columns(X_train)

# Drop the date in 'time' column
X_train = extract_time_components(X_train)

# Remove 'Year' from 'year' column
X_train = clean(X_train)

# Encode date
X_train = encode_date(X_train)

# Dropped 'year' column as all the years should be 2024 and considered a redundant feature
X_train = drop_cols(X_train)

# Categorical cols: 'year', 'on_campus', 'main_reason_for_taking_isb', 'has_exam', 'weather', 'trip'
categorical_features = [0, 1, 2, 5, 6, 15]

# SMOTE-NC
smote_nc = SMOTENC(categorical_features = categorical_features, 
                   categorical_encoder = None, 
                   sampling_strategy = 'auto', 
                   random_state = 42,
                   k_neighbors = 5) # ** have to adjust accordingly because the training-test split might have resulted in some majors having lesser than 5 counts

# Apply SMOTE-NC on the training data
X_train_resampled, y_train_resampled = smote_nc.fit_resample(X_train, y_train)

# Save resampled data
resampled_train_data = pd.DataFrame(X_train_resampled, columns=X_train.columns)  # Create dataframe for resampled features
resampled_train_data['major'] = y_train_resampled  # add back major column to the resampled data

# Transform columns back to original sequence and format
resampled_train_data = transform_original_cols(resampled_train_data)

# Upload to repository
resampled_train_data.to_csv(os.path.join(os.path.dirname(__file__), '../data/resampled_train_trip_data.csv'), index=False)



## Balance test set
# If "start", "end" and "bus_num" are in separate columns, synthesised data may have nonsensical data (eg. "start" and "end" being the same). So we need to combine these 3 columns into one single column, "trip"
X_train = combine_trip_columns(X_train)

# Drop the date in 'time' column
X_train = extract_time_components(X_train)

# Remove 'Year' from 'year' column
X_train = clean(X_train)

# Encode date
X_train = encode_date(X_train)

# Dropped 'year' column as all the years should be 2024 and considered a redundant feature
X_train = drop_cols(X_train)

# Categorical cols: 'year', 'on_campus', 'main_reason_for_taking_isb', 'has_exam', 'weather', 'trip'
categorical_features = [0, 1, 2, 5, 6, 15]

# SMOTE-NC
smote_nc = SMOTENC(categorical_features = categorical_features, 
                   categorical_encoder = None, 
                   sampling_strategy = 'auto', 
                   random_state = 42,
                   k_neighbors = 5) # ** have to adjust accordingly because the training-test split might have resulted in some majors having lesser than 5 counts

# Apply SMOTE-NC on the training data
X_train_resampled, y_train_resampled = smote_nc.fit_resample(X_train, y_train)

# Save resampled data
resampled_train_data = pd.DataFrame(X_train_resampled, columns=X_train.columns)  # Create dataframe for resampled features
resampled_train_data['major'] = y_train_resampled  # add back major column to the resampled data

# Transform columns back to original sequence and format
resampled_train_data = transform_original_cols(resampled_train_data)

# Upload to repository
resampled_train_data.to_csv(os.path.join(os.path.dirname(__file__), '../data/resampled_train2_trip_data.csv'), index=False)
