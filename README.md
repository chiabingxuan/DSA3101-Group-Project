# DSA3101 Project: Optimising the NUS Bus System

- [DSA3101 Project: Optimising the NUS Bus System](#dsa3101-project-optimising-the-nus-bus-system)
  - [1. Introduction](#1-introduction)
  - [2. Business Understanding](#2-business-understanding)
  - [3. Data Understanding](#3-data-understanding)
    - [3.1 Data Acquisition](#31-data-acquisition)
    - [3.2 Data Dictionary of Original Survey Data](#32-data-dictionary-of-original-survey-data)
    - [3.3 Data Quality Assessment](#33-data-quality-assessment)
  - [4. Data Preparation](#4-data-preparation)
    - [4.1 Initial Data Cleaning](#41-initial-data-cleaning)
    - [4.2 Initial Data Exploration](#42-initial-data-exploration)
  - [5. Modeling](#5-modeling)
    - [5.1 Algorithms Considered](#51-algorithms-considered)
    - [5.2 Algorithm Selection Criteria](#52-algorithm-selection-criteria)
      - [5.2.1. Relevance](#521-relevance)
      - [5.2.2 Adaptability](#522-adaptability)
      - [5.2.3 Value-add](#523-value-add)
    - [5.3 Detailed Description of Chosen Algorithm](#53-detailed-description-of-chosen-algorithm)
      - [5.3.1. Bus Stop Prioritization and Sorting Algorithm](#531-bus-stop-prioritization-and-sorting-algorithm)
      - [5.3.2 User Customization Algorithm](#532-user-customization-algorithm)
  - [6. Evaluation](#6-evaluation)
    - [6.1 Limitations of current approaches](#61-limitations-of-current-approaches)
      - [6.1.1 Limitations of Bus Stop Prioritzation and Sorting Algorithm](#611-limitations-of-bus-stop-prioritzation-and-sorting-algorithm)
      - [6.1.2 Limitations of User Customization Algorithm](#612-limitations-of-user-customization-algorithm)
    - [6.2 Suggestions for model improvements](#62-suggestions-for-model-improvements)
      - [6.2.1 Improvements for Bus Stop Prioritzation and Sorting Algorithm](#621-improvements-for-bus-stop-prioritzation-and-sorting-algorithm)
      - [6.2.2 Improvements for User Customization Algorithm](#622-improvements-for-user-customization-algorithm)
  - [7. Deployment](#7-deployment)
  - [8. Technical Implementation](#8-technical-implementation)
    - [8.1 Repository Structure](#81-repository-structure)
    - [Repository Structure](#repository-structure)
    - [8.2 Setup Instructions](#82-setup-instructions)
    - [8.3 Dependency Management](#83-dependency-management)
    - [8.4 Code Style Guide Adherence](#84-code-style-guide-adherence)
  - [9. Analytical Findings](#9-analytical-findings)
  - [10. Recommendations](#10-recommendations)
  - [11. Future Work](#11-future-work)
  - [12. Lessons Learned](#12-lessons-learned)
  - [13. References](#13-references)
  - [14. Appendices](#14-appendices)

## 1. Introduction

## 2. Business Understanding

## 3. Data Understanding

### 3.1 Data Acquisition

We collected survey data to investigate the travel patterns and satisfaction levels of NUS students, with regards to the NUS bus system. In our survey, respondents were asked to share **two bus trips** that they embarked on for the day. The [survey link](https://docs.google.com/forms/d/1zh5M9Sccn3ifxcOOJd2UMj7cQSFKPWmvD-RG1PZA9QM/edit) was circulated online on various NUS platforms, including the official Telegram channel for the NUS College of Humanities and Sciences.

### 3.2 Data Dictionary of Original Survey Data

From our survey, we are able to obtain tabular data in the form of a CSV file, `survey.csv`. Each row of the CSV file corresponds to a single survey response (two bus trips). In `survey_cleaning.py`, we load the CSV file into a `pandas.DataFrame`, `survey_data`. The data dictionary for `survey_data` is shown below. Given that the column names are rather long, a short description of each attribute is provided instead. Note that all attributes are required.

| Description of Attribute | Data Type |
| :---: | :---: |
| Year of study | object |
| Major | object |
| Is the respondent staying on campus? | object |
| Main reason for taking the school bus | object |
| Number of times the respondent takes the school bus per day  | object |
| Duration spent riding the school bus per day (in minutes) | object |
| Date | object |
| Does the respondent have an exam that day? | object |
| Trip 1: Starting bus stop | object |
| Trip 1: Ending bus stop | object |
| Trip 1: Bus number | object |
| Trip 1: Time of day | object |
| Trip 1: Weather | object |
| Trip 1: Number of people at starting bus stop | int64 |
| Trip 1: Waiting time (in minutes) | object |
| Trip 1: Satisfaction level for waiting time | int64 |
| Trip 1: Crowdedness level | int64 |
| Trip 1: Satisfaction level for crowdedness | int64 |
| Trip 1: Comfort level | int64 |
| Trip 1: Safety level | int64 |
| Trip 1: Overall satisfaction level | int64 |
| Trip 2: Starting bus stop | object |
| Trip 2: Ending bus stop | object |
| Trip 2: Bus number | object |
| Trip 2: Time of day | object |
| Trip 2: Weather | object |
| Trip 2: Number of people at starting bus stop | object |
| Trip 2: Waiting time (in minutes) | object |
| Trip 2: Satisfaction level for waiting time | int64 |
| Trip 2: Crowdedness level | int64 |
| Trip 2: Satisfaction level for crowdedness | int64 |
| Trip 2: Comfort level | int64 |
| Trip 2: Safety level | int64 |
| Trip 2: Overall satisfaction level | int64 |
| Other factors influencing satisfaction level | object |

### 3.3 Data Quality Assessment
We first refer to the `survey_cleaning.py` file. To begin, the `reshape()` function is called. This function takes in `survey_data` as an input and returns two `pandas.DataFrame`s as output - `trip_data` and `other_feedback_data`. Each row of `trip_data` corresponds to a single NUS bus trip, while each row of `other_feedback_data` corresponds to open-ended comments that a given respondent has made, pertaining to the NUS bus system. Consequently, the number of rows of `trip_data` is twice that of `other_feedback_data`.

In the `clean_trip_data()` and `clean_other_feedback_data()` functions that are subsequently called, the columns of `trip_data` and `other_feedback_data` are renamed for conciseness.

The data dictionaries for `trip_data` and `other_feedback_data` are as follows:

**trip_data:**
| Attribute | Data Type | Description of Attribute |
| :---: | :---: | :---: |
| year | object | Year of study |
| major | object | Major |
| on_campus | object | Is the respondent staying on campus? |
| main_reason_for_taking_isb | object | Main reason for taking the school bus |
| trips_per_day  | object | Number of times the respondent takes the school bus per day |
| duration_per_day | object | Duration spent riding the school bus per day (in minutes) |
| date | object | Date |
| has_exam | object | Does the respondent have an exam that day? |
| start | object | Starting bus stop |
| end | object | Ending bus stop |
| bus_num | object | Bus number |
| time | object | Time of day |
| weather | object | Weather |
| num_people_at_bus_stop | object | Number of people at starting bus stop |
| waiting_time | object | Waiting time (in minutes) |
| waiting_time_satisfaction | int64 | Satisfaction level for waiting time |
| crowdedness | int64 | Crowdedness level |
| crowdedness_satisfaction | int64 | Satisfaction level for crowdedness |
| comfort | int64 | Comfort level |
| safety | int64 | Safety level |
| overall_satisfaction | int64 | Overall satisfaction level |

**other_feedback_data:**
| Attribute | Data Type | Description of Attribute |
| :---: | :---: | :---: |
| year | object | Year of study |
| major | object | Major |
| on_campus | object | Is the respondent staying on campus? |
| main_reason_for_taking_isb | object | Main reason for taking the school bus |
| trips_per_day | object | Number of times the respondent takes the school bus per day |
| duration_per_day | object | Duration spent riding the school bus per day (in minutes) |
| date | object | Date |
| has_exam | object | Does the respondent have an exam that day? |
| feedback | object | Other factors influencing satisfaction level |

From the above, there are some numerical attributes which are being assigned the `object` data type instead, such as `num_people_at_bus_stop` for `trip_data`. This means that there are some problematic survey inputs for these attributes, which `pandas` cannot convert to the `int64` data type. Hence, some data type conversion has to be done.

By calling `clean_trip_data()` on `trip_data`, we also discovered the following issues, with regards to data quality:

* `trips_per_day`: 2 entries that do not correspond exactly to an integer (eg. "2-3 times")
* `duration_per_day`: 24 entries that do not correspond exactly to an integer (eg. "15mins")
* `num_people_at_bus_stop`: 2 entries that do not correspond exactly to an integer (eg. "40-50")
* `waiting_time`: 4 entries that do not correspond exactly to an integer (eg. "5min")
* `time`: 16 entries which fall outside of NUS bus operating hours (eg. 1:00:00 am, might have mistakenly entered "am" instead of "pm")
* `major`: Inconsistent formatting (eg. "Data Science and Analytics" can be entered as "dsa", "DSA", "Dsa", etc.)

By calling `clean_other_feedback_data()` on `other_feedback_data`, we discovered the following issues, with regards to data quality:

* `trips_per_day`: 1 entries that do not correspond exactly to an integer
* `duration_per_day`: 12 entries that do not correspond exactly to an integer
* `major`: Inconsistent formatting

Note also that since all fields of the survey are required, there are no missing values in both `trip_data` and `other_feedback_data`. In addition, the data is taken directly from our survey results, so there are no duplicate rows in both data frames.

## 4. Data Preparation
### 4.1 Initial Data Cleaning
With this in mind, we proceed to clean both `trip_data` and `other_feedback_data` in `survey_cleaning.py`.

By calling `clean_trip_data()` on `trip_data`, we do the following:
* Rename all columns (as mentioned in 3.3: Data Quality Assessment)
* Trim whitespace for the 6 columns that require this (`major`, `main_reason_for_taking_isb`, `trips_per_day`, `duration_per_day`, `num_people_at_bus_stop` and `waiting_time`)
* Convert `trips_per_day`, `duration_per_day`, `num_people_at_bus_stop` and `waiting_time` columns to `int64` data type
  * For the 32 entries that do not correspond exactly to an integer, we only keep the first integer that appears (eg. if the entry is "15-20 minutes", we only keep "15"). Then, we convert this modified entry to `int64`
* Correct invalid times in the `time` column, converting them from "AM" to "PM" (or vice versa) where necessary
  * Modified 16 entries
* Use a `MAPPINGS` dictionary to standardise the formatting of the `major` column
  * Modified 498 entries
* Remove rows corresponding to invalid bus trips
  * Removed 1 row where `start` and `end` are the same
  * Removed 43 rows where `bus_num` is not serviced in either `start` or `end`

By calling `clean_other_feedback_data()` on `other_feedback_data`, we do the following:
* Rename all columns
* Trim whitespace for the 5 columns that require this (`major`, `main_reason_for_taking_isb`, `trips_per_day`, `duration_per_day` and `feedback`)
* Convert `trips_per_day` and `duration_per_day` columns to `int64` data type
  * For the 13 entries that do not correspond exactly to an integer, we only keep the first integer that appears. Then, we convert this modified entry to `int64`
* Use a `MAPPINGS` dictionary to standardise the formatting of the `major` column
  * Modified 249 entries

### 4.2 Initial Data Exploration
After this first round of data cleaning, we now create visualisations to better understand the distributions of values for each attribute. Consider the common attributes for `trip_data` and `other_feedback_data`. Note that the distribution of each of these attributes is similar for both `pandas.DataFrames`. Hence, it suffices to investigate the distributions of attributes for `trip_data`.

In `survey_cleaning.py`, by calling `visualise_data()` on `trip_data`, we obtain the following insights:
* `year`: The counts of both "Year 5" and "Masters/PhD" are very low (both less than 15), compared to the other years of study (all greater than 100)
  * We choose to remove these rows as outliers, by calling `remove_outliers()`
* `major`: An overwhelming number of rows corresponds to "data science and analytics"
  * Hence, our data is skewed with respect to `major` - synthetic data generation is needed to conduct oversampling on the minority majors
* `main_reason_for_taking_isb`: An overwhelming number of rows corresponds to "To go to class" (greater than 400)
* `trips_per_day`: There are some rows with unusually large values for this attribute (ie. more than 20)
  * We choose to remove these rows as outliers, by calling `remove_outliers()`
* `bus_num`: There are no rows corresponding to bus E
  * Hence, we choose to exclude bus E from our analysis
* `num_people_at_bus_stop`: There are some rows with unusually large values for this attribute (ie. more than 80)
  * We choose to remove these rows as outliers, by calling `remove_outliers()`
  * While there are some other values that the box plot classifies as outliers (eg. 60), we choose not to remove these rows. This is because it is genuinely possible for there to be that many people at a single bus stop (eg. on the day of an exam)
* `waiting_time`: While there some values that the box plot classifies as outliers (eg. 25 min), we choose not to remove these rows. This is because it is genuinely possible for the waiting time to be that long (eg. when one misses a few buses in a row, due to the crowd size)

With this information, we call `remove_outliers()` on both `trip_data` and `other_feedback_data` to remove the aforementioned outliers.

For `trip_data`:
* 12 outliers removed for `year`
* 2 outliers removed for `trips_per_day`
* 4 outliers removed for `num_people_at_bus_stop`

For `other_feedback_data`:
* 6 outliers removed for `year`
* 1 outlier removed for `trips_per_day`

## 5. Modeling  

**Subgroup A: User Behavior and Satisfaction**
**How can we segment our users based on their travel behavior and preferences?**
* Develop a user segmentation model using the collected data
* Identify unique needs and pain points for each user segment

### 5.1 Modelling Technqiues Considered
* K-Means, K-Modes, and K-Prototypes were the 3 main modelling techniques considered at first.

### 5.2 Model Selection Criteria
* The main criterion considered was whether or not the model is applicable to our dataset.
* K-Means was NOT chosen because it is a clustering model applicable to datasets containing only continuous (numerical) features.
* K-Modes was NOT chosen because it is a clustering model applicable to datasets containing only categorical features.
* Since our dataset contains a mix of continuous and categorical features, K-Prototypes is the chosen model. This is because
K-Prototypes is a hybrid of K-Means and K-Modes that is designed for clustering data with both continuous and categorical features. 
* For continuous (numerical) features, K-Means uses the squared Euclidean distance as a measure of how similar 2 data points are, with smaller distances indicating higher similarity.
* For categorical featues, K-Modes uses a simple matching dissimilarity measure which counts the number of categories that do not match between 2 data points. 
* K-Prototypes combines both of the above into a dissimilarity measure that gives a comprehensive indication of similarity across both continuous (numerical) and categorical features.

### 5.3 Detailed Description of the Chosen Model
#### Dimensionality Reduction
* Dimensionality reduction should always be done before clustering. This is because clustering generally depends on some sort of distance measure. 
* Points near each other are in the same cluster; points far apart are in different clusters. 
* But in high dimensional spaces, distance measures do not work very well. 
* We reduce the number of dimensions first so that our distance metric in clustering will make sense.

#### Algorithmic Dimensionality Reduction
* ALGORITHMIC DIMENSIONALITY REDUCTION METHODS WERE CONSIDERED, BUT REJECTED FOR THE FOLLOWING REASON.
* PCA: inappropriate because it also applies to datasets comprising solely continuous(numerical) data, whereas our dataset comprises categorical data as well. 
* One-hot encoding the categorical variables, and then applying the PCA algorithm over the resulting data, DOES NOT WORK AS WELL. This is because the weight given to a categorical variable would inherently depend on the number of modalities available to the variable, and on the probabilities of these modalities. As a result, it would be impossible to give a similar weight to all the initial variables over the calculated components.
* Factor Analysis of Mixed Data (FAMD): appropriate for our mixed (categorical + continuous) dataset. This is because FAMD wants to give the exact same weight to all the variables, continuous or categorical, when searching for the principal components. So, Python libraries, such as "light_famd" and "prince" implementing FAMD were tried and tested, BUT did not work out due to compatibility issues with our data frame.
* MOREOVER, FAMD ultimately still increases our data's number of features beyond 16 with one-hot encoding, worsening the Curse of Dimensionality.

#### Manual Dimensionality Reduction Using Domain Knowledge
* As standard practice, we replace all inf values with NaN, and remove all NaN values.
* Firstly, we remove the '1900-01-01' from all rows of the 'time' column since it is redundant.
* Secondly, we combine the 'date' and 'time' columns into a new 'datetime' columnm, convert this 'datetime' column into datetime type,
extract the hour of the day (0-24) from the 'datetime' column and put this into a new 'hour' column.
* Thirdly, we extract the day of the week (Monday-Sunday) from the 'date' column and put this into a new 'day_of_week' column.
* Fourthly, we combine the 'start', 'end', and 'bus_num' columns into a new 'trip' column.
* Fifth, we combine the 'duration_per_day' and 'trips_per_day' columns into a new 'duration_per_trip' column by dividing the 2 columns, indicating the extent of usage of the ISB. However, this introduces inf values into the dataset, so once again, we replace all inf values with NaN, and remove all NaN values, to deal with this issue.
* Lastly, we remove the following columns for various reasons:
  * 'date','time','datetime' columns since they are replaced by 'day_of_week' and 'hour' columns
  * start','end','bus_num' columns since they are replaced by 'trip' column
  * duration_per_day', 'trips_per_day' columns since they are replaced by 'duration_per_trip' column
  * 'waiting_time_satisfaction', 'crowdedness_satsifaction' columns since the relationship is rather obvious: higher waiting time and higher crowdedness level = lower corresponding satisfaction
* After the above process, the number of featurs is effectively reduced from 21 to 16.

#### Modelling Process
* We convert the continuous variable columns into "float" type, and categorical variable columns into "str" type.
* We also employ the normalisation technique of Min-Max Scaling so that the scale of continuous data is rescaled/changed to fall between 0 and 1, while preserving the original shape/distribution of continuous data with no distortion. This is because ML algorithms tend to perform better, or converge faster, when the different features are on a smaller scale. Standardisation is NOT chosen as the scaling method here because we DO NOT KNOW FOR SURE that our continuous data follows a normal distribution.
* Firstly, we create an untrained K-Prototypes model using the KPrototypes() function and the optimal K = 3.
* Secondly, we train the K-Prototypes model using the input TRAINING dataset (as a numpy array) and fit_predict() function.
* Thirdly, with respect to the input dataset, we add a new column for cluster labels associated with each row (data point), as procured by fit_predict(), and accessed using the .labels_ attribute of the trained K-Prototypes model.
* Fourthly, we proceed to use a custom-defined cluster_profile() function to visualise the 3 clusters.
* cluster_profile() groups the input dataframe by the clusters, using the cluster labels outputted by the K-Prototypes model earlier.Subsequently, for each cluster, cluster_profile() proceeds to compute the mean of each continuous/numerical column, and identify the mode (most frequently-occurring category) of each categorical column.
* Lastly, we simply call print(cluster_profile(name_of_our_dataset)) to visualise the 3 clusters.
* (TO BE CONTINUED)

### 5.4 Model Performance Metrics and Interpretation
#### Elbow Method to Find the Optimal K (Number of Clusters)
* It involves running the K-Prototypes clustering model for different values of K, calculating the total cluster variance for each K using the cost_ attribute.
* "Total Cluster Variance" is essentially equivalent to the intra(within)-cluster variance, which we seek to minimize, and at the same time,
maximize the inter(between)-cluster variance since total variance is constant. Ideally, this will ensure a clear distinction between
the clusters, indicating good performance of the clustering model.
* The key is to identify the "elbow" point on the plot, where the rate of decrease in total cluster variance sharply changes, and total cluster variance becomes almost constant.
* This elbow point signifies a balance between capturing variance in the data and avoiding unnecessary complexity, and is the most appropriate K for the given dataset.
* Firstly, we extract the values of the dataframe and store them in a numpy array.
* Then, we create a dictionary to store values of K as keys, and corresponding total cluster variances as values.
* Subsequently, for each value of K, we create an untrained K-Prototypes model using the KPrototypes() function and that specific value of K, then train the K-Prototypes model using the input dataset (as a numpy array) and fit() function. After training the model, we find the total cluster variance for the given K using the .cost_ attribute of trained model, and assign total cluster variance as a value to the current key of K in the dictionary.
* Finally, we use the dictionary's keys (K values), and values (total cluster variances) to construct the Elbow plot.
* The "elbow point" is supposed to be the point on the plot where the total cluster variance starts to decrease at a much slower rate.
* From the given plot, it seems that the optimal K = 3, BUT the "elbow point" is not so clear and sharp.
* This is because the Elbow Method often fails to give a specific value for the optimal K if the input dataset has abnormal distribution.

#### Silhouette Method to Find the Optimal K (Number of Clusters)
* The SILHOUETTE METHOD IS USED TO COMPLEMENT THE ELBOW METHOD
* The silhouette value measures how similar a point is to its own cluster (cohesion) compared to other clusters (separation).
* The "Average Silhouette Score" for a dataset lies between -1 and 1.
* A high Average Silhouette Score (closer to 1) indicates that the data points are well-matched to their own clusters and poorly matched to neighboring clusters.
* So, a high Average Silhouette Score == appropriate clustering configuration.
* A low Average Silhouette Score (closer to -1) == inappropriate clustering configuration with too many or too few clusters.
* A clustering with an Average Silhouette Score of over 0.7 == "strong"; of over 0.5 == "reasonable"; of over 0.25 == "weak"
* However, with increasing dimensionality of the data, it becomes difficult to achieve such high values because of the Curse of Dimensionality, as the distances become more similar.
* Firstly, we use a custom-defined mixed_distance() function to calculate the distance between 2 data points having mixed categorical and continuous features. It does so by using the matching_dissim() function to calculate the distance between 2 data points' categorical features, and using the euclidean_dissim() function to calculate the distance between 2 data points' continuous features, and finally returning the sum of the 2 distances calculated.
* Secondly, we use a custom-defined dm_prototypes() function to calculate the distance matrix to be used for K-Prototypes clustering later on, which in turn makes use of the mixed_distance() function we defined earlier.
* Then, we create a dictionary to store values of K as keys, and corresponding average silhouette scores as values.
* Subsequently, for each value of K, we create an untrained K-Prototypes model using the KPrototypes() function and that specific value of K, then train the K-Prototypes model using the input dataset (as a numpy array) and fit() function. After training the model, we find the cluster labels for the data points using the .labels_ attribute of trained model.
* The silhouette_score() function proceeds to take the distance matrix computed earlier using dm_prototypes() as the 1st argument, and cluster labels for the data points as the 2nd argument, with the metric parameter set to "precomputed" to specify that we are passing the distance matrix as input, and NOT the entire dataframe, to eventually calculate the average silhouette score for each K, and assign average silhouette score as a value to the current key of K in the dictionary
* Finally, we use the dictionary's keys (K values), and values (average silhouette scores) to construct the Silhoeutte plot.
* From the given plot, the Average Silhouette Score is maximised at K = 2, so the optimal K should be 2 based on the Silhouette Method
* However, from the Elbow Method, the "elbow point" is located at K = 3
* On top of that, the difference in Average Silhouette Score between K = 2 (0.03958666420217967) and K = 3 (0.03291258008340998) is relatively small, and K = 3 yields the 2nd-highest Average Silhouette Score
* So, it seems REASONABLE/ACCEPTABLE that the COMPROMISE BETWEEN the ELBOW AND SILHOUETTE METHODS would be to TAKE OPTIMAL K = 3.

#### K-Prototypes Model Interpretation
* (TO BE CONTINUED)

**Subgroup B: System Optimization and Forecasting**  
**What changes to routes and schedules would optimize the public transport network?**
* Create an algorithm to optimize route planning based on predicted demand and user preferences.

### 5.1 Algorithms Considered
* The 1st approach we considered was to model the roads and bus stops as edges and vertices. We will then assign weights to the edges and proceed to use Single Source Shortest Path Algorithms, such as Dijkstra's Algorithm to find the shortest path between the bus stops. The shortest paths will then be the optimized routes.
* The 2nd approach we considered was to use the current routes, but optimize the order of bus stops each bus visits. The idea is to organize bus stops according to their importance at different times and conditions. This entails assigning priority scores to certain bus stops under different scenarios and sorting the bus stops to produce the optimized order of visit.

### 5.2 Algorithm Selection Criteria
#### 5.2.1. Relevance
  * 1st Approach:  
    Shortest Path algorithm is effective at finding the shortest path, but it primarily focuses on minimizing travel distances between stops, not passenger preferences or demand. It does not factor in bus stop popularity or times when specific stops are likely to see higher demand.
  * 2nd Approach:  
    By prioritizing stops based on demand and user preferences, this approach is explicitly designed to optimize according to passenger needs. The priority scoring accounts for fluctuating demand across days, times, and events, allowing routes to adapt based on who needs the service and when. This makes it more responsive to actual user preferences and system demand.
  * Conclusion:  
    The 2nd approach aligns better with the goal of responding to passenger needs which directly addresses the issue at hand.

#### 5.2.2 Adaptability
  * 1st Approach:  
    Shortest Path algorithm require predefined road networks and do not adapt well to temporal factors like day, hour, or special events, since they treat the network as a static entity. While real-time adjustments could theoretically be added, they would require substantial computational resources and frequent recalculations.
  * 2nd Approach:  
    This approach allows the system to adjust routes dynamically based on predefined priority scores under varying conditions. Since each bus stop’s priority can shift according to time-based demand and satisfaction data, the model naturally adapts without requiring computationally intensive recalculations.
  * Conclusion:  
    The 2nd approach ismore flexible and adaptable to varying demand, making it a more practical choice for a dynamic transportation network.
  
#### 5.2.3 Value-add
  * 1st Approach:  
    The current bus routes are already optimized by transportation professionals to follow the shortest or most efficient paths possible, rendering a new shortest-path calculation unnecessary. Implementing Dijkstra’s or similar algorithms would likely replicate existing routes without providing added benefit, making this approach redundant for the current setup.
  * 2nd Approach:  
    Since this approach is not aimed at finding new paths but rather optimizes the order of stops based on historical demand and user preferences, it adds value by focusing on enhancing passenger satisfaction and operational efficiency. By reorganizing stops rather than recalculating routes, this approach complements the pre-established routes without duplicating existing efforts.
  * Conclusion:  
    The redundancy of recalculating shortest paths reinforces that the 2nd approach, which prioritizes stops based on demand brings more added benefits.

### 5.3 Detailed Description of Chosen Algorithm
#### 5.3.1. Bus Stop Prioritization and Sorting Algorithm  
  * Initialize the MinMaxScaler:  
    `scaler = MinMaxScaler()`  
    Sets up a MinMaxScaler, which is used to normalize numerical columns by scaling values to a range, typically [0, 1].

  * Define the Normalization Function:  
    `normalize_group(group)` is defined to normalize specific columns in each group.  
    Within the function:  
    The columns `num_people_at_bus_stop` and `overall_satisfaction` are normalized to bring their values to a common scale.  
    Categorical columns like `weather` and `has_exam` are excluded from normalization.

  * Initialize an Empty Dictionary:  
    `bus_route_priorities = {}` creates a dictionary to store prioritized bus stop orders for different conditions.

  * Iterate through Each Bus:  
    A loop iterates over each unique bus number in the dataset `unique_bus_numbers`.  
    For each bus, a DataFrame `bus_df` is created, containing data specific to that bus.

  * Loop through Each Day of the Week:  
    For each bus, another loop iterates through each unique day of the week.  
    A new DataFrame `bus_day_df` is created for the bus data on that specific day.

  * Loop through Each Hour of the Day:  
    Within each day, a loop iterates over each unique hour.  
    A new DataFrame `bus_hour_df` is created for data during that hour.

  * Loop through Each Weather Condition:  
    For each hour, a loop iterates over unique weather conditions.  
    A new DataFrame `bus_weather_df` is created to contain data for that specific weather condition.

  * Loop through Each Exam Status:  
    Within each weather condition, a loop iterates over the unique values for `has_exam` (where 0 and 1 stands for having exam and not having exam respectively).  
    A new DataFrame `bus_exam_df` is created for each exam status scenario.

  * Normalize the Data by Bus Stop:  
    The data is copied to a new DataFrame `df_hour` to avoid altering the original.  
    The normalize_group function is applied group-wise for each starting bus stop within the filtered data `df_hour`.  
    `df_hour_normalized` stores the normalized DataFrame by bus stop.

  * Calculate Priority Scores by Bus Stop:  
    The normalized data is grouped by starting bus stop to calculate the average values for `num_people_at_bus_stop` and `overall_satisfaction`.  
    A `priority_score` column is created, calculated as the sum of normalized `num_people_at_bus_stop` and normalized `overall_satisfaction` values.  
    Normalization here ensures that `priority_score` reflects both demand and satisfaction equally, making the prioritization system fairer and more reliable across different bus stops and conditions.

  * Sort Bus Stops by Priority Score:  
    The bus stops are sorted in descending order based on `priority_score`.  
    `average_stats_by_start_sorted` holds the sorted list of bus stops for the current scenario.

  * Store the Sorted Priority in a Dictionary:  
    For each combination of bus number, day, hour, weather, and exam status, the sorted bus stop priority is stored in the dictionary `bus_route_priorities`.  

  * Sort the Dictionary:  
    The dictionary is sorted based on the tuple keys (bus number, day of the week, hour, weather, and exam status).  
    The result is stored in `sorted_bus_route_priorities`.

  * Print the Sorted Priorities:  
    A loop prints out the priority order of bus stops for each bus, day, hour, weather, and exam condition, showing the optimal order of bus stops per scenario.  

  * Summary:  
    The above algorithm is designed to optimize bus stop prioritization based on survey data, taking into account factors like demand (number of people at the bus stop), user satisfaction, time of day, day of the week, weather conditions, and whether there’s an exam. By creating priority scores for each bus stop, it identifies the most important stops under specific conditions.

#### 5.3.2 User Customization Algorithm   
  * Dictionary Initialization:  
    `days_of_week`, `time_ranges`, `weather_conditions`, and `exam_statuses` are dictionaries used to map numerical or binary values to their descriptive labels (e.g., "Monday" for day 1, "Sunny" for weather 0, etc.).

  * Retrieve Unique Bus Numbers:  
    Extracts all unique bus numbers from the `sorted_bus_route_priorities` dictionary.  
    Displays these bus numbers for the user to choose from.

  * User Bus Number Selection:  
    Asks the user to select a bus number from the displayed options.  
    Sets `terminate_algorithm` to 0, used later to check if any invalid input is encountered, if so, algorithm should be stopped prematurely.

  * Check for Valid Bus Number:  
    If the selected bus number exists in `sorted_bus_route_priorities`, it continues to the next step. If not, an error is printed, and the process is terminated.

  * Display Days for Selected Bus:  
    Extracts and displays all unique days available for the chosen bus number.  
    Asks the user to select a day and verifies if it is valid.

  * Display Hours for Selected Bus and Day:  
    If the day is valid, it retrieves and displays available hours for the selected bus and day.  
    Asks the user to pick an hour and verifies if it is valid.

  * Display Weather Conditions for Selected Bus, Day, and Hour:    
    If the hour is valid, it retrieves and displays weather conditions for the selected bus, day, and hour.    
    Asks the user to pick a weather condition and verifies if it is valid.

  * Display Exam Status for Selected Bus, Day, Hour, and Weather:  
    If the weather condition is valid, it retrieves and displays exam status options for the selected bus, day, hour, and weather.  
    Asks the user to pick an exam status and verifies if it is valid.

  * Retrieve and Display Final Bus Route:  
    If all inputs are valid, it constructs a `final_tuple` of the selected options (bus number, day, hour, weather, exam status).  
    Retrieves the priority order of bus stops for this specific tuple from `bus_route_priorities`.

  * Organize Final Routes:  
    Separates prioritized stops from the complete list of stops (`all_routes` for the selected bus).  
    Combines prioritized stops with non-prioritized stops to form the `final_routes`, which places higher-priority stops first.

  * Display User Selection and Bus Stop Order:  
    Displays the selected bus settings (bus number, day, time, weather, exam status) for the user’s confirmation.  
    Prints out:  
    The priority order of bus stops based on the calculated priority score.  
    The final optimized order of bus stops, which first includes priority stops followed by remaining stops.

  * Summary:  
    The above algorithm uses the output of 5.3.1 Bus Stop Prioritization and Sorting Algorithm and enables personalized bus route prioritization by allowing users to select criteria such as bus number, day, time, weather, and exam status. It validates each input, retrieves priority stops based on user demand and satisfaction, and outputs an optimized order of bus stops, ensuring efficient and tailored service.

**How can we better allocate capacity across different routes and times to meet varying demand?**

## 6. Evaluation
### 6.1 Limitations of current approaches  
#### 6.1.1 Limitations of Bus Stop Prioritzation and Sorting Algorithm  
    * Over-simplification:  
      The calculation of `priority_score` using only two factors (number of people and user satisfaction) might not capture other important variables, such as bus stop accessibility, operational constraints, etc.  
    * Scalability:  
      The nested loops iterating over buses, days, hours, weather conditions, and exam statuses can lead to a combinatorial explosion, making the algorithm inefficient with large datasets or when many unique combinations exist.  
    * Lack of Real-time Updates:  
      The algorithm might not be very apt at incorporating real-time changes, such as sudden shifts in demand or changes in weather, which can affect bus stop prioritization. Outdated data can lead to suboptimal prioritization

#### 6.1.2 Limitations of User Customization Algorithm  
    * User Input Validity:  
      The algorithm depends on users making correct selections. If users misunderstand the options or input invalid choices (even if they are checked), it can lead to frustration and a poor user experience.  
    * Limited Customizations:  
      Although the algorithm allows for some user customization, it may not cover all potential user preferences and scenarios, limiting its practicaly and user experience.

### 6.2 Suggestions for model improvements  
#### 6.2.1 Improvements for Bus Stop Prioritzation and Sorting Algorithm  
    * Addressing Over-simplication:  
      Incorporate additional factors into the `priority_score`, such as bus stop accessibility ratings, operational constraints, etc. This could provide a more comprehensive view of each bus stop's importance.  
    * Addressing Scalability:  
      Implement optimization techniques such as memoization or heuristics to reduce the number of calculations needed by avoiding redundant computations.  
    * Addressing Lack of Real-time Updates:  
      Develop a mechanism to dynamically adjust priorities based on real-time information, such as changes in demand or environmental conditions.

#### 6.2.2 Improvements for User Customization Algorithm  
    * Addressing User Input Validity:     
    Design a more intuitive user interface with clear instructions and tooltips to guide users in making their selections correctly.  
    * Addressing Limited Customizations:  
      Allow users to specify additional criteria for customization and even scenarios that are not covered by our current survey data.

## 7. Deployment

## 8. Technical Implementation
### 8.1 Repository Structure
### Repository Structure

```plaintext
├── data/                                     # Dataset files and resources for analysis
│   └── cleaned_other_feedback_data.csv       # Preprocessed feedback data for analysis
│   └── cleaned_trip_data.csv                 # Preprocessed trip data for synthesis and analysis
│   └── combined_trip_data.csv                # Combined train and test synthetic trip data for modeling
│   └── filtered_nus_weekday.csv              # NOT IN USE
│   └── sdv_metadata.json                     # Metadata configuration for SDV
│   └── singapore_aug24_data.csv              # NOT IN USE
│   └── survey.csv                            # Original survey data 
│   └── syn_metadata.json                     # Metadata conifguration for comparing test and train set
│   └── test_trip_data_after_sdv.csv          # Test data after SDV
│   └── test_trip_data_before_sdv.csv         # Test data before SDV
│   └── train_trip_data_after_sdv.csv         # Train data after SDV and SMOTE-NC
│   └── train_trip_data_after_smote.csv       # Train data affter SMOTE-NC
├── src/                                      # Source code for data analysis, cleaning and modeling
│   ├── analyse_travel_patterns.py            # Analysis of travel patterns from trip data
│   ├── capacity_allocation.py                # Allocates transport capacity based on demand
│   ├── config.py                             # Configuration settings
│   ├── demand_forecasting.py                 # Forecasts demand using trip data
│   ├── main.py                               # Main script to execute all files
│   ├── Route_Optimization.py                 # Optimizes travel routes based on trip data
│   ├── smote.py                              # Applies SMOTE-NC to balance 'major' class
│   ├── survey_cleaning.py                    # Cleans and preprocesses survey data
│   ├── synthetic_data_generation_test.py     # Generates synthetic data using SDV for test dataset
│   ├── synthetic_data_generation_train.py    # Generates synthetic data using SDV for train dataset after SMOTE-NC
│   ├── train_vs_test.py                      # Compares training and test datasets
│   ├── User_Segmentation_Model.py            # Segments users based on trip data
├── visualisations/                           # Visual output files generated by scripts
│   └── nus_heat_map_timelapse.html           # Heat map of crowd levels at respective bus stops across time
│   └── nus_heat_map.html                     # Heat map of crowd levels
├── .gitignore                                # Specifies files and directories to ignore in git
├── README.md                                 # Overview, setup, and usage instructions for the project
└── requirements.txt                          # List of all libraries required to run the scripts
```

### 8.2 Setup Instructions
To set up the project on a local machine, follow the steps:
* If you do not have Git installed, visit [Git website](https://git-scm.com/downloads) for instructions on installation. Once installed, you can check by running 
  * ```git --version ```
* Clone the repository via SSH or HTTPS
  * `git clone git@github.com:chiabingxuan/DSA3101-Group-Project.git` or
  * `git clone https://github.com/chiabingxuan/DSA3101-Group-Project.git`
### 8.3 Dependency Management
Dependencies are managed in requirements.txt. follow the step below:
* Install libraries required
  * `pip install -r requirements.txt`
### 8.4 Code Style Guide Adherence
Code style PEP 8 have been adapted for this project
## 9. Analytical Findings

## 10. Recommendations

## 11. Future Work
11.1 Additional research areas in the future  
  * 11.1.1 Simulation and Modeling for Optimal Routing 
    * Use computer simulations to test and optimise various route and scheduling configurations under different conditions.   
      * Discrete Event Simulation (DES):                                                                                                                                                     
        Using DES like SimPy, helps to focus on key events, like shuttles arriving at or departing from stops, to understand the impact on waiting times and bus crowdedness. This is useful for simulating peak periods and assessing the crowdedness at stops.
        
## 12. Lessons Learned

## 13. References

## 14. Appendices
