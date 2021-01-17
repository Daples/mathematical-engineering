class Node:
    def __init__(self, data):
        self.up = None
        self.down = None
        self.data = data

class Tree:
    def __init__(self):
        self.root = None
        self.depth = 0

    def create_depth(self, N):
        if self.root is None:
            self.root = Node(0)
        self.create_depth_aux(N, self.root)
        self.depth = N

    def create_depth_aux(self, N, node):
        if N > 0:
            node.down = Node(0)
            node.up = Node(0)
            self.create_depth_aux(N - 1, node.down)
            self.create_depth_aux(N - 1, node.up)

    def calc_in_depth(self, j, fun, cut=False):
        self.calc_in_depth_aux(0, j, j, fun, self.root, cut)

    def calc_in_depth_aux(self, i, j, jmax, fun, node, cut):
        if j == 0:
            if cut and i <= jmax:
                node.data = fun(node, i)
            elif not cut:
                node.data = fun(node, i)
        else:
            if node.up is not None:
                self.calc_in_depth_aux(i, j - 1, jmax, fun, node.up, cut)
            if node.down is not None:
                self.calc_in_depth_aux(2 ** (j - 1) + i, j - 1, jmax, fun, node.down, cut)
