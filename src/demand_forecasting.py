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

"""
1. prepare the data 
- categorical: one hot encoding
- numerical: normalise the numbers

2. target variable
- number of people at the bus stop

3. random forest

4. evaluate the model
"""
data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/cleaned_trip_data.csv"), keep_default_na=False)

# Identify categorical and numerical columns
categorical_cols = ['year', 'major', 'on_campus', 'main_reason_for_taking_isb', 'weather', 'bus_num']
numerical_cols = ['trips_per_day', 'duration_per_day', 'waiting_time', 'waiting_time_satisfaction', 
                  'crowdedness', 'crowdedness_satisfaction', 'comfort', 'safety', 'overall_satisfaction']

"""
# Time-based features
data['date'] = pd.to_datetime(data['date'])
data['day_of_week'] = data['date'].dt.dayofweek  # Monday=0, Sunday=6
data['month'] = data['date'].dt.month
data['hour'] = pd.to_datetime(data['time']).dt.hour  # Assumes 'time' is in HH:MM format
"""

# Lagged features (previous day's demand)
data['demand_lag_1'] = data['num_people_at_bus_stop'].shift(1)
data['rolling_demand_7'] = data['num_people_at_bus_stop'].rolling(window=7).mean()


# Interaction features (does not change the rmse a lot)
# data['weather_crowdedness'] = data['weather'].astype(str) + '_' + data['crowdedness'].astype(str)

"""
# Derived features
data['average_trip_duration'] = data['duration_per_day'] / data['trips_per_day']
data['waiting_time_satisfaction_adjusted'] = data['waiting_time'] * data['waiting_time_satisfaction']

# Encoding categorical variables
data = pd.get_dummies(data, columns=categorical_cols)
"""

# Drop rows with NaN values (from lagging)
data = data.dropna()


X = data.drop(columns=['num_people_at_bus_stop'])  # Features
y = data['num_people_at_bus_stop']  # Target variable (demand)


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

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train the model
model.fit(X_train, y_train)

# Make predictions / output of floored predictions
y_pred = np.floor(model.predict(X_test))
print(y_pred)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

print(f'MAE: {mae}')
print(f'RMSE: {rmse}')

"""
to do:
- define a function where it can give a singular output that is under a specific bus stop location, and not just any number
- aka use the bus stops as a feature variable?? (dk if i got the correct term lol...)
"""

# Adding bus_stop_name and time to the categorical columns
categorical_cols = ['year', 'major', 'on_campus', 'main_reason_for_taking_isb', 'weather', 'bus_num', 'bus_stop_name', 'time']

# Define the function
def predict_demand_for_bus_stop(data, model, bus_stop, time):
    """
    Predicts the demand for a specific bus stop at a given time.
    
    Parameters:
    - data (DataFrame): The complete dataset with features.
    - model (Pipeline): Trained model pipeline for predictions.
    - bus_stop (str): Name of the bus stop for which to predict demand.
    - time (str): Time of day (e.g., '08:00') for which to predict demand.

    Returns:
    - dict: Dictionary containing bus stop, time, and predicted demand.
    """
    
    # Filter data for the specific bus stop and time
    data_filtered = data[(data['bus_stop_name'] == bus_stop) & (data['time'] == time)]
    
    if data_filtered.empty:
        return {"error": f"No data available for bus stop {bus_stop} at {time}."}
    
    # Drop target variable and apply preprocessing
    X_filtered = data_filtered.drop(columns=['num_people_at_bus_stop'])
    
    # Make prediction
    predicted_demand = model.predict(X_filtered)
    predicted_demand = np.floor(predicted_demand).astype(int)  # Flooring the prediction
    
    # Return as structured output
    return {
        "bus_stop_name": bus_stop,
        "time": time,
        "predicted_demand": predicted_demand[0]  # single prediction for this bus stop and time
    }

# Example usage
output = predict_demand_for_bus_stop(data, model, bus_stop='Stop A', time='08:00')
print(output)
