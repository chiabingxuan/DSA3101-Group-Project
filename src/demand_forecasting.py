# import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os
import numpy as np
import config 

# import train and test datasets
train = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False))
test = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test_trip_data_after_sdv.csv"), keep_default_na=False))

# Identify categorical and numerical columns
categorical_cols = ['year', 'major', 'on_campus', 'main_reason_for_taking_isb', 'weather', 'bus_num']
numerical_cols = ['trips_per_day', 'duration_per_day', 'waiting_time', 'waiting_time_satisfaction', 
                  'crowdedness', 'crowdedness_satisfaction', 'comfort', 'safety', 'overall_satisfaction']


# feature selection
"""
# Time-based features
data['date'] = pd.to_datetime(data['date'])
data['day_of_week'] = data['date'].dt.dayofweek  # Monday=0, Sunday=6
data['month'] = data['date'].dt.month
data['hour'] = pd.to_datetime(data['time']).dt.hour  # Assumes 'time' is in HH:MM format


# Lagged features (previous day's demand)
train['demand_lag_1'] = train['num_people_at_bus_stop'].shift(1)
train['rolling_demand_7'] = train['num_people_at_bus_stop'].rolling(window=7).mean()

test['demand_lag_1'] = test['num_people_at_bus_stop'].shift(1)
test['rolling_demand_7'] = test['num_people_at_bus_stop'].rolling(window=7).mean()


# Interaction features (does not change the rmse a lot)
# data['weather_crowdedness'] = data['weather'].astype(str) + '_' + data['crowdedness'].astype(str)


# Derived features
data['average_trip_duration'] = data['duration_per_day'] / data['trips_per_day']
data['waiting_time_satisfaction_adjusted'] = data['waiting_time'] * data['waiting_time_satisfaction']

# Encoding categorical variables
data = pd.get_dummies(data, columns=categorical_cols)
"""

# Drop rows with NaN values (from lagging)
train = train.dropna()
test = test.dropna()

# Dropping the y variable / target variable
X_train = train.drop(columns=['num_people_at_bus_stop'])  # Features
y_train = train['num_people_at_bus_stop']  # Target variable (demand)

X_test = test.drop(columns=['num_people_at_bus_stop'])  # Features
y_test = test['num_people_at_bus_stop']  # Target variable (demand)

# change the datetime object to drop the year, and only keep the time 
X_train['time'] = pd.to_datetime(X_train['time']).dt.time
X_test['time'] = pd.to_datetime(X_test['time']).dt.time

# Preprocess data with a pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# Define model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=0))
])

# Train the model
model.fit(X_train, y_train)

# Make predictions / output of floored predictions
y_pred = np.floor(model.predict(X_test)).astype(int)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

# Convert predictions and true values to a DataFrame for visualisations
output_df = pd.DataFrame({
    'bus_stop_name': X_test['start'],  # Corrected column name
    'time': X_test['time'],                    # Include the time column from the test set
    'actual_demand': y_test,
    'predicted_demand': y_pred
})

# Aggregating the output, grouped by the hourly intervals and the bus_stop_name
# Convert 'time' to datetime.time format to exclude the year component
output_df['time'] = pd.to_datetime(output_df['time'], format='%H:%M:%S', errors='coerce').dt.time

# Use lowercase 'h' for the floor method
output_df['hour_interval'] = pd.to_datetime(output_df['time'].astype(str), format='%H:%M:%S').dt.floor('h').dt.time

# Group by bus_stop_name and hour_interval to get the average demand
aggregated_output = output_df.groupby(['hour_interval', 'bus_stop_name']).agg(
    actual_demand=('actual_demand', 'mean'),
    predicted_demand=('predicted_demand', 'mean')
).round().astype(int).reset_index()

# Preparing an array of bus stop names, and each bus_stop_name is an array with the predicted demand for hourly intervals
# Step 1: Get unique bus stop names
bus_stops = aggregated_output['bus_stop_name'].unique()
hour_intervals = sorted(output_df['hour_interval'].unique())

# Step 2: Initialize a dictionary to hold the arrays, so that the length of each inner array is the same
demand_arrays = {bus_stop: [0] * len(hour_intervals) for bus_stop in bus_stops}

# Populate the demand arrays with the predicted demand
for _, row in output_df.iterrows():
    bus_stop = row['bus_stop_name']
    hour = row['hour_interval']
    hour_index = hour_intervals.index(hour)
    demand_arrays[bus_stop][hour_index] = row['predicted_demand']

# Convert to a list of lists
final_demand_array = list(demand_arrays.values())

"""
Output:

MAE: 19.067862714508582
RMSE: 20.59987655779927

print(final_demand_array)
[
[22, 25, 32, 21, 31, 15, 8, 37, 8, 19, 12, 22, 18, 32, 0], 
[22, 34, 29, 20, 24, 27, 33, 0, 0, 18, 12, 9, 0, 0, 0], 
[29, 24, 21, 18, 27, 15, 16, 34, 30, 15, 19, 30, 28, 26, 16], 
[23, 29, 10, 19, 12, 20, 33, 9, 21, 19, 23, 16, 11, 17, 0], 
[29, 16, 34, 19, 27, 24, 22, 34, 27, 13, 23, 23, 24, 22, 15], 
[20, 19, 22, 14, 18, 18, 27, 23, 22, 18, 14, 19, 21, 0, 0], 
[25, 26, 26, 30, 24, 20, 21, 21, 14, 26, 11, 20, 33, 0, 0], 
[27, 16, 29, 22, 19, 15, 27, 14, 15, 15, 35, 35, 29, 23, 17], 
[28, 31, 18, 18, 33, 24, 16, 34, 21, 28, 24, 17, 35, 35, 19]
]

# Display the result
for bus_stop, demands in demand_arrays.items():
    print(f"Bus Stop {bus_stop}: {demands}")

Bus Stop BIZ2 / Opp HSSML: [22, 25, 32, 21, 31, 15, 8, 37, 8, 19, 12, 22, 18, 32, 0]
Bus Stop COM3: [22, 34, 29, 20, 24, 27, 33, 0, 0, 18, 12, 9, 0, 0, 0]
Bus Stop IT / CLB: [29, 24, 21, 18, 27, 15, 16, 34, 30, 15, 19, 30, 28, 26, 16]
Bus Stop Kent Ridge MRT / Opp Kent Ridge MRT: [23, 29, 10, 19, 12, 20, 33, 9, 21, 19, 23, 16, 11, 17, 0]
Bus Stop LT13 / Ventus: [29, 16, 34, 19, 27, 24, 22, 34, 27, 13, 23, 23, 24, 22, 15]
Bus Stop LT27 / S17: [20, 19, 22, 14, 18, 18, 27, 23, 22, 18, 14, 19, 21, 0, 0]
Bus Stop PGP: [25, 26, 26, 30, 24, 20, 21, 21, 14, 26, 11, 20, 33, 0, 0]
Bus Stop UHC / Opp UHC: [27, 16, 29, 22, 19, 15, 27, 14, 15, 15, 35, 35, 29, 23, 17]
Bus Stop UTown: [28, 31, 18, 18, 33, 24, 16, 34, 21, 28, 24, 17, 35, 35, 19]
"""