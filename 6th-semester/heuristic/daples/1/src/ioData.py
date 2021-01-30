import os


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


def print_routes(number, vehicles, nodes, sol_routes):
    current_folder = os.getcwd()
    out_folder = os.path.join(current_folder, 'HFCCVRP_sol')

    if not os.path.isdir(out_folder):
        os.mkdir(out_folder)

    file_name = 'hfccvrp' + str(number) + '.sol'
    file_name = os.path.join(current_folder, 'HFCCVRP_sol', file_name)
    output_file = open(file_name, 'w')

    for route in sol_routes:
        current_vehicle = vehicles['index'][nodes['assigned'][route[1]][1]]
        output_file.write(str(current_vehicle) + '\t')

        nodes_in_route = len(route)
        output_file.write(str(nodes_in_route) + '\t')

        for node in route:
            output_file.write(str(node) + '\t')

        output_file.write('\n')

    output_file.close()

