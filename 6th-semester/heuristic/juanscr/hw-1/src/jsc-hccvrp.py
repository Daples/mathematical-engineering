import numpy as np
import os
import time
import math
import itertools


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

        def get_cost(self, node):
            cost = self.distance(node)
            return cost

        def __str__(self):
            return str(self.index)

    class Route:
        def __init__(self, bus, base, i):
            self.edges = []
            self.demand = 0
            self.bus = bus

            self.edges.append(base)
            self.edges.append(i)
            self.edges.append(base)
            self.demand += i.demand

        def get_end_points(self):
            return [self.edges[1], self.edges[-2]]

        def has_node(self, node):
            return node in self.edges

        def can_merge(self, node1, node2, route):
            demand = self.demand + route.demand

            e1 = self.get_end_points()
            e2 = route.get_end_points()

            end1 = node1 in e1
            end2 = node2 in e2

            rev1 = node1 is e1[0] and node2 is e2[0]
            rev2 = node1 is e1[1] and node2 is e2[1]

            return (demand <= self.bus.cap and end1 and end2), rev1, rev2

        def merge(self, node1, node2, route, nodes_routes):
            can, rev1, rev2 = self.can_merge(node1, node2, route)

            if can:
                if rev1:
                    self.edges = list(reversed(self.edges))
                if rev2:
                    route.edges = list(reversed(route.edges))

                self.edges.pop()
                self.demand += route.demand

                for node in route.edges[1:]:
                    self.edges.append(node)
                    if node.index > 0:
                        nodes_routes[node.index - 1] = self

            return can

        def add_final(self, node):
            end = self.get_end_points()
            st = end[0]
            end = end[1]

            d1 = st.distance(node)
            d2 = end.distance(node)

            if d2 < d1:
                self.edges.insert(-1, node)
            else:
                self.edges.insert(1, node)
            self.demand += node.demand

        def __str__(self):
            string = ""
            for i in range(len(self.edges) - 1):
                edge = self.edges[i]
                string += str(edge.index) + " -- "
            return string + "0"

    def __init__(self, num):
        self.x = num
        self.dir = os.getcwd() + "/datos/HFCCVRP"
        self.dir1 = os.getcwd()
        self.dir2 = os.getcwd() + "/tables"
        self.base = None
        self.nodes = []
        self.buses = []
        self.routes = []
        self.time = 0

        self.get_data()

    def place(self):
        return self.dir + '/hfccvrp' + str(self.x) + '.vrp'

    def read_file(self):
        def remove(elem):
            return elem.replace("\n", "").replace(",", ".").replace("\t", ",").split(",")
        file = open(self.place())
        lines = file.readlines()
        lines = list(map(lambda x: remove(x), lines))
        lines[0] = list(filter(lambda x: len(x) > 0, lines[0]))
        return lines

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

    def calc_savings(self):
        ln = len(self.nodes)
        savings = {}
        # Calculate savings
        for i in range(ln):
            node = self.nodes[i]
            for j in range(i + 1, ln):
                node1 = self.nodes[j]
                key = node.get_cost(self.base) + node1.get_cost(self.base) - node.get_cost(node1)
                savings[key] = (node, node1)
        return savings

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

    def solve(self):
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

    def objective(self):
        z = 0
        for route in self.routes:
            for i in range(1, len(route.edges) - 1):
                ti = 0
                for j in range(i, len(route.edges) - 1):
                    node0 = route.edges[j]
                    node1 = route.edges[j + 1]
                    ti += node0.distance(node1) * route.bus.vel
                z += route.edges[i].demand * ti
        return z

    def lower_bound(self):
        pair = list(itertools.combinations(self.nodes, 2))
        d = list(map(lambda x: x[0].distance(x[1]), pair))
        d = list(filter(lambda x: x > 0, d))
        p = max(d)
        td = sum(list(map(lambda x: x.demand, self.nodes)))

        mc = self.buses[0].cap
        mv = self.buses[0].vel

        r = p/(2 * math.pi)
        theta = 2*math.pi/len(self.nodes)

        dist = r * math.sqrt(2 * (1 - math.cos(theta)))
        demand = int(td / len(self.nodes))

        ar = []
        route = []
        for i in range(len(self.nodes)):
            route.append(i)
            if demand * len(route) > mc:
                route.pop()
                ar.append(route)
                route = []
        if route is not []:
            ar.append(route)

        lb = 0
        for route in ar:
            for i in range(len(route)):
                lb += demand * dist * mv * (len(route) - i - 1)
            lb += demand * dist * mv * len(route)

        return lb

    def gen_file(self):
        self.solve()
        if not os.path.isdir(self.dir1):
            os.mkdir(self.dir1)
        f1 = open(self.dir1 + "/hfccvrp" + str(self.x) + ".sol", "w")
        for i in range(len(self.routes)):
            string = str(self.routes[i].bus.index)
            string += " " + str(len(self.routes[i].edges))
            for node in self.routes[i].edges:
                string += " " + str(node.index)
            f1.write(string + "\n")


for prob in range(1, 22):
    file1 = Vrp(prob)
    file1.solve()
    lb = file1.lower_bound()
    z = file1.objective()
    print(prob, ". z =", file1.objective())
    print("LBC =", (z - lb)/lb)
