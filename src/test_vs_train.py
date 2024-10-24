import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Train dataset
train_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data.csv"), keep_default_na=False)
X_train = train_data.drop(columns=['major'])  # Features
y_train = train_data['major']  # Target variable

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