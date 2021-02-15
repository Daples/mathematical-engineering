import math as m
import numpy as np
import matplotlib.pyplot as plt


def distance(p1, p2):
    if p1[0] == p2[0]:
        return abs(p1[1] - p2[1])
    return abs(p1[1]) + abs(p2[1]) + abs(p1[0] - p2[0])


def generate_points(n, r, h=0.1):
    def move(dir1, m2):
        p1 = [0, 0]
        while distance((0, 0), p1) < r:
            p1[0] += dir1*h
            p1[1] = m2*p1[0]
        p1[0] -= dir1*h
        p1[1] = m2*p1[0]
        return p1

    points = []
    for i in range(n):
        m1 = m.tan(m.pi*i/n)
        points.append(move(1, m1))
        points.append(move(-1, m1))

    return points


figure = generate_points(50, 1, h=0.01)
xs = np.array(list(map(lambda x: x[0], figure)))
ys = np.array(list(map(lambda x: x[1], figure)))

plt.scatter(xs, ys)
plt.show()
