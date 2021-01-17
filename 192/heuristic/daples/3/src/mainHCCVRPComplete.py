from ioData import read_data, print_routes
from local_search import vnd_noise
from grasp import of, of_by_routes, grasp
from sweepHCCVRP import sweep
import time

file_name_grasp = 'grasp.csv'
file_name_vnd = 'vnd_noise.csv'
outfile_grasp = open(file_name_grasp, 'w')
outfile_vnd = open(file_name_vnd, 'w')


for i in range(1, 22):

    print('dataset ' + str(i))
    # Read data set
    vehicles, nodes = read_data(i)
    print('finished reading data')

    # Constructive Algorithm
    sol = sweep(vehicles, nodes)
    z = of(vehicles, nodes, sol)
    print('finished constructive solution')

    # GRASP
    # if i != 20:
    #     time_prev = time.clock()
    #     sol_grasp, z_grasp = grasp(nodes, vehicles)
    #     time_after = time.clock()
    #     if sol_grasp == 'NaN':
    #         outfile_grasp.write(str(i) + ',' + str(len(nodes['index'])) + ',' + 'inf,inf,inf\n')
    #         continue
    #     print('finished GRASP')
    #     exec_time = str(round(time_after - time_prev, 2))
    #     percent = str(round(100 * ((z - z_grasp) / z), 2))
    #
    #     outfile_grasp.write(str(i) + ',' + str(len(nodes['index'])) + ',' + percent + ',' + exec_time + ',' +
    #                       str(round(z_grasp, 2)) + '\n')

    time_prev = time.clock()
    sol_vnd, z_vnd = vnd_noise(sol, nodes, vehicles, z)
    time_after = time.clock()
    print('finished VND noise')
    exec_time = str(round(time_after - time_prev, 2))
    percent = str(round(100 * ((z - z_vnd) / z), 2))

    outfile_vnd.write(str(i) + ',' + str(len(nodes['index'])) + ',' + percent + ',' + exec_time + ',' +
                  str(round(z_vnd, 2)) + '\n')

outfile_grasp.close()
outfile_vnd.close()