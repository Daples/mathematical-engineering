import sympy as sp
from sympy.abc import x, t
import numpy as np
import matplotlib.pyplot as plt


np.random.seed(123456789)


# Calculate a brownian motion
def brownian_motion(n, tf, delta_t):
    mb = np.zeros((n, int(tf / delta_t)))
    for i in range(n):
        for j in range(1, int(tf / delta_t)):
            mb[i, j] = mb[i, j - 1] + np.sqrt(delta_t) * np.random.normal(0, 1)
    return mb


# Euler Maruyama method
def euler_m(f, g, delta_t, x0, n, bm=None, tf=-1, t0=-1):
    # Initialize optional parameters
    if bm is None:
        bm = brownian_motion(n, tf - t0, delta_t)
    if tf < 0:
        tf = 1
    if t0 < 0:
        t0 = 0

    # Simulation
    xt = np.zeros((x0.size, int((tf - t0) / delta_t), n))
    for j in range(n):
        xt[:, 0, j] = x0
    for i in range(1, int((tf - t0) / delta_t)):
        t_val = t0 + i*delta_t
        for j in range(n):
            fx = f.subs([(x, xt[:, i - 1, j]), (t, t_val)]).evalf()
            gx = g.subs([(x, xt[:, i - 1, j]), (t, t_val)]).evalf()
            xt[:, i, j] = xt[:, i-1, j] + fx * delta_t + gx * (bm[j, i] - bm[j, i - 1])
    return xt


# Milstein method
def mils(f, g, delta_t, x0, bm=None, tf=-1, t0=-1):
    # Initialize optional parameters
    if bm is None:
        bm = brownian_motion(1, tf - t0, delta_t)
    if tf < 0:
        tf = 1
    if t0 < 0:
        t0 = 0

    # Simulation
    xt = np.zeros((x0.size, int((tf - t0) / delta_t)))
    xt[:, 0] = x0
    for i in range(1, int((tf - t0) / delta_t)):
        t_val = t0 + i*delta_t
        fx = f.subs([(x, xt[:, i - 1]), (t, t_val)]).evalf()
        gx = g.subs([(x, xt[:, i - 1]), (t, t_val)]).evalf()
        gpx = g.diff(x).subs([(x, xt[:, i - 1]), (t, t_val)]).evalf()
        delta_b = bm[0, i] - bm[0, i - 1]
        xt[:, i] = xt[:, i-1] + fx * delta_t + gx * delta_b + 0.5 * gpx * gx * (delta_b ** 2 - delta_t)
    return xt
