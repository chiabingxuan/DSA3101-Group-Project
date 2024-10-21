"""
possible reasons on unclean / unstandardised data:
- Removing special characters.
- Standardizing capitalization (lowercase or title case depending on preference).
- Correcting common misspellings.
- Removing extra spaces between words.

code from chatgpt
"""

import re
import test_case as test

def clean_major(majors):

    # Step 1: Dictionary to get the mappings
    mappings = {
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
    'ppe-xdp': 'politics, philosophy, economics',
    'econs' : 'economics' 
    }

    # Step 2: Initiate a empty list to append cleaned majors 
    cleaned_majors = []

    # Step 3: Iterate through the responses to clean
    for major in majors:
        major = major.lower()
    
        # Step 4: Replace using the mapping dictionary, if applicable
        cleaned_major = mappings.get(major, major)  # Use the original field if not found in mapping
        
        # Step 5: Capitalise each word
        cleaned_major = cleaned_major.title()

        # Step 6: Append into the empty list
        cleaned_majors.append(cleaned_major)

    """
    # Step 3: Apply known corrections
    for wrong, right in mappings.items():
        major = re.sub(wrong, right, major)

    major = re.sub(r'([a-z])([A-Z])', r'\1 \2', major)
    
    # Step 4: Remove special characters
    major = re.sub(r'[^a-z\s]', '', major)
    
    # Step 5: Replace multiple spaces with a single space
    major = re.sub(r'\s+', ' ', major).strip()
    
    # 
    """

    print(cleaned_majors)
    return cleaned_majors

# Test case
cleaned_majors = clean_major(test.fields_of_study)