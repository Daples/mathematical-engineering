from ioData import read_data, print_routes
from ga import hybrid_ga


for i in range(1, 22):
    if i == 17 or i == 20:
        continue

    # Read data set
    vehicles, nodes = read_data(i)

    # GA
    sol_ga, z_ga = hybrid_ga(nodes, vehicles)

    print_routes(i, vehicles, nodes, sol_ga, 'hybrid')
