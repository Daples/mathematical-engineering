from sweepHCCVRP import sweep, of
from ioData import read_data, print_routes, plot_routes
from local_search import two_opt, simulated_annealing, one_one_exchange, vnd, move, swap
import matplotlib.pyplot as plt
import os
import time


# current_folder = os.getcwd()
# out_folder = os.path.join(current_folder, 'HFCCVRP_sol')
#
# if not os.path.isdir(out_folder):
#     os.mkdir(out_folder)
#
file_name = 'vnd.csv'
# file_name = os.path.join(current_folder, 'HFCCVRP_sol', file_name)
output_file = open(file_name, 'w')

for i in range(1, 22):
    print(i)
    f = 0
    # Read data set
    vehicles, nodes = read_data(i)

    # Constructive Algorithm
    sol = sweep(vehicles, nodes)
    z = of(vehicles, nodes, sol)
    # print('Sweep: ' + str(round(z, 2)))
    f = plot_routes(f, sol, nodes, 'Sweep')

    # print(test(sol, nodes, vehicles))

    # # 2 Opt
    # sol_two_opt = two_opt(sol, nodes)
    # z_two_opt = of(vehicles, nodes, sol_two_opt)
    # print('2-opt: ' + str(round(z_two_opt, 2)))
    # # f = plot_routes(f, sol_two_opt, nodes, '2-Opt')

    # swap in-route
    # sol_swap, z_swap = swap(sol, nodes, vehicles, z)
    # print('swap: ' + str(z_swap))
    # f = plot_routes(f, sol_swap, nodes, 'Move')
    # plt.show()

    # Move in-route
    # sol_move, z_move = move(sol, nodes, vehicles, z)
    # print('move: ' + str(z_move))
    # f = plot_routes(f, sol_move, nodes, 'Move')
    # plt.show()

    # # 1-1 Exchange
    # sol_1_1_exchange, z_1_1 = one_one_exchange(sol, nodes, vehicles, z)
    # print('1-1 Exchange: ' + str(round(z_1_1, 2)))
    # # f = plot_routes(f, sol_1_1_exchange, nodes, '1-1 Exchange')

    # Simulated Annealing
    # time_prev = time.clock()
    # sol_annealing, z_annealing = simulated_annealing(sol, nodes, vehicles, z)
    # time_aft = time.clock()
    # print('Simulated Annealing: ' + str(round(z_annealing, 2)))
    # f = plot_routes(f, sol_annealing, nodes, 'Simulated Annealing')

    # VND
    # time_prev = time.clock()
    # sol_vnd, z_vnd = vnd(sol, nodes, vehicles, z)
    # time_aft = time.clock()
    # print('VND: ' + str(round(z_vnd, 2)))
    # f = plot_routes(f, sol_vnd, nodes, 'VND')
    plt.show()

    # Output data
    # print_routes(i, vehicles, nodes, sol)

    # percent = str(round(100 * (z - z_vnd) / z, 2))
    # exec_time = str(round(time_aft - time_prev, 2))
    # output_file.write(str(i) + ',' + str(len(nodes['index'])) + ',' + percent + ',' + str(exec_time) + ',' + str(round(z,2)) + ',' + str(round(z_vnd,2)) + '\n')

output_file.close()
