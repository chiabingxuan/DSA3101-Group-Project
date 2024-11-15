import survey_cleaning
import smote
import synthetic_data_generation_train
import synthetic_data_generation_test
import drivers_of_satisfaction
import analyse_travel_patterns
import predict_disruption_impact
import demand_forecasting
import User_Segmentation_Model
import Route_Optimisation
import Simulation_Of_System_Efficiency_and_User_Satisfaction
import capacity_allocation

if __name__ == "__main__":
    # 1. Clean the data
    print("-------------------------- Run survey_cleaning.py --------------------------")
    survey_cleaning.main()

    # 2. Conduct train-test split, before using SMOTE to conduct oversampling on training data
    print("-------------------------- Run smote.py --------------------------")
    smote.main()

    # 3. Use SDV to synthesise more training data
    print("-------------------------- Run synthetic_data_generation_train.py --------------------------")
    synthetic_data_generation_train.main()

    # 4. Use SDV to synthesise more testing data
    print("-------------------------- Run synthetic_data_generation_test.py --------------------------")
    synthetic_data_generation_test.main()

    # 5. Analysing user satisfaction
    print("-------------------------- Run drivers_of_satisfaction.py --------------------------")
    drivers_of_satisfaction.main()

    # 6. User segmentation
    print("-------------------------- Run User_Segmentation_Model.py --------------------------")
    User_Segmentation_Model.main()

    # 7. Analyse travel patterns
    print("-------------------------- Run analyse_travel_patterns.py --------------------------")
    analyse_travel_patterns.main()

    # 8. Predicting impact of bus disruptions
    print("-------------------------- Run predict_disruption_impact.py --------------------------")
    predict_disruption_impact.main()

    # 9. Demand forecasting
    print("-------------------------- Run demand_forecasting.py --------------------------")
    demand_forecasting.main()

    # 10. Route optimisation
    print("-------------------------- Run Route_Optimisation.py --------------------------")
    Route_Optimisation.main()

    # 11. Simulating system efficiency and user satisfaction
    print("-------------------------- Run Simulation_Of_System_Efficiency_and_User_Satisfaction.py --------------------------")
    Simulation_Of_System_Efficiency_and_User_Satisfaction.main()
    
    # 12. Capacity allocation
    print("-------------------------- Run capacity_allocation.py --------------------------")
    capacity_allocation.main(run_allocation = True)
