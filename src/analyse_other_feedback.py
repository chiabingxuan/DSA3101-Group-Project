import pandas as pd
import numpy as np
import os


if __name__ == "__main__":
    other_feedback_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "../data/cleaned_survey_other_feedback_data.csv"), keep_default_na=False)
