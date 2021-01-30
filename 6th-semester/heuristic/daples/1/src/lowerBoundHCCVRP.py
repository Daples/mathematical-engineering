from sweepHCCVRP import of


def lower_bound_vrp(nodes, vehicles):

    min_cap = max(vehicles['capacity'])
    max_vel = min(vehicles['velocity'])
    lb_routes = []
    ideal_vehicle = {'index': [0], 'num_vehicles': [float('Inf')], 'capacity': [min_cap], 'velocity': [max_vel]}

    for node in nodes['index']:
        lb_routes.append([node])

    nodes['assigned'] = []
    for i in range(len(nodes['index'])):
        nodes['assigned'].append([1, 0])

    sol_lb = of(ideal_vehicle, nodes, lb_routes)

    return sol_lb
