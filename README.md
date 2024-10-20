# DSA3101 Project: Optimising Public Transport in NUS

- [DSA3101 Project: Optimising Public Transport in NUS](#dsa3101-project-optimising-public-transport-in-nus)
  - [1. Introduction](#1-introduction)
  - [2. Business Understanding](#2-business-understanding)
  - [3. Data Understanding](#3-data-understanding)
  - [4. Data Preparation](#4-data-preparation)
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

We collected survey data to investigate the travel patterns and satisfaction levels of NUS students, with regards to the NUS bus system. In our survey, respondents were asked to share **two bus trips** that they embarked on for the day. The [survey link](https://docs.google.com/forms/d/1zh5M9Sccn3ifxcOOJd2UMj7cQSFKPWmvD-RG1PZA9QM/edit) was circulated online on various NUS platforms, including the official Telegram channel for the NUS College of Humanities and Sciences.

From our survey, we are able to obtain tabular data in the form of a CSV file, `survey.csv`. Each row of the CSV file corresponds to a single survey response (two bus trips). In `survey_cleaning.py`, we load the CSV file into a `pandas.DataFrame`, `survey_data`. The data dictionary for `survey_data` is shown below. Given that the column names are rather long, a short description of each attribute is provided instead. Note that all attributes are required.

| Description of Attribute | Data Type |
| :---:   | :---: |
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
| Trip 2: Number of people at starting bus stop | int64 |
| Trip 2: Waiting time (in minutes) | object |
| Trip 2: Satisfaction level for waiting time | int64 |
| Trip 2: Crowdedness level | int64 |
| Trip 2: Satisfaction level for crowdedness | int64 |
| Trip 2: Comfort level | int64 |
| Trip 2: Safety level | int64 |
| Trip 2: Overall satisfaction level | int64 |
| Other factors influencing satisfaction level | object |

From the above, there are some numerical attributes which are being assigned the `object` data type instead, such as "Trip 1: Waiting time (in minutes)". This means that there are some problematic survey inputs for these attributes, which `pandas` cannot convert to the `int64` data type. Hence, some cleaning has to be done.

## 4. Data Preparation

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