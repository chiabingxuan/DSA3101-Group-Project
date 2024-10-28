# Importing all necessary libraries
import numpy as np
import pandas as pd
import sklearn
import math
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
from kmodes.kprototypes import KPrototypes
from kmodes import kprototypes
# To implement a progress bar tracking the progress of the for loops used below since they take quite a long time to execute
from tqdm import tqdm
# To ignore the DeprecationWarning invoked in Silhouette Method below
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Importing the training data set (AFTER SMOTE-NC and SDV) as a Pandas dataframe
dataframe = pd.read_csv('C:/Users/65905/Downloads/DSA3101-Group-Project/data/train_trip_data_after_sdv.csv', encoding='utf-8')

#Replace all inf values with NaN
dataframe = dataframe.replace([np.inf, -np.inf], np.nan) 

#Remove all NaN values
dataframe = dataframe.dropna()

# Remove the '1900-01-01' from all rows of the 'time' column since it is redundant
dataframe['time'] = dataframe['time'].str.replace('1900-01-01', '')

# Combine the 'date' and 'time' columns into a new 'datetime' column
dataframe['datetime'] = dataframe['date'] + ' ' + dataframe['time']

# Convert the 'datetime' column into datetime type
dataframe['datetime'] = pd.to_datetime(dataframe['datetime']) 

# Extract the day of the week (Monday-Sunday) from the 'date' column and puts this into a new 'day_of_week' column
dataframe['day_of_week'] = dataframe['datetime'].dt.day_name()

# Extract the hour of the day (0-24) from the 'datetime' column and puts this into a new 'hour' column
dataframe['hour'] = dataframe['datetime'].dt.hour

# Combine the 'start', 'end', and 'bus_num' columns into a new 'trip' column
dataframe['trip'] = dataframe['start'] + ' ' + dataframe['end'] + ' ' + dataframe['bus_num']

# Combine the 'duration_per_day' and 'trips_per_day' columns into a new 'duration_per_trip' column indicating extent of usage of ISB
dataframe['duration_per_day'] = dataframe['duration_per_day'].astype(float)
dataframe['trips_per_day'] = dataframe['trips_per_day'].astype(float)
dataframe['duration_per_trip'] = dataframe['duration_per_day'] / dataframe['trips_per_day']

# This returns False at first, so no NaN values introduced in 'duration_per_trip'
print(dataframe['duration_per_trip'].isnull().any())

# This returns True at first, so there ARE inf values introduced in 'duration_per_trip'
print(np.isinf(dataframe['duration_per_trip']).any())

dataframe = dataframe.replace([np.inf, -np.inf], np.nan) 
dataframe = dataframe.dropna() 

#Now, this should return False
print(np.isinf(dataframe['duration_per_trip']).any())

# Dimensionality reduction should always be done before clustering.
# This is because clustering generally depends on some sort of distance measure. 
# Points near each other are in the same cluster; points far apart are in different clusters. 
# But in high dimensional spaces, distance measures do not work very well. 
# You reduce the number of dimensions first so that your distance metric in clustering will make sense.

# REMOVE THE FOLLOWING COLUMNS FOR VARIOUS REASONS, AS PART OF MANUAL DIMENSIONALITY REDUCTION
# 'date','time','datetime' columns since they are replaced by 'day_of_week' and 'hour' columns
# start','end','bus_num' columns since they are replaced by 'trip' column
# duration_per_day', 'trips_per_day' columns since they are replaced by 'duration_per_trip' column
# 'waiting_time_satisfaction', 'crowdedness_satsifaction' columns since the relationship is rather obvious
# higher waiting time and higher crowdedness level = lower corresponding satisfaction
dataframe = dataframe.drop(['date', 'time','datetime','datetime','start','end','bus_num','duration_per_day','trips_per_day',
                            'waiting_time_satisfaction','crowdedness_satisfaction'], axis = 'columns')

continuous_variable_columns = ["num_people_at_bus_stop", "waiting_time", "crowdedness", "comfort", "safety", "overall_satisfaction", "duration_per_trip"]
categorical_variable_columns = ["year", "major", "on_campus", "main_reason_for_taking_isb", "has_exam", "weather", "day_of_week", "hour", "trip"]

# Convert the continuous variable columns into "float" type
dataframe[continuous_variable_columns] = dataframe[continuous_variable_columns].astype(float)

# Convert the categorical variable columns into "str" type
dataframe[categorical_variable_columns] = dataframe[categorical_variable_columns].astype(str)

