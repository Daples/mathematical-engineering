import numpy as np
import os
import time
import matplotlib.pyplot as plt
from matplotlib import cm, colors


class Vrp:
    class Bus:
        def __init__(self, line):
            self.index = int(line[0])
            self.quantity = int(line[1])
            self.cap = int(line[2])
            self.vel = float(line[3])

    class Node:
        def __init__(self, line):
            self.index = int(line[0])
            self.x = int(line[1])
            self.y = int(line[2])
            self.demand = int(line[3])

        def distance(self, node):
            return np.sqrt((self.x - node.x)**2 + (self.y - node.y)**2)

        def __str__(self):
            return str(self.index)

    class Route:
        def __init__(self, bus, base, i):
            self.edges = []
            self.centroid = [0, 0]
            self.demand = 0
            self.bus = bus

            self.edges.append(base)
            self.edges.append(i)
            self.edges.append(base)
            self.centroid[0] += (base.x + i.x)/2
            self.centroid[1] += (base.y + i.y)/2
            self.demand += i.demand

        # Gets cost of route
        def cost(self):
            z = 0
            for i in range(1, len(self.edges) - 1):
                ti = 0
                for j in range(i, len(self.edges) - 1):
                    node0 = self.edges[j]
                    node1 = self.edges[j + 1]
                    ti += node0.distance(node1) * self.bus.vel
                z += self.edges[i].demand * ti
            return z

        def distance(self, route):
            return ((self.centroid[0] - route.centroid[0]) ** 2 +
                    (self.centroid[1] - route.centroid[1]) ** 2) ** 0.5

        # Gets end points of route
        def get_end_points(self):
            return [self.edges[1], self.edges[-2]]

        # If two routes can merge given two nodes
        def can_merge(self, node1, node2, route):
            demand = self.demand + route.demand

            e1 = self.get_end_points()
            e2 = route.get_end_points()

            end1 = node1 in e1
            end2 = node2 in e2

            rev1 = node1 is e1[0] and node2 is e2[0]
            rev2 = node1 is e1[1] and node2 is e2[1]

            return (demand <= self.bus.cap and end1 and end2), rev1, rev2

        # Merge two routes given two nodes
        def merge(self, node1, node2, route, nodes_routes):
            can, rev1, rev2 = self.can_merge(node1, node2, route)

            if can:
                if rev1:
                    self.edges = list(reversed(self.edges))
                if rev2:
                    route.edges = list(reversed(route.edges))

                self.edges.pop()
                self.demand += route.demand
                l1 = len(self.edges)
                self.centroid[0] *= l1
                self.centroid[1] *= l1

                for node in route.edges[1:]:
                    self.edges.append(node)
                    if node != self.edges[0]:
                        self.centroid[0] += node.x
                        self.centroid[1] += node.y
                    if node.index > 0:
                        nodes_routes[node.index - 1] = self
                self.centroid[0] /= len(self.edges) - 1
                self.centroid[1] /= len(self.edges) - 1

            return can

        # Add node to final of route
        def add_final(self, node):
            end = self.get_end_points()
            st = end[0]
            end = end[1]

            d1 = st.distance(node)
            d2 = end.distance(node)

            self.centroid[0] *= len(self.edges) - 1
            self.centroid[1] *= len(self.edges) - 1

            self.centroid[0] += node.x
            self.centroid[1] += node.y

            self.centroid[0] /= len(self.edges)
            self.centroid[1] /= len(self.edges)

            if d2 < d1:
                self.edges.insert(-1, node)
            else:
                self.edges.insert(1, node)
            self.demand += node.demand

        # Two opt between routes operator
        def two_opt(self, route, taboo=False):
            def aux_cost(bus, l1, l2):
                ls = [l1, l2]
                z = 0
                index2_l = 0
                inc2 = 0
                for i1 in range(1, len(l1) + len(l2) - 1):
                    if i1 >= len(l1):
                        inc2 = len(l1)
                        index2_l = 1
                    index_l = 0
                    index1_l = 0
                    inc = 0
                    inc1 = 0
                    for j1 in range(i1, len(l1) + len(l2) - 1):
                        if j1 >= len(l1):
                            inc = len(l1)
                            index_l = 1
                        node = ls[index_l][j1 - inc]

                        if j1 + 1 >= len(l1):
                            inc1 = len(l1)
                            index1_l = 1
                        node1 = ls[index1_l][j1 + 1 - inc1]
                        z += ls[index2_l][i1 - inc2].demand * node.distance(node1) * bus.vel
                return z
            total_min = self.cost() + route.cost()
            cost_min = total_min
            first = True
            best = False
            for i in range(1, len(self.edges) - 2):
                j_best = -1
                t_change = -1

                bi = self.edges[:i + 1]
                di = sum(map(lambda x: x.demand, bi))

                bi1 = self.edges[i + 1:]
                di1 = sum(map(lambda x: x.demand, bi1))
                for j in range(1, len(route.edges) - 2):
                    bj = route.edges[:j + 1]
                    dj = sum(map(lambda x: x.demand, bj))

                    bj1 = route.edges[j + 1:]
                    dj1 = sum(map(lambda x: x.demand, bj1))

                    # Route connecting self[i] with route[j + 1] for first configuration of buses
                    did1 = di + dj1 <= self.bus.cap
                    did2 = dj + di1 <= route.bus.cap
                    if did1 and did2:
                        c = aux_cost(self.bus, bi, bj1) + aux_cost(route.bus, bj, bi1)
                        if first and taboo:
                            cost_min = c
                            first = False
                        if c < cost_min:
                            cost_min = c
                            j_best = j
                            t_change = 0

                    # Route connecting self[i] with route[j]
                    did1 = dj + di <= self.bus.cap
                    did2 = di1 + dj1 <= route.bus.cap
                    if did1 and did2:
                        c = aux_cost(self.bus, bj, list(reversed(bi))) + \
                            aux_cost(route.bus, list(reversed(bi1)), bj1)
                        if first and taboo:
                            cost_min = c
                            first = False
                        if c < cost_min:
                            cost_min = c
                            j_best = j
                            t_change = 1
                if j_best != -1:
                    bi = self.edges[:i + 1]
                    bi1 = self.edges[i + 1:]

                    bj = route.edges[:j_best + 1]
                    bj1 = route.edges[j_best + 1:]
                    if t_change == 0:
                        self.edges = bi + bj1
                        route.edges = bj + bi1
                    else:
                        self.edges = bj + list(reversed(bi))
                        route.edges = list(reversed(bi1)) + bj1
                    if cost_min < total_min:
                        best = True

            return best

        # Swap inside route operator
        def swap(self):
            cost_min = self.cost()
            for i in range(1, len(self.edges) - 1):
                j_best = -1
                for j in range(i + 1, len(self.edges) - 1):
                    self.edges[i], self.edges[j] = self.edges[j], self.edges[i]
                    c = self.cost()
                    if c < cost_min:
                        cost_min = c
                        j_best = j

                    self.edges[i], self.edges[j] = self.edges[j], self.edges[i]

                if j_best != -1:
                    self.edges[i], self.edges[j_best] = self.edges[j_best], self.edges[i]

        # 2-h-opt operator
        def two_h_opt(self):
            def aux_cost(bus, l1, l2, l3, l4=list()):
                ls = [l1, l2, l3, l4]
                z = 0
                index2_l = 0
                inc2 = 0
                for i1 in range(1, len(l1) + len(l2) + len(l3) + len(l4) - 1):
                    if i1 >= len(l1) + len(l2) + len(l3):
                        inc2 = len(l1) + len(l2) + len(l3)
                        index2_l = 3
                    elif i1 >= len(l1) + len(l2):
                        inc2 = len(l1) + len(l2)
                        index2_l = 2
                    elif i1 >= len(l1):
                        inc2 = len(l1)
                        index2_l = 1
                    index_l = 0
                    index1_l = 0
                    inc = 0
                    inc1 = 0
                    for j1 in range(i1, len(l1) + len(l2) + len(l3) + len(l4) - 1):
                        if j1 >= len(l1) + len(l2) + len(l3):
                            inc = len(l1) + len(l2) + len(l3)
                            index_l = 3
                        elif j1 >= len(l1) + len(l2):
                            inc = len(l1) + len(l2)
                            index_l = 2
                        elif j1 >= len(l1):
                            inc = len(l1)
                            index_l = 1
                        node = ls[index_l][j1 - inc]

                        if j1 + 1 >= len(l1) + len(l2) + len(l3):
                            inc1 = len(l1) + len(l2) + len(l3)
                            index1_l = 3
                        elif j1 + 1 >= len(l1) + len(l2):
                            inc1 = len(l1) + len(l2)
                            index1_l = 2
                        elif j1 + 1 >= len(l1):
                            inc1 = len(l1)
                            index1_l = 1
                        node1 = ls[index1_l][j1 + 1 - inc1]
                        z += ls[index2_l][i1 - inc2].demand * node.distance(node1) * bus.vel
                return z
            c_min = self.cost()
            for i in range(1, len(self.edges) - 2):
                j_best = -1
                t_change = -1
                si = self.edges[:i+1]
                for j in range(i + 4, len(self.edges) - 2):
                    sj = self.edges[j+1:]
                    # Normal two opt
                    ij = self.edges[i + 1: j + 1]
                    c = aux_cost(self.bus, si, list(reversed(ij)), sj)
                    if c < c_min:
                        c_min = c
                        j_best = j
                        t_change = 0

                    # Additional node switch 1
                    c = aux_cost(self.bus, si, [self.edges[j]], self.edges[i + 1:j], sj)
                    c1 = self.cost()
                    if c < c_min:
                        c_min = c
                        j_best = j
                        t_change = 1

                    # Additional node switch 2
                    c = aux_cost(self.bus, si, self.edges[i+2:j+1], [self.edges[i + 1]], sj)
                    if c < c_min:
                        c_min = c
                        j_best = j
                        t_change = 2

                if j_best != -1:
                    if t_change == 0:
                        ij = self.edges[i + 1: j_best + 1]
                        self.edges = si + list(reversed(ij)) + self.edges[j_best + 1:]
                    elif t_change == 1:
                        self.edges = si + [self.edges[j_best]] + self.edges[i + 1:j_best] + self.edges[j_best + 1:]
                    else:
                        self.edges = si + self.edges[i+2:j_best+1] + [self.edges[i + 1]] + self.edges[j_best + 1:]

        # String representation of route
        def __str__(self):
            string = ""
            for i in range(len(self.edges) - 1):
                edge = self.edges[i]
                string += str(edge.index) + " -- "
            return string + "0"

    def __init__(self, num):
        self.x = num
        self.dir = os.getcwd() + "/datos/HFCCVRP"
        self.dir1 = os.getcwd() + "/vns"
        self.dir2 = os.getcwd() + "/local_search"
        self.base = None
        self.nodes = []
        self.buses = []
        self.routes = []
        self.time = 0

        self.get_data()

    # Get place of problem file
    def place(self):
        return self.dir + '/hfccvrp' + str(self.x) + '.vrp'

    # Structure file for reading
    def read_file(self):
        def remove(elem):
            return elem.replace("\n", "").replace(",", ".").replace("\t", ",").split(",")
        file = open(self.place())
        lines = file.readlines()
        lines = list(map(lambda x: remove(x), lines))
        lines[0] = list(filter(lambda x: len(x) > 0, lines[0]))
        return lines

    # Get data of the problem, given the structure that read file made
    def get_data(self):
        lines = self.read_file()
        n = int(lines[0][0])
        m = int(lines[0][1])

        # Add buses
        for i in range(1, m + 1):
            bus1 = Vrp.Bus(lines[i])
            self.buses.append(bus1)

        # Add nodes
        self.base = Vrp.Node(lines[m + 1])
        for j in range(m + 2, n + m + 2):
            node = Vrp.Node(lines[j])
            self.nodes.append(node)

        ds = sum(list(map(lambda x: x.demand, self.nodes)))
        dis = 0
        for bus in self.buses:
            dis += bus.quantity*bus.cap

        if ds > dis:
            print("Warning! Problem does not have solution", ds, ">", dis)

    # Calculate savings for CW algorithm
    def calc_savings(self):
        ln = len(self.nodes)
        savings = {}
        # Calculate savings
        for i in range(ln):
            node = self.nodes[i]
            for j in range(i + 1, ln):
                node1 = self.nodes[j]
                key = node.distance(self.base) + node1.distance(self.base) - node.distance(node1)
                savings[key] = (node, node1)
        return savings

    # Insert nodes not chosen
    def add_residuals(self, used):
        used_aux = list(np.where(used == 0)[0])
        used_aux = sorted(used_aux, key=lambda x: self.nodes[x].demand, reverse=True)
        for i in used_aux:
            for route in self.routes:
                if route.demand + self.nodes[i].demand <= route.bus.cap:
                    route.add_final(self.nodes[i])
                    used[i] = 1
                    break
        if sum(used) != len(used):
            print("Warning! Not all nodes used, not used", np.where(used == 0))

    # CW variation algorithm
    def clark_wright(self, savings, used, bus, nodes_routes):
        ln = len(used)
        # First routes
        self.routes = []
        for i in range(ln):
            if not used[i]:
                route = Vrp.Route(bus, self.base, self.nodes[i])
                self.routes.append(route)
                nodes_routes.append(route)
            else:
                nodes_routes.append(None)

        for key in sorted(savings.keys(), reverse=True):
            connection = savings[key]

            node0 = connection[0]
            node1 = connection[1]

            if not used[node0.index - 1] and not used[node1.index - 1]:
                route0 = nodes_routes[node0.index - 1]
                route1 = nodes_routes[node1.index - 1]

                if route0 is route1:
                    continue

                can = route0.merge(node0, node1, route1, nodes_routes)
                if can:
                    self.routes.remove(route1)

    # Make an initial solution using the constructive algorithm
    def initial_solution(self):
        ln = len(self.nodes)
        used = np.zeros(ln)
        real_routes = []

        t = time.time()
        # Calculate savings
        savings = self.calc_savings()
        for bus in self.buses:
            nodes_routes = []
            # Clark Wright Algorithm
            self.clark_wright(savings, used, bus, nodes_routes)

            real_routes += sorted(self.routes, key=lambda x: x.demand, reverse=True)[:bus.quantity]
            for route in real_routes:
                for i in range(1, len(route.edges) - 1):
                    node = route.edges[i]
                    used[node.index - 1] = 1

        self.routes = real_routes
        self.add_residuals(used)
        self.time = time.time() - t

    # Calculate objective function for problem
    def objective(self):
        z = 0
        for route in self.routes:
            z += route.cost()
        return z

    # Get a lower bound for the problem
    def lower_bound(self):
        # Property smaller bus
        mv = self.buses[0].vel
        lb = 0
        for node in self.nodes:
            lb += node.demand * node.distance(self.base) * mv
        return lb

    # Write actual solution
    def write_solution(self, f1):
        for i in range(len(self.routes)):
            string = str(self.routes[i].bus.index)
            string += " " + str(len(self.routes[i].edges))
            for node in self.routes[i].edges:
                string += " " + str(node.index)
            f1.write(string + "\n")
        f1.close()

    # Generate file of solution for work 1
    def gen_file_1(self):
        self.initial_solution()
        f1 = open("/hfccvrp" + str(self.x) + ".sol", "w")
        self.write_solution(f1)

    # Generate file of solution of work 2
    def gen_file2(self):
        self.initial_solution()
        self.vns()
        if not os.path.isdir(self.dir1):
            os.makedirs(self.dir1)
        f1 = open(self.dir1 + "/hfccvrp" + str(self.x) + ".sol", "w")
        self.write_solution(f1)

        self.initial_solution()
        self.taboo_search()
        if not os.path.isdir(self.dir2):
            os.makedirs(self.dir2)
        f1 = open(self.dir2 + "/hfccvrp" + str(self.x) + ".sol", "w")
        self.write_solution(f1)

    # Draw solution
    def draw(self):
        def add_arrow(line, position=None, direction='right', size=15, color=None):
            if color is None:
                color = line.get_color()

            xdata = line.get_xdata()
            ydata = line.get_ydata()

            if position is None:
                position = xdata.mean()
            # find closest index
            start_ind = np.argmin(np.absolute(xdata - position))
            if direction == 'right':
                end_ind = start_ind + 1
            else:
                end_ind = start_ind - 1

            line.axes.annotate('',
                               xytext=(xdata[start_ind], ydata[start_ind]),
                               xy=(xdata[end_ind], ydata[end_ind]),
                               arrowprops=dict(arrowstyle="->", color=color),
                               size=size
                               )
        base = self.routes[0].edges[0]
        color1 = plt.get_cmap('gist_rainbow')
        color_norm = colors.Normalize(vmin=0, vmax=len(self.routes) - 1)
        scalar_map = cm.ScalarMappable(norm=color_norm, cmap=color1)

        for i in range(len(self.routes)):
            route = self.routes[i]
            color = scalar_map.to_rgba(i)
            for j in range(len(route.edges) - 1):
                node1 = route.edges[j]
                node2 = route.edges[j + 1]

                xs = [node1.x - base.x, node2.x - base.x]
                ys = [node1.y - base.y, node2.y - base.y]

                l1 = plt.plot(xs, ys, color=color)[0]
                add_arrow(l1)
                plt.plot(xs, ys, 'o', color=color)
        plt.show()

    # Makes two opt for the nearest routes
    def neighbor1(self, taboo_list, taboo=False):
        moves = []
        best = False
        for i in range(len(self.routes)):
            route = self.routes[i]
            j_best = -1
            best = 0
            find = False
            for j in range(len(self.routes)):
                if taboo_list[i, j] != 0:
                    taboo_list[i, j] -= 1
                    continue
                route1 = self.routes[j]
                if j == i:
                    continue
                if not find:
                    best = route.distance(route1)
                    j_best = j
                    find = True
                    continue
                d = route.distance(route1)
                if d < best:
                    best = d
                    j_best = j
            best = route.two_opt(self.routes[j_best], taboo=taboo)
            moves.append((i, j_best))
        return moves, best

    # Makes swap for every route
    def neighbor2(self):
        for route in self.routes:
            route.swap()

    # Makes 2.5-opt algorithm for every route
    def neighbor3(self):
        for route in self.routes:
            route.two_h_opt()

    # Taboo search
    def taboo_search(self, max_iterations=15, taboo_iterations=2):
        taboo_list = np.zeros((len(self.routes), len(self.routes)))
        best_sol = self.routes.copy()
        i = 0
        while i < max_iterations:
            taboo_moves, best = self.neighbor1(taboo_list=taboo_list)
            for pair in taboo_moves:
                taboo_list[pair[0], pair[1]] = taboo_iterations
                taboo_list[pair[1], pair[0]] = taboo_iterations
            if not best:
                i += 1
            else:
                i = 0
                best_sol = self.routes.copy()
            self.neighbor2()
        self.routes = best_sol

    # Variable neighborhood
    def vns(self, max_iterations=5):
        zeros = np.zeros((len(self.routes), len(self.routes)))
        j = 0
        for i in range(max_iterations):
            if j == 0:
                m1 = self.neighbor2
                m2 = self.neighbor3
                j = 1
            else:
                m1 = self.neighbor3
                m2 = self.neighbor2
                j = 0
            self.neighbor1(zeros)
            m1()
            m2()


for prob in range(16, 17):
    file1 = Vrp(prob)
    file1.initial_solution()
    file1.draw()
    file1.taboo_search()
