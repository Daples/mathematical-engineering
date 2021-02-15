from sweepHCCVRP import sweep, of
from lowerBoundHCCVRP import lower_bound_vrp
from ioData import read_data, print_routes


for i in range(1, 22):
    # Read data set
    vehicles, nodes = read_data(i)

    # Calculate lower bound
    lb = lower_bound_vrp(nodes, vehicles)

    # Constructive Algorithm
    sol = sweep(vehicles, nodes)

    # Calculate Objective Function
    z = of(vehicles, nodes, sol)

    # Output data
    print_routes(i, vehicles, nodes, sol)

