# DSA3101 Project: Optimising Public Transport in NUS

- [DSA3101 Project: Optimising Public Transport in NUS](#dsa3101-project-optimising-public-transport-in-nus)
  - [1. Introduction](#1-introduction)
  - [2. Business Understanding](#2-business-understanding)
  - [3. Data Understanding](#3-data-understanding)
    - [3.1 Data Acquisition](#31-data-acquisition)
    - [3.2 Data Dictionary of Original Survey Data](#32-data-dictionary-of-original-survey-data)
    - [3.3 Data Quality Assessment](#33-data-quality-assessment)
  - [4. Data Preparation](#4-data-preparation)
    - [4.1 Initial Data Cleaning](#41-initial-data-cleaning)
  - [5. Modelling](#5-modelling)
  - [6. Evaluation](#6-evaluation)
  - [7. Deployment](#7-deployment)
  - [8. Technical Implementation](#8-technical-implementation)
  - [9. Analytical Findings](#9-analytical-findings)
  - [10. Recommendations](#10-recommendations)
  - [11. Future Work](#11-future-work)
  - [12. Lessons Learned](#12-lessons-learned)
  - [13. References](#13-references)
  - [14. Appendix](#14-appendix)

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
| Trip 1: Number of people at starting bus stop | object |
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

* `trips_per_day`: 4 entries that do not correspond exactly to an integer (eg. "2-3 times")
* `duration_per_day`: 26 entries that do not correspond exactly to an integer (eg. "15mins")
* `num_people_at_bus_stop`: 4 entries that do not correspond exactly to an integer (eg. "40-50")
* `waiting_time`: 6 entries that do not correspond exactly to an integer (eg. "5min")
* `time`: 16 entries which fall outside of NUS bus operating hours (eg. 1:00:00 am, might have mistakenly entered "am" instead of "pm")
* `major`: Inconsistent formatting (eg. "Data Science and Analytics" can be entered as "dsa", "DSA", "Dsa", etc.)

By calling `clean_other_feedback_data()` on `other_feedback_data`, we discovered the following issues, with regards to data quality:

* `trips_per_day`: 2 entries that do not correspond exactly to an integer
* `duration_per_day`: 13 entries that do not correspond exactly to an integer
* `major`: Inconsistent formatting

Note also that since all fields of the survey are required, there are no missing values in both `trip_data` and `other_feedback_data`. In addition, the data is taken directly from our survey results, so there are no duplicate rows in both data frames.

## 4. Data Preparation
### 4.1 Initial Data Cleaning
With this in mind, we proceed to clean both `trip_data` and `other_feedback_data` in `survey_cleaning.py`.

By calling `clean_trip_data()` on `trip_data`, we do the following:
* Rename all columns (as mentioned in 3.3: Data Quality Assessment)
* Trim whitespace for the 6 columns that require this (`major`, `main_reason_for_taking_isb`, `trips_per_day`, `duration_per_day`, `num_people_at_bus_stop` and `waiting_time`)
* Convert `trips_per_day`, `duration_per_day`, `num_people_at_bus_stop` and `waiting_time` columns to `int64` data type
  * For the 40 entries that do not correspond exactly to an integer, we only keep the first integer that appears (eg. if the entry is "15-20 minutes", we only keep "15"). Then, we convert this modified entry to `int64`
* Correct invalid times in the `time` column, converting them from "AM" to "PM" (or vice versa) where necessary
  * Modiifed 16 entries
* Use a `MAPPINGS` dictionary to standardise the formatting of the `major` column
  * Modified 492 entries
* Remove rows corresponding to invalid bus trips
  * Removed 1 row where `start` and `end` are the same
  * Removed 42 rows where `bus_num` is not serviced in either `start` or `end`

By calling `clean_other_feedback_data()` on `other_feedback_data`, we do the following:
* Rename all columns (as mentioned in 3.3: Data Quality Assessment)
* Trim whitespace for the 6 columns that require this (`major`, `main_reason_for_taking_isb`, `trips_per_day`, `duration_per_day` and `feedback`)
* Convert `trips_per_day` and `duration_per_day` columns to `int64` data type
  * For the 15 entries that do not correspond exactly to an integer, we only keep the first integer that appears. Then, we convert this modified entry to `int64`
* Use a `MAPPINGS` dictionary to standardise the formatting of the `major` column
  * Modified 246 entries

## 5. Modelling

## 6. Evaluation

## 7. Deployment

## 8. Technical Implementation

## 9. Analytical Findings

## 10. Recommendations

## 11. Future Work

## 12. Lessons Learned

## 13. References

## 14. Appendix