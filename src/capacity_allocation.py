
import numpy as np
from scipy.optimize import linprog

#################################################################################
### Objective of model: Minimise unmet demand                                 ###
### Constraints: Total buses cannot exceed maximum number of buses            ###
### Decision variable: Number of buses allocated for each route and time slot ###
#################################################################################

# Maximum bus capacity per trip
bus_capacity = 50

# Maximum number of buses we have to allocate
max_buses = 50

# Flatten the demand_forecast matrix to work with linear programming
(num_routes, num_time_slots) = demand_forecast.shape
flattened_demand = demand_forecast.flatten()

# Unmet Demand = Forecasted Demand - Bus Capacity
objective_coeffs = -flattened_demand  # Using negative demand to maximize service in linprog

### Setting up constraints ###

# Equality constraint (requires condition to hold exactly):
# Total number of buses
A_eq = np.ones((1, num_routes * num_time_slots))
b_eq = [max_buses]
# This means: 1 x1 + 1 x2 + ... + 1 xn = max_buses

# Inequality constraint (allows for a range of possible values)
# Individual demand at each route-time slot
A_ub = np.eye(num_routes * num_time_slots)
b_ub = flattened_demand  # Upper bounds on demand per route per time slot
# This means: x1 <= d1 ; x2 <= d2 ; ... ; xn <= dn

# Setting up bounds for decision variables (buses allocated) (>= 0 & <= required demand)
bounds = [(0, bus_capacity)] * (num_routes * num_time_slots)
# Ensures each allocation (per route per time slot) does not exceed bus capacity

# Run the linear programming optimization
result = linprog(c = objective_coeffs, A_eq = A_eq, b_eq = b_eq, A_ub = A_ub, b_ub = b_ub, bounds = bounds, method = "highs")

# Print results
if result.success:
    allocated_buses = result.x.reshape(num_routes, num_time_slots)
    print("Optimized Capacity Allocation (Buses per Route per Time Slot):")
    print(allocated_buses)
else:
    print("Optimization failed:", result.message)
