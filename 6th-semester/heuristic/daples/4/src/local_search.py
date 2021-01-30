from grasp import of, check_route
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
