from sweepHCCVRP import of, check_route
import copy
import numpy as np


# In-Route
def two_opt(sol, nodes, best=1, p=0.5):
    def dist(n1, n2):
        x = (n1[0] - n2[0]) ** 2
        y = (n1[1] - n2[1]) ** 2
        return (x + y) ** 0.5

    new_sol = copy.deepcopy(sol)
    neighborhood = [copy.deepcopy(sol)]

    for route in new_sol:
        if len(route) > 3:
            n = len(route)
            for i in range(1, n - 2):
                for j in range(i + 2, n - 1):
                    if best:
                        coord_current = nodes['coord'][route[i]]
                        coord_next_current = nodes['coord'][route[i + 1]]
                        coord_target = nodes['coord'][route[j]]
                        coord_next_target = nodes['coord'][route[j + 1]]
                        d1 = dist(coord_current, coord_next_current) + dist(coord_target, coord_next_target)
                        d2 = dist(coord_current, coord_target) + dist(coord_next_target, coord_next_current)
                        if d2 < d1:
                            route[i + 1:j + 1] = route[i + 1:j + 1][::-1]
                    else:
                        if np.random.rand() < p:
                            route[i + 1:j + 1] = route[i + 1:j + 1][::-1]
                            neighborhood.append(copy.deepcopy(new_sol))
    if best:
        return new_sol
    else:
        return neighborhood


def two_opt_noise(sol, nodes, best=1, p=0.5, r=0.5, l=3):

    def dist_noise(n1, n2, sigma):
        x = (n1[0] - n2[0]) ** 2
        y = (n1[1] - n2[1]) ** 2
        return (x + y) ** 0.5 + np.random.uniform(-sigma, sigma)

    def fill_dist_matrix(nodes, sigma):
        n = len(nodes['index'])
        dist_matrix = [[0] * n] * n
        for i in range(n):
            for j in range(n):
                if i != j:
                    node_i = nodes['coord'][i]
                    node_j = nodes['coord'][j]
                    dist_matrix[i][j] = dist_noise(node_i, node_j, sigma)
        return dist_matrix

    new_sol = copy.deepcopy(sol)
    if not best:
        neighborhood = [copy.deepcopy(sol)]
    dist_matrix = fill_dist_matrix(nodes, 0)
    sigma = max(dist for node in dist_matrix for dist in node)/4
    while sigma > 10 ** -4:
        j = 0
        while j < l:
            for route in new_sol:
                if len(route) > 3:
                    n = len(route)
                    for i in range(1, n - 2):
                        for j in range(i + 2, n - 1):
                            if best:
                                d1 = dist_matrix[route[i]][route[i + 1]] + dist_matrix[route[j]][route[j + 1]]
                                d2 = dist_matrix[route[i]][route[j]] + dist_matrix[route[j + 1]][route[i + 1]]
                                if d2 < d1:
                                    route[i + 1:j + 1] = route[i + 1:j + 1][::-1]
                            else:
                                if np.random.rand() < p:
                                    route[i + 1:j + 1] = route[i + 1:j + 1][::-1]
                                    neighborhood.append(copy.deepcopy(new_sol))
            j += 1
        sigma = sigma * r
        dist_matrix = fill_dist_matrix(nodes, sigma)
    if best:
        return new_sol
    else:
        return neighborhood


def move(sol, nodes, vehicles, old_z):
    new_sol = copy.deepcopy(sol)
    prev_sol = copy.deepcopy(sol)
    for r in range(len(new_sol)):
        route = new_sol[r]
        n = len(route)
        if len(route) > 4:
            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    route.insert(j, route.pop(i))
                    z = of(vehicles, nodes, new_sol)
                    if z < old_z:
                        route_prev = prev_sol[r]
                        route_prev.insert(j, route_prev.pop(i))
                        old_z = z
                    else:
                        route.insert(j, route.pop(i))
    return prev_sol, old_z


# Inter-Route
def one_one_exchange(sol, nodes, vehicles, old_z):
    new_sol = copy.deepcopy(sol)
    prev_sol = copy.deepcopy(sol)
    for r1 in range(len(new_sol) - 1):
        for r2 in range(r1, len(new_sol)):
            for i in range(1, len(new_sol[r1]) - 1):
                for j in range(1, len(new_sol[r2]) - 1):
                    new_sol[r1][i], new_sol[r2][j] = new_sol[r2][j], new_sol[r1][i]
                    nodes['assigned'][i][1], nodes['assigned'][j][1] = nodes['assigned'][j][1], nodes['assigned'][i][1]
                    if check_route(new_sol[r1], nodes, vehicles['capacity'][nodes['assigned'][i][1]]) and \
                            check_route(new_sol[r2], nodes, vehicles['capacity'][nodes['assigned'][j][1]]):
                        new_z = of(vehicles, nodes, new_sol)
                        if new_z - old_z < 0:
                            prev_sol = copy.deepcopy(new_sol)
                            old_z = new_z
                        else:
                            new_sol[r1][i], new_sol[r2][j] = new_sol[r2][j], new_sol[r1][i]
                            nodes['assigned'][i][1], nodes['assigned'][j][1] = nodes['assigned'][j][1], \
                                                                               nodes['assigned'][i][1]
                    else:
                        new_sol[r1][i], new_sol[r2][j] = new_sol[r2][j], new_sol[r1][i]
                        nodes['assigned'][i][1], nodes['assigned'][j][1] = nodes['assigned'][j][1], \
                                                                           nodes['assigned'][i][1]
    return prev_sol, old_z


# VND
def vnd(sol, nodes, vehicles, old_z, l=5):
    j = 0
    new_sol = copy.deepcopy(sol)
    z = old_z
    while j <= l:
        if j % 3 == 0:
            new_sol = two_opt(new_sol, nodes)
            z = of(vehicles, nodes, new_sol)
        elif j % 3 == 1:
            new_sol, z = one_one_exchange(new_sol, nodes, vehicles, z)
        elif j % 3 == 2:
            new_sol, z = move(new_sol, nodes, vehicles, z)
        j += 1
    return new_sol, z


def vnd_noise(sol, nodes, vehicles, old_z, l=5):
    j = 0
    new_sol = copy.deepcopy(sol)
    z = old_z
    while j <= l:
        if j % 3 == 0:
            noise = j % 2
            new_sol = two_opt_noise(new_sol, nodes, vehicles)
            z = of(vehicles, nodes, new_sol)
        elif j % 3 == 1:
            new_sol, z = one_one_exchange(new_sol, nodes, vehicles, z)
        elif j % 3 == 2:
            new_sol, z = move(new_sol, nodes, vehicles, z)
        j += 1
    return new_sol, z
