# import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os

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

# Make predictions
y_pred = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

print(f'MAE: {mae}')
print(f'RMSE: {rmse}')