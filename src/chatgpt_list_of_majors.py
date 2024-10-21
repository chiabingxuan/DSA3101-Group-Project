"""
    Using ChatGPT to normalise list of majors, ensuring consistency

    Prompt: 
    Consider the following list of majors offered by the National University of Singapore (NUS):

    <insert list here>

    Some of these majors are actually the same. For example, "dsa" is an abbreviation of "data science and analytics", 
    which is also the same as "data science & analytics" and “Data Science and Analytics”. 
    With reference to information that you can find regarding the names and abbreviations of NUS majors, 
    please create a mapping dictionary of this list of majors, ensuring that the same majors are mapped to the same output (all in lowercase). 
    Please put in alphabetical order, with the mapped versions collated together.
    """



major_mapping = {
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
    'adsa': 'data science and analytics',
    
    "dentistry": "dentistry",
    "faculty of dentistry": "dentistry",
    
    "economics": "economics",
    'econs' : 'economics',
    
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
    'data science n psych': 'psychology',
    
    "quantitative finance": "quantitative finance",
    
    "social work": "social work",
    
    "sociology": "sociology",
    
    "statistics": "statistics"
}
