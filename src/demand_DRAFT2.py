# Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os
import numpy as np
from xgboost import XGBRegressor
from sklearn.preprocessing import MinMaxScaler

####################################################################################################
### Objective of model: Predict the demand at specific bus stops at different time interval      ###
### Decision variable: Number of people at a specific bus stop and the  time slot                ###
####################################################################################################

def demand_forecasting():
    '''Preparing the data'''
    # import train and test datasets
    train = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False))
    test = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test_trip_data_after_sdv.csv"), keep_default_na=False))

    # Drop rows with NaN values (from lagging)
    train = train.dropna()
    test = test.dropna()

    # Separate features and target
    X_train = train.drop(columns=['num_people_at_bus_stop'])
    y_train = train['num_people_at_bus_stop']
    X_test = test.drop(columns=['num_people_at_bus_stop'])
    y_test = test['num_people_at_bus_stop']

    # Extract columns and categorize them
    categorical_cols = []
    numerical_cols = []

    for col in X_train.columns:
        if col == 'time' or col == 'date':  # Check if the column name is 'time' or 'date'
            continue
        elif X_train[col].dtype == 'object':  # If column is of type object, it's categorical
            categorical_cols.append(col)
        elif pd.api.types.is_numeric_dtype(X_train[col]):  # If it's numerical
            numerical_cols.append(col)
        elif X_train[col].dtype == 'bool':  # Boolean columns
            categorical_cols.append(col)

    # Change datetime object to only keep time
    X_train['time'] = pd.to_datetime(X_train['time']).dt.time
    X_test['time'] = pd.to_datetime(X_test['time']).dt.time

    '''Adding Interaction Feature between has_exam & waiting time'''
    # One-hot encode the 'has_exam' column
    encoder1 = OneHotEncoder(drop='first', sparse_output=False)
    has_exam_encoded = encoder1.fit_transform(X_train[['has_exam']])

    # Convert encoded array to DataFrame
    encoded_cols = encoder1.get_feature_names_out(['has_exam'])
    has_exam_df = pd.DataFrame(has_exam_encoded, columns=encoded_cols, index=X_train.index)

    # Add the encoded columns to X_train
    X_train = pd.concat([X_train, has_exam_df], axis=1)

    # Repeat for X_test
    has_exam_encoded_test = encoder1.transform(X_test[['has_exam']])
    has_exam_df_test = pd.DataFrame(has_exam_encoded_test, columns=encoded_cols, index=X_test.index)
    X_test = pd.concat([X_test, has_exam_df_test], axis=1)

    # Create interaction feature
    for col in encoded_cols:
        X_train[f'{col}_waiting_time_interaction'] = X_train[col] * X_train['waiting_time']
        X_test[f'{col}_waiting_time_interaction'] = X_test[col] * X_test['waiting_time']

    # Add interaction columns to numerical_cols
    numerical_cols.extend([f'{col}_waiting_time_interaction' for col in encoded_cols])

    '''Adding Interaction Feature between has_exam & duration_per_day'''
    # Create interaction feature
    for col in encoded_cols:
        X_train[f'{col}_duration_per_day_interaction'] = X_train[col] * X_train['duration_per_day']
        X_test[f'{col}_duration_per_day_interaction'] = X_test[col] * X_test['duration_per_day']

    # Add interaction columns to numerical_cols
    numerical_cols.extend([f'{col}_duration_per_day_interaction' for col in encoded_cols])

    '''Adding Interaction Feature between weather and duration_per_day'''
    # One-hot encode the 'weather' column
    encoder2 = OneHotEncoder(drop='first', sparse_output=False)
    weather_encoded = encoder2.fit_transform(X_train[['weather']])

    # Convert encoded array to DataFrame
    encoded_cols_weather = encoder2.get_feature_names_out(['weather'])
    weather_df = pd.DataFrame(weather_encoded, columns=encoded_cols_weather, index=X_train.index)
    
    # Add the encoded columns to X_train 
    X_train = pd.concat([X_train, weather_df], axis=1)

    # Repeat the process for X_test
    weather_encoded_test = encoder2.transform(X_test[['weather']])
    weather_df_test = pd.DataFrame(weather_encoded_test, columns=encoded_cols_weather, index=X_test.index)
    X_test = pd.concat([X_test, weather_df_test], axis=1)

    # Create the interaction feature 
    for col in encoded_cols_weather:
        X_train[f'{col}_duration_interaction'] = X_train[col] * X_train['duration_per_day']
        X_test[f'{col}_duration_interaction'] = X_test[col] * X_test['duration_per_day']

    # Add interaction columns to numerical_cols
    numerical_cols.extend([f'{col}_duration_interaction' for col in encoded_cols_weather])

    '''Adding Interaction Feature between weather and waiting_time'''
    # Create the interaction feature 
    for col in encoded_cols_weather:
        X_train[f'{col}_waiting_time_interaction'] = X_train[col] * X_train['waiting_time']
        X_test[f'{col}_waiting_time_interaction'] = X_test[col] * X_test['waiting_time']

    # Add interaction columns to numerical_cols
    numerical_cols.extend([f'{col}_waiting_time_interaction' for col in encoded_cols_weather])
    
    '''Feature Selection'''
    excluded_features = ['year', 'major', 'on_campus', 'main_reason_for_taking_isb', 
                         'waiting_time_satisfaction', 'crowdedness', 'crowdedness_satisfaction', 'comfort', 
                         'safety', 'overall_satisfaction', 'weather', 'has_exam']

    # Remove excluded features from categorical and numerical columns
    categorical_cols = [col for col in categorical_cols if col not in excluded_features]
    numerical_cols = [col for col in numerical_cols if col not in excluded_features]

    # Filter X_train and X_test to include only selected features
    X_train_selected = X_train[categorical_cols + numerical_cols]
    X_test_selected = X_test[categorical_cols + numerical_cols]

    '''Train the Model and Evaluate Feature Importance'''
    # Preprocessor for selected features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', MinMaxScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ]
    )

    # Define model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', XGBRegressor(n_estimators=100, random_state=0))
    ])

    # Fit the model
    model.fit(X_train_selected, y_train)

    ''' Feature Importance '''
    feature_names = (preprocessor.transformers_[0][1].get_feature_names_out(numerical_cols).tolist() +
                     preprocessor.transformers_[1][1].get_feature_names_out(categorical_cols).tolist())
    importances = model.named_steps['regressor'].feature_importances_
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    '''Evaluate Model Performance'''
    y_pred = np.floor(model.predict(X_test)).astype(int)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    model_accuracy = model.score(X_test_selected, y_test)

    # Create a DataFrame to display model performance
    model_performance_df = pd.DataFrame({
        'Metric': ['Root Mean Square Error', 'Mean Absolute Error', 'Model Accuracy'],
        'Value': [rmse, mae, model_accuracy]
    })

    '''Creating Output for Demand Forecasting'''
    output_df = pd.DataFrame({
        'bus_stop_name': X_test['start'],
        'time': X_test['time'],
        'actual_demand': y_test,
        'predicted_demand': y_pred
    })

    output_df['hour_interval'] = pd.to_datetime(output_df['time'].astype(str), format='%H:%M:%S').dt.floor('h').dt.time
    aggregated_output = output_df.groupby(['hour_interval', 'bus_stop_name']).agg(
        actual_demand=('actual_demand', 'mean'),
        predicted_demand=('predicted_demand', 'mean')
    ).round().astype(int).reset_index()

    bus_stops = aggregated_output['bus_stop_name'].unique()
    hour_intervals = sorted(output_df['hour_interval'].unique())
    demand_arrays = {bus_stop: [0] * len(hour_intervals) for bus_stop in bus_stops}

    for _, row in output_df.iterrows():
        bus_stop = row['bus_stop_name']
        hour = row['hour_interval']
        hour_index = hour_intervals.index(hour)
        demand_arrays[bus_stop][hour_index] = row['predicted_demand']

    final_demand_array = list(demand_arrays.values())

    return final_demand_array, feature_importance_df, model_performance_df

def main():
    demand_forecasting()

demand_forecasting()
