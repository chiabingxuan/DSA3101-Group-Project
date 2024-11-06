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
    - [4.3 Synthetic Data Generation](#43-synthetic-data-generation)
  - [5. Subgroup A: User Behavior and Satisfaction](#5-subgroup-a-user-behavior-and-satisfaction)
    - [5.1 Key Factors Influencing User Satisfaction](#51-key-factors-influencing-user-satisfaction)
    - [5.2 User Segmentation](#52-user-segmentation)
      - [5.2.1 Models Considered](#521-models-considered)
      - [5.2.2 Model Selection Critieria](#522-model-selection-critieria)
        - [5.2.2.1 Relevance](#5221-relevance)
      - [5.2.3 Detailed Description of the Chosen Model](#523-detailed-description-of-the-chosen-model)
        - [5.2.3.1 Dimensionality Reduction](#5231-dimensionality-reduction)
        - [5.2.3.2 Manual Dimensionality Reduction Using Domain Knowledge](#5232-manual-dimensionality-reduction-using-domain-knowledge)
        - [5.2.3.3 Modelling Process](#5233-modelling-process)
      - [5.2.4 Model Performance Metrics and Interpretation](#524-model-performance-metrics-and-interpretation)
        - [5.2.4.1 Elbow Method to Find Optimal K (Number of Clusters)](#5241-elbow-method-to-find-optimal-k-number-of-clusters)
        - [5.2.4.2 Silhouette Method to Find the Optimal K (Number of Clusters)](#5242-silhouette-method-to-find-the-optimal-k-number-of-clusters)
        - [5.2.4.3 K-Prototypes Model Interpretation](#5243-k-prototypes-model-interpretation)
    - [5.3 Analysing Travel Patterns](#53-analysing-travel-patterns)
      - [5.3.1 Creating Tableau Visualisations](#531-creating-tableau-visualisations)
        - [5.3.1.1 General Peak Hours](#5311-general-peak-hours)
        - [5.3.1.2 Individual Bus Services](#5312-individual-bus-services)
        - [5.3.1.3 Day of Week](#5313-day-of-week)
        - [5.3.1.4 Exam Period](#5314-exam-period)
      - [5.3.2 Creating Origin-Destination Matrix](#532-creating-origin-destination-matrix)
      - [5.3.3 Creating Timelapses](#533-creating-timelapses)
        - [5.3.3.1 Overall Fluctuations in Ridership](#5331-overall-fluctuations-in-ridership)
        - [5.3.3.2 Popular Trips Throughout the Day](#5332-popular-trips-throughout-the-day)
        - [5.3.3.3 Popular Trips Across User Segments](#5333-popular-trips-across-user-segments)
    - [5.3.4 Opportunities for Service Improvements](#534-opportunities-for-service-improvements)
    - [5.4 Evaluation](#54-evaluation)
      - [5.4.1 Evaluation of model performance against business objectives](#541-evaluation-of-model-performance-against-business-objectives)
      - [5.4.2 Limitations of Current Approach](#542-limitations-of-current-approach)
      - [5.4.3 Suggestions for Model Improvements](#543-suggestions-for-model-improvements)
  - [6 Subgroup B: System Optimization and Forecasting](#6-subgroup-b-system-optimization-and-forecasting)
    - [6.1 Demand Forecasting Model](#61-demand-forecasting-model)
      - [6.1.1 Models Considered](#611-models-considered)
      - [6.1.2 Model Selection Criteria](#612-model-selection-criteria)
      - [6.1.3 Detailed Description of Chosen Model(s)](#613-detailed-description-of-chosen-models)
      - [6.1.4 Model Performance Metrics and Interpretation](#614-model-performance-metrics-and-interpretation)
        - [6.1.4.1 Time Complexity:](#6141-time-complexity)
        - [6.1.4.2 Space Complexity:](#6142-space-complexity)
    - [6.2 Route Optimization](#62-route-optimization)
      - [6.2.1 Algorithms Considered](#621-algorithms-considered)
      - [6.2.2 Algorithm Selection Criteria](#622-algorithm-selection-criteria)
      - [6.2.3 Detailed Description of Chosen Algorithm](#623-detailed-description-of-chosen-algorithm)
        - [6.2.3.1 Bus Stop Prioritization and Sorting Algorithm](#6231-bus-stop-prioritization-and-sorting-algorithm)
        - [6.2.3.2 User Customization Algorithm](#6232-user-customization-algorithm)
        - [6.2.3.3 Impact Simulation Model](#6233-impact-simulation-model)
      - [6.2.4 Performance Metrics and Interpretation](#624-performance-metrics-and-interpretation)
        - [6.2.4.1 Bus Stop Prioritization and Sorting Algorithm](#6241-bus-stop-prioritization-and-sorting-algorithm)
        - [6.2.4.1.1 Time Complexity:](#62411-time-complexity)
        - [6.2.4.1.2 Space Complexity:](#62412-space-complexity)
        - [6.2.4.2 User Customization Algorithm](#6242-user-customization-algorithm)
        - [6.2.4.2.1 Time Complexity:](#62421-time-complexity)
        - [6.2.4.2.2 Space Complexity:](#62422-space-complexity)
        - [6.2.4.3 Impact Simulation Model](#6243-impact-simulation-model)
          - [6.2.4.3.1 Time Complexity:](#62431-time-complexity)
          - [6.2.4.3.2 Space Complexity:](#62432-space-complexity)
    - [6.3 Capacity Allocation Optimization Model](#63-capacity-allocation-optimization-model)
      - [6.3.1 Modeling Techinques Considered](#631-modeling-techinques-considered)
      - [6.3.2 Model Selection Criteria](#632-model-selection-criteria)
      - [6.3.3 Detailed Description of Chosen Model](#633-detailed-description-of-chosen-model)
      - [6.3.4 Performance Metrics and Interpretation](#634-performance-metrics-and-interpretation)
        - [6.3.4.1 Time Complexity: Explain](#6341-time-complexity-explain)
        - [6.3.4.2 Space Complexity: Explain](#6342-space-complexity-explain)
    - [6.4 Evaluation](#64-evaluation)
      - [6.4.1 Demand Forecasting Model](#641-demand-forecasting-model)
        - [6.4.1.1 Evaluation of model performance against business objectives](#6411-evaluation-of-model-performance-against-business-objectives)
        - [6.4.1.2 Limitations of Current Approach](#6412-limitations-of-current-approach)
        - [6.4.1.3 Suggestions for Model Improvements](#6413-suggestions-for-model-improvements)
      - [6.4.2 Route Optimization](#642-route-optimization)
        - [6.4.2.1 Bus Stop Prioritization and Sorting Algorithm, User Customization Algorithm](#6421-bus-stop-prioritization-and-sorting-algorithm-user-customization-algorithm)
          - [6.4.2.1.1 Evaluation of model performance against business objectives](#64211-evaluation-of-model-performance-against-business-objectives)
          - [6.4.2.1.2 Limitations of Current Approach](#64212-limitations-of-current-approach)
        - [6.4.2.1.3 Suggestions for Model Improvements](#64213-suggestions-for-model-improvements)
        - [6.4.2.2 Impact Simulation Model](#6422-impact-simulation-model)
          - [6.4.2.2.1 Evaluation of model performance against business objectives](#64221-evaluation-of-model-performance-against-business-objectives)
          - [6.4.2.2.2 Limitations of Current Approach](#64222-limitations-of-current-approach)
        - [6.4.2.2.3 Suggestions for Model Improvements](#64223-suggestions-for-model-improvements)
        - [6.4.2.3 Capcacity Allocation Optimization Model](#6423-capcacity-allocation-optimization-model)
          - [6.4.2.3.1 Evaluation of model performance against business objectives](#64231-evaluation-of-model-performance-against-business-objectives)
          - [6.4.2.3.2 Limitations of Current Approach](#64232-limitations-of-current-approach)
        - [6.4.2.3.3 Suggestions for Model Improvements](#64233-suggestions-for-model-improvements)
  - [7. Deployment](#7-deployment)
  - [8. Technical Implementation](#8-technical-implementation)
    - [8.1 Repository Structure](#81-repository-structure)
    - [Repository Structure](#repository-structure)
    - [8.2 Setup Instructions](#82-setup-instructions)
    - [8.3 Dependency Management](#83-dependency-management)
    - [8.4 Code Style Guide Adherence](#84-code-style-guide-adherence)
  - [9. Analytical Findings](#9-analytical-findings)
  - [10. Recommendations](#10-recommendations)
    - [Prioritized list of recommendations](#prioritized-list-of-recommendations)
    - [Implementation roadmap](#implementation-roadmap)
    - [Expected impact of each recommendations](#expected-impact-of-each-recommendations)
  - [11. Future Work](#11-future-work)
  - [12. Lessons Learned](#12-lessons-learned)
  - [13. References](#13-references)
  - [14. Appendices](#14-appendices)

## 1. Introduction

**Overview of Data Scavengers**
Data Scavengers is a collaborative project aimed at collecting real time data to optimise the bus system in NUS by utilising various models, such as Route Optimisation, Demand Forecasting and Capacity Allocation models. Visualisations have also been made to assist us in understanding the current problems faced.

**Project Objectives**

- Predict the demand of bus users at a specific bus stop at specific hour intervals
- Optimise the bus routes to reduce waiting times
- Allocate the capacity of buses to meet the demand

**Team Members**

- Bing Xuan -
- Chong Gui - Route Optimisations
- Yeongkyu -
- Wei Ting - User Segmentation
- Haidah -
- Beckham - SMOTE analysis
- Iffah - Capacity Allocation
- Rean -

**Quick Links**
???

## 2. Business Understanding

**Business Problem Statement**
How can NUS develop an efficient, reliable and safe internal bus system that optimally allocates resources to meet fluctuating demand, enhance student mobility and safety, and reduce operational costs?

**Business Problem**
The school's current internal transportation system faces challenges in meeting the varying demands of students commuting at different time periods, or during seasonal events. The existing resource allocation, which includes the routes and schedules may not adequately support peak times, such as the time periods between 1030 hrs to 1330 hrs, or periods like exams or campus events. Additionally, there are concerns about ensuring students' safety and comfort, and minimising the waiting times. Without an optimised and responsive transport system, students may experience delays, overcrowding, or safety concerns. In turn, impacting their academic performance, punctuality, as well as their overall campus experience.

**Key Stakeholders and their needs**
<u>Students</u>

- _Primary Users_: Students are the primary users of the bus system, and are our target focus. They rely heavily on the Internal Bus System, to commute between campus facilities, dorms, cafeterias to libraries and faculties. Their needs are focused around convenience, safety, punctuality and minimal wait times.
- _Specific Needs_: Reliable transport during peak times like class start/end times, during exams.

**Success Criteria for the project**

- _Enhance Student Mobility_: Ensure that students have access to a convenient and punctual transportation for commuting to campus and school facilities, supporting timely attendance and overall ease of movement
- _Improve Safety Standards_: Prioritise a safe environment for students while on their commute, ensuring the students' well-being.
- _Optimise Resource Allocation_: Efficient allocation of buses, schedules, and routes to balance operational costs with demand.
- _Provide Flexibility during Seasonal Events_: Adjust bus schedules and allocate additional buses during seasonal events, such as exams, to accomodate higher demand and ensure students reach the destinations punctually, as well as minimise the waiting time during post exams.

## 3. Data Understanding

### 3.1 Data Acquisition

We collected survey data to investigate the travel patterns and satisfaction levels of NUS students, with regards to the NUS bus system. In our survey, respondents were asked to share **two bus trips** that they embarked on for the day. The [survey link](https://docs.google.com/forms/d/1zh5M9Sccn3ifxcOOJd2UMj7cQSFKPWmvD-RG1PZA9QM/edit) was circulated online on various NUS platforms, including the official Telegram channel for the NUS College of Humanities and Sciences (CHS).

### 3.2 Data Dictionary of Original Survey Data

From our survey, we are able to obtain tabular data in the form of a CSV file, `survey.csv`. Each row of the CSV file corresponds to a single survey response (two bus trips). In `survey_cleaning.py`, we load the CSV file into a `pandas.DataFrame`, `survey_data`. The data dictionary for `survey_data` is shown below. Given that the column names are rather long, a short description of each attribute is provided instead. Note that all attributes are required.

|                  Description of Attribute                   | Data Type |
| :---------------------------------------------------------: | :-------: |
|                        Year of study                        |  object   |
|                            Major                            |  object   |
|            Is the respondent staying on campus?             |  object   |
|            Main reason for taking the school bus            |  object   |
| Number of times the respondent takes the school bus per day |  object   |
|  Duration spent riding the school bus per day (in minutes)  |  object   |
|                            Date                             |  object   |
|         Does the respondent have an exam that day?          |  object   |
|                  Trip 1: Starting bus stop                  |  object   |
|                   Trip 1: Ending bus stop                   |  object   |
|                     Trip 1: Bus number                      |  object   |
|                     Trip 1: Time of day                     |  object   |
|                       Trip 1: Weather                       |  object   |
|        Trip 1: Number of people at starting bus stop        |   int64   |
|              Trip 1: Waiting time (in minutes)              |  object   |
|         Trip 1: Satisfaction level for waiting time         |   int64   |
|                  Trip 1: Crowdedness level                  |   int64   |
|         Trip 1: Satisfaction level for crowdedness          |   int64   |
|                    Trip 1: Comfort level                    |   int64   |
|                    Trip 1: Safety level                     |   int64   |
|             Trip 1: Overall satisfaction level              |   int64   |
|                  Trip 2: Starting bus stop                  |  object   |
|                   Trip 2: Ending bus stop                   |  object   |
|                     Trip 2: Bus number                      |  object   |
|                     Trip 2: Time of day                     |  object   |
|                       Trip 2: Weather                       |  object   |
|        Trip 2: Number of people at starting bus stop        |  object   |
|              Trip 2: Waiting time (in minutes)              |  object   |
|         Trip 2: Satisfaction level for waiting time         |   int64   |
|                  Trip 2: Crowdedness level                  |   int64   |
|         Trip 2: Satisfaction level for crowdedness          |   int64   |
|                    Trip 2: Comfort level                    |   int64   |
|                    Trip 2: Safety level                     |   int64   |
|             Trip 2: Overall satisfaction level              |   int64   |
|        Other factors influencing satisfaction level         |  object   |

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
| trips_per_day | object | Number of times the respondent takes the school bus per day |
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

- `trips_per_day`: 2 entries that do not correspond exactly to an integer (eg. "2-3 times")
- `duration_per_day`: 24 entries that do not correspond exactly to an integer (eg. "15mins")
- `num_people_at_bus_stop`: 2 entries that do not correspond exactly to an integer (eg. "40-50")
- `waiting_time`: 4 entries that do not correspond exactly to an integer (eg. "5min")
- `time`: 16 entries which fall outside of NUS bus operating hours (eg. 1:00:00 am, might have mistakenly entered "am" instead of "pm")
- `major`: Inconsistent formatting (eg. "Data Science and Analytics" can be entered as "dsa", "DSA", "Dsa", etc.)

By calling `clean_other_feedback_data()` on `other_feedback_data`, we discovered the following issues, with regards to data quality:

- `trips_per_day`: 1 entries that do not correspond exactly to an integer
- `duration_per_day`: 12 entries that do not correspond exactly to an integer
- `major`: Inconsistent formatting

Note also that since all fields of the survey are required, there are no missing values in both `trip_data` and `other_feedback_data`. In addition, the data is taken directly from our survey results, so there are no duplicate rows in both data frames.

## 4. Data Preparation

### 4.1 Initial Data Cleaning

With this in mind, we proceed to clean both `trip_data` and `other_feedback_data` in `survey_cleaning.py`.

By calling `clean_trip_data()` on `trip_data`, we do the following:

- Rename all columns (as mentioned in 3.3: Data Quality Assessment)
- Trim whitespace for the 6 columns that require this (`major`, `main_reason_for_taking_isb`, `trips_per_day`, `duration_per_day`, `num_people_at_bus_stop` and `waiting_time`)
- Convert `trips_per_day`, `duration_per_day`, `num_people_at_bus_stop` and `waiting_time` columns to `int64` data type
  - For the 32 entries that do not correspond exactly to an integer, we only keep the first integer that appears (eg. if the entry is "15-20 minutes", we only keep "15"). Then, we convert this modified entry to `int64`
- Correct invalid times in the `time` column, converting them from "AM" to "PM" (or vice versa) where necessary
  - Modified 16 entries
- Use a `MAPPINGS` dictionary to standardise the formatting of the `major` column
  - Modified 498 entries
- Remove rows corresponding to invalid bus trips
  - Removed 1 row where `start` and `end` are the same
  - Removed 43 rows where `bus_num` is not serviced in either `start` or `end`

By calling `clean_other_feedback_data()` on `other_feedback_data`, we do the following:

- Rename all columns
- Trim whitespace for the 5 columns that require this (`major`, `main_reason_for_taking_isb`, `trips_per_day`, `duration_per_day` and `feedback`)
- Convert `trips_per_day` and `duration_per_day` columns to `int64` data type
  - For the 13 entries that do not correspond exactly to an integer, we only keep the first integer that appears. Then, we convert this modified entry to `int64`
- Use a `MAPPINGS` dictionary to standardise the formatting of the `major` column
  - Modified 249 entries

### 4.2 Initial Data Exploration

After this first round of data cleaning, we now create visualisations to better understand the distributions of values for each attribute. Consider the common attributes for `trip_data` and `other_feedback_data`. Note that the distribution of each of these attributes is similar for both `pandas.DataFrames`. Hence, it suffices to investigate the distributions of attributes for `trip_data`. All visualisations from this phase of data exploration can be found under `visualisations/initial_data_exploration/`.

In `survey_cleaning.py`, by calling `visualise_data()` on `trip_data`, we obtain the following insights:

- `year`: The counts of both "Year 5" and "Masters/PhD" are very low (both less than 15), compared to the other years of study (all greater than 100)
  - We choose to remove these rows as outliers, by calling `remove_outliers()`
- `major`: An overwhelming number of rows corresponds to "data science and analytics"
  - Hence, our data is skewed with respect to `major` - synthetic data generation is needed to conduct oversampling on the minority majors
- `main_reason_for_taking_isb`: An overwhelming number of rows corresponds to "To go to class" (greater than 400)
- `trips_per_day`: There are some rows with unusually large values for this attribute (ie. more than 20)
  - We choose to remove these rows as outliers, by calling `remove_outliers()`
- `bus_num`: There are no rows corresponding to bus E
  - Hence, we choose to exclude bus E from our analysis
- `num_people_at_bus_stop`: There are some rows with unusually large values for this attribute (ie. more than 80)
  - We choose to remove these rows as outliers, by calling `remove_outliers()`
  - While there are some other values that the box plot classifies as outliers (eg. 60), we choose not to remove these rows. This is because it is genuinely possible for there to be that many people at a single bus stop (eg. on the day of an exam)
- `waiting_time`: While there some values that the box plot classifies as outliers (eg. 25 min), we choose not to remove these rows. This is because it is genuinely possible for the waiting time to be that long (eg. when one misses a few buses in a row, due to the crowd size)

With this information, we call `remove_outliers()` on both `trip_data` and `other_feedback_data` to remove the aforementioned outliers.

For `trip_data`:

- 12 outliers removed for `year`
- 2 outliers removed for `trips_per_day`
- 4 outliers removed for `num_people_at_bus_stop`

For `other_feedback_data`:

- 6 outliers removed for `year`
- 1 outlier removed for `trips_per_day`

### 4.3 Synthetic Data Generation

In preparation for Modeling, a substantial amount of data is required for training machine learning models effectively, thus we will conduct the following synthetic data generation methods to augment our dataset.

1. We will perform a 80-20 train-test split to generate synthetic data for both the training and test sets separately to prevent data leakage.

2. Synthetic Minority Over-sampling Technique for Nominal and Continuous (SMOTE-NC)

   - We chose to use SMOTE-NC as it accomodates datasets containing both nominal and continuous variables, thus ideal for our dataset which contains both types of variables. In contrast, SMOTE can only handle continuous features.
   - Our dataset `cleaned_trip_data.csv` is imbalanced for the `major` variable, where the highest count in the training set is 95 for "data science and analytics" while lowest is 8 for "architecture" and "industrial systems engineering". Therefore we need to conduct over-sampling as mentioned in 4.2.
   - We will apply SMOTE-NC `smote.py` on the train set to balance the `major` variable, resulting in a balanced sample of 95 counts for each major in `major`.
   - The balanced sample dataset is saved as `train_trip_data_after_smote.csv`
   - Some important points to take note:
     - We combined `start`, `end`, `bus_num` into a single `trip` column. This approach prevents SMOTE-NC from individually generating synthetic data for each column, which may result in the case where the `start` and `end` being the same which is not logical for a person taking the bus.
     - We decomposed `date` and `time` into its numerical components: day, month, year, hour, and minute, so that it can be processed by SMOTE-NC as it cannot directly process datetime type values.

3. Synthetic Data Vault (SDV)

   - After `major` classes are balanced, we can proceed with using SDV to increase the size of our dataset.
   - We adopted the Gaussian Copula model to help us create realistic synthetic samples that are characteristically close to the original dataset.
   - We will apply SDV onto the train set after SMOTE-NC has been done `train_trip_data_after_smote.csv` and onto the test set `test_trip_data_before_sdv.csv`
   - Overall train dataset: `train_trip_data_after_sdv.csv`
   - Overall test dataset: `test_trip_data_after_sdv.csv`

4. Further notes
   - We did not implement SMOTE-NC onto the test dataset as after the 80-20 train-test split, it resulted in some majors in `major` column having less than 5 counts. This prevents us from oversampling the test dataset to balance the majors as the model parameter was set to `k_neighbors = 5` for the train set. Decreasing the `k_neighbors` is not feasible as it may lead to overfitting.
   - Thus we only used SDV to generate synthetic data for test dataset, while both SMOTE-NC and SDV were used for train dataset.

## 5. Subgroup A: User Behavior and Satisfaction

- How can we segment our users based on their travel behavior and preferences?
- Develop a user segmentation model using the collected data
- Identify unique needs and pain points for each user segment

### 5.1 Key Factors Influencing User Satisfaction

### 5.2 User Segmentation

#### 5.2.1 Models Considered

- There are 3 main modelling techniques considered at first.
  - K-Means
  - K-Modes
  - K-Prototypes

#### 5.2.2 Model Selection Critieria

##### 5.2.2.1 Relevance

- K-Means was not chosen because it is a clustering model applicable to datasets containing only continuous (numerical) features.
- K-Modes was not chosen because it is a clustering model applicable to datasets containing only categorical features.
- Since our dataset contains a mix of continuous and categorical features, K-Prototypes is the chosen model. This is because K-Prototypes is a hybrid of K-Means and K-Modes that is designed for clustering data with both continuous and categorical features.
- For continuous (numerical) features, K-Means uses the squared Euclidean distance as a measure of how similar 2 data points are, with smaller distances indicating higher similarity.
- For categorical featues, K-Modes uses a simple matching dissimilarity measure which counts the number of categories that do not match between 2 data points.
- K-Prototypes combines both of the above into a dissimilarity measure that gives a comprehensive indication of similarity across both continuous (numerical) and categorical features.
- Algorithmic Dimensionality Reduction methods were considered, but rejected for the following reasons:
  - Principal Component Analysis (PCA): inappropriate because it applies to datasets comprising solely continuous(numerical) data, whereas our dataset comprises categorical data as well.
  - Encoding the categorical variables, and then applying the PCA algorithm over the resulting data, does not work as well.
  - This is because the weight given to a categorical variable would inherently depend on the number of modalities available to the variable, and on the probabilities of these modalities. As a result, it would be impossible to give a similar weight to all the initial variables over the calculated principal components.
  - Factor Analysis of Mixed Data (FAMD): appropriate for our mixed (categorical + continuous) dataset. This is because FAMD wants to give the exact same weight to all the variables, continuous or categorical, when searching for the principal components.
  - However, Python libraries, such as `light_famd` and `prince` implementing FAMD were tried and tested, but did not work out due to compatibility issues with our data frame, and lack of updates.
  - Moreover, FAMD ultimately still increases our data's number of features beyond 16 with encoding, worsening the Curse of Dimensionality, which defeats the original purpose of dimensionality reduction.

#### 5.2.3 Detailed Description of the Chosen Model

##### 5.2.3.1 Dimensionality Reduction

- Dimensionality reduction should always be done before clustering. This is because clustering generally depends on some sort of distance measure.
- Points near each other are in the same cluster; points far apart are in different clusters.
- But in high dimensional spaces, distance measures do not work very well.
- We reduce the number of dimensions first so that our distance metric in clustering will make sense.

##### 5.2.3.2 Manual Dimensionality Reduction Using Domain Knowledge

- As standard practice, we replace all inf values with NaN, and remove all NaN values, to ensure inf and NaN values do not interfere with the code.
- Firstly, we remove the '1900-01-01' from all rows of the `time` column since it is redundant.
- Secondly, we combine the `date` and `time` columns into a new `datetime` columnm, convert this `datetime` column into the datetime type, extract the hour of the day (0-24) from the `datetime` column and put this into a new `hour` column.
- Thirdly, we extract the day of the week (Monday-Sunday) from the `date` column and put this into a new `day_of_week` column.
- Fourthly, we combine the `start`, `end`, and `bus_num` columns into a new `trip` column.
- Fifth, we combine the `duration_per_day` and `trips_per_day` columns into a new `duration_per_trip` column by dividing the 2 columns, indicating the extent of usage of the ISB. However, this introduces inf values into the dataset, so once again, we replace all inf values with NaN, and remove all NaN values, to deal with this issue.
- Lastly, we remove the following columns for various reasons:
  - `date`,`time`,`datetime` columns since they are replaced by `day_of_week` and `hour` columns
  - `start`,`end`,`bus_num` columns since they are replaced by `trip` column
  - `duration_per_day`, `trips_per_day` columns since they are replaced by `duration_per_trip` column
  - `waiting_time_satisfaction`, `crowdedness_satsifaction` columns since the relationship is rather obvious: higher waiting time and higher crowdedness level = lower corresponding satisfaction
- After the above process, the number of features is effectively reduced from 21 to 16.

##### 5.2.3.3 Modelling Process

- We convert the continuous variable columns into `float` type, and categorical variable columns into `str` type.
- We also employ the normalisation technique of Min-Max Scaling so that the scale of continuous data is rescaled/changed to fall between 0 and 1, while preserving the original shape/distribution of continuous data with no distortion. This is because Machine Learning (ML) algorithms tend to perform better, or converge faster, when the different features are on a smaller scale. Standardisation is not chosen as the scaling method here because we do not know for sure that our continuous data follows a normal distribution.
- Firstly, we create an untrained K-Prototypes model using the `KPrototypes()` function and the optimal K = 3.
- Secondly, we train the K-Prototypes model using the input training dataset (as a numpy array) and `fit_predict()` function.
- Thirdly, with respect to the input dataset, we add a new column for cluster labels associated with each row (data point), as procured by `fit_predict()`, and accessed using the `.labels_` attribute of the trained K-Prototypes model.
- Fourthly, we proceed to use a custom-defined `cluster_profile()` function to visualise the 3 clusters.
- `cluster_profile()` groups the input dataframe by the clusters, using the cluster labels outputted by the K-Prototypes model earlier.
  Subsequently, for each cluster, `cluster_profile()` proceeds to compute the median of each continuous/numerical column, and identify the mode (most frequently-occurring category) of each categorical column.
- Here, the median is the preferred measure of central tendency because it is less affected by outliers than the mean, and
  also because we do not know for sure that our continuous data is symmetrical or normally distributed- so the mean is not as appropriate here.
- Lastly, we simply call `print(cluster_profile(name_of_our_dataset))` to visualise the 3 clusters.

#### 5.2.4 Model Performance Metrics and Interpretation

##### 5.2.4.1 Elbow Method to Find Optimal K (Number of Clusters)

- It involves running the K-Prototypes clustering model for different values of K, calculating the total cluster variance for each K using the `.cost_` attribute.
- "Total Cluster Variance" is essentially equivalent to the intra(within)-cluster variance, which we seek to minimize, and at the same time, maximize the inter(between)-cluster variance since total variance is constant. Ideally, this will ensure a clear distinction between the clusters, indicating good performance of the clustering model.
- The key is to identify the "elbow" point on the plot, where the rate of decrease in total cluster variance sharply changes, and total cluster variance becomes almost constant.
- This elbow point signifies a balance between capturing variance in the data and avoiding unnecessary complexity, and is the most appropriate K for the given dataset.
- Firstly, we extract the values of the dataframe and store them in a numpy array.
- Then, we create a dictionary to store values of K as keys, and corresponding total cluster variances as values.
- Subsequently, for each value of K, we create an untrained K-Prototypes model using the `KPrototypes()` function and that specific value of K, then train the K-Prototypes model using the input dataset (as a numpy array) and `fit()` function. After training the model, we find the total cluster variance for the given K using the `.cost_` attribute of trained model, and assign total cluster variance as a value to the current key of K in the dictionary.
- Finally, we use the dictionary's keys (K values), and values (total cluster variances) to construct the Elbow plot.
- The "elbow point" is supposed to be the point on the plot where the total cluster variance starts to decrease at a much slower rate.
- From the given plot, it seems that the optimal K = 3, but the "elbow point" is not so clear and sharp.
- This is because the Elbow Method often fails to give a specific value for the optimal K if the input dataset has abnormal distribution.

##### 5.2.4.2 Silhouette Method to Find the Optimal K (Number of Clusters)

- The Silhouette Method is used to complement the Elbow Method.
- The silhouette value measures how similar a point is to its own cluster (cohesion) compared to other clusters (separation).
- The "Average Silhouette Score" for a dataset lies between -1 and 1.
- A high Average Silhouette Score (closer to 1) indicates that the data points are well-matched to their own clusters and poorly matched to neighboring clusters.
- So, a high Average Silhouette Score == appropriate clustering configuration.
- A low Average Silhouette Score (closer to -1) == inappropriate clustering configuration with too many or too few clusters.
- A clustering with an Average Silhouette Score of over 0.7 == "strong"; of over 0.5 == "reasonable"; of over 0.25 == "weak"
- However, with increasing dimensionality of the data, it becomes difficult to achieve such high values because of the Curse of Dimensionality, as the distances become more similar.
- Firstly, we use a custom-defined `mixed_distance()` function to calculate the distance between 2 data points having mixed categorical and continuous features. It does so by using the `matching_dissim()` function to calculate the distance between 2 data points' categorical features, and using the `euclidean_dissim()` function to calculate the distance between 2 data points' continuous features, and finally returning the sum of the 2 distances calculated.
- Secondly, we use a custom-defined `dm_prototypes()` function to calculate the distance matrix to be used for K-Prototypes clustering later on, which in turn makes use of the `mixed_distance()` function we defined earlier.
- Then, we create a dictionary to store values of K as keys, and corresponding average silhouette scores as values.
- Subsequently, for each value of K, we create an untrained K-Prototypes model using the `KPrototypes()` function and that specific value of K, then train the K-Prototypes model using the input dataset (as a numpy array) and `fit()` function. After training the model, we find the cluster labels for the data points using the `.labels_` attribute of trained model.
- The `silhouette_score()` function proceeds to take the distance matrix computed earlier using `dm_prototypes()` as the 1st argument, and cluster labels for the data points as the 2nd argument, with the `metric` parameter set to "precomputed" to specify that we are passing the distance matrix as input, and not the entire dataframe, to eventually calculate the average silhouette score for each K, and assign average silhouette score as a value to the current key of K in the dictionary
- Finally, we use the dictionary's keys (K values), and values (average silhouette scores) to construct the Silhouette plot.
- From the given plot, the Average Silhouette Score is maximised at K = 2, so the optimal K should be 2 based on the Silhouette Method
- However, from the Elbow Method, the "elbow point" is located at K = 3
- On top of that, the difference in Average Silhouette Score between K = 2 (0.03958666420217967) and K = 3 (0.03291258008340998) is relatively small, and K = 3 yields the 2nd-highest Average Silhouette Score
- So, it seems reasonable/acceptable that the compromise between the Elbow and Silhouette methods would be to take optimal K = 3.

##### 5.2.4.3 K-Prototypes Model Interpretation

- Our K-Prototypes model procured 3 clusters.

- Cluster 0 has the following attributes.

|            Column            |                     Value                      |
| :--------------------------: | :--------------------------------------------: |
|             Year             |                       1                        |
|            Major             |             Biomedical Engineering             |
|          On_Campus           |                       No                       |
|  Main Reason for Taking ISB  |                 To go to Class                 |
|           Has Exam           |                       No                       |
|           Weather            |                     Sunny                      |
|         Day of Week          |                    Thursday                    |
|             Hour             |                       11                       |
|             Trip             | IT/CLB to Kent Ridge MRT/Opp Kent Ridge MRT A2 |
| Number of People at Bus Stop |                    0.314286                    |
|         Waiting Time         |                    0.300000                    |
|         Crowdedness          |                    0.666667                    |
|           Comfort            |                    0.333333                    |
|            Safety            |                    0.333333                    |
|     Overall Satisfaction     |                    0.333333                    |

- Cluster 1 has the following attributes.

|            Column            |                     Value                      |
| :--------------------------: | :--------------------------------------------: |
|             Year             |                       3                        |
|            Major             |                    Business                    |
|          On_Campus           |                       No                       |
|  Main Reason for Taking ISB  |                 To go to Class                 |
|           Has Exam           |                       No                       |
|           Weather            |                     Sunny                      |
|         Day of Week          |                    Thursday                    |
|             Hour             |                       13                       |
|             Trip             | Kent Ridge MRT/Opp Kent Ridge MRT to IT/CLB A1 |
| Number of People at Bus Stop |                    0.200000                    |
|         Waiting Time         |                    0.166667                    |
|         Crowdedness          |                    0.444444                    |
|           Comfort            |                    0.555556                    |
|            Safety            |                    0.666667                    |
|     Overall Satisfaction     |                    0.555556                    |

- Cluster 2 has the following attributes.

|            Column            |                     Value                      |
| :--------------------------: | :--------------------------------------------: |
|             Year             |                       2                        |
|            Major             |                   Chemistry                    |
|          On_Campus           |                       No                       |
|  Main Reason for Taking ISB  |                 To go to Class                 |
|           Has Exam           |                       No                       |
|           Weather            |                     Sunny                      |
|         Day of Week          |                    Thursday                    |
|             Hour             |                       12                       |
|             Trip             | IT/CLB to Kent Ridge MRT/Opp Kent Ridge MRT A2 |
| Number of People at Bus Stop |                    0.357143                    |
|         Waiting Time         |                    0.200000                    |
|         Crowdedness          |                    0.777778                    |
|           Comfort            |                    0.555556                    |
|            Safety            |                    0.666667                    |
|     Overall Satisfaction     |                    0.555556                    |

- Across the 3 clusters labelled 0, 1 and 2, we observe that they share certain similarities in the following aspects:

  - Do not stay on campus
  - Main reason for taking the ISB is to go to class
  - On the day of the bus trip chosen to input in the survey, there was no exam, it was a Thursday, and the weather was sunny.
  - So, perhaps the features of `on_campus`, `main_reason_for_taking_ISB`, `has_exam`, `day_of_week`, and `weather`, are not as useful
    for identifying each cluster's pain points and needs in this context.

- Between clusters 1 and 2, we observe that they have the exact same overall satisfaction level = 0.555556,
  safety level = 0.66667, and comfort level = 0.55556.

  - However, cluster 2 has a higher crowdedness level = 0.77778 compared to cluster 1 with a lower crowdedness level = 0.444444.
  - At the same time, cluster 2 has a longer waiting time = 0.200000 compared to cluster 1 with a shorter waiting time = 0.166667.
  - By intuition, cluster 2 should thus have a lower overall satisfaction level than cluster 1, but yet this is clearly not the case.
  - One possible reason is that for cluster 2, there exists other factors influencing overall satisfaction, that are even more
    important than crowdedness and waiting time- which could be the smell of the bus (whether or not the bus smells pleasant), and/or the attitude of the bus driver, amongst the many responses to our ending survey question: "Are there any other factors that influence how satisfied you are with the NUS bus system?" Perhaps, for cluster 2, most of them felt that the bus smelt pleasant during their bus trips, and/or most of them also were very pleased with the positive attitudes of the bus drivers, which in turn outweighed the more negative factors of higher crowdedness levels and longer waiting times (relative to cluster 1).

- Between clusters 0 and 1, we observe that:

  - Cluster 0 has a longer waiting time = 0.300000 compared to cluster 1 with a shorter waiting time = 0.166667.
  - Cluster 0 has a higher crowdedness level = 0.666667 compared to cluster 1 with a lower crowdedness level = 0.444444.
  - Cluster 0 has a lower comfort level = 0.333333 compared to cluster 1 with a higher comfort level = 0.555556.
  - Cluster 0 has a lower safety level = 0.333333 compared to cluster 1 with a higher safety level = 0.666667.
  - This reaffirms our initial beliefs on the relationship between the 4 factors and overall satisfaction, which is that a longer waiting time, higher crowdedness level, lower comfort level, and lower safety level, all translate to a lower overall satisfaction level. This is backed by cluster 0 having a lower overall satisfaction level = 0.333333, compared to cluster 1 with a higher overall satisfaction level = 0.555556.

- From the comparisons we drew between cluster 0 (year 1 students) and cluster 1 (year 3 students), there are 3 more possible insights that we can draw:

  - Firstly, since students in earlier years (cluster 0) exhibit lower overall satisfaction levels, this may reflect a steeper learning curve in navigating the campus and transportation systems, indicating that year 1 students might be struggling to adapt to both academic demands and logistical challenges simultaneously. In other words, this suggests an adjustment phase for year 1 students where they are not only acclimating to university life but also learning to navigate a potentially complex transportation network. This might indicate that the National University of Singapore (NUS) should consider mentorship programs or orientation sessions focusing on transportation logistics to help ease this transition.
  - Secondly, since cluster 1 (year 3 students) shows improved overall satisfaction levels compared to cluster 0 (year 1 students), this may suggest that as students progress from their first year to their third year, they likely become more familiar with the transportation system and class schedules, resulting in less anxiety and frustration during commutes.
  - Thirdly, cluster 1’s travel time at 1 PM coincides with post-lunch schedules, which may contribute to higher student energy levels and correspondingly, better ability to manage travel expectations while using the ISB, contributing to higher overall satisfaction levels. Conversely, earlier travel times at 11 AM in cluster 0 may lead to fatigue or a rush, influencing their overall experience negatively.

- Moreover, we note that despite cluster 2 (year 2 students) having the highest crowdedness level = 0.777778, it still has a moderate overall satisfaction level = 0.555556. This suggests that as students progress past their first year, it is relatively easy for most of them to be accustomed / desensitised to crowded conditions as they accept high crowd levels as the "norm". In turn, such a change in mindset is part of students internalising that usage of ISB services is a necessity (since most of them use the ISB to go to class, as indicated by how clusters 0, 1, and 2 all have the exact same `main_reason_for_taking_ISB` = to go to class). This desensitisation to crowded conditions might buffer the negative impact of crowdedness on overall satisfaction levels.

### 5.3 Analysing Travel Patterns

- Analyse and visualise travel patterns across different routes, times, and user segments.
- Identify opportunities for service improvements based on these patterns.

For the analysis of common bus travel patterns among students, we refer to Tableau visualisations under `visualisations/Dashboards/` and `analyse_travel_patterns.py`. Within `analyse_travel_patterns.py`, the `main()` functions from `origin_destination_matrix.py` and `make_timelapses_for_travel_patterns.py` are called, in that order.

#### 5.3.1 Creating Tableau Visualisations

We create [Tableau dashboards](https://chiabingxuan.github.io/DSA3101-Group-Project/) to visualise how travel patterns vary throughout the day. This is done by taking various scenarios into consideration - dashboard filters such as "Bus Number", "Starting Bus Stops", "Weather" and "Exam" are incorporated into our visualisations.

##### 5.3.1.1 General Peak Hours

From the graph, we note that **a typical day's rush hours range from 10 am to 2 pm**, where the number of trips remain consistently above 500. The number of bus trips **peaks at approximately 11 am** (679 trips), during the lunch break.

##### 5.3.1.2 Individual Bus Services

The usage of each bus service (A1, A2, D1, D2) also varies in a similar way throughout the day, with **D1 being much less utilised than the others**. This is most likely because D1 services fewer bus stops, and thus a smaller area of the campus.

In addition, each of the usages of A1, A2 and D1 **peaks at two separate time periods (11 am and 1 pm - 2 pm)**. Evidently, students have a greater need to commute from one place to another, both before and after their lunch.

In comparison, the ridership for bus service D2 **peaks at 11 am only** (240 trips). This could be accounted for by the fact that D2 services University Town (UTown), unlike A1 and A2:

- For students who commute to UTown right before the lunchtime period, they may be more inclined to stay there for longer periods of time, given that there is a wider variety of amenities (eg. Education Resource Centre) available in the area.
- Students may be travelling to UTown in order to access bus service 96, which goes to Clementi MRT Station - they have no intention of subsequently travelling to other bus stops within campus.

Hence, there is no notable peak in ridership for D2 in the early afternoon. Although D1 also services UTown, it is a significantly less popular bus service than D2 - figures associated with D1 should be treated with less weightage than other bus services.

##### 5.3.1.3 Day of Week

During the weekend (Saturday - Sunday), **peak hours occur later in the day, at around 1 pm** (62 trips). This is a rightwards shift in comparison to weekdays (Monday - Friday), when the **busiest hours range from 11 am - 12 pm** (at least 590 trips). This may be attributed to the differences in the purpose of travel, between weekdays and weekends. Unlike weekdays, schedules for weekends consist of fewer classes and more college activities for leisure, with events beginning later in the day. On Saturdays and Sundays, students travel on campus to attend these recreational activities, instead of going for classes. Consequently, they begin their commute closer to midday, pushing peak hours to around 1 pm.

##### 5.3.1.4 Exam Period

Consider the bus trips starting from Kent Ridge MRT / Opp Kent Ridge MRT. On days with no examinations, the number of these trips increases consistently from 7 am - 11 am (from 27 trips to 198 trips), whilst decreasing consistently from 11 am - 7 pm (from 198 trips to 9 trips). Contrastingly, the number of trips originating from Kent Ridge MRT / Opp Kent Ridge MRT sees **two additional sharp spikes throughout a typical examination day** - namely, **10 am** (29 trips) and **3 pm** (16 trips). These sudden jumps in ridership may stem from an increase in the number of students travelling to examination venues (ie. UHC / Opp UHC) for their morning and afternoon papers respectively.

#### 5.3.2 Creating Origin-Destination Matrix

In `origin_destination_matrix.py`, we create

#### 5.3.3 Creating Timelapses

In `make_timelapses_for_travel_patterns.py`, we use `folium` to create timelapses that outline the travel patterns over a 16 hour period (7 am - 11 pm). Here, for each timelapse, we also call the `filter_route_counts()` function in `filter_count.py` to obtain a CSV file that describes the most popular bus trips throughout the day. For example, for `nus_a1_trip_markers_timelapse.html`, `nus_a1_trip_markers_timelapse_popular_trips.csv` shows the most popular trips involving bus service A1 throughout the day. These CSV files can be found in `data/timelapse_popular_trips/`.

The following timelapses were created and saved under `visualisations/timelapses/`:

|                  File Name                  |                         Timelapse                          |
| :-----------------------------------------: | :--------------------------------------------------------: |
|      `nus_trip_markers_timelapse.html`      |                 Timelapse of all bus trips                 |
|   `nus_exam_trip_markers_timelapse.html`    |          Timelapse of all bus trips on a exam day          |
|  `nus_no_exam trip_markers_timelapse.html`  |        Timelapse of all bus trips on a non-exam day        |
|    `nus_a1_trip_markers_timelapse.html`     |      Timelapse of bus trips involving bus service A1       |
|    `nus_a2_trip_markers_timelapse.html`     |      Timelapse of bus trips involving bus service A2       |
|    `nus_d1_trip_markers_timelapse.html`     |      Timelapse of bus trips involving bus service D1       |
|    `nus_d2_trip_markers_timelapse.html`     |      Timelapse of bus trips involving bus service D2       |
| `nus_cluster_0_trip_markers_timelapse.html` | Timelapse of bus trips involving passengers from cluster 0 |
| `nus_cluster_1_trip_markers_timelapse.html` | Timelapse of bus trips involving passengers from cluster 1 |
| `nus_cluster_2_trip_markers_timelapse.html` | Timelapse of bus trips involving passengers from cluster 2 |

For each timelapse, the positions of all the bus stops are labelled in white text. Each trip corresponds to a single straight line. The line is coloured according to the bus service involved in the given trip (here, we use the standard colours found on the [official NUS website](https://uci.nus.edu.sg/oca/mobilityservices/getting-around-nus/), as specified in `config.py`). One end of this line coincides with the starting bus stop - represented by the green marker - while the other end matches up with the ending bus stop - this is indicated by the red marker. In addition, for timelapses illustrating individual bus services, the overall route of the given bus service is marked out using a strongly weighted `PolyLine`.

##### 5.3.3.1 Overall Fluctuations in Ridership

We take a preliminary look at the travel patterns, with reference to `nus_trip_markers_timelapse.html`. It can be seen that the number of lines drawn **remain consistently high from 10 am - 2 pm**, further supporting the conclusion drawn in Section 5.5.1. However, we look to delve deeper into more specific time periods for which the network of lines drawn is significantly dense. We sieve out a few time periods that are of note:

|     Time Period     |      Possible Reason       |
| :-----------------: | :------------------------: |
|  8.50 am - 9.10 am  |        9 am classes        |
| 9.30 am - 10.10 am  |       10 am classes        |
| 10.30 am - 11.10 am |       11 am classes        |
| 11.40 am - 12.10 pm | 12 pm classes + lunch hour |
| 12.40 pm - 1.10 pm  | 1 pm classes + lunch hour  |
|  1.30 pm - 1.40 pm  | 2 pm classes + lunch hour  |
|  2.00 pm - 2.10 pm  | 2 pm classes + lunch hour  |
|  2.30 pm - 3.10 pm  |        3 pm classes        |
|  3.30 pm - 4.30 pm  |     Afternoon classes      |

From these observations, we can tell that the number of students using the NUS bus system **spikes on an hourly basis**, especially **in the morning and early afternoon**. We deduce that this is due to the fact that classes at NUS occur at regular one-hour intervals. From our previous analyses, students mainly take the school bus to attend their classes - it is thus not surprising that the demand for bus services peaks every hour. However, this hourly trend is less apparent in the late afternoon. Furthermore, the number of trips is **significantly greater during the lunchtime period**, when students commute from their classrooms to bus stops that are near canteens and eateries.

##### 5.3.3.2 Popular Trips Throughout the Day

From `nus_trip_markers_timelapse.html`, the following are observed to be the **busiest bus stops**:

- Kent Ridge MRT / Opp Kent Ridge MRT
- UTown
- IT / CLB
- LT13 / Ventus
- COM3

Looking at the timelapses for individual bus services, we get a general idea of which bus trips are popular. With reference to `data/timelapse_popular_trips/`, we obtain the following list of the most frequent bus trips for each bus service, along with their corresponding time periods:

| Bus Service |                  Time Period                  |                Start                |                 End                 |
| :---------: | :-------------------------------------------: | :---------------------------------: | :---------------------------------: |
|     A1      | 1.30 pm, 2.40 pm - 2.50 pm, 3.30 pm - 3.50 pm | Kent Ridge MRT / Opp Kent Ridge MRT |              IT / CLB               |
|     A2      |                  2 pm, 3 pm                   | Kent Ridge MRT / Opp Kent Ridge MRT |            LT13 / Ventus            |
|     A2      |          10.40 am, 11.40 am, 2.40 pm          |              IT / CLB               | Kent Ridge MRT / Opp Kent Ridge MRT |
|     D1      |     11.30 am, 12.20 pm, 2.30 pm - 2.40 pm     |              IT / CLB               |                UTown                |
|     D1      |                   10.30 am                    |            LT13 / Ventus            |                UTown                |
|     D2      |              10.40 am, 11.50 am               | Kent Ridge MRT / Opp Kent Ridge MRT |                COM3                 |
|     D2      |             12.30 pm, 3 pm, 5 pm              |                COM3                 | Kent Ridge MRT / Opp Kent Ridge MRT |

From the above, we can see that **Kent Ridge MRT / Opp Kent Ridge MRT is a remarkable hotspot** for bus rides. For each bus service (A1, A2, D2) that services Kent Ridge MRT / Opp Kent Ridge MRT, this bus stop is consistently involved in the most popular trips. This is understandable, given that this bus stop crucially connects the NUS campus to Singapore's MRT network. Note that from the late morning to early afternoon, students are generally commuting from their classrooms (eg. **IT / CLB and COM3**) to places like **the MRT station and UTown**. This could be because there are more dining options available at these locations - students are therefore more inclined to travel there for their meals. Although trips to and from the MRT station are both common throughout the afternoon, there are **more trips pointing towards the MRT station in the evening** (eg. COM3 to Kent Ridge MRT / Opp Kent Ridge MRT at 5 pm). As their daily schedules come to a close, students are increasingly travelling to the MRT station, so as to head home.

##### 5.3.3.3 Popular Trips Across User Segments

The following are the trips that students from each cluster (0, 1 and 2) engage in the most:

| Cluster | Bus Service |        Time Period        |                Start                |                 End                 |
| :-----: | :---------: | :-----------------------: | :---------------------------------: | :---------------------------------: |
|    0    |     A1      | 1.30 pm, 3.50 pm, 4.50 pm | Kent Ridge MRT / Opp Kent Ridge MRT |              IT / CLB               |
|    0    |     A2      |     11.40 am, 3.50 pm     |              IT / CLB               | Kent Ridge MRT / Opp Kent Ridge MRT |
|    1    |     A1      |     2.30 pm, 3.30 pm      | Kent Ridge MRT / Opp Kent Ridge MRT |              IT / CLB               |
|    1    |     A2      |           2 pm            | Kent Ridge MRT / Opp Kent Ridge MRT |            LT13 / Ventus            |
|    1    |     A2      |          1.50 pm          | Kent Ridge MRT / Opp Kent Ridge MRT |          BIZ2 / Opp HSSML           |
|    1    |     D2      |         10.40 am          | Kent Ridge MRT / Opp Kent Ridge MRT |                COM3                 |
|    2    |     A2      |     12 pm, 2 pm, 3 pm     | Kent Ridge MRT / Opp Kent Ridge MRT |            LT13 / Ventus            |
|    2    |     A2      |     10.40 am, 2.40 pm     |              IT / CLB               | Kent Ridge MRT / Opp Kent Ridge MRT |

From this information, we can draw the following conclusions:

- Students from **cluster 0** tend to travel between **Kent Ridge MRT / Opp Kent Ridge MRT** and **IT / CLB**
  - From Section 5.2.4.3, we see that this cluster generally corresponds to newer students (ie. Year 1) who are studying Biomedical Engineering. Since IT / CLB is a short distance from College of Design and Engineering (CDE), it makes sense for this category of students to commute to and from this bus stop more frequently
- Students from **cluster 1** tend to travel from **Kent Ridge MRT / Opp Kent Ridge MRT** to bus stops like **LT13 / Ventus**, **BIZ2 / Opp HSSML** and **COM3**
  - Firstly, note that LT13 / Ventus is near to the Faculty of Arts and Social Sciences (FASS), BIZ2 / Opp HSSML is next to the NUS Business School, and COM3 is located within the School of Computing (SoC). All 3 schools are within close proximity of one another
  - From Section 5.2.4.3, we see that this cluster is generally composed of older students (ie. Year 3) who are studying Business courses. Upon arriving at Kent Ridge MRT, these students thus have a higher tendency to subsequently travel to the aforementioned bus stops for their classes
- Students from **cluster 2** tend to travel between **Kent Ridge MRT / Opp Kent Ridge MRT** to bus stops like **LT13 / Ventus** and **IT / CLB**
  - From Section 5.2.4.3, we see that this cluster generally consists of Year 2 students who are studying Chemistry courses. As Year 2 Science students, they are more likely to be reading courses associated with the College of Humanities and Sciences, of which a significant number take place at FASS. Hence, this group of students have a greater need to travel to LT13 / Ventus, which is one of the closer bus stops to FASS. Given that the Central Library is connected to FASS, it is possible that these students prefer to study there in between their classes. This would also explain why they favour travelling from IT / CLB to the MRT station.

### 5.3.4 Opportunities for Service Improvements

From the insights that we have gleaned, we propose the following service improvements to the NUS bus system:

- More school buses should service the campus from 10 am - 2 pm, which correspond to the general peak hours
- Moreover, we should ensure that more school buses service the campus at the turn of every hour (eg. 8.50 am - 9.10 am, 9.30 am - 10.10 am, etc.), to meet the demands of students travelling to and from class
- During weekdays:
  - For all bus services, the number of buses in operation should be gradually increased from 10 am - 11 am, which is when transport demand is expected to be the highest
  - For bus services A1, D1 and D2, it is especially imperative that we account for the heightened ridership during after-lunch hours, keeping the number of buses high from 1 pm - 2 pm
- During weekends:
  - For all bus services, the number of buses in operation should be gradually increased from 12 pm - 1 pm, which is when transport demand is expected to be the highest
- Note that UHC / Opp UHC is the closest bus stop to most examination venues. Hence during examination periods, we should increase the number of A1 and D2 buses travelling from Kent Ridge MRT to Opp UHC, as well as increase the number of A2 and D2 buses travelling from UHC to Opp Kent Ridge MRT. This increase in bus allocation should primarily take place from 9.30 am - 10.30 am (examinations in the morning) and from 2.30 pm - 3.30 pm (examinations in the afternoon)
- From the list of most frequent bus stops for each bus service, we propose a new bus service (**DS**):
  - Route: LT13 / Ventus ⟷ IT / CLB ⟷ UTown ⟷ Kent Ridge MRT / Opp Kent Ridge MRT ⟷ COM3 ⟷ LT13 / Ventus
  - Operating Hours: 10.30 am - 3.30 pm
  - Purpose: To not only accommodate some of the most popular trips identified, but also to increase the number of buses travelling to UTown and the MRT station during lunch hours. This thus relieves the pressure on other bus services. This bus route also has fewer stops compared to those of other bus services, allowing students to travel to their destinations more swiftly


### 5.4 Evaluation

#### 5.4.1 Evaluation of model performance against business objectives

#### 5.4.2 Limitations of Current Approach

#### 5.4.3 Suggestions for Model Improvements

## 6 Subgroup B: System Optimization and Forecasting

### 6.1 Demand Forecasting Model

#### 6.1.1 Models Considered

#### 6.1.2 Model Selection Criteria

#### 6.1.3 Detailed Description of Chosen Model(s)

#### 6.1.4 Model Performance Metrics and Interpretation

##### 6.1.4.1 Time Complexity:

##### 6.1.4.2 Space Complexity:

### 6.2 Route Optimization

#### 6.2.1 Algorithms Considered

- The 1st approach we considered was to model the roads and bus stops as edges and vertices. We will then assign weights to the edges and proceed to use Single Source Shortest Path Algorithms, such as Dijkstra's Algorithm to find the shortest path between the bus stops. The shortest paths will then be the optimized routes.
- The 2nd approach we considered was to use the current routes, but optimize the order of bus stops each bus visits. The idea is to organize bus stops according to their importance at different times and conditions. This entails assigning priority scores to certain bus stops under different scenarios and sorting the bus stops to produce the optimized order of visit.

#### 6.2.2 Algorithm Selection Criteria

- **Relevance**:

  - 1st Approach:
    - Shortest Path algorithm is effective at finding the shortest path, but it primarily focuses on minimizing travel distances between stops, not passenger preferences or demand. It does not factor in bus stop popularity or times when specific stops are likely to see higher demand.
  - 2nd Approach:
    - By prioritizing stops based on demand and user preferences, this approach is explicitly designed to optimize according to passenger needs. The priority scoring accounts for fluctuating demand across days, times, and events, allowing routes to adapt based on who needs the service and when. This makes it more responsive to actual user preferences and system demand.
  - Conclusion:
    - The 2nd approach aligns better with the goal of responding to passenger needs which directly addresses the issue at hand.

- **Adaptability**:

  - 1st Approach:
    - Shortest Path algorithm require predefined road networks and do not adapt well to temporal factors like day, hour, or special events, since they treat the network as a static entity. While real-time adjustments could theoretically be added, they would require substantial computational resources and frequent recalculations.
  - 2nd Approach:
    - This approach allows the system to adjust routes dynamically based on predefined priority scores under varying conditions. Since each bus stop’s priority can shift according to time-based demand and satisfaction data, the model naturally adapts without requiring computationally intensive recalculations.
  - Conclusion:
    - The 2nd approach ismore flexible and adaptable to varying demand, making it a more practical choice for a dynamic transportation network.

- **Value-add**:
  - 1st Approach:
    - The current bus routes are already optimized by transportation professionals to follow the shortest or most efficient paths possible, rendering a new shortest-path calculation unnecessary. Implementing Dijkstra’s or similar algorithms would likely replicate existing routes without providing added benefit, making this approach redundant for the current setup.
  - 2nd Approach:
    - Since this approach is not aimed at finding new paths but rather optimizes the order of stops based on historical demand and user preferences, it adds value by focusing on enhancing passenger satisfaction and operational efficiency. By reorganizing stops rather than recalculating routes, this approach complements the pre-established routes without duplicating existing efforts.
  - Conclusion:
    - The redundancy of recalculating shortest paths reinforces that the 2nd approach, which prioritizes stops based on demand brings more added benefits.

#### 6.2.3 Detailed Description of Chosen Algorithm

##### 6.2.3.1 Bus Stop Prioritization and Sorting Algorithm

- **Initialize the MinMaxScaler**:

  - `scaler = MinMaxScaler()`
  - Sets up a MinMaxScaler, which is used to normalize numerical columns by scaling values to a range, typically [0, 1].

- **Define the Normalization Function**:

  - `normalize_group(group)` is defined to normalize specific columns in each group.
  - Within the function:
    - The columns `num_people_at_bus_stop` and `overall_satisfaction` are normalized to bring their values to a common scale.
    - Categorical columns like `weather` and `has_exam` are excluded from normalization.

- **Initialize an Empty Dictionary**:

  - `bus_route_priorities = {}` creates a dictionary to store prioritized bus stop orders for different conditions.

- **Iterate through Each Bus**:

  - A loop iterates over each unique bus number in the dataset `unique_bus_numbers`.
  - For each bus, a DataFrame `bus_df` is created, containing data specific to that bus.

- **Loop through Each Day of the Week**:

  - For each bus, another loop iterates through each unique day of the week.
  - A new DataFrame `bus_day_df` is created for the bus data on that specific day.

- **Loop through Each Hour of the Day**:

  - Within each day, a loop iterates over each unique hour.
  - A new DataFrame `bus_hour_df` is created for data during that hour.

- **Loop through Each Weather Condition**:

  - For each hour, a loop iterates over unique weather conditions.
  - A new DataFrame `bus_weather_df` is created to contain data for that specific weather condition.

- **Loop through Each Exam Status**:

  - Within each weather condition, a loop iterates over the unique values for `has_exam` (where 0 and 1 stands for having exam and not having exam respectively).
  - A new DataFrame `bus_exam_df` is created for each exam status scenario.

- **Normalize the Data by Bus Stop**:

  - The data is copied to a new DataFrame `df_hour` to avoid altering the original.
  - The normalize_group function is applied group-wise for each starting bus stop within the filtered data `df_hour`.
  - `df_hour_normalized` stores the normalized DataFrame by bus stop.

- **Calculate Priority Scores by Bus Stop**:

  - The normalized data is grouped by starting bus stop to calculate the average values for `num_people_at_bus_stop` and `overall_satisfaction`.
  - A `priority_score` column is created, calculated as the sum of normalized `num_people_at_bus_stop` and normalized `overall_satisfaction` values.
  - Normalization here ensures that `priority_score` reflects both demand and satisfaction equally, making the prioritization system fairer and more reliable across different bus stops and conditions.

- **Sort Bus Stops by Priority Score**:

  - The bus stops are sorted in descending order based on `priority_score`.
  - `average_stats_by_start_sorted` holds the sorted list of bus stops for the current scenario.

- **Store the Sorted Priority in a Dictionary**:

  - For each combination of bus number, day, hour, weather, and exam status, the sorted bus stop priority is stored in the dictionary `bus_route_priorities`.

- **Sort the Dictionary**:

  - The dictionary is sorted based on the tuple keys (bus number, day of the week, hour, weather, and exam status).
  - The result is stored in `sorted_bus_route_priorities`.

- **Print the Sorted Priorities**:

  - A loop prints out the priority order of bus stops for each bus, day, hour, weather, and exam condition, showing the optimal order of bus stops per scenario.

- **Summary**:
  - The above algorithm is designed to optimize bus stop prioritization based on survey data, taking into account factors like demand (number of people at the bus stop), user satisfaction, time of day, day of the week, weather conditions, and whether there’s an exam. By creating priority scores for each bus stop, it identifies the most important stops under specific conditions.

##### 6.2.3.2 User Customization Algorithm

- **Dictionary Initialization**:

  - `days_of_week`, `time_ranges`, `weather_conditions`, and `exam_statuses` are dictionaries used to map numerical or binary values to their descriptive labels (e.g., "Monday" for day 1, "Sunny" for weather 0, etc.).

- **Retrieve Unique Bus Numbers**:

  - Extracts all unique bus numbers from the `sorted_bus_route_priorities` dictionary.
  - Displays these bus numbers for the user to choose from.

- **User Bus Number Selection**:

  - Asks the user to select a bus number from the displayed options.
  - Sets `terminate_algorithm` to 0, used later to check if any invalid input is encountered, if so, algorithm should be stopped prematurely.

- **Check for Valid Bus Number**:

  - If the selected bus number exists in `sorted_bus_route_priorities`, it continues to the next step. If not, an error is printed, and the process is terminated.

- **Display Days for Selected Bus**:

  - Extracts and displays all unique days available for the chosen bus number.
  - Asks the user to select a day and verifies if it is valid.

- **Display Hours for Selected Bus and Day**:

  - If the day is valid, it retrieves and displays available hours for the selected bus and day.
  - Asks the user to pick an hour and verifies if it is valid.

- **Display Weather Conditions for Selected Bus, Day, and Hour**:

  - If the hour is valid, it retrieves and displays weather conditions for the selected bus, day, and hour.
  - Asks the user to pick a weather condition and verifies if it is valid.

- **Display Exam Status for Selected Bus, Day, Hour, and Weather**:

  - If the weather condition is valid, it retrieves and displays exam status options for the selected bus, day, hour, and weather.
  - Asks the user to pick an exam status and verifies if it is valid.

- **Retrieve and Display Final Bus Route**:

  - If all inputs are valid, it constructs a `final_tuple` of the selected options (bus number, day, hour, weather, exam status).
  - Retrieves the priority order of bus stops for this specific tuple from `bus_route_priorities`.

- **Organize Final Routes**:

  - Separates prioritized stops from the complete list of stops (`all_routes` for the selected bus).
  - Combines prioritized stops with non-prioritized stops to form the `final_routes`, which places higher-priority stops first.

- **Display User Selection and Bus Stop Order**:

* Displays the selected bus settings (bus number, day, time, weather, exam status) for the user’s confirmation.
* Prints out:
  - The priority order of bus stops based on the calculated priority score.
  - The final optimized order of bus stops, which first includes priority stops followed by remaining stops.

- **Summary**:

* The above algorithm uses the output of 5.3.1 Bus Stop Prioritization and Sorting Algorithm and enables personalized bus route prioritization by allowing users to select criteria such as bus number, day, time, weather, and exam status. It validates each input, retrieves priority stops based on user demand and satisfaction, and outputs an optimized order of bus stops, ensuring efficient and tailored service.

##### 6.2.3.3 Impact Simulation Model

#### 6.2.4 Performance Metrics and Interpretation

##### 6.2.4.1 Bus Stop Prioritization and Sorting Algorithm

##### 6.2.4.1.1 Time Complexity:

- **Outer Loop over Each Bus `for bus_num in unique_bus_numbers`**:
- This loop iterates over each unique bus in `unique_bus_numbers`. Denote the number of unique bus as B.

  - **Loop over Each Day `for day in bus_df['day_of_week'].unique()`**:
  - This iterates over each unique days of the week for each bus. Denote the number of unique days as D.

    - **Loop over Each Hour `for hour in bus_day_df['hour'].unique()`**:
    - This iterates over each unique hours for the day. Denote the number of unique hours as H.

      - **Loop over Each Weather Condition `for weather in bus_hour_df['weather'].unique()`**:
      - This loop iterates over each unique weather conditions for each hour. Denote the number of unique weather conditions as W.

        - **Loop over Exam Status `for has_exam in bus_weather_df['has_exam'].unique()`**:
        - This iterates over each unique exam status for each weather condition. Denote the number of unique exam status as E.

          - **Grouping and Normalization by Bus Stop `df_hour.groupby('start', group_keys=False).apply(normalize_group)`**:
          - The `groupby` operation divides data by unique bus stops, and `apply(normalize_group)` is used to normalize the selected columns. Denote the number of unique bus stops as S.
          - MinMaxScaler normalization on two columns `num_people_at_bus_stop` and `overall_satisfaction` is an O(N) operation. Denote the number of records per bus stop as N.
          - Applying `normalize_group` and mean calculations for each bus stop is an O(N) operation. Denote the number of records per bus stop as N.
          - **Sorting Bus Stops by Priority Score `average_stats_by_start.sort_values(by='priority_score', ascending=False)`**:
          - Sorting a list of bus stops by priority_score is an O(SlogS) operation. Denote the number of unique bus stops as S.

- **Dictionary Storage and Sorting `sorted(bus_route_priorities.items(), key=lambda x: (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4]))`**:
- Sorting a dictionary with K entries based on its keys has a complexity of O(KlogK), where K is the number of dictionary entries, K = B × D × H × W × E.

- **Total Time Complexity**: **O((K(N + SlogS)) + O(KlogK))**, where K = B × D × H × W × E, S = number of unique bus stops and N = number of records per bus stop.

##### 6.2.4.1.2 Space Complexity:

- **DataFrames (e.g., `bus_df`, `bus_day_df`, `bus_hour_df`)**:

  - Each DataFrame subset of df2 holds filtered records based on unique values in loops. The memory usage scales with O(N) for each segment. Denote the number of records per bus stop as N.

- **Dictionary `bus_route_priorities`**:

  - The dictionary bus_route_priorities stores sorted bus stop orders for each combination of factors, with K entries. Denote K = B × D × H × W × E.
  - Each entry in the dictionary holds a list of bus stops, making the space complexity for the dictionary O(K×S), where K = B × D × H × W × E and S = number of unique bus stops.

- **Total Space Complexity: **O(N + K(S))\*\*\*\*, where N = number of records per bus stop, K = B × D × H × W × E and S = number of unique bus stops.

##### 6.2.4.2 User Customization Algorithm

##### 6.2.4.2.1 Time Complexity:

- **Mapping Initialization**:
  - The dictionaries (`days_of_week`, `time_ranges`, `weather_conditions`, `exam_statuses`) are initialized. These operations are O(1) since they involve constant time lookups.
- **Extracting Unique Bus Numbers**:

  - `unique_bus_numbers` is extracted using `sorted(set([key[0] for key in sorted_bus_route_priorities.keys()]))`, which iterates through keys of sorted_bus_route_priorities.

- **Nested Loops in `run_algorithm`**:

  - The function navigates through several nested `for` loops and `if` conditions based on user inputs.
  - Denote the number of unique bus as B.
  - Denote the number of unique days as D.
  - Denote the number of unique hours as H.
  - Denote the number of unique weather conditions as W.
  - Denote the number of unique exam status as E.
  - Denote K = B × D × H × W × E.
  - The maximum number of tuples in `sorted_bus_route_priorities` would then be K, which represents the total combinations of bus schedules.

- **Checking Valid User Inputs using `if` Conditions**:

  - At each stage (bus, day, hour, weather, and exam status), the code checks if the user input matches a valid option. These checks are all O(1).

- **Retrieving and Sorting Priorities**:

  - After constructing the tuple for the chosen schedule `final_tuple`, the code retrieves `bus_route` which is the list of prioritized bus stops for that schedule.
  - Separating `bus_route` into `prioritized_stops` and `non_prioritized_stops` is O(M), where M is the total number of bus stops for a given bus.

- **Total Time Complexity**: **O(K + M)**, where K = B × D × H × W × E and M = total number of bus stops for a given bus.

##### 6.2.4.2.2 Space Complexity:

- **Mapping Dictionary (`days_of_week`, `time_ranges`, `weather_conditions`, `exam_statuses`)**:

  - Similar to above, denote K = B × D × H × W × E
  - The dictionary contribute to O(K) space.

- **Extracted Unique Bus Numbers `unique_bus_numbers`**:

  - `unique_bus_number`s stores unique bus numbers derived from `sorted_bus_route_priorities`. Denote this as B.

- **Bus Routes Dictionaries**:

  - Let N be the total number of keys in `sorted_bus_route_priorities` and `bus_route_priorities`, which would be at most K = B × D × H × W × E based on combinations of bus numbers, days, hours, weather conditions, and exam statuses.
  - These 2 dictionaries will collectively contribute to O(K) space.

- **User Selection Variables (`selected_bus_num`, `selected_day`, `selected_hour`, `selected_weather`, `selected_exam`)**:

  - These variables are single values used to store the user’s choices and are overwritten with each new selection. They contribute O(1) space in total.

- **Extracted Unique Values per Selection (e.g., `unique_days`,`unique_hours`, `unique_weathers`, `unique_exams`)**:

  - These sets hold unique values of days, hours, weather conditions, and exam statuses based on the current selection.
  - Each set size depends on the possible values per category but is independent of N. They require O(D + H + W + E) space in total.

- **Final Route Lists (`prioritized_stops`, `non_prioritized_stops`, `final_routes`)**:

  - These lists hold the bus stops based on the selected route configuration.
  - Let M represent the total number of bus stops for the selected bus.
  - `prioritized_stops` and `non_prioritized_stops` each take O(M) space.
  - `final_routes` combines both lists, also resulting in O(M) space.

- **Total Space Complexity**: **O(K + M)**, K = B × D × H × W × E and M = total number of bus stops for a given bus.

##### 6.2.4.3 Impact Simulation Model

###### 6.2.4.3.1 Time Complexity:

###### 6.2.4.3.2 Space Complexity:

### 6.3 Capacity Allocation Optimization Model

#### 6.3.1 Modeling Techinques Considered

- Some techniques considered include linear programming, stochastic modelling, machine learning models (clustering techniques) such as K-Means, and network flow models.
- These methods handle complexity and existing constraints in the real world, which allow for optimization that ensures resource efficiency. Models like stochastic modelling also incorporate uncertainty and variability due to factors like demand peaks, unpredictable events, and/or seasonal changes, which makes the system more resilient. These techniques can be integrated with the demand forecasting model to facilitate real-time and adaptive, efficient allocation.

#### 6.3.2 Model Selection Criteria

**Our group decided to use linear programming to model capacity allocation.**

- **Relevance**:

  - Linear programming effectively meets the objective of finding the optimal solution- number of
    buses to allocate to each bus stop for every hour.

- **Ease of Integration**:

  - Linear programming can be integrated with other modelling techniques, including the
    (previously-defined) demand forecasting model, to enhance decision-making. This ensures
    capacity allocation also takes into account demand size, and remains optimal by minimising
    the number of unmet demands.

- **Flexibility**:

  - Linear programming depends on parameters that can be defined and adjusted. This
    increases the model's adaptability to changes, including demand forecasts during
    peak hours, special events, and seasonal variations.

- **Feasibility**:
  - Linear programming can manage multiple constraints, which increases its feasibility in handling the complexity of the real world.

#### 6.3.3 Detailed Description of Chosen Model

- **Defining model components**:

  - We begin by defining the components of the model. The model’s objective is to minimise the unmet demand of passengers using the NUS Internal Shuttle Bus (ISB) Services. This implies (indirectly) reducing passenger waiting times caused by missed buses due to overcrowding. A constraint identified in this problem and model is that the total number of buses must not exceed the maximum fleet capacity. Lastly, the model’s decision variable, the choice that is being controlled in order to achieve the objective, is the number of buses allocated to each bus stop for each hour.

- **Input: Forecasted Demand**:

  - From the demand forecasting model, the forecasted demand `demand_forecast` is represented by an array which has a number of rows equal to the number of bus stops `num_routes` and a number of columns equal to the number of hourly intervals `num_time_slots` in the analysis.
  - We initialised `(num_routes, num_time_slots)` as the shape of `demand_forecast`.
  - Sample `demand_forecast`
    - ` [  
       [30, 50, 80, 100], # Bus stop A demand across four hours  
       [40, 70, 90, 120], # Bus stop B demand across four hours  
       [20, 60, 85, 110], # Bus stop C demand across four hours  
       ]
  - We flattened `demand_forecast` for linear programming.
  - This is assigned to `flattened_demand`.

- **Setting up objective coefficients**:

  - Objective coefficients are the values associated with (multiplied to) the decision variables in linear
    programming. They quantify how much each variable contributes in the overall optimization.
  - Our optimization problem is a minimization problem. Thus, the coefficients are set to
    `-flattened_demand`.
  - This is assigned to `objective_coefficients`.

- **Setting up constraints**:

  - We initialised the (average) capacity of each bus `bus_capacity` and the maximum number of buses available for deployment `max_buses` since these values are fixed and not variable.
  - We have estimated `bus_capacity` to be 50 and let `max_buses` to be 6.
  - `max_buses` is estimated based on the assumption that ISB is able and willing to expand its fleet size to twice the current size as part of achieving the business objectives.
  - There are 2 types of constraints in linear programming: equality constraints and inequality constraints.
  - An equality constraint refers to a condition that requires a variable to hold exactly at a specified value.
    - We defined the left-hand side of the equality `A_eq` to be a matrix of ones, with 1 row and (`num_routes` \* `num_time_slots`) columns. The right-hand side `b_eq` is an array containing `max_buses`.
  - An inequality constraint, on the other hand, allows for a range of possible values. In defining inequality constraints, we consider the upper bounds.
    - We defined the left-hand side of the inequality `A_ub` to be an identity matrix- a matrix in which all of its diagonal elements are ones and the rest are zeros- having (`num_routes` \* `num_time_slots`) rows and columns. The right hand side `b_ub` (upper bound) is `flattened_demand`.

- **Setting up bounds**:

  - We set up the bounds for the decision variables of the problem. The lower bound is set to 0, while the upper bound is set to `bus_capacity`.
  - This also ensures that the total number of people boarding the bus, as accounted for in the model's optimisation, does not exceed its capacity for safety and practical purposes.
  - The bounds are stored as a tuple `(0, bus_capacity)` in an array with 1 row and (`num_routes` \* `num_time_slots`) columns.

- **Model output**:
  - The objective coefficients, constraints and bounds are input into the function `linprog` with `method = “highs”`. The output is assigned to `result`.
  - If the optimization is a success, the model reshapes `result` to the initial `demand_forecast` shape, and assigns it to `allocated_buses`. The model then prints out the message “Optimised Capacity Allocation (Buses per Route per Time Slot): `allocated_buses`”.
  - If the optimization fails, the model prints out the message "Optimization failed: `result.message`”, where `result.message` is the error message.

#### 6.3.4 Performance Metrics and Interpretation

##### 6.3.4.1 Time Complexity: Explain

##### 6.3.4.2 Space Complexity: Explain

### 6.4 Evaluation

#### 6.4.1 Demand Forecasting Model

##### 6.4.1.1 Evaluation of model performance against business objectives

##### 6.4.1.2 Limitations of Current Approach

##### 6.4.1.3 Suggestions for Model Improvements

#### 6.4.2 Route Optimization

##### 6.4.2.1 Bus Stop Prioritization and Sorting Algorithm, User Customization Algorithm

###### 6.4.2.1.1 Evaluation of model performance against business objectives

- **Demand Prediction Accuracy**:

  - By segmenting data based on detailed features (bus, day, hour, weather, and exam status), the algorithm provides a granular view of demand patterns.
  - This level of detail supports robust demand forecasting, allowing for better resource allocation during peak and off-peak periods, reducing operational costs, and improving the user experience by managing overcrowding effectively.

- **Scalability**:

  - The algorithm’s complexity depends heavily on the number of combinations of factors (K) and the number of stops (S). If K or S grows significantly, the runtime can become a constraint, especially with high data volume (N records per stop).
  - For large-scale systems with hundreds of bus stops and numerous combinations, this algorithm could become computationally intensive and may need optimization (e.g., parallel processing) to run efficiently in real-time or near real-time. Such enhancements would be necessary for dynamic adjustments but could increase operational costs.
  - The space complexity O(N+K(S)) implies high memory usage, especially as unique factor combinations (K) and bus stops (S) increase. This high dimensionality can lead to excessive memory needs, making the algorithm less scalable and costly to implement in large transit systems.

- **Operational Cost Management**:

  - MinMaxScaler and normalization steps are O(N) operations, providing necessary preprocessing for effective comparisons without excessive complexity.
  - Grouping and normalization, combined with sorting steps, may incur computational costs, especially for larger datasets.
  - These costs can be justified if the model significantly improves scheduling and capacity management. However, if the scale grows, costs could outweigh benefits, so monitoring computational resources and runtime is essential for balancing cost-effectiveness.

- **Flexibility in Route Adjustment**:
  - The priority-based ranking system allows dynamic route adjustments based on changing factors like weather and exam schedules, aligning with the objective of flexible, real-time optimization.
  - This flexibility allows transport authorities to respond to real-time data, potentially minimizing underused capacity during off-peak times or adjusting routes to better serve users during high-demand periods, directly impacting user satisfaction and loyalty.

###### 6.4.2.1.2 Limitations of Current Approach

- **Over-simplification**:

  - The calculation of `priority_score` using only two factors (number of people and user satisfaction) might not capture other important variables, such as bus stop accessibility, operational constraints, etc.

- **Scalability**:

  - The nested loops iterating over buses, days, hours, weather conditions, and exam statuses can lead to a combinatorial explosion, making the algorithm inefficient with large datasets or when many unique combinations exist.

- **Lack of Real-time Updates**:

  - The algorithm might not be very apt at incorporating real-time changes, such as sudden shifts in demand or changes in weather, which can affect bus stop prioritization. Outdated data can lead to suboptimal prioritization

- **User Input Validity**:

  - The algorithm depends on users making correct selections. If users misunderstand the options or input invalid choices (even if they are checked), it can lead to frustration and a poor user experience.

- **Limited Customizations**:
  - Although the algorithm allows for some user customization, it may not cover all potential user preferences and scenarios, limiting its practicaly and user experience.

##### 6.4.2.1.3 Suggestions for Model Improvements

- **Addressing Over-simplication**:

  - Incorporate additional factors into the `priority_score`, such as bus stop accessibility ratings, operational constraints, etc. This could provide a more comprehensive view of each bus stop's importance.

- **Addressing Scalability**:

  - Implement optimization techniques such as memoization or heuristics to reduce the number of calculations needed by avoiding redundant computations.

- **Addressing Lack of Real-time Updates**:

  - Develop a mechanism to dynamically adjust priorities based on real-time information, such as changes in demand or environmental conditions.

- **Addressing User Input Validity**:

  - Design a more intuitive user interface with clear instructions and tooltips to guide users in making their selections correctly.

- **Addressing Limited Customizations**:
  - Allow users to specify additional criteria for customization and even scenarios that are not covered by our current survey data.

##### 6.4.2.2 Impact Simulation Model

###### 6.4.2.2.1 Evaluation of model performance against business objectives

###### 6.4.2.2.2 Limitations of Current Approach

##### 6.4.2.2.3 Suggestions for Model Improvements

##### 6.4.2.3 Capcacity Allocation Optimization Model

###### 6.4.2.3.1 Evaluation of model performance against business objectives

- The model minimises the number of passengers unable to board the bus each hour (and maximises bus utilisation) without exceeding capacity. This effectively reduces wait times for passengers and increases their satisfaction levels, given the negative correlation between wait time and user satisfaction.
- Keeping optimization upper bound at the (average) capacity of the bus also ensures that the safety of the ISB service is accounted for and remains a top priority.

###### 6.4.2.3.2 Limitations of Current Approach

- **Simplified assumptions**:
  - The model does not account for potential disruptions, such as traffic delays and mechanical failures. The output might be too optimistic. As a result, in these instances, the model could overestimate the number of passengers that can be served, and in turn, fall short of objectives.
  - The assumption made for the value of `max_buses` did not take into account other constraints such as budget and number of drivers.

##### 6.4.2.3.3 Suggestions for Model Improvements

- **Feedback Loops**:

  - Mechanisms can be implemented to regularly update the model based on actual data and user feedback. This allows for the identification and refinement of gaps to improve the model’s accuracy and effectiveness.
  - However, this project is constrained by limited access to the actual ISB service for testing, as well as by the time needed to collect additional data and feedback over time.

- **Sensitivity Analysis**:
  - Sensitivity analyses can be conducted to understand how variations in `max_buses` affect the results. This would allow for determining the number of additional shuttle buses ISB should acquire in order to optimise capacity allocation, for a given budget and other relevant constraints, assuming the bus type remains the same and the bus capacity does not change.
  - However, in this project, we are constrained by limited information on ISB and its resources.

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

- If you do not have Git installed, visit [Git website](https://git-scm.com/downloads) for instructions on installation. Once installed, you can check by running
  - `git --version `
- Clone the repository via SSH or HTTPS
  - `git clone git@github.com:chiabingxuan/DSA3101-Group-Project.git` or
  - `git clone https://github.com/chiabingxuan/DSA3101-Group-Project.git`

### 8.3 Dependency Management

Dependencies are managed in requirements.txt. follow the step below:

- Install libraries required
  - `pip install -r requirements.txt`

### 8.4 Code Style Guide Adherence

Code style PEP 8 have been adapted for this project

## 9. Analytical Findings

## 10. Recommendations

### Prioritized list of recommendations

1. Implement a dynamic bus allocation system based on predicted demand
   - The demand for buses changes throughout the day at different stops. Instead of sticking to a fixed schedule, we can adjust the number of buses based on these demand patterns — adding more buses during busy times and reducing them during quieter hours. This way, we can better match demand when it is needed.
2. Implement a new optimized route
   - The route optimization model can guide drivers in prioritizing which bus stops to visit first, especially during peak hours. Unlike the usual approach of following a fixed route, this model allows buses to respond to real-time demand, ensuring that high-demand stops are reached earlier.

### Implementation roadmap

### Expected impact of each recommendations

## 11. Future Work

11.1 Additional research areas in the future

- 11.1.1 Simulation and Modeling for Optimal Routing
  - Use computer simulations to test and optimise various route and scheduling configurations under different conditions.
    - Discrete Event Simulation (DES):  
      Using DES like SimPy, helps to focus on key events, like shuttles arriving at or departing from stops, to understand the impact on waiting times and bus crowdedness. This is useful for simulating peak periods and assessing the crowdedness at stops.
- 11.1.2 Passenger Flow and Mobility Patterns
  - Study passenger movement patterns on campus. Research methods like mobility clustering analysis to identify frequently travelled paths or "hotspots" on campus, which can help in refining routes to maximise coverage.
    - Using clustering techniques, like K-means clustering, can help in determining high-demand locations, popular routes, and peak times, which can then inform adjustments to the shuttle routes or schedules.
    - K-means clustering:
      - Use methods like the Elbow Method to determine an optimal number of clusters. K-means will assign each trip or stop location to a cluster by minimising the distance to the cluster’s centroid.
      - Each cluster’s centroid (average location and time) represents a high-demand area and its typical usage time.
      - For example, one cluster might reveal that many students travel between dorms and lecture halls in the morning, while another shows high movement to recreation areas in the evening.

## 12. Lessons Learned

## 13. References

## 14. Appendices
