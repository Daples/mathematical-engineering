from data-structures import LinkedList as Ll
from data-structures import DigraphAM, DigraphAL
import math as mt

class GraphAlgorithms:
    @staticmethod
    def most_children(directed_graph):
        max_children = 0
        max = 0
        for e in range(directed_graph.n):
            ar = directed_graph.search(e)
            if max_children < len(ar):
                max = e
                max_children = len(ar)

        return max

    # Pseudocode extracted from: https://es.wikipedia.org/wiki/Algoritmo_de_Dijkstra
    # Translated to python by ourselves
    @staticmethod
    def dijkstra(directed_graph, start):
        distance = [0] * directed_graph.n
        for i in range(directed_graph.n):
            if i != start:
                if directed_graph.are_related(start, i):
                    distance[i] = mt.inf
                else:
                    distance[i] = directed_graph.weight(start, i)

        seen = [False] * directed_graph.n
        seen[start] = True
        while False in seen:
            distance = sorted(distance)
            vertex = 0
            index = 1
            while seen[vertex]:
                vertex = index
                index += 1

            seen[vertex] = True
            children = directed_graph.search(vertex)
            for child in children:
                temp_dist = distance[vertex] + directed_graph.weight(vertex, child)
                if distance[child] > temp_dist:
                    distance[child] = temp_dist

        return distance

    @staticmethod
    def bi():
        n = int(input())
        graphs = []
        while n != 0:
            graph = DigraphAM(n)
            graphs.append(graph)
            connections = int(input())
            for i in range(connections):
                rel = input().split(" ")
                graph.insert(int(rel[0]), int(rel[1]))
                graph.insert(int(rel[1]), int(rel[0]))
            n = int(input())

        # O(nm) n el tamaño de vertices en el grafo
        # Y m siendo el máximo número de hijos que tenga un grafo

        def bi_color(graph):
            color = [0] * graph.n  # c1
            visit = [False] * graph.n # c2

            def dfs(node, active):  # O(n)
                children = graph.search(node)
                color[node] = active
                visit[node] = True
                for child in children:
                    if not visit[child]:
                        if active == 1:
                            dfs(child, 0)
                        else:
                            dfs(child, 1)

            dfs(0, 1)  # O(n)

            for i in range(graph.n):  # c3 * n
                children = graph.search(i)  # Matrix: O(n), Linked List: O(m) (children)
                for child in children:  # c4 * n * m
                    if color[child] == color[i]: # c3 n * m
                        return False

            return True #

        for graph in graphs:
            if bi_color(graph):
                print("Is bi colorable")
            else:
                print("Is not bi colorable")

    @staticmethod
    def tests():
        graph1AL = DigraphAL(3)
        graph1AL.insert(0, 1, 5)
        graph1AL.insert(1, 2, 10)
        graph1AL.insert(2, 0, 40)

        graph1AM = DigraphAM(3)
        graph1AM.insert(0, 1, 5)
        graph1AM.insert(1, 2, 10)
        graph1AM.insert(2, 0, 40)

        graph2AL = DigraphAL(3)
        graph2AL.insert(0, 1, 3)
        graph2AL.insert(1, 2, 50)

        graph2AM = DigraphAM(3)
        graph2AM.insert(0, 1, 3)
        graph2AM.insert(1, 2, 50)

        if GraphAlgorithms.dijkstra(graph1AL, 0) == GraphAlgorithms.dijkstra(graph1AM, 0):
            print("First test passed!")
        else:
            print("First test failed!")

        if GraphAlgorithms.dijkstra(graph2AL, 0) == GraphAlgorithms.dijkstra(graph2AM, 0):
            print("Second test passed!")
        else:
            print("Second test failed!")


GraphAlgorithms.tests()
