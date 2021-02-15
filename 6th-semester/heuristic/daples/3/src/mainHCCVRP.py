from ioData import read_data, print_routes
from local_search import vnd_noise
from grasp import of, grasp
from sweepHCCVRP import sweep


for i in range(1, 22):
    # Read data set
    vehicles, nodes = read_data(i)

    # Constructive Algorithm
    sol = sweep(vehicles, nodes)
    z = of(vehicles, nodes, sol)
    print_routes(i, vehicles, nodes, sol, 'constructive')

    # GRASP
    if i != 17 and i != 20:
        sol_grasp, z_grasp = grasp(nodes, vehicles)
        print_routes(i, vehicles, nodes, sol_grasp, 'grasp')

    # VND Noise
    sol_vnd, z_vnd = vnd_noise(sol, nodes, vehicles, z)
    print_routes(i, vehicles, nodes, sol_vnd, 'vnd_noise')

