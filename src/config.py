import datetime

# 1. survey_cleaning.py
"""
Possible reasons on unclean / unstandardised data:
- Removing special characters.
- Standardising capitalisation (lowercase or title case depending on preference).
- Correcting common misspellings.
- Removing extra spaces between words.

Using ChatGPT to generate a mapping (dictionary) that normalises list of majors, ensuring consistency

Prompt: 
Consider the following list of majors offered by the National University of Singapore (NUS):

<insert list here>

Some of these majors are actually the same. For example, "dsa" is an abbreviation of "data science and analytics", 
which is also the same as "data science & analytics" and “Data Science and Analytics”. 
With reference to information that you can find regarding the names and abbreviations of NUS majors, 
please create a mapping dictionary of this list of majors, ensuring that the same majors are mapped to the same output (all in lowercase). 
Please put in alphabetical order, with the mapped versions collated together.
"""

MAJOR_MAPPING = {
    "accountancy": "accountancy",
    "architecture": "architecture",
    "anthropology": "anthropology", 
    "biomedical engineering": "biomedical engineering", 
    "bza": "business analytics",
    "business analytics": "business analytics", 
    "business": "business",
    "business administration": "business",
    "chemistry": "chemistry",
    "chem": "chemistry", 
    "computer science": "computer science",
    "cs": "computer science",  
    "data science": "data science and analytics",
    "data science & analytics": "data science and analytics",
    "data science and analytics": "data science and analytics",
    "dsa": "data science and analytics",
    "data science and analytics!": "data science and analytics",
    "data science and analtytics": "data science and analytics",
    "adsa": "data science and analytics", 
    "dentistry": "dentistry",
    "faculty of dentistry": "dentistry",
    "economics": "economics",
    "econs" : "economics",
    "engineering": "mechanical engineering", # edge case  
    "engineering - material science and engineering": "materials science and engineering",
    "materials science and engineering": "materials science and engineering",
    "material science & engineering": "materials science and engineering",   
    "environmental science": "environmental studies",  
    "environmental studies": "environmental studies",
    "eve": "environmental engineering",  
    "food science and technology": "food science and technology",
    "fst": "food science and technology",  
    "geography": "geography",
    "global studies": "global studies",
    "history": "history",
    "industrial systems engineering": "industrial systems engineering",
    "ise": "industrial systems engineering",  
    "law": "law",
    "life sci": "life sciences",
    "life science": "life sciences",
    "life sciences": "life sciences",
    "malay studies": "malay studies",
    "mathematics": "mathematics",
    "mechanical engineering": "mechanical engineering",  
    "nursing": "nursing",   
    "pharmaceutical science": "pharmaceutical science",
    "political science": "political science",
    "political sciences": "political science",
    "politics, philoshopy, economics": "politics, philosophy, economics",
    "ppe-xdp": "politics, philosophy, economics",
    "psych": "psychology",
    "psychology": "psychology",
    "data science n psych": "psychology", # Edge case, a mixture of 2 majors
    "data science n psychology": "psychology",
    "quantitative finance": "quantitative finance",
    "quantitate finance": "quantitative finance",
    "quantitave finance": "quantitative finance",
    "social work": "social work",
    "sociology": "sociology",
    "statistics": "statistics"
}

BUS_NUMS_OF_BUS_STOPS = {
        "Kent Ridge MRT / Opp Kent Ridge MRT": ["A1", "A2", "D2"],
        "LT27 / S17": ["A1", "A2", "D2"],
        "UHC / Opp UHC": ["A1", "A2", "D2"],
        "UTown": ["D1", "D2", "E"],
        "COM3": ["D1", "D2"],
        "BIZ2 / Opp HSSML": ["A1", "A2", "D1"],
        "LT13 / Ventus": ["A1", "A2", "D1"],
        "IT / CLB": ["A1", "A2", "D1", "E"],
        "PGP": ["A1", "A2", "D2"]
}

FIRST_BUS_TIME, LAST_BUS_TIME = datetime.time(hour=7, minute=0), datetime.time(hour=23, minute=0) # just general operating hours for now (7 am - 11 pm), we can change this in the future if we want

# 2. synthetic_data_generation_train.py
NUM_NEW_ROWS_SYNTHESISED_TRAIN = 2000

# 3. synthetic_data_generation_test.py
NUM_NEW_ROWS_SYNTHESISED_TEST = 1160

# 4. analyse_travel_patterns.py
NUS_COORDINATES = (1.2975, 103.7764)

BUS_STOP_COORDINATES = {
    "Kent Ridge MRT / Opp Kent Ridge MRT": (1.2949169774094218, 103.78450347558939),
    "LT27 / S17": (1.2974629302644196, 103.78085273302771),
    "UHC / Opp UHC": (1.2988678848068846, 103.7759206887556),
    "UTown": (1.3035493102220883, 103.7745363670092),
    "COM3": (1.2949516906131686, 103.77494690050855),
    "BIZ2 / Opp HSSML": (1.2931431812053542, 103.7750819279268),
    "LT13 / Ventus": (1.2952473123850663, 103.77060867365277),
    "IT / CLB": (1.296984108396615, 103.77264737349888),
    "PGP": (1.2914385089186413, 103.78047445708181)
}

BUS_NUM_COLOURS = {
    "A1": "red",
    "A2": "yellow",
    "D1": "pink",
    "D2": "purple"
}

BUS_NUM_ROUTES = {
    "A1": ["LT13 / Ventus", "BIZ2 / Opp HSSML", "PGP", "Kent Ridge MRT / Opp Kent Ridge MRT", "LT27 / S17", "UHC / Opp UHC", "IT / CLB", "LT13 / Ventus"],
    "A2": ["IT / CLB", "UHC / Opp UHC", "LT27 / S17", "Kent Ridge MRT / Opp Kent Ridge MRT", "PGP", "BIZ2 / Opp HSSML", "LT13 / Ventus", "IT / CLB"],
    "D1": ["COM3", "BIZ2 / Opp HSSML", "LT13 / Ventus", "IT / CLB", "UTown", "IT / CLB", "LT13 / Ventus", "BIZ2 / Opp HSSML", "COM3"],
    "D2": ["COM3", "PGP", "Kent Ridge MRT / Opp Kent Ridge MRT", "LT27 / S17", "UHC / Opp UHC", "UTown", "UHC / Opp UHC", "LT27 / S17", "Kent Ridge MRT / Opp Kent Ridge MRT", "PGP", "COM3"]
}

BUS_STOP_NAMES = list(BUS_STOP_COORDINATES.keys())
