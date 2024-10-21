"""
possible reasons on unclean / unstandardised data:
- Removing special characters.
- Standardizing capitalization (lowercase or title case depending on preference).
- Correcting common misspellings.
- Removing extra spaces between words.

code from chatgpt
"""

import re
import test_case

def clean_major(major):

    # Step 1: Convert to lowercase for normalization
    major = major.lower()
    
    # Step 2: Replace common misspellings and variants
    """
    corrections = {
        #'datsci': 'data science',
        #'datscience': 'data science',
        #'data scienceanaly': 'data science and analytics',
        #'analytizs': 'analytics',
        #'mat.erial': 'material',
        #'engin!': 'engineering',
        #'psychology': 'psychology',
        #'soc iology': 'sociology',
        #'enviromental': 'environmental',
        #'life sciences': 'life sciences',
        #'computer science': 'computer science',
        #'politi cal': 'political',
        
        'data science & analytics': 'data science and analytics',
        'dsa': 'data science and analytics',
        'cs': 'computer science',
        'sci': 'science',
        'data science': "data science and analytics",
        'faculty of dentistry': 'dentistry',
        'eve': 'environmental engineering',
        'psych': 'psychology',
        'engineering - material science and engineering': 'material science and engineering',
        'data science n psych': 'psychology',
        'bza': 'business analytics',
        'chem': 'chemistry',
        'fst': 'food science and technology',
        'ise': 'industrial systems engineering',
        'analytics!': 'analytics',
        'adsa': 'data science and analytics',
        'material science & engineering' : 'material science and engineering',
        'PPE-XDP': 'politics, philosophy, economics' 
        
    } """


    # Step 3: Apply known corrections
    for wrong, right in corrections.items():
        major = re.sub(wrong, right, major)

    major = re.sub(r'([a-z])([A-Z])', r'\1 \2', major)
    
    # Step 4: Remove special characters
    major = re.sub(r'[^a-z\s]', '', major)
    
    # Step 5: Replace multiple spaces with a single space
    major = re.sub(r'\s+', ' ', major).strip()
    
    # Step 6: Capitalize each word (Title Case)
    major = major.title()
    
    return major
    
    
# Clean the unclean data
"""
unclean_majors = [
    'DataScienceandAnalytics ', 'dataScIENCEANDanalytics', ' data science and analyzics',
    'data!science an@alytics', 'data  science and ANALYTICS', 'data_science_and_analytics',
    'life SCIENCEs', 'data sc1ence & analytics', 'life Scienc es', 'Nursing',
    ' data Science andanalytics', 'datasci ence & analytics', 'data-science/ analytics',
    'social-work', 'BusinessAdministration ', 'DataScienceAn@lytics', 'Data  Science And Analytics ',
    'nursing!', 'data-science  andanalytics', 'data  science   and analytics', 'data@science/analytics',
    'data scienceanaly Tics', 'data_sciENCE analytics', 'computer  science', 'life-sciences!',
    'dent!stry', 'geoGRaphy', 'Geography', 'politiCalScienCe', 'psychology ', 'computerscience',
    'bUSiness ', 'Data Science & analytics', 'EnviRonmentalstudies', ' data Science + Analytics',
    'Dentistry ', 'DENTISTRY', 'Data-Science &Analytics', 'Data Science +An@lytics', 'mathemat ics',
    'DATA SCIENCEANDanalytics ', 'data science/ analytics', 'law!', 'Data.Science +analytics',
    ' Data  scienceanalytics', 'CompuTER ScIENCe', 'CheMISTRY', 'd@ta science analytics',
    'Data_sciencean@lytics', 'DATA SCIENCE&Analytics', 'data S C IENCE analytics', 'sociol ogy',
    ' data-science AndAnAlytics ', 'Computerscience', 'D@taScience &Analytics', 'datscienceanaly@tics',
    'computer SCIENCE', 'CoMPUTER-SCIENCE', 'computer   science', 'EcoNOMICS', 'history ',
    'datascienceandalytics!', 'Datsci enceanalytics', 'mechanIcal engineering', 'data scienceAnd analytics',
    'data Science and ANALYTICS', 'matEriAls science & engineering', 'Political science', 'MalayStud ies',
    'Global Studies', 'Anthropo logy', 'AccOuntancy', 'Lifes CIENCES', 'geoGRaphy ', 'PharmaceuticalScience!',
    'econom ics', 'Nurs ing', ' History', 'LIFEsciences ', 'ENGineering', 'biomedicalENGINEERING',
    'Quantitative-fin@ance', 'DATSceinceandanalytics ', 'Enviromental Studies', 'life sciencEs', 'psy chology',
    'DataScience ANALYTICS', 'stat!stics', 'Eng ineering -mat.erial science ', 'Material-Science &Eng!',
    'data-science and_analytics', 'data_science @analytics', 'l!fe sciences', 'DataSCIEnce_n_psychology',
    'datascience and analytic s', 'data-SCIENCE! analytics', 'econ OMICS', 'economics', 'socIOlogy',
    'Data_Sci_en_analytics', 'SOcIOlogy', 'datscienceanalytics', 'AnthroPOlogy'
]


# Apply the cleaning function to each major
cleaned_majors = [clean_major(major) for major in unclean_majors]

# Display cleaned majors
print(cleaned_majors)
"""

#testcase_clean = [clean_major(major) for major in test_case.fields_of_study]
#print(testcase_clean)

# Clean the data
cleaned_fields = []
for field in test_case:
    # Replace using the mapping dictionary, if applicable
    cleaned_field = mapping.get(field, field)  # Use the original field if not found in mapping
    cleaned_fields.append(cleaned_field)

# Print the cleaned list
print(cleaned_fields)

