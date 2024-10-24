import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Train dataset
train_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data.csv"), keep_default_na=False)
X_train = train_data.drop(columns=['major'])  # Features
y_train = train_data['major']  # Target variable

## Encode (same as in smote.py)
# If "start", "end" and "bus_num" are in separate columns, synthesised data may have nonsensical data (eg. "start" and "end" being the same). So we need to combine these 3 columns into one single column, "trip"
X_train['trip'] = X_train['start'] + ',' + X_train['end'] + ',' + X_train['bus_num']
X_train.drop(['start', 'end', 'bus_num'], axis=1, inplace=True)

# Drop the date in 'time' column
X_train['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S') 
X_train['hour'] = X_train['time'].dt.hour
X_train['minute'] = X_train['time'].dt.minute
X_train.drop(columns=['time'], inplace=True)

X_train['year'] = X_train['year'].str.replace('Year ', '').astype(int) # Remove 'Year' from 'year' column, can do in data cleaning?

# Convert 'date' column to datetime format
X_train['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')

# Encode date
X_train['yeardate'] = X_train['date'].dt.year
X_train['month'] = X_train['date'].dt.month
X_train['day_of_month'] = X_train['date'].dt.day

X_train = X_train.drop(columns=['yeardate', 'date']) # Dropped 'year' column as all the years should be 2024 and considered a redundant feature

# Categorical cols: 'year', 'on_campus', 'main_reason_for_taking_isb', 'has_exam', 'weather', 'trip'
categorical_features = ['year', 'on_campus', 'main_reason_for_taking_isb', 'has_exam', 'weather', 'trip']

# Encode the categorical columns to do randomforestclassifier

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Test dataset
test_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/test_trip_data.csv"), keep_default_na=False)
X_test = test_data.drop(columns=['major'])  # Features
y_test = test_data['major']  # Target variable

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(classification_report(y_test, y_pred))