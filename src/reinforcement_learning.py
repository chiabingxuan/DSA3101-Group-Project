import os

# Load data
data = pd.DataFrame(pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/train_trip_data_after_sdv.csv"), keep_default_na=False))

# Obtain hour from 'time'
data['time'] = pd.to_datetime(data['time'])
data['hour'] = data['time'].data.hour

# Aggregate features
data_agg = data.groupby()


has_exam
start
end
time
weather
num_people_at_bus_stop
waiting_time
crowdedness
overall_satisfaction

