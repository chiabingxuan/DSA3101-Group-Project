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

# If "start", "end" and "bus_num" are in separate columns, synthesised data may have nonsensical data (eg. "start" and "end" being the same). So we need to combine these 3 columns into one single column, "trip"
X_train['trip'] = X_train['start'] + ',' + X_train['end'] + ',' + X_train['bus_num']
X_train.drop(['start', 'end', 'bus_num'], axis=1, inplace=True)

# Drop the date in 'time' column
X_train['time'] = pd.to_datetime(X_train['time'], format='%Y-%m-%d %H:%M:%S') 
X_train['hour'] = X_train['time'].dt.hour
X_train['minute'] = X_train['time'].dt.minute
X_train.drop(columns=['time'], inplace=True)

X_train['year'] = X_train['year'].str.replace('Year ', '').astype(int) # Remove 'Year' from 'year' column, can do in data cleaning?

# Convert 'date' column to datetime format
X_train['date'] = pd.to_datetime(X_train['date'], format='%Y-%m-%d')

# Encode date
X_train['yeardate'] = X_train['date'].dt.year
X_train['month'] = X_train['date'].dt.month
X_train['day_of_month'] = X_train['date'].dt.day

X_train = X_train.drop(columns=['yeardate', 'date']) # Dropped 'year' column as all the years should be 2024 and considered a redundant feature

# Categorical cols: 'year', 'on_campus', 'main_reason_for_taking_isb', 'has_exam', 'weather', 'trip'
categorical_features = [0, 1, 2, 5, 6, 15]

# SMOTE-NC
smote_nc = SMOTENC(categorical_features = categorical_features, 
                   categorical_encoder = None, 
                   sampling_strategy = 'auto', 
                   random_state = 42,
                   k_neighbors = 5) # ** have to adjust accordingly because the training-test split might have resulted in some majors having lesser than 5 counts

# Apply SMOTE-NC on the training data
X_resampled, y_resampled = smote_nc.fit_resample(X_train, y_train)


# Save resampled data
resampled_data = pd.DataFrame(X_resampled, columns=X_train.columns)  # Create dataframe for resampled features
resampled_data['major'] = y_resampled  # add back major column to the resampled data

# Transform columns back to original sequence and format
resampled_data[['start', 'end', 'bus_num']] = resampled_data['trip'].str.split(',', expand=True)
resampled_data['yeardate'] = '2024'
resampled_data['date'] = pd.to_datetime(resampled_data[['yeardate', 'month', 'day_of_month']].astype(str).agg('-'.join, axis=1))
resampled_data['time'] = pd.to_datetime('1900-01-01 ' + resampled_data['hour'].astype(str) + ':' + resampled_data['minute'].astype(str))

original_cols = ['year', 'major', 'on_campus', 'main_reason_for_taking_isb', 'trips_per_day',
                    'duration_per_day', 'date', 'has_exam', 'start', 'end', 'bus_num', 
                    'time', 'weather', 'num_people_at_bus_stop', 'waiting_time', 
                    'waiting_time_satisfaction', 'crowdedness', 'crowdedness_satisfaction', 
                    'comfort', 'safety', 'overall_satisfaction']

resampled_data = resampled_data[original_cols]

# Testing dataset
X_test['major'] = y_test
X_test = X_test[original_cols]


# Upload to repository
X_test.to_csv(os.path.join(os.path.dirname(__file__), '../data/sampled_test_trip_data.csv'), index=False)
resampled_data.to_csv(os.path.join(os.path.dirname(__file__), '../data/resampled_trip_data.csv'), index=False)
