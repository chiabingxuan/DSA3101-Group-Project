# Install the necessary library
!pip install faker

# from faker import Faker
from faker import Factory
import pandas as pd
import random
import csv

# read in the CSV file
df = pd.read_csv("/content/hypothetical_trip_data.csv")

# Initialize Faker
fake = Faker()

# Define a function to anonymize data
def anonymize_data(df):
  df['ID'] = df['ID'].apply(lambda x: fake.random_int(min=1000, max=9999))  # Anonymize ID with random numbers
  df['Name'] = df['Name'].apply(lambda x: fake.name())  # Anonymize names
  df['Email'] = df['Email'].apply(lambda x: fake.email())  # Anonymize emails
  df['year'] = df['year'].apply(lambda x: f"Year {random.randint(1, 4)}")  # Anonymize year with random year
  major = list(set(df['major'].tolist())) # Store the list of possible majors
  df['major'] = df['major'].apply(lambda x: random.choice(major))  # Anonymize major with random majors
  df['date'] = df['date'].apply(lambda x: fake.date_between(start_date='-10y', end_date='today'))  # Anonymize date with random
  df['time'] = df['time'].apply(lambda x: fake.time())  # Anonymize time with random time
  return df


# Apply the function to DataFrame
df_anonymized = anonymize_data(df.copy()) # Create a copy so original isn't changed

# Print the anonymized DataFrame
df_anonymized

# WARNING: This will overwrite the original 'hypothetical_trip_data.csv' file with the anonymized data.
# This action is irreversible. Proceed with caution!
df_anonymized.to_csv('hypothetical_trip_data.csv', index=False)