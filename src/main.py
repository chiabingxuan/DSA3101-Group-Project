import survey_cleaning
import smote
import synthetic_data_generation_train
import synthetic_data_generation_test
import analyse_travel_patterns

if __name__ == "__main__":
    # 1. Clean the data
    survey_cleaning.main()

    # 2. Conduct train-test split, before using SMOTE to conduct oversampling on training data
    smote.main()

    # 3. Use SDV to synthesise more training data
    synthetic_data_generation_train.main()

    # 4. Use SDV to synthesise more testing data
    synthetic_data_generation_test.main()

    # 5. Analysing user satisfaction

    # 6. User segmentation

    # 7. Analyse travel patterns
    analyse_travel_patterns.main(want_overall_data=False, want_exam_day=False)
