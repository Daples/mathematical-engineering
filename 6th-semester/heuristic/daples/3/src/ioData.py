import os
import matplotlib.pyplot as plt
import numpy as np
from grasp import of_by_routes


def read_data(number):
    current_folder = os.getcwd()
    file_name = 'hfccvrp' + str(number) + '.vrp'
    file_name = os.path.join(current_folder, 'HFCCVRP', file_name)
    data_file = open(file_name, 'r')
    data = data_file.read()
    data_file.close()

    data = data.split('\n')
    first_line = data[0].split('\t')
    n = int(first_line[0])
    m = int(first_line[1])
    data = data[1::]

    # Vehicles
    vehicles = {'index': [0]*m, 'num_vehicles': [0]*m, 'capacity': [0]*m, 'velocity': [0]*m}
    for k in range(m):
        data_inline = data[k].split('\t')
        vehicles['index'][k] = int(data_inline[0])
        vehicles['num_vehicles'][k] = int(data_inline[1])
        vehicles['capacity'][k] = int(data_inline[2])
        vehicles['velocity'][k] = float(data_inline[3].replace(',', '.'))

    data = data[m::]

    # Nodes
    nodes = {'index': [0]*(n+1), 'coord': [0]*(n+1), 'demand': [0]*(n+1)}
    for i in range(n+1):
        data_inline = data[i].split('\t')
        nodes['index'][i] = int(data_inline[0])
        nodes['coord'][i] = (int(data_inline[1]), int(data_inline[2]))
        nodes['demand'][i] = int(data_inline[3])

    return vehicles, nodes


def print_routes(number, vehicles, nodes, sol_routes, method):
    current_folder = os.getcwd()
    out_folder = os.path.join(current_folder, 'HFCCVRP_sol_' + method)

    if not os.path.isdir(out_folder):
        os.mkdir(out_folder)

    file_name = 'hfccvrp' + str(number) + '.sol'
    file_name = os.path.join(current_folder, 'HFCCVRP_sol_' + method, file_name)
    output_file = open(file_name, 'w')

    of_routes = []
    for route in sol_routes:
        of_routes.append(of_by_routes(vehicles, nodes, route))

    j = 0
    for route in sol_routes:
        current_vehicle = vehicles['index'][nodes['assigned'][route[1]][1]]
        output_file.write(str(current_vehicle) + '\t')

        nodes_in_route = len(route)
        output_file.write(str(nodes_in_route) + '\t')

        for node in route:
            output_file.write(str(node) + '\t')

        output_file.write(str(of_routes[j]))
        j += 1

        output_file.write('\n')

    output_file.write(str(sum(of_routes)))
    output_file.close()


def plot_routes(f, sol, nodes, title):
    plt.figure(f)
    k = 0
    for route in sol:
        c = tuple(np.random.rand(3, ))
        xs = [nodes['coord'][j][0] for j in route]
        ys = [nodes['coord'][j][1] for j in route]
        plt.plot(xs, ys, 'o-', color=c, label=str(k))
        k += 1
    plt.legend()
    plt.title(str(len(nodes['index'])) + ' ' + title)
    return f + 1
