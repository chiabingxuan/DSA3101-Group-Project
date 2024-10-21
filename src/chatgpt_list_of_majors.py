"""
    Using ChatGPT to normalise list of majors, ensuring consistency

    Prompt: 
    Consider the following list of majors offered by the National University of Singapore (NUS):

    <insert list here>

    Some of these majors are actually the same. For example, "dsa" is an abbreviation of "data science and analytics", which is also the same as "data science & analytics" and “Data Science and Analytics”. With reference to information that you can find regarding the names and abbreviations of NUS majors, please carry out a one-to-one mapping of this list of majors, ensuring that the same majors are mapped to the same output (all in lowercase). Do the mapping element-wise, returning a Python list of strings. Since the mapping is one-to-one, the length of the list should not change.
    """

[
    'data science and analytics', 'data science and analytics', 'data science and analytics', 'data science and analytics', 
    'data science and analytics', 'data science and analytics', 'data science and analytics', 'environmental studies', 
    'computer science', 'data science and analytics', 'life sciences', 'business', 'dentistry', 'dentistry', 
    'data science and analytics', 'data science and analytics', 'data science and analytics', 'life sciences', 
    'nursing', 'data science and analytics', 'business', 'social work', 'data science and analytics', 'nursing', 
    'data science and analytics', 'data science and analytics', 'data science and analytics', 'data science and analytics', 
    'data science and analytics', 'computer science', 'life sciences', 'faculty of dentistry', 'geography', 
    'geography', 'political science', 'psychology', 'computer science', 'data science and analytics', 
    'data science and analytics', 'data science and analytics', 'mathematics', 'chemistry', 'law', 
    'data science and analytics', 'computer science', 'data science and analytics', 'data science and analytics', 
    'data science and analytics', 'data science and analytics', 'data science and analytics', 'sociology', 
    'data science and analytics', 'data science and analytics', 'data science and analytics', 'computer science', 
    'computer science', 'computer science', 'economics', 'data science and analytics', 'data science and analytics', 
    'data science and analytics', 'data science and analytics', 'history', 'data science and analytics', 
    'data science and analytics', 'mechanical engineering', 'data science and analytics', 'materials science and engineering', 
    'political science', 'malay studies', 'global studies', 'anthropology', 'life sciences', 'geography', 'pharmaceutical science', 
    'economics', 'data science and analytics', 'life sciences', 'data science and analytics', 'nursing', 'history', 
    'life sciences', 'engineering', 'biomedical engineering', 'quantitative finance', 'environmental science', 'psychology', 
    'data science and analytics', 'statistics', 'materials science and engineering', 'materials science and engineering', 
    'environmental science', 'data science and analytics', 'data science and analytics', 'life sciences', 
    'data science and analytics', 'sociology', 'anthropology', 'environmental science', 'data science and analytics', 
    'economics', 'economics', 'sociology', 'data science and analytics', 'data science and analytics', 
    'business analytics', 'chemistry', 'mathematics', 'psychology', 'life sciences', 'data science and analytics', 
    'chemistry', 'architecture', 'life sciences', 'food science and technology', 'mathematics', 'law', 
    'dentistry', 'dentistry', 'nursing', 'food science and technology', 'data science and analytics', 'biomedical engineering', 
    'sociology', 'social work', 'anthropology', 'life sciences', 'malay studies', 'global studies', 
    'political science', 'nursing', 'data science and analytics', 'geography', 'statistics', 'materials science and engineering', 
    'economics', 'sociology', 'environmental science', 'chemistry', 'computer science', 'computer science', 
    'chemistry', 'computer science', 'chemistry', 'social work', 'social work', 'chemistry', 'history', 
    'life sciences', 'architecture', 'biomedical engineering', 'quantitative finance', 'politics, philosophy, economics', 
    'political science'
]
