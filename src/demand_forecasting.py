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
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

####################################################################################################
### Objective of model: Predict the demand at specific bus stops at different time interval      ###
### Decision variable: Number of people at a specific bus stop and the  time slot                ###
####################################################################################################

def demand_forecasting():
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

    # One-hot encode the 'has_exam' column
    encoder = OneHotEncoder(drop='first', sparse_output=False)
    has_exam_encoded = encoder.fit_transform(X_train[['has_exam']])

    # Convert encoded array to DataFrame
    encoded_cols = encoder.get_feature_names_out(['has_exam'])
    has_exam_df = pd.DataFrame(has_exam_encoded, columns=encoded_cols, index=X_train.index)

    # Add the encoded columns to X_train
    X_train = pd.concat([X_train, has_exam_df], axis=1)

    # Repeat the process for X_test
    has_exam_encoded_test = encoder.transform(X_test[['has_exam']])
    has_exam_df_test = pd.DataFrame(has_exam_encoded_test, columns=encoded_cols, index=X_test.index)
    X_test = pd.concat([X_test, has_exam_df_test], axis=1)

    # Create the interaction feature
    for col in encoded_cols:
        X_train[f'{col}_duration_interaction'] = X_train[col] * X_train['duration_per_day']
        X_test[f'{col}_duration_interaction'] = X_test[col] * X_test['duration_per_day']

    # Add interaction columns to numerical_cols
    numerical_cols.extend([f'{col}_duration_interaction' for col in encoded_cols])

    # Preprocess data with a pipeline
    # One hot encoding to transform the categorical columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])

    # Define model pipeline - preprocessing the random forest model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=0))
    ])

    # Train the model with the data
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy_before = model.score(X_test, y_test)
    # print(accuracy_before)

    '''feature importance'''
    # Get feature names from the preprocessor
    feature_names = (preprocessor.transformers_[0][1].get_feature_names_out(numerical_cols).tolist() +
                    preprocessor.transformers_[1][1].get_feature_names_out(categorical_cols).tolist())

    # Extract feature importances
    importances = model.named_steps['regressor'].feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})

    # Rank features by importance
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    # Set Pandas display option to show all rows
    pd.set_option('display.max_rows', None)

    # Print the entire feature importance DataFrame
    print(feature_importance_df)

    # Select top N features (example selecting top 10 features)
    top_features = feature_importance_df['Feature'][:10].values
    X_train_selected = X_train[top_features]
    X_test_selected = X_test[top_features]

    '''Creating an output from the demand forecasting model'''
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
    # print(final_demand_array)

    """
    Output:

    MAE: 19.067862714508582
    RMSE: 20.59987655779927

    print(final_demand_array)
    [
    [21, 16, 47, 29, 15, 22, 29, 10, 21, 30, 26, 20, 26, 11, 20], 
    [28, 16, 22, 43, 24, 13, 19, 24, 27, 20, 21, 25, 13, 25, 18], 
    [14, 21, 25, 22, 24, 19, 25, 22, 25, 25, 30, 22, 23, 19, 19], 
    [32, 27, 25, 30, 28, 36, 17, 30, 25, 28, 25, 17, 18, 31, 0], 
    [23, 21, 35, 19, 16, 36, 28, 28, 8, 21, 0, 29, 11, 0, 0], 
    [19, 21, 36, 17, 27, 30, 23, 13, 11, 11, 25, 25, 19, 18, 0], 
    [32, 24, 27, 15, 20, 16, 14, 18, 16, 25, 41, 26, 13, 15, 22],
    [0, 31, 19, 31, 23, 22, 33, 29, 21, 20, 10, 20, 0, 0, 17], 
    [0, 30, 0, 25, 27, 31, 27, 15, 21, 18, 33, 23, 18, 0, 0]
    ]

    # Display the result
    for bus_stop, demands in demand_arrays.items():
        print(f"Bus Stop {bus_stop}: {demands}")

    Bus Stop BIZ2 / Opp HSSML: [21, 16, 47, 29, 15, 22, 29, 10, 21, 30, 26, 20, 26, 11, 20]
    Bus Stop COM3: [28, 16, 22, 43, 24, 13, 19, 24, 27, 20, 21, 25, 13, 25, 18]
    Bus Stop IT / CLB: [14, 21, 25, 22, 24, 19, 25, 22, 25, 25, 30, 22, 23, 19, 19]
    Bus Stop Kent Ridge MRT / Opp Kent Ridge MRT: [32, 27, 25, 30, 28, 36, 17, 30, 25, 28, 25, 17, 18, 31, 0]
    Bus Stop LT13 / Ventus: [23, 21, 35, 19, 16, 36, 28, 28, 8, 21, 0, 29, 11, 0, 0]
    Bus Stop LT27 / S17: [19, 21, 36, 17, 27, 30, 23, 13, 11, 11, 25, 25, 19, 18, 0]
    Bus Stop PGP: [32, 24, 27, 15, 20, 16, 14, 18, 16, 25, 41, 26, 13, 15, 22]
    Bus Stop UHC / Opp UHC: [0, 31, 19, 31, 23, 22, 33, 29, 21, 20, 10, 20, 0, 0, 17]
    Bus Stop UTown: [0, 30, 0, 25, 27, 31, 27, 15, 21, 18, 33, 23, 18, 0, 0]
    """


    #######################################################################################
    ### Objective: To create visualisations                                             ###
    ### Visualisation 1) Actual vs Predicted demand                                     ###
    #######################################################################################

    """
    for bus_stop in bus_stops:
        plt.plot(hour_intervals, demand_arrays[bus_stop], label=bus_stop)

    plt.title('Predicted Demand Throughout the Day')
    plt.xlabel('Time Intervals')
    plt.ylabel('Number of People')
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    """

def main():
    demand_forecasting()