# NORMALISATION OF ALL CONTINUOUS VARIABLE COLUMNS OF "float" TYPE
# Min-Max Scaling is chosen as the normalisation technique here
# The scale of continuous data is rescaled/changed to fall between 0 and 1, while preserving the original shape/distribution of continuous data with no distortion.
# This is because ML algorithms tend to perform better, or converge faster, when the different features are on a smaller scale. 
# Standardisation is NOT chosen as the scaling method here because we DO NOT KNOW FOR SURE that our continuous data follows a normal distribution.
scaler = MinMaxScaler(feature_range=(0, 1))
dataframe[continuous_variable_columns] = scaler.fit_transform(dataframe[continuous_variable_columns])

# CHOSEN MODEL FOR SEGMENTING USERS BASED ON TRAVEL BEHAVIOR AND PREFERENCES: K-PROTOTYPES CLUSTERING.
# K-Prototypes is a hybrid of K-Means and K-Modes that is designed for clustering data with both continuous (numerical) and categorical features. 
# For continuous (numerical) features, K-Means uses the squared Euclidean distance as a measure of how similar 2 data points are, with smaller distances indicating higher similarity.
# For categorical featues, K-Modes uses a simple matching dissimilarity measure which counts the number of categories that do not match between 2 data points. 
# K-Prototypes combines both of the above into a dissimilarity measure that gives a comprehensive indication of similarity across both continuous (numerical) and categorical features.

# ELBOW METHOD FOR FINDING OPTIMAL K = NUMBER OF CLUSTERS
# It involves running the K-prototypes clustering model for different values of K, calculating the total cluster variance for each K using the cost_ attribute.
# The key is to identify the "elbow" point on the plot, where the rate of decrease in total cluster variance sharply changes,
# and total cluster variance becomes almost constant.
# This elbow point signifies a balance between capturing variance in the data and avoiding unnecessary complexity, and is the most appropriate K for the given dataset.
# Extract the values of the dataframe and store them in a numpy array called df_array
df_array = dataframe.values

# Re-specify all the types (continuous=float/categorical=str) of each column in df_array
df_array[:, 0:6] = df_array[:, 0:6].astype(str)
df_array[:, 6:12] = df_array[:, 6:12].astype(float)
df_array[:, 12:15] = df_array[:, 12:15].astype(str)
df_array[:, 15] = df_array[:, 15].astype(float)

# Create a dictionary called total_cluster_variance to store values of K as keys, and corresponding total cluster variances as values
total_cluster_variance = dict() 
 
# For each value of K,
for k in tqdm(range(2,11), total = 9):
    # create an untrained K-Prototypes model using the KPrototypes() function and that specific value of K,
    untrained_model = kprototypes.KPrototypes(n_clusters=k,max_iter=20)
    # then train the K-Prototypes model using the input dataset (as a numpy array) and fit() function
    trained_model = untrained_model.fit(df_array, categorical=[0, 1, 2, 3, 4, 5, 12, 13, 14])
    # after training the model, find the total cluster variance for the given K using the .cost_ attribute of trained model
    total_cluster_variance[k]=trained_model.cost_
    # and assign total cluster variance as a value to the current key of K in the dictionary
 
plt.xlabel('Values of K') 
plt.ylabel('Total Cluster Variance') 
plt.title('Elbow Method For Optimal k')
# Plot the data
plt.plot(total_cluster_variance.keys(), total_cluster_variance.values()) 
plt.scatter(total_cluster_variance.keys(), total_cluster_variance.values())
# Show the plot 
plt.show()

# From the given plot, it seems that the optimal K = 7, BUT it is not too clear as the "elbow point" is not so clear and sharp.
# This is because the Elbow Method often fails to give a specific value for the optimal K if the input dataset has abnormal distribution.

# In such an ambiguous case, the SILHOUETTE METHOD IS USED TO COMPLEMENT THE ELBOW METHOD
# The silhouette value measures how similar a point is to its own cluster (cohesion) compared to other clusters (separation).
# The range of the Silhouette value is between +1 and -1. \
# A high value is desirable and indicates that the point is placed in the correct cluster. 
# If many points have a negative Silhouette value, it may indicate that we have created too many or too few clusters.
# Use a custom-defined mixed_distance() function to calculate distance between 2 data points having mixed categorical and continuous features
# "a" and "b" are the 2 data points; "categorical" takes a list of indices of categorical features within input data
def mixed_distance(a,b,categorical=None): 
    # If there are no categorical features within input data,
    if categorical is None: 
        # just use euclidean_dissim() to calculate distance between 2 data points' continuous features
        num_score=kprototypes.euclidean_dissim(a,b) 
        return num_score
     # Else if there are BOTH categorical and continuous features within input data,
    else:
        cat_index=categorical
        a_cat=[]
        b_cat=[]
        for index in cat_index:
            a_cat.append(a[index])
            b_cat.append(b[index])
        a_num=[]
        b_num=[]
        l=len(a)
        for index in range(l):
            if index not in cat_index:
                a_num.append(a[index])
                b_num.append(b[index])
                
        a_cat=np.array(a_cat).reshape(1,-1)
        a_num=np.array(a_num).reshape(1,-1)
        b_cat=np.array(b_cat).reshape(1,-1)
        b_num=np.array(b_num).reshape(1,-1)
        # use matching_dissim() to calcualte distance between 2 data points' categorical features
        cat_score=kprototypes.matching_dissim(a_cat,b_cat) 
        # use euclidean_dissim() to calculate distance between 2 data points' continuous features
        num_score=kprototypes.euclidean_dissim(a_num,b_num) 
        # then return the sum of 2 distances calculated separately
        return cat_score+num_score 
    
