import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTENC
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv('../data/cleaned_trip_data.csv') # replace with latest cleaned dataset 

# Drop the date in 'time' column
data['time'] = pd.to_datetime(data['time'], format='%d/%m/%Y %H:%M') 
data['hour'] = data['time'].dt.hour
data['minute'] = data['time'].dt.minute
data.drop(columns=['time'], inplace=True)

data['year'] = data['year'].str.replace('Year ', '').astype(int) # Remove 'Year' from 'year' column, can do in data cleaning?

# Convert 'date' column to datetime format
data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')

# Encode date
data['yeardate'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data['day_of_week'] = data['date'].dt.dayofweek

data = data.drop(columns=['yeardate', 'date']) # Dropped 'year' column as all the years should be 2024 and considered a redundant feature


X = data.drop(columns=['major'])  # Features
y = data['major']  # Target

# Categorical cols
categorical_features =  [0, 1, 2, 5, 6, 7, 8, 9]

# Split the data into training and testing sets 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify = y)

# SMOTE-NC
smote_nc = SMOTENC(categorical_features=categorical_features, 
                   categorical_encoder=None, 
                   sampling_strategy='auto', 
                   random_state=0,
                   k_neighbors=5) # ** have to adjust accordingly because the training-test split might have resulted in some majors having lesser than 5 counts

# Apply SMOTE-NC on the training data
X_resampled, y_resampled = smote_nc.fit_resample(X_train, y_train)

# Save resampled data
resampled_data = pd.DataFrame(X_resampled, columns=X.columns)  # Create dataframe for resampled features
resampled_data['major'] = y_resampled  # add back major column to the resampled data
resampled_data.to_csv('../data/resampled_trip_data.csv', index=False)
