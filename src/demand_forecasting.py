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
print(f'MAE: {mae}')
print(f'RMSE: {rmse}')

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

# Step 2: Initialize a nested list for the output
nested_array = []

# Step 3: Iterate through each bus stop and gather its predicted demands
for bus_stop in bus_stops:
    # Filter the DataFrame for the current bus stop
    demands = aggregated_output.loc[aggregated_output['bus_stop_name'] == bus_stop, 'predicted_demand'].tolist()
    # Append the list of demands to the nested array
    nested_array.append(demands)
print(nested_array)



"""
Output:

MAE: 19.119905956112852
RMSE: 20.640052216161987

nested_array:
[
[23, 29, 33, 23, 24, 18, 17, 26, 21, 12, 21, 26, 20, 23], 
[18, 32, 26, 20, 23, 29, 30, 19, 18, 9], 
[24, 21, 16, 21, 24, 19, 21, 21, 20, 24, 21, 26, 23, 26, 16],
[22, 22, 24, 21, 22, 24, 24, 23, 20, 23, 21, 22, 22, 21], 
[20, 26, 23, 25, 24, 20, 22, 19, 19, 23, 18, 23, 20, 26, 14], 
[25, 23, 22, 19, 24, 23, 18, 19, 23, 19, 22, 22, 22], 
[24, 20, 28, 28, 22, 24, 19, 24, 13, 32, 19, 22, 34], 
[21, 22, 21, 24, 20, 23, 22, 24, 22, 22, 25, 20, 22, 21, 18], 
[19, 23, 24, 23, 22, 23, 21, 23, 25, 25, 22, 21, 30, 24, 18]
]

# Display the resulting nested array
for i, demands in enumerate(nested_array):
    print(f"{bus_stops[i]}: {demands}")

BIZ2 / Opp HSSML: [23, 29, 33, 23, 24, 18, 17, 26, 21, 12, 21, 26, 20, 23]
COM3: [18, 32, 26, 20, 23, 29, 30, 19, 18, 9]
IT / CLB: [24, 21, 16, 21, 24, 19, 21, 21, 20, 24, 21, 26, 23, 26, 16]
Kent Ridge MRT / Opp Kent Ridge MRT: [22, 22, 24, 21, 22, 24, 24, 23, 20, 23, 21, 22, 22, 21]
LT13 / Ventus: [20, 26, 23, 25, 24, 20, 22, 19, 19, 23, 18, 23, 20, 26, 14]
LT27 / S17: [25, 23, 22, 19, 24, 23, 18, 19, 23, 19, 22, 22, 22]
PGP: [24, 20, 28, 28, 22, 24, 19, 24, 13, 32, 19, 22, 34]
UHC / Opp UHC: [21, 22, 21, 24, 20, 23, 22, 24, 22, 22, 25, 20, 22, 21, 18]
UTown: [19, 23, 24, 23, 22, 23, 21, 23, 25, 25, 22, 21, 30, 24, 18]
"""