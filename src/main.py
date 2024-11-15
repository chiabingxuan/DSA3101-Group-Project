from .survey_cleaning import main as survey_cleaning_main
from .smote import main as smote_main
from .synthetic_data_generation_train import main as synthetic_data_generation_train_main
from .synthetic_data_generation_test import main as synthetic_data_generation_test_main
from .drivers_of_satisfaction import main as drivers_of_satisfaction_main
from .analyse_travel_patterns import main as analyse_travel_patterns_main
from .predict_disruption_impact import main as predict_disruption_impact_main
from .demand_forecasting import main as demand_forecasting_main
from .demand_forecast_visualisation import main as demand_forecast_visualisation_main
from .User_Segmentation_Model import main as User_Segmentation_Model_main
from .Route_Optimisation import main as Route_Optimisation_main
from .Simulation_Of_System_Efficiency_and_User_Satisfaction import main as Simulation_Of_System_Efficiency_and_User_Satisfaction_main
from .capacity_allocation import main as capacity_allocation_main

if __name__ == "__main__":
    # 1. Clean the data
    print("-------------------------- Run survey_cleaning.py --------------------------\n")
    survey_cleaning_main()

    # 2. Conduct train-test split, before using SMOTE to conduct oversampling on training data
    print("-------------------------- Run smote.py --------------------------\n")
    smote_main()

    # 3. Use SDV to synthesise more training data
    print("-------------------------- Run synthetic_data_generation_train.py --------------------------\n")
    synthetic_data_generation_train_main()

    # 4. Use SDV to synthesise more testing data
    print("-------------------------- Run synthetic_data_generation_test.py --------------------------\n")
    synthetic_data_generation_test_main()

    # 5. Analysing user satisfaction
    print("-------------------------- Run drivers_of_satisfaction.py --------------------------\n")
    drivers_of_satisfaction_main()

    # 6. User segmentation
    print("-------------------------- Run User_Segmentation_Model.py --------------------------\n")
    User_Segmentation_Model_main()

    # 7. Analyse travel patterns
    print("-------------------------- Run analyse_travel_patterns.py --------------------------\n")
    analyse_travel_patterns_main()

    # 8. Predicting impact of bus disruptions
    print("-------------------------- Run predict_disruption_impact.py --------------------------\n")
    predict_disruption_impact_main()

    # 9. Demand forecasting
    print("-------------------------- Run demand_forecasting.py --------------------------\n")
    demand_forecasting_main()

    # 10. Demand forecasting visualisation
    print("-------------------------- Run demand_forecast_visualisation.py --------------------------\n")
    demand_forecast_visualisation_main()

    # 11. Route optimisation
    print("-------------------------- Run Route_Optimisation.py --------------------------\n")
    Route_Optimisation_main()

    # 12. Simulating system efficiency and user satisfaction
    print("-------------------------- Run Simulation_Of_System_Efficiency_and_User_Satisfaction.py --------------------------\n")
    Simulation_Of_System_Efficiency_and_User_Satisfaction_main()
    
    # 13. Capacity allocation
    print("-------------------------- Run capacity_allocation.py --------------------------\n")
    capacity_allocation_main()