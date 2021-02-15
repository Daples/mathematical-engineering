from sweepHCCVRP import sweep, of
from ioData import read_data, print_routes
from local_search import simulated_annealing,  vnd


for i in range(1, 2):
    print(i)
    # Read data set
    vehicles, nodes = read_data(i)

    # Constructive Algorithm
    sol = sweep(vehicles, nodes)
    z = of(vehicles, nodes, sol)
    print(z)
    # print_routes(i, vehicles, nodes, sol, 'constructive')

    # Simulated Annealing
    sol_annealing, z_annealing = simulated_annealing(sol, nodes, vehicles, z)
    print(z_annealing)
    # print_routes(i, vehicles, nodes, sol_annealing, 'annealing')


    # VND
    sol_vnd, z_vnd = vnd(sol, nodes, vehicles, z)
    print(z_vnd)
    # print_routes(i, vehicles, nodes, sol_vnd, 'vnd')
