import numpy as np
from scipy.optimize import linprog
import demand_forecasting as df

def capacity_allocation():
    # Forecasted demand as a 2D matrix: [routes x time slots]
    forecasted_demand = df.demand_forecasting()
    forecasted_demand = np.array(forecasted_demand)
    
    # Maximum bus capacity per trip
    bus_capacity = 20
    total_buses_available = 8
    
    # Dimensions of forecasted demand matrix
    num_routes, num_time_slots = forecasted_demand.shape

    # Objective function: prioritize minimizing unmet demand
    c = -forecasted_demand.flatten()  # Flatten for 1D linprog

    # Inequality constraints (total buses available)
    # For each allocation, we ensure that the total buses do not exceed the fleet size.
    A_ub = np.ones((1, num_routes * num_time_slots))
    b_ub = [total_buses_available]

    print("A_ub----------------------------------")
    print(A_ub)
    print("b_ub----------------------------------")
    print(b_ub)

    # Demand constraints: buses per route and time slot must at least meet demand
    A_demand = np.eye(num_routes * num_time_slots)
    b_demand = (forecasted_demand / bus_capacity).flatten()

    print("A_demand----------------------------------")
    print(A_demand)
    print("b_demand----------------------------------")
    print(b_demand)

    # Combine inequality constraints
    A_ub = np.vstack([A_ub, A_demand])
    b_ub = np.hstack([b_ub, b_demand])

    # Solve the linear programming problem
    result = linprog(c, A_ub=A_ub, b_ub=1.2*b_ub, method='highs')
    print(result)

    # Output the results
    # Print results
    if result.success:
        allocated_buses = result.x.reshape(num_routes, num_time_slots)
        print("Optimized Capacity Allocation (Buses per Route per Time Slot):")
        print(allocated_buses)
    else:
        print("Optimization failed:", result.message)

def main():
    capacity_allocation()

capacity_allocation()