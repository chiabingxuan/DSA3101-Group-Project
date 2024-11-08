import numpy as np
from scipy.optimize import linprog
import demand_forecasting as df

def capacity_allocation():

    # Import forecasted demand
    forecasted_demand = df.demand_forecasting()
    forecasted_demand = np.array(forecasted_demand) # Make into an array

    # Dimensions of forecasted demand matrix
    num_routes, num_time_slots = forecasted_demand.shape # To preserve shape

    ### ---------- CONSTRAINTS ---------- ###

    num_boarded = 20 # Ave number of people that can board the bus
    total_buses_available = 20 * num_routes * num_time_slots

    # Objective function: prioritize minimizing unmet demand
    c = -forecasted_demand.flatten()  # Flatten for 1D linprog

    # INEQUALITY CONSTRAINTS

    # For each allocation, we ensure that the total buses do not exceed the fleet size.
    A_ub = np.ones((1, num_routes * num_time_slots))
    b_ub = [total_buses_available]

    print("A_ub----------------------------------")
    print(A_ub)
    print("b_ub----------------------------------")
    print(b_ub)

    # Demand constraints: buses per route and time slot must at least meet demand
    A_demand = np.eye(num_routes * num_time_slots)
    b_demand = (forecasted_demand / num_boarded).flatten()

    print("A_demand----------------------------------")
    print(A_demand)
    print("b_demand----------------------------------")
    print(b_demand)

    # Combine inequality constraints
    A_ub = np.vstack([A_ub, A_demand])
    b_ub = np.hstack([b_ub, b_demand])

    # Solve the linear programming problem
    result = linprog(c, A_ub = A_ub, b_ub = 1.2 * b_ub, method = 'highs') # *1.2 to allow flexibility
    print(result)

    # Output the results
    # Print results
    if result.success:
        allocated_buses = result.x.reshape(num_routes, num_time_slots)

        # Round up the values in the result array
        allocated_buses_rounded = np.ceil(allocated_buses)

        print("Optimized Capacity Allocation (Buses per Route per Time Slot):")
        print(allocated_buses_rounded)
    else:
        print("Optimization failed:", result.message)

def main():
    capacity_allocation()

capacity_allocation()