# Data Scavengers: Optimising the NUS Bus System

- [Data Scavengers: Optimising the NUS Bus System](#data-scavengers-optimising-the-nus-bus-system)
  - [1. Project Overview](#1-project-overview)
  - [2. Technical Implementation](#2-technical-implementation)
    - [2.1 Repository Structure](#21-repository-structure)
    - [2.2 Setup Instructions](#22-setup-instructions)
    - [2.3 Dependency Management](#23-dependency-management)
    - [2.4 Code Style Guide Adherence](#24-code-style-guide-adherence)
  - [3. Data Understanding](#3-data-understanding)
    - [3.1 Data Acquisition](#31-data-acquisition)
    - [3.2 Data Dictionary](#32-data-dictionary)

## 1. Project Overview

Data Scavengers is a collaborative project aimed at collecting real time data to optimise the bus system in NUS by utilising various models, such as Route Optimisation, Demand Forecasting and Capacity Allocation models. Visualisations have also been made to assist us in understanding the current problems faced.

**Project Objectives**

- Predict the demand of bus users at a specific bus stop at specific hour intervals
- Optimise the bus routes to reduce waiting times
- Allocate the capacity of buses to meet the demand

## 2. Technical Implementation

### 2.1 Repository Structure

```plaintext
DSA3101-Group-Project
│
├── data/                                    # Dataset files and resources for analysis
│   ├── timelapse_popular_trips/             # Dataset files for popular trip counts based on segments
│   │   ├── nus_a1_trip_markers_timelapse_popular_trips.csv            # Popular trips on bus service A1
│   │   ├── nus_a2_trip_markers_timelapse_popular_trips.csv            # Popular trips on bus service A2
│   │   ├── nus_cluster_0_trip_markers_timelapse_popular_trips.csv     # Popular trips on cluster 0
│   │   ├── nus_cluster_1_trip_markers_timelapse_popular_trips.csv     # Popular trips on cluster 1
│   │   ├── nus_cluster_2_trip_markers_timelapse_popular_trips.csv     # Popular trips on cluster 2
│   │   ├── nus_d1_trip_markers_timelapse_popular_trips.csv            # Popular trips on bus service D1
│   │   ├── nus_d2_trip_markers_timelapse_popular_trips.csv            # Popular trips on bus service D2
│   │   ├── nus_exam_trip_markers_timelapse_popular_trips.csv          # Popular trips on exam days
│   │   ├── nus_no_exam_trip_markers_timelapse_popular_trips.csv       # Popular trips on non-exam days
│   │   └── nus_trip_markers_timelapse_popular_trips.csv               # Popular trips overall
│   │
│   ├── cleaned_other_feedback_data.csv       # Preprocessed feedback data for analysis
│   ├── cleaned_trip_data.csv                 # Preprocessed trip data for synthesis and analysis
│   ├── combined_trip_data.csv                # Combined train and test synthetic trip data for modeling
│   ├── sdv_metadata.json                     # Metadata configuration for SDV
│   ├── survey.csv                            # Original survey data
│   ├── test_trip_data_after_sdv.csv          # Test data after SDV
│   ├── test_trip_data_before_sdv.csv         # Test data before SDV
│   ├── train_trip_data_after_sdv.csv         # Train data after SDV and SMOTE-NC
│   └── train_trip_data_after_smote.csv       # Train data after SMOTE-NC
│
├── ethics and privacy enhancements/          # Scripts for data privacy and encryption
│   ├── Data Decrypter/
│   │   ├── Data Decrypter.py                 # Script for decrypting data
│   │   └── decoded_data.csv                  # Decrypted dataset
│   ├── Data Encrypter/
│   │   ├── Data Encrypter.py                 # Script for encrypting data
│   │   └── hypothetical_trip_data.csv        # Encrypted dataset for hypothetical trips
│   ├── Shared/
│   │   ├── encoded_data.csv                  # Encoded data file
│   │   └── encrypted_decoding_dict.enc       # Encryption dictionary
│   ├── Data Anonymizer.py                    # Script for anonymizing data
│   └── README.md                             # Documentation for ethics and privacy enhancements
│
├── src/                                          # Source code for data analysis, cleaning, and modeling
│   ├── __pycache__/                              # Python bytecode cache directory
│   │   ├── config.cpython-312.pyc                # Compiled bytecode for config.py
│   │   └── demand_forecasting.cpython-312.pyc    # Compiled bytecode for demand_forecasting.py
│   ├── analyse_travel_patterns.py                # Analysis of travel patterns from trip data
│   ├── capacity_allocation.py                    # Allocates transport capacity based on demand
│   ├── config.py                                 # Configuration settings
│   ├── demand_forecasting.py                     # Forecasts demand using trip data
│   ├── Drivers_of_Satisfaction.ipynb             # Analysis of satisfaction drivers
│   ├── filter_count.py                           # Script to count unique trips at 10 min interval
│   ├── main.py                                   # Main script to execute all files
│   ├── make_timelapses_for_travel_patterns.py    # Creates timelapses of travel patterns
│   ├── origin_destination_matrix.py              # Computes origin-destination matrix
│   ├── Route_Optimization.py                     # Optimizes travel routes based on trip data
│   ├── Simulation of System Efficiency And Us.py # Simulates system efficiency
│   ├── smote.py                                  # Applies SMOTE-NC to balance data
│   ├── survey_cleaning.py                        # Cleans and preprocesses survey data
│   ├── synthetic_data_generation_test.py         # Generates synthetic test data using SDV
│   ├── synthetic_data_generation_train.py        # Generates synthetic train data using SDV after SMOTE-NC
│   └── User_Segmentation_Model.py                # Segments users based on trip data
│
├── visualisations/                               # Visual output files generated by scripts
│   ├── Dashboards/                               # Dashboard visualisations and interactive files
│   │   ├── Graph_Of_Hourly_Distribution_Of_Bus_Trips/                                    # Visualisation of bus trip distributions
│   │   │   ├── (Interactive) Graph_Of_Hourly_Distribution_Of_Bus_Trips.twbx              # Tableau workbook for interactive distribution visualization
│   │   │   ├── (Interactive) Link_to_Dashboard.txt                                       # Link to interactive dashboard online
│   │   │   └── (Non-Interactive) Image_of_Graph_Of_Hourly_Distribution_Of_Bus_Trips.png  # Image of hourly bus trip distribution
│   │   ├── Overall_Satisfaction_Score_Against_Factors/                                   # Visualisation of satisfaction scores
│   │   │   ├── (Interactive) Link_to_Dashboard.txt                                       # Link to interactive dashboard online
│   │   │   ├── (Interactive) Overall_Satisfaction_Score_Against_Factors.twbx             # Tableau workbook for satisfaction scores
│   │   │   └── (Non-Interactive) Image_of_Overall_Satisfaction_Score_Against_Factors.png # Image of satisfaction score against factors
│   │   ├── Word_Cloud_With_Frequency_Charts/                                             # Word cloud with frequency chart
│   │   │   ├── (Interactive) Link_to_Dashboard.txt                                       # Link to interactive dashboard online
│   │   │   ├── (Interactive) Word_Cloud_Bubble_With_Frequency_Charts.twbx                # Tableau workbook for interactive word cloud
│   │   │   └── (Non-Interactive) Image_of_Word_Cloud_Bubble_With_Frequency_Charts.png    # Image of word cloud with frequency chart
│   │   └── README.md                                                                     # Documentation for the Dashboards folder
│   │
│   ├── initial_data_exploration/                               # Visualisations for exploratory data analysis
│   │   ├── initial_bus_num_bar_chart.png                       # Bar chart of bus service distributions
│   │   ├── initial_comfort_histogram.png                       # Histogram of comfort scores
│   │   ├── initial_crowdedness_histogram.png                   # Histogram of crowdedness scores
│   │   ├── initial_crowdedness_satisfaction_histogram.png      # Histogram of crowdedness satisfaction scores
│   │   ├── initial_duration_per_day_box_plot.png               # Box plot of duration spent on bus per day
│   │   ├── initial_end_bar_chart.png                           # Bar chart of trip end locations
│   │   ├── initial_has_exam_bar_chart.png                      # Bar chart of exam vs non-exam responses
│   │   ├── initial_main_reason_for_taking_isb_bar_chart.png    # Bar chart for main reason for taking isb
│   │   ├── initial_major_bar_chart.png                         # Bar chart of distribution of major
│   │   ├── initial_num_people_at_bus_stop_box_plot.png         # Box plot of number of people at bus stops
│   │   ├── initial_on_campus_bar_chart.png                     # Bar chart of distribution of people staying on campus
│   │   ├── initial_overall_satisfaction_histogram.png          # Histogram of overall satisfaction scores
│   │   ├── initial_safety_histogram.png                        # Histogram of safety scores
│   │   ├── initial_start_bar_chart.png                         # Bar chart of trip start locations
│   │   ├── initial_trips_per_day_box_plot.png                  # Box plot of number of bus trips taken per day
│   │   ├── initial_waiting_time_box_plot.png                   # Box plot of waiting time for buses
│   │   ├── initial_waiting_time_satisfaction_histogram.png     # Histogram of waiting time satisfaction scores
│   │   ├── initial_weather_bar_chart.png                       # Bar chart of distribution of weather
│   │   └── initial_year_bar_chart.png                          # Bar chart of distribution of student year
│   │
│   ├── timelapses/                                             # Timelapse visualizations
│   │   ├── nus_a1_trip_markers_timelapse.html                  # Timelapse of trip markers for bus service A1
│   │   ├── nus_a2_trip_markers_timelapse.html                  # Timelapse of trip markers for bus service A2
│   │   ├── nus_cluster_0_trip_markers_timelapse.html           # Timelapse of trip markers for cluster 0
│   │   ├── nus_cluster_1_trip_markers_timelapse.html           # Timelapse of trip markers for cluster 1
│   │   ├── nus_cluster_2_trip_markers_timelapse.html           # Timelapse of trip markers for cluster 2
│   │   ├── nus_d1_trip_markers_timelapse.html                  # Timelapse of trip markers for bus service D1
│   │   ├── nus_d2_trip_markers_timelapse.html                  # Timelapse of trip markers for bus service D2
│   │   ├── nus_exam_trip_markers_timelapse.html                # Timelapse of trip markers for students with exams
│   │   ├── nus_no_exam_trip_markers_timelapse.html             # Timelapse of trip markers for students with no exams
│   │   └── nus_trip_markers_timelapse.html                     # Timelapse of overall trip markers
│   │
│   ├── Elbow_Method_for_Optimal_K.png                  # Visualization for elbow method to determine optimal K
│   ├── od_probability_matrices.html                    # HTML file for OD probability matrices
│   └── Silhouette_Method_for_Optimal_K.png             # Visualization for silhouette method to determine optimal K
│
├── .gitignore                                # Specifies files and directories to ignore in git
├── index.html                                # Entry point for any web-based interface
├── README.md                                 # Overview, setup, and usage instructions for the project
└── requirements.txt                          # List of all libraries required to run the scripts
```

### 2.2 Setup Instructions

To set up the project on a local machine, follow the steps below:

1. If you do not have Git installed, visit the [Git website](https://git-scm.com/downloads) for instructions on installation. Once installed, you can verify your version of Git by running the following in your terminal:

```
git --version
```

2. Clone the repository. You can do so via SSH:

```
git clone git@github.com:chiabingxuan/DSA3101-Group-Project.git
```

Alternatively, you can also clone the repository via HTTPS:

```
git clone https://github.com/chiabingxuan/DSA3101-Group-Project.git
```

3. In `config.py`, you can adjust the configuration parameters to your liking.
4. Set your working directory to the folder containing the cloned repository:

```
cd DSA3101-Group-Project
```

5. Create a Python virtual environment named `venv/`:

```
python -m venv .
```

6. Activate the virtual environment:

```
venv\Scripts\activate
```

7. Install necessary packages:

```
pip install -r requirements.txt
```

8. Run the main program:

```
python main.py
```

9. To deactivate your virtual environment, run the following:

```
deactivate
```

### 2.3 Dependency Management

Dependencies are managed in `requirements.txt`.

### 2.4 Code Style Guide Adherence

PEP-8 coding style has been adapted for this project.

## 3. Data Understanding

### 3.1 Data Acquisition

We collected survey data to investigate the travel patterns and satisfaction levels of NUS students, with regards to the NUS bus system. In our survey, respondents were asked to share **two bus trips** that they embarked on for the day. The [survey link](https://docs.google.com/forms/d/1zh5M9Sccn3ifxcOOJd2UMj7cQSFKPWmvD-RG1PZA9QM/edit) was circulated online on various NUS platforms, including the official Telegram channel for the NUS College of Humanities and Sciences (CHS).

### 3.2 Data Dictionary

From our survey, we are able to obtain tabular data in the form of a CSV file, `survey.csv`. Each row of the CSV file corresponds to a single survey response (two bus trips). In `survey_cleaning.py`, we load the CSV file into a `pandas.DataFrame`, `survey_data`. The data dictionary for `survey_data` is shown below. Given that the column names are rather long, a short description of each attribute is provided instead. Note that all attributes are required.

1. `cleaned_other_feedback_data.csv`

| Field Name                 | Description                                                    | Data Type | Allowed Values                         | Example                    |
| -------------------------- | -------------------------------------------------------------- | --------- | -------------------------------------- | -------------------------- |
| year                       | Year of student                                                | String    | "Year 1", "Year 2", "Year 3", "Year 4" | Year 1                     |
| major                      | The student’s major                                            | String    | Various majors                         | Data Science and Analytics |
| on_campus                  | Indicates whether the student lives on campus                  | String    | "Yes", "No"                            | No                         |
| main_reason_for_taking_isb | The main purpose of using the internal shuttle bus             | String    | "To go to class", "To go to MRT", etc. | To go to class             |
| trips_per_day              | Number of bus trips taken by the student per day               | Integer   | Positive integer                       | 2                          |
| duration_per_day           | Total time spent on the bus per day in minutes                 | Integer   | Positive integer                       | 15                         |
| date                       | Date of trips                                                  | Date      | yyyy-mm-dd                             | 2024-09-16                 |
| has_exam                   | Indicates if the student has exams on the day                  | String    | "Yes", "No"                            | No                         |
| feedback                   | Open-ended feedback provided by the student on the bus service | String    | Free response                          | "Seat availability"        |

2. `cleaned_trip_data.csv`

| Field Name                 | Description                                              | Data Type | Allowed Values                         | Example                    |
| -------------------------- | -------------------------------------------------------- | --------- | -------------------------------------- | -------------------------- |
| year                       | Year of student                                          | String    | "Year 1", "Year 2", "Year 3", "Year 4" | Year 1                     |
| major                      | The student’s major                                      | String    | Various majors                         | Data Science and Analytics |
| on_campus                  | Indicates whether the student lives on campus            | String    | "Yes", "No"                            | No                         |
| main_reason_for_taking_isb | The main purpose of using the internal shuttle bus       | String    | "To go to class", "To go to MRT", etc. | To go to class             |
| trips_per_day              | Number of bus trips taken by the student per day         | Integer   | Positive integer                       | 2                          |
| duration_per_day           | Total time spent on the bus per day in minutes           | Integer   | Positive integer                       | 15                         |
| date                       | Date of trips                                            | Date      | yyyy-mm-dd                             | 2024-09-16                 |
| has_exam                   | Indicates if the student has exams on the day            | String    | "Yes", "No"                            | No                         |
| start                      | Starting location of the bus trip                        | String    | Various locations on campus            | Kent Ridge MRT             |
| end                        | Destination of the bus trip                              | String    | Various locations on campus            | LT27 / S17                 |
| bus_num                    | Number of the bus used                                   | String    | Bus codes such as "A1", "A2", etc.     | A1                         |
| time                       | Time the bus was taken                                   | Time      | HH:MM:SS                               | 08:50:00                   |
| weather                    | Weather condition during the bus trip                    | String    | "Sunny", "Rainy", etc.                 | Sunny                      |
| num_people_at_bus_stop     | Number of people at the bus stop at the time of boarding | Integer   | Positive integer                       | 20                         |
| waiting_time               | Time spent waiting for the bus in minutes                | Integer   | Positive integer                       | 6                          |
| waiting_time_satisfaction  | Satisfaction level with waiting time                     | Integer   | Scale from 1 (low) to 10 (high)        | 7                          |
| crowdedness                | Level of crowdedness experienced on the bus              | Integer   | Scale from 1 (low) to 10 (high)        | 9                          |
| crowdedness_satisfaction   | Satisfaction level with bus crowdedness                  | Integer   | Scale from 1 (low) to 10 (high)        | 7                          |
| comfort                    | Comfort level experienced on the bus                     | Integer   | Scale from 1 (low) to 10 (high)        | 7                          |
| safety                     | Safety level felt during the bus trip                    | Integer   | Scale from 1 (low) to 10 (high)        | 8                          |
| overall_satisfaction       | Overall satisfaction with the bus service                | Integer   | Scale from 1 (low) to 10 (high)        | 8                          |

3. `combined_trip_data.csv`

   Similar to `cleaned_trip_data.csv`

4. `survey.csv`

| Field Name                                                                                | Description of Attribute                                    | Data Type | Allowed Values                                              | Example                             |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------------- | --------- | ----------------------------------------------------------- | ----------------------------------- |
| Timestamp                                                                                 | Date and time when the response was recorded                | object    | Any valid timestamp format (e.g., yyyy-mm-dd hh:mm:ss)      | 9/26/2024 15:49:00                  |
| What year of study are you in?                                                            | Year of study                                               | object    | Year 1, Year 2, Year 3, Year 4                              | Year 1                              |
| What major are you studying?                                                              | Major                                                       | object    | Various majors                                              | DSA                                 |
| Do you stay on campus?                                                                    | Is the respondent staying on campus?                        | object    | Yes, No                                                     | No                                  |
| In general, what is the main reason that you take the school bus?                         | Main reason for taking the school bus                       | object    | To go to class, To go for meals, To go to MRT, Other        | To go to class                      |
| On a normal school day, how many times do you take the school bus?                        | Number of times the respondent takes the school bus per day | object    | Non-negative integer                                        | 2                                   |
| On a normal school day, how long do you spend riding the school bus                       | Duration spent riding the school bus per day (in minutes)   | object    | Non-negative integer                                        | 5                                   |
| Please enter today's date.                                                                | Date                                                        | object    | Valid date format (dd-mm-yyyy)                              | 9/16/2024                           |
| Do you have an exam today?                                                                | Does the respondent have an exam that day?                  | object    | Yes, No                                                     | No                                  |
| Which bus stop did you board the bus from? (Trip 1)                                       | Trip 1: Starting bus stop                                   | object    | Bus stop names                                              | Kent Ridge MRT / Opp Kent Ridge MRT |
| Which bus stop did you alight at? (Trip 1)                                                | Trip 1: Ending bus stop                                     | object    | Bus stop names                                              | LT27 / S17                          |
| Which bus did you take? (Trip 1)                                                          | Trip 1: Bus number                                          | object    | Bus number (e.g., A1, A2, D1, D2)                           | A1                                  |
| What time of day did this trip take place? (Trip 1)                                       | Trip 1: Time of day                                         | object    | Valid time format (e.g., hh:mm am/pm)                       | 8:50:00 am                          |
| What was the weather like during your trip? (Trip 1)                                      | Trip 1: Weather                                             | object    | Sunny, Rainy                                                | Sunny                               |
| When you were boarding the bus, approximately how many people were there                  | Trip 1: Number of people at starting bus stop               | int64     | Non-negative integer                                        | 20                                  |
| How long did you have to wait for the bus? (Trip 1)                                       | Trip 1: Waiting time (in minutes)                           | object    | Non-negative integer                                        | 6 minutes                           |
| With regards to waiting time, how satisfied are you with the trip? (Trip 1)               | Trip 1: Satisfaction level for waiting time                 | int64     | 1-10 (1 being least satisfied, 10 being most satisfied)     | 7                                   |
| On a scale from 1 to 10, how crowded was the bus? (Trip 1)                                | Trip 1: Crowdedness level                                   | int64     | 1-10 (1 being least crowded, 10 being most crowded)         | 7                                   |
| With regards to crowdedness, how satisfied are you with the trip? (Trip 1)                | Trip 1: Satisfaction level for crowdedness                  | int64     | 1-10 (1 being least satisfied, 10 being most satisfied)     | 9                                   |
| On a scale from 1 to 10, how comfortable was the trip for you? (Trip 1)                   | Trip 1: Comfort level                                       | int64     | 1-10 (1 being least comfortable, 10 being most comfortable) | 7                                   |
| On a scale from 1 to 10, how safe was the trip for you? (Trip 1)                          | Trip 1: Safety level                                        | int64     | 1-10 (1 being least safe, 10 being most safe)               | 7                                   |
| On a scale from 1 to 10, how satisfied are you with the trip overall? (Trip 1)            | Trip 1: Overall satisfaction level                          | int64     | 1-10 (1 being least satisfied, 10 being most satisfied)     | 9                                   |
| Which bus stop did you board the bus from? (Trip 2)                                       | Trip 2: Starting bus stop                                   | object    | Bus stop names                                              | Kent Ridge MRT / Opp Kent Ridge MRT |
| Which bus stop did you alight at? (Trip 2)                                                | Trip 2: Ending bus stop                                     | object    | Bus stop names                                              | LT27 / S17                          |
| Which bus did you take? (Trip 2)                                                          | Trip 2: Bus number                                          | object    | Bus number (e.g., A1, A2, D1, D2)                           | A2                                  |
| What time of day did this trip take place? (Trip 2)                                       | Trip 2: Time of day                                         | object    | Valid time format (e.g., hh:mm am/pm)                       | 12:00:00 pm                         |
| What was the weather like during your trip? (Trip 2)                                      | Trip 2: Weather                                             | object    | Sunny, Rainy                                                | Sunny                               |
| When you were boarding the bus, approximately how many people were there                  | Trip 2: Number of people at starting bus stop               | object    | Non-negative integer                                        | 14                                  |
| How long did you have to wait for the bus? (Trip 2)                                       | Trip 2: Waiting time (in minutes)                           | object    | Non-negative integer                                        | 3                                   |
| With regards to waiting time, how satisfied are you with the trip? (Trip 2)               | Trip 2: Satisfaction level for waiting time                 | int64     | 1-10 (1 being least satisfied, 10 being most satisfied)     | 8                                   |
| On a scale from 1 to 10, how crowded was the bus? (Trip 2)                                | Trip 2: Crowdedness level                                   | int64     | 1-10 (1 being least crowded, 10 being most crowded)         | 6                                   |
| With regards to crowdedness, how satisfied are you with the trip? (Trip 2)                | Trip 2: Satisfaction level for crowdedness                  | int64     | 1-10 (1 being least satisfied, 10 being most satisfied)     | 7                                   |
| On a scale from 1 to 10, how comfortable was the trip for you? (Trip 2)                   | Trip 2: Comfort level                                       | int64     | 1-10 (1 being least comfortable, 10 being most comfortable) | 7                                   |
| On a scale from 1 to 10, how safe was the trip for you? (Trip 2)                          | Trip 2: Safety level                                        | int64     | 1-10 (1 being least safe, 10 being most safe)               | 6                                   |
| On a scale from 1 to 10, how satisfied are you with the trip overall? (Trip 2)            | Trip 2: Overall satisfaction level                          | int64     | 1-10 (1 being least satisfied, 10 being most satisfied)     | 8                                   |
| Are there any other factors that influence how satisfied you are with the NUS bus system? | Other factors influencing satisfaction level                | object    | Free response                                               | "Seat availability"                 |

5. `test_trip_data_after_sdv.csv`

   Similar to `cleaned_trip_data.csv`

6. `test_trip_data_before_sdv.csv`

   Similar to `cleaned_trip_data.csv`

7. `test_trip_data_before_sdv.csv`

   Similar to `cleaned_trip_data.csv`

8. `train_trip_data_after_smote.csv`

   Similar to `cleaned_trip_data.csv`
