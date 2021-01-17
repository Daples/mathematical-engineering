#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from fenics import *

class QuadrilateralMesh:
    def __init__(self, vertex_left, vertex_right, part_x, part_y):
        self.vertex_left = vertex_left
        self.vertex_right = vertex_right
        self.part_x = part_x
        self.part_y = part_y

        # Lazily evaluate params
        self.mesh = None
        self.nodes = None
        self.cells = None

    def create_nodes(self):
        x = np.linspace(self.vertex_left[0], self.vertex_right[0], self.part_x)
        y = np.linspace(self.vertex_left[1], self.vertex_right[1], self.part_y)

        # Meshgrid
        xx, yy = np.meshgrid(x, y)

        # Array nodes
        z = 0
        self.nodes = np.zeros((xx.shape[0] * xx.shape[1], 3))
        for i in range(xx.shape[0]):
            for j in range(xx.shape[1]):
                self.nodes[z, :] = [z, xx[i, j], yy[i, j]]
                z += 1

    def create_cells(self):
        if self.nodes is None:
            self.create_nodes()
        width = (self.vertex_right[0] - self.vertex_left[0]) / (self.part_x - 1)
        height = (self.vertex_right[1] - self.vertex_left[1]) / (self.part_y - 1)

        self.cells = []
        z = 0
        for i in range(self.nodes.shape[0]):
            if self.nodes[i, 1] == self.vertex_right[0]:
                continue
            if self.nodes[i, 2] == self.vertex_right[1]:
                continue

            # Create rectangles
            rectangle = np.array([z, 0, 0, 0, self.nodes[i, 0]], dtype=int)
            filled = 0
            for j in range(self.nodes.shape[0]):
                if i == j:
                    continue
                distance_x = self.nodes[j, 1] - self.nodes[i, 1]
                distance_y = self.nodes[j, 2] - self.nodes[i, 2]
                if distance_x >= 0 and distance_y >= 0:
                    if distance_x < 1.5 * width and distance_y < DOLFIN_EPS:
                        rectangle[3] = self.nodes[j, 0]
                        filled += 1

                    elif distance_x < DOLFIN_EPS and distance_y < 1.5 * height:
                        rectangle[2] = self.nodes[j, 0]
                        filled += 1

                    elif distance_x < 1.5 * width and distance_y < 1.5 * height:
                        rectangle[1] = self.nodes[j, 0]
                        filled += 1
                if filled >= 3:
                    break

            z += 1
            self.cells.append(rectangle)
        self.cells = np.array(self.cells)

    def create_mesh(self):
        if self.cells is None:
            self.create_cells()

        self.mesh = Mesh()
        editor = MeshEditor()
        editor.open(self.mesh, 'quadrilateral', 2, 2)

        editor.init_vertices(self.nodes.shape[0])
        editor.init_cells(self.cells.shape[0])

        for i in range(self.nodes.shape[0]):
            editor.add_vertex(int(self.nodes[i, 0]), Point(*self.nodes[i, 1:]))

        for i in range(self.cells.shape[0]):
            editor.add_cell(self.cells[i, 0], self.cells[i, 1:])
        editor.close(order=False)

    def get_mesh(self):
        if self.mesh is None:
            self.create_mesh()
        return self.mesh
