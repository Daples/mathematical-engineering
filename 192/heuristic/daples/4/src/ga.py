from grasp import of, grasp, check_route
import random
from local_search import vnd
import numpy as np
import copy


def tournament(sols, vehicles, nodes, L=30):
    selected_sols = []
    selected_vehicles = []
    selected_nodes = []
    while len(selected_sols) < L:
        i1 = random.randint(0, len(sols) - 1)
        sol1 = sols.pop(i1)
        z1 = of(vehicles[i1], nodes[i1], sol1)
        i2 = random.randint(0, len(sols) - 1)
        sol2 = sols.pop(i2)
        z2 = of(vehicles[i2], nodes[i2], sol2)

        if z1 < z2:
            selected_sols.append(sol1)
            selected_vehicles.append(vehicles[i1])
            selected_nodes.append(nodes[i1])
            sols.insert(i2, sol2)
        else:
            selected_sols.append(sol2)
            selected_vehicles.append(vehicles[i2])
            selected_nodes.append(nodes[i2])
            sols.insert(i1, sol1)
    return selected_sols, selected_nodes, selected_vehicles


def one_point_crossover(sol, nodes, vehicles):
    r1 = sol[random.randint(0, len(sol) - 1)]
    r1_og = copy.deepcopy(r1)
    r2 = sol[random.randint(0, len(sol) - 1)]
    r2_og = copy.deepcopy(r2)
    v_r1 = nodes['assigned'][r1[1]][1]
    v_r2 = nodes['assigned'][r2[1]][1]
    cap_v_r1 = vehicles['capacity'][v_r1]
    cap_v_r2 = vehicles['capacity'][v_r2]

    if len(r1) > 3 and len(r2) > 3:
        index_cross = random.randint(1, min(len(r1) - 2, len(r2) - 2))
        r1 = r1_og[:index_cross] + r2_og[index_cross + 1:]
        r2 = r2_og[:index_cross] + r1_og[index_cross + 1:]
        feasible = check_route(r1, nodes, cap_v_r1) and check_route(r2, nodes, cap_v_r2)
        if feasible:
            # swap vehicles
            for i in r1:
                nodes['assigned'][i][1] = v_r1
            for i in r2:
                nodes['assigned'][i][1] = v_r2
            return sol, nodes, vehicles
        else:
            feasible = check_route(r1, nodes, cap_v_r2) and check_route(r2, nodes, cap_v_r1)
            if feasible:
                # swap vehicles
                for i in r1:
                    nodes['assigned'][i][1] = v_r2
                for i in r2:
                    nodes['assigned'][i][1] = v_r1
                return sol, nodes, vehicles
            else:
                return None, None, None
    else:
        return sol, nodes, vehicles


def mutation(child, vehicles, nodes, l=5):
    k = 0
    while True and k < l:
        r1 = child[random.randint(0, len(child) - 1)]
        r2 = child[random.randint(0, len(child) - 1)]
        i = random.randint(1, min(len(r1), len(r2)) - 1)
        r1[i], r2[i] = r2[i], r1[i]
        v1, v2 = nodes['assigned'][r1[i]][1], nodes['assigned'][r2[i]][1]
        nodes['assigned'][r1[i]][1], nodes['assigned'][r2[i]][1] = v2, v1
        feasible = check_route(r1, nodes, vehicles['capacity'][v1]) and check_route(r2, nodes, vehicles['capacity'][v2])
        if feasible:
            break
        else:
            r1[i], r2[i] = r2[i], r1[i]
            v1, v2 = nodes['assigned'][r1[i]][1], nodes['assigned'][r2[i]][1]
            nodes['assigned'][r1[i]][1], nodes['assigned'][r2[i]][1] = v2, v1
        k += 1
    return child, vehicles, nodes


def hybrid_ga_vnd(nodes, vehicles, gen=5, l=3, p_mut=0.4, people=60):
    sols, complete_nodes, complete_vehicles = grasp(nodes, vehicles, k=people)  # Initial solutions
    j = 0
    selected_sols = sols
    while j < gen:
        selected_sols, selected_nodes, selected_vehicles = tournament(selected_sols, complete_vehicles,
                                                                      complete_nodes)  # Selection by tournament
        while len(selected_sols) < people:
            index_sol = random.randint(0, len(selected_sols) - 1)
            for k in range(l):
                child, node, vehicle = one_point_crossover(selected_sols[index_sol], selected_nodes[index_sol],
                                                           selected_vehicles[index_sol])
                if child is not None:
                    z_child = of(vehicle, node, child)
                    if random.random() < p_mut:  # Mutation
                        child, vehicle, node = mutation(child, vehicle, node)
                    child, z_child = vnd(child, node, vehicle, z_child)  # Local search
                    selected_sols.append(child)
                    selected_nodes.append(node)
                    selected_vehicles.append(vehicle)
                    break
        j += 1
    j = 0
    best_z = np.Inf
    best_sol = []
    for sol in selected_sols:
        z = of(selected_vehicles[j], selected_nodes[j], sol)
        if z < best_z:
            best_z = z
            best_sol = sol
        j += 1
    return best_sol, best_z


def hybrid_ga(nodes, vehicles, gen=5, l=3, p_mut=0.4, people=60):
    sols, complete_nodes, complete_vehicles = grasp(nodes, vehicles, k=people)  # Initial solutions
    j = 0
    selected_sols = sols
    while j < gen:
        selected_sols, selected_nodes, selected_vehicles = tournament(selected_sols, complete_vehicles,
                                                                      complete_nodes)  # Selection by tournament
        while len(selected_sols) < people:
            index_sol = random.randint(0, len(selected_sols) - 1)
            for k in range(l):
                child, node, vehicle = one_point_crossover(selected_sols[index_sol], selected_nodes[index_sol],
                                                           selected_vehicles[index_sol])
                if child is not None:
                    z_child = of(vehicle, node, child)
                    if random.random() < p_mut:  # Mutation
                        child, vehicle, node = mutation(child, vehicle, node)
                    selected_sols.append(child)
                    selected_nodes.append(node)
                    selected_vehicles.append(vehicle)
                    break
        j += 1
    j = 0
    best_z = np.Inf
    best_sol = []
    index = [i for i in range(len(selected_sols))]
    selected_sols_aux = list(zip(index, selected_sols))
    selected_sols_aux = random.sample(selected_sols_aux, 10)

    for t in selected_sols_aux:
        sol = t[1]
        i = t[0]
        sol, z = vnd(sol, selected_nodes[i], selected_vehicles[i], best_z)  # Local search
        if z < best_z:
            best_z = z
            best_sol = sol
        j += 1
    return best_sol, best_z
