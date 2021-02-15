import numpy as np


def sweep(vehicles, nodes):
    n = len(nodes['index'])
    m = len(vehicles['index'])

    # Center depot:
    nodes['relative_coord'] = [0] * n
    for i1 in range(n):
        nodes['relative_coord'][i1] = tuple(np.subtract(nodes['coord'][i1], nodes['coord'][0]))

    # Calculate angles
    nodes['phase'] = [0] * (n - 1)
    for i1 in range(1, n):
        nodes['phase'][i1 - 1] = np.arctan2(nodes['relative_coord'][i1][1], nodes['relative_coord'][i1][0])

    # Sort angles
    aux_matrix_nodes = [[i1 for i1 in nodes['index']], [i1 for i1 in nodes['phase']]]
    aux_matrix_nodes = np.array([aux_matrix_nodes[0][1:], aux_matrix_nodes[1]])
    aux_matrix_nodes = aux_matrix_nodes.transpose()
    aux_matrix_nodes = aux_matrix_nodes[np.argsort(aux_matrix_nodes[:, 1])]

    # Sort capacities
    aux_matrix_vehicles = np.array([[i1 for i1 in vehicles['index']],
                                    [i1 for i1 in vehicles['capacity']], [i for i in vehicles['num_vehicles']]]).dot(-1)
    aux_matrix_vehicles = aux_matrix_vehicles.transpose()
    aux_matrix_vehicles = -1 * aux_matrix_vehicles[np.argsort(aux_matrix_vehicles[:, 1])]

    # Permanently assigned to route
    nodes['assigned'] = []
    for i1 in range(n):
        nodes['assigned'].append([0, 0])
    nodes['assigned'][0] = [1, 0]

    # Route per vehicle
    total_vehicles = sum(vehicles['num_vehicles'])
    sol_routes = []
    for i1 in range(total_vehicles):
        sol_routes.append([])
    demand_sol_routes = [0] * total_vehicles

    c = 0

    for k in range(m):  # iterates over types of vehicles
        routes = []
        demand_routes = []

        sort_demands = nodes['demand'][1:]

        max_cap = aux_matrix_vehicles[k][1]
        vehicle_max_cap = aux_matrix_vehicles[k][0]

        assign = list(map(lambda x: x[0], nodes['assigned'][1:]))
        route_demand = 0
        route = []

        ms = min(sort_demands)

        for z1 in range(len(assign)):
            if assign[z1]:
                sort_demands[z1] = ms - 1

        parent = sort_demands.index(max(sort_demands))
        sort_demands[parent] = ms - 1

        i1 = int(np.where(aux_matrix_nodes[:, 0] == parent + 1)[0])

        counter = False
        while sum(assign) < n - 1:  # iterates over ordered nodes by phase
            # If reach end of graph, turn other way
            if i1 == aux_matrix_nodes.shape[0]:
                i1 = parent
                counter = True
            elif i1 == -1:
                i1 = parent
                counter = False

            # Skips assigned nodes
            current_node = int(aux_matrix_nodes[i1, 0])
            if assign[current_node - 1]:
                if counter:
                    i1 -= 1
                else:
                    i1 += 1
                continue

            route_demand += nodes['demand'][current_node]

            # New route when capacity exceeded
            if route_demand > max_cap:
                demand_routes.append(route_demand - nodes['demand'][current_node])
                route_demand = 0
                routes.append(route)
                route = []
                parent = sort_demands.index(max(sort_demands))
                sort_demands[parent] = ms - 1
                i1 = int(np.where(aux_matrix_nodes[:, 0] == parent + 1)[0])
                counter = False
            else:
                assign[current_node - 1] = 1
                sort_demands[current_node - 1] = ms - 1
                if counter:
                    route.insert(0, current_node)
                    i1 -= 1
                else:
                    route.append(current_node)
                    i1 += 1

        # Sorts routes by demand
        lengths_routes = [x for x in demand_routes]
        lengths_routes = zip(lengths_routes, [vehicle for vehicle in range(len(routes))])
        max_nodes_routes = sorted(lengths_routes, reverse=True)[:vehicles['num_vehicles'][vehicle_max_cap]]

        # Permanently assign nodes to route
        for route in max_nodes_routes:
            for l in routes[route[1]]:
                nodes['assigned'][l] = [1, m - k - 1]
            sol_routes[c] = routes[route[1]]
            demand_sol_routes[c] = demand_routes[route[1]]
            c += 1

    # Checks if missing nodes can be added to existing routes
    for j in nodes['index']:
        if not nodes['assigned'][j][0]:
            for i1 in range(len(sol_routes)):
                route = sol_routes[i1]
                if len(route) == 0:
                    route.append(j)
                    nodes['assigned'][j][0] = 1
                    break

                index_bus = nodes['assigned'][route[0]][1]
                if demand_sol_routes[i1] + nodes['demand'][j] < vehicles['capacity'][index_bus]:
                    route.append(j)
                    nodes['assigned'][j][0] = 1
                    break
    return sol_routes


# Objective Function
def of(vehicles, nodes, sol_routes):
    z = 0
    for route in sol_routes:
        route.append(0)
        for i1 in range(len(route) - 1):
            r1 = route[i1]
            for j1 in range(i1 + 1, len(route)):
                r2 = route[j1]
                dist = ((nodes['coord'][r1][0] - nodes['coord'][r2][0]) ** 2 +
                        (nodes['coord'][r1][1] - nodes['coord'][r2][1]) ** 2) ** 0.5

                z += nodes['demand'][r1] * dist * vehicles['velocity'][nodes['assigned'][r1][1]]
        route.insert(0, 0)
    return z
