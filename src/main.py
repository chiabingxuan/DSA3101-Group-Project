import survey_cleaning
import smote
import synthetic_data_generation_train
import synthetic_data_generation_test
import drivers_of_satisfaction
import analyse_travel_patterns
import demand_forecasting
import User_Segmentation_Model
import Route_Optimization
import capacity_allocation

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
    drivers_of_satisfaction.main()

    # 6. User segmentation
    User_Segmentation_Model.main()

    # 7. Analyse travel patterns
    analyse_travel_patterns.main()

    # 8. Demand forecasting
    demand_forecasting.main()

    # 9. Route optimisation
    Route_Optimization.main()

    # 10. Capacity allocation
    capacity_allocation.main()
