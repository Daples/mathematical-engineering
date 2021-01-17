from ioData import read_data, print_routes, plot_routes
from ga import hybrid_ga, hybrid_ga_vnd
from sweepHCCVRP import sweep, of
import matplotlib.pyplot as plt
import time

# outfile = open('ga.csv', 'w')

for i in range(1, 2):
    print('dataset:', i)

    if i == 17 or i == 20:
        continue

    # Read data set
    vehicles, nodes = read_data(i)

    # GA
    # tb = time.time()
    sol = sweep(vehicles, nodes)
    z = of(vehicles, nodes, sol)
    sol_ga, z_ga = hybrid_ga_vnd(nodes, vehicles)
    for i in sol_ga:
        print(i)

    print('constructive:', z)
    print('hybrid:', z_ga)
    f = 1
    f = plot_routes(f, sol, nodes, 'Construction')
    f = plot_routes(f, sol_ga, nodes, 'Hybrid')
    plt.show()
    # ta = time.time()
    # exec_time = str(round(ta - tb, 2))

    # outfile.write(str(i) + ',' + str(len(nodes['index']))  + ',' + exec_time + ',' + str(round(z_ga, 2)) + '\n')
    # print_routes(i, vehicles, nodes, sol_ga, 'hybrid')

# outfile.close()
