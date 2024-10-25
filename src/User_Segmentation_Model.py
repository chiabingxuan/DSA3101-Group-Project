#Importing all necessary libraries
import numpy as np
import pandas as pd
import math
from kmodes.kprototypes import KPrototypes
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score
from kmodes.kmodes import KModes
from kmodes import kprototypes

#Importing the testing data set (AFTER SMOTE-NC and SDV) as a Pandas dataframe
dataframe = pd.read_csv('C:/Users/65905/Downloads/DSA3101-Group-Project/data/train_trip_data.csv', encoding='utf-8')

dataframe = dataframe.replace([np.inf, -np.inf], np.nan)

dataframe = dataframe.dropna()

#Remove the '1900-01-01' from all rows of the 'time' column since it is redundant
dataframe['time'] = dataframe['time'].str.replace('1900-01-01', '')

#Combine the 'date' and 'time' columns into a new 'datetime' column
dataframe['datetime'] = dataframe['date'] + ' ' + dataframe['time']

#Convert the 'datetime' column into datetime type
dataframe['datetime'] = pd.to_datetime(dataframe['datetime']) 

#Extract the day of the week (Monday-Sunday) from the 'date' column and puts this into a new 'day_of_week' column
dataframe['day_of_week'] = dataframe['datetime'].dt.day_name()

#Extract the hour of the day (0-24) from the 'datetime' column and puts this into a new 'hour' column
dataframe['hour'] = dataframe['datetime'].dt.hour

#Combine the 'start', 'end', and 'bus_num' columns into a new 'trip' column
dataframe['trip'] = dataframe['start'] + ' ' + dataframe['end'] + ' ' + dataframe['bus_num']

#Combine the 'duration_per_day' and 'trips_per_day' columns into a new 'duration_per_trip' column indicating extent of usage of ISB
dataframe['duration_per_day'] = dataframe['duration_per_day'].astype(float)
dataframe['trips_per_day'] = dataframe['trips_per_day'].astype(float)
dataframe['duration_per_trip'] = dataframe['duration_per_day'] / dataframe['trips_per_day']

#This returns False at first, so no NaN values introduced in 'duration_per_trip'
print(dataframe['duration_per_trip'].isnull().any())

#This returns True at first, so there ARE inf values introduced in 'duration_per_trip'
print(np.isinf(dataframe['duration_per_trip']).any())

dataframe = dataframe.replace([np.inf, -np.inf], np.nan) #Replace all inf values with NaN
dataframe = dataframe.dropna() #Remove all NaN values

#Now, this should return False
print(np.isinf(dataframe['duration_per_trip']).any())

#Remove the following columns for various reasons
#'date','time','datetime' columns since they are replaced by 'day_of_week' and 'hour' columns
#'start','end','bus_num' columns since they are replaced by 'trip' column
#'duration_per_day', 'trips_per_day' columns since they are replaced by 'duration_per_trip' column
#'waiting_time_satisfaction', 'crowdedness_satsifaction' columns since the relationship is rather obvious
#higher waiting time and higher crowdedness level = lower corresponding satisfaction
dataframe = dataframe.drop(['date', 'time','datetime','datetime','start','end','bus_num','duration_per_day','trips_per_day',
                            'waiting_time_satisfaction','crowdedness_satisfaction'], axis = 'columns')

continuous_variable_columns = ["num_people_at_bus_stop", "waiting_time", "crowdedness", "comfort", "safety", "overall_satisfaction", "duration_per_trip"]
categorical_variable_columns = ["year", "major", "on_campus", "main_reason_for_taking_isb", "has_exam", "weather", "day_of_week", "hour", "trip"]

#Standardising ALL CONTINUOUS VARIABLE COLUMNS of "float" type
#Traditionally, clustering algorithms go with standardisation because of the freedom in bounds.
#When you are clustering, you want your clusters to be able to cover any sort of bounds, including those yet to be seen.
#So, normalisation is NOT chosen as the scaling method used since it imposes bounds of 0-100.
dataframe[continuous_variable_columns] = dataframe[continuous_variable_columns].apply(lambda x: (x - x.mean()) / np.std(x))

#Convert the continuous variable columns into "float" type
dataframe[continuous_variable_columns] = dataframe[continuous_variable_columns].astype(float)