# # Use a custom-defined dm_prototypes() function to calculate distance matrix for k-prototypes clustering
def dm_prototypes(dataset,categorical=None):
    # If the input dataset is a dataframe,
    if type(dataset).__name__=='DataFrame': 
        # then we take out the values as a numpy array; so if the input dataset is a numpy array, just use it as is
        dataset=dataset.values 
    lenDataset=len(dataset)
    # Create an empty 2D numpy array, to be used as the distance matrix
    distance_matrix=np.zeros(lenDataset*lenDataset).reshape(lenDataset,lenDataset) 
    for i in range(lenDataset):
        for j in range(lenDataset):
            x1= dataset[i]
            x2= dataset[j]
            # Use mixed_distance() defined earlier to calculate distance between each pair of data points' continuous and categorical features,
            distance=mixed_distance(x1, x2,categorical=categorical) 
            # and then use calculated distance to populate the distance matrix,
            distance_matrix[i][j]=distance 
            distance_matrix[j][i]=distance 
    # and finally return the populated distance matrix
    return distance_matrix 

distance_matrix=dm_prototypes(df_array,categorical=[0, 1, 2, 3, 4, 5, 12, 13, 14])

# Create a dictionary called silhouette_scores to store values of K as keys, and corresponding silhouette scores as values
silhouette_scores = dict()

# For each value of K,
for k in tqdm(range(2,11), total = 9):
    # create an untrained K-Prototypes model using the KPrototypes() function and that specific value of K,
    untrained_model = kprototypes.KPrototypes(n_clusters=k,max_iter=20)
    # then train the K-Prototypes model using the input dataset (as a numpy array) and fit() function
    trained_model = untrained_model.fit(df_array, categorical=[0, 1, 2, 3, 4, 5, 12, 13, 14])
    # after training the model, for the given k, find the cluster labels for the data points using the .labels_ attribute of trained model
    cluster_labels = trained_model.labels_
    # silhouette_score() function takes the distance matrix as the 1st argument and cluster labels for the data points as the 2nd argument,
    # with the metric parameter set to "precomputed" to specify that we are passing the distance matrix as input, and NOT the entire dataframe,
    # to then calculate the average silhouette score for each K,
    score=silhouette_score(distance_matrix, cluster_labels,metric="precomputed")
    silhouette_scores[k]=score
    # and assign average silhouette score as a value to the current key of K in the dictionary

print(silhouette_scores)

plt.xlabel('Values of K') 
plt.ylabel('Average Silhouette Score') 
plt.title('Silhouette Method For Optimal k')
# Plot the data
plt.plot(silhouette_scores.keys(), silhouette_scores.values()) 
plt.scatter(silhouette_scores.keys(), silhouette_scores.values())
# Show the plot 
plt.show()

# From the given plot, the average silhouette score is maximised at K = 2, so the optimal K should be K = 2.

# IMPLEMENTING THE K-PROTOTYPES ALGORITHM USING THE OPTIMAL K = 2
# Create an untrained K-Prototypes model using the KPrototypes() function and the optimal K = 2,
segmentation_model = kprototypes.KPrototypes(n_clusters = 2, max_iter = 20, random_state = 42)
# Train the K-Prototypes model using the input dataset (as a numpy array) and fit_predict() function
segmentation_model.fit_predict(df_array, categorical=[0, 1, 2, 3, 4, 5, 12, 13, 14])
# Add a new column for cluster labels associated with each row (data point)
dataframe['cluster_labels_of_data_point'] = segmentation_model.labels_
# To visualise the clustered multidimensional data WITHOUT PCA/t-SNE (TO BE CONTINUED) (NEED TO FIGURE OUT HOW)