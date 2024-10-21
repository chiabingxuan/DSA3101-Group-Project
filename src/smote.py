import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTENC
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv('cleaned_trip_data.csv')

# Drop the date in 'time' column
data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S').dt.strftime('%H:%M')


# Convert 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'])

# encode date
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data['day_of_week'] = data['date'].dt.dayofweek


X = data.drop(columns=['major'])  # Features
y = data['major']  # Target

# Categorical cols
categorical_features =  [0, 1, 2, 6, 7, 8, 9, 11]

# Split the data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# SMOTE-NC
smote_nc = SMOTENC(categorical_features=categorical_features, 
                   categorical_encoder=None, 
                   sampling_strategy='auto', 
                   random_state=0, 
                   k_neighbors=5)

# Apply SMOTE-NC on the training data
X_resampled, y_resampled = smote_nc.fit_resample(X_train, y_train)