#Conver the categorical variable columns into "str" type
dataframe[categorical_variable_columns] = dataframe[categorical_variable_columns].astype(str)

#Dimensionality reduction should always be done before clustering.
#This is because clustering generally depends on some sort of distance measure. 
#Points near each other are in the same cluster; points far apart are in different clusters. 
#But in high dimensional spaces, distance measures do not work very well. 
#You reduce the number of dimensions first so that your distance metric in clustering will make sense.


#Chosen model for segmenting users based on travel behavior and preferences: K-prototype clustering.
#K-prototype is a hybrid of K-means and K-modes that is designed for clustering data with both categorical and continuous features. 
#K-means uses euclidean distance between continuous features
#K-modes uses dissimilarity between categorical features
#K-prototype uses a dissimilarity measure that combines both of the above.

#Elbow Method for Finding the Optimal K = Number of Clusters
#It involves running the K-prototypes clustering model for different values of K, calculating the total cluster variance for each K using the cost_ attribute.
#The key is to identify the "elbow" point on the plot, where the rate of decrease in total cluster variance sharply changes,
#and total cluster variance becomes almost constant.
#This elbow point signifies a balance between capturing variance in the data and avoiding unnecessary complexity, and is the most appropriate K for the given dataset.
cost = []
for num_clusters in list(range(1,20)):
    kproto = KPrototypes(n_clusters=num_clusters)
    kproto.fit_predict(dataframe, categorical=[0, 1, 2, 3, 4, 5, 12, 13, 14])
    cost.append(kproto.cost_)

plt.xlabel('Values of K') 
plt.ylabel('Total Cluster Variance') 
plt.title('Elbow Method For Optimal k')
plt.plot(cost) #Plot the data
plt.show() #Show the plot

#From the given plot, it seems that the optimal K = 7, BUT it is not too clear as the "elbow point" is not so clear and sharp.
#In such an ambiguous case, the Silhouette Method is used to COMPLEMENT the Elbow Method.
#The silhouette value measures how similar a point is to its own cluster (cohesion) compared to other clusters (separation).
#The range of the Silhouette value is between +1 and -1. \
#A high value is desirable and indicates that the point is placed in the correct cluster. 
#If many points have a negative Silhouette value, it may indicate that we have created too many or too few clusters.
def mixed_distance(a,b,categorical=None, alpha=0.01):
    if categorical is None:
        num_score=kprototypes.euclidean_dissim(a,b)
        return num_score
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
        cat_score=kprototypes.matching_dissim(a_cat,b_cat)
        num_score=kprototypes.euclidean_dissim(a_num,b_num)
        return cat_score+num_score*alpha

def dm_prototypes(dataset,categorical=None,alpha=0.1):
    #if the input dataset is a dataframe, we take out the values as a numpy. 
    #If the input dataset is a numpy array, we use it as is.
    if type(dataset).__name__=='DataFrame':
        dataset=dataset.values    
    lenDataset=len(dataset)
    distance_matrix=np.zeros(lenDataset*lenDataset).reshape(lenDataset,lenDataset)
    for i in range(lenDataset):
        for j in range(lenDataset):
            x1= dataset[i]
            x2= dataset[j]
            distance=mixed_distance(x1, x2,categorical=categorical,alpha=alpha)
            distance_matrix[i][j]=distance
            distance_matrix[j][i]=distance
    return distance_matrix

silhouette_scores = []
distance_matrix=dm_prototypes(dataframe,categorical=[0, 1, 2, 3, 4, 5, 12, 13, 14],alpha=0.1)

for k in list(range(2,20)): #dissimilarity is undefined for a single cluster, thus, minimum number of clusters should be 2
    untrained_model = kprototypes.KPrototypes(n_clusters=k,max_iter=20)
    trained_model = untrained_model.fit(dataframe, categorical=[0, 1, 2, 3, 4, 5, 12, 13, 14])
    cluster_labels = trained_model.labels_
    score=silhouette_score(distance_matrix, cluster_labels,metric="precomputed")
    silhouette_scores.append(score)

plt.xlabel('Values of K') 
plt.ylabel('Silhouette Scores') 
plt.title('Silhouette Method For Optimal k')
plt.plot(silhouette_scores) #Plot the data
plt.show() #Show the plot












