# Data Scavengers: Optimising the NUS Bus System

- [Data Scavengers: Optimising the NUS Bus System](#data-scavengers-optimising-the-nus-bus-system)
  - [1. Introduction](#1-introduction)
  - [2. Business Understanding](#2-business-understanding)
  - [3. Technical Implementation](#3-technical-implementation)
    - [3.1 Repository Structure](#31-repository-structure)
    - [3.2 Setup Instructions](#32-setup-instructions)
    - [3.3 Dependency Management](#33-dependency-management)
    - [3.4 Code Style Guide Adherence](#34-code-style-guide-adherence)
  - [4. Data Understanding](#4-data-understanding)
    - [4.1 Data Acquisition](#41-data-acquisition)
    - [4.2 Data Dictionary of Original Survey Data](#42-data-dictionary-of-original-survey-data)
    - [4.3 Data Quality Assessment](#43-data-quality-assessment)
  - [5. Data Preparation](#5-data-preparation)
    - [5.1 Initial Data Cleaning](#51-initial-data-cleaning)
    - [5.2 Initial Data Exploration](#52-initial-data-exploration)
    - [5.3 Synthetic Data Generation](#53-synthetic-data-generation)

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

## 3. Technical Implementation

### 3.1 Repository Structure

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

### 3.2 Setup Instructions

To set up the project on a local machine, follow the steps below:

1. Ensure that you have Python 3.13 installed. If not, you can visit the [Python website](https://www.python.org/downloads/) for instructions on installation. Once installed, you can verify your version of Python by running the following in your terminal:
```
python --version
```
2. If you do not have Git installed, visit the [Git website](https://git-scm.com/downloads) for instructions on installation. Once installed, you can verify your version of Git by running the following in your terminal:
```
git --version
```
3. Clone the repository. You can do so via SSH:
```
git clone git@github.com:chiabingxuan/DSA3101-Group-Project.git
```
&nbsp; &nbsp; &nbsp; &nbsp;Alternatively, you can also clone the repository via HTTPS:
```
git clone https://github.com/chiabingxuan/DSA3101-Group-Project.git
```
4. In `config.py`, you can adjust the configuration parameters to your liking.
5. Set your working directory to the folder containing the cloned repository:
```
cd DSA3101-Group-Project
```
6. Create a Python virtual environment named `venv/`:
```
python -m venv .
```
7. Activate the virtual environment:
```
venv\Scripts\activate
```
8. Install necessary packages:
```
pip install -r requirements.txt
```
9. Run the main program:
```
python main.py
```
10. To deactivate your virtual environment, run the following:
```
deactivate
```

### 3.3 Dependency Management

Dependencies are managed in `requirements.txt`.

### 3.4 Code Style Guide Adherence

PEP-8 coding style has been adapted for this project.

## 4. Data Understanding

### 4.1 Data Acquisition

We collected survey data to investigate the travel patterns and satisfaction levels of NUS students, with regards to the NUS bus system. In our survey, respondents were asked to share **two bus trips** that they embarked on for the day. The [survey link](https://docs.google.com/forms/d/1zh5M9Sccn3ifxcOOJd2UMj7cQSFKPWmvD-RG1PZA9QM/edit) was circulated online on various NUS platforms, including the official Telegram channel for the NUS College of Humanities and Sciences (CHS).

### 4.2 Data Dictionary of Original Survey Data

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

### 4.3 Data Quality Assessment

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

## 5. Data Preparation

### 5.1 Initial Data Cleaning

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

### 5.2 Initial Data Exploration

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

### 5.3 Synthetic Data Generation

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
