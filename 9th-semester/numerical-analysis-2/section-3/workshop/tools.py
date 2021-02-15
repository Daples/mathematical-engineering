#!/usr/bin/env python3

from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np

rc('text', usetex=True)

# Auxiliar function for plotting
def getZ(x, y, u_func):
    Z = np.zeros(x.shape)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            Z[i, j] = u_func(x[i, j], y[i, j])
    return Z

def plot3d(x_part, y_part, u, name):
    xline = np.linspace(0, 1, x_part)
    yline = np.linspace(0, 1, y_part)
    X, Y = np.meshgrid(xline, yline)
    Z = getZ(X, Y, u)

    # Plotting
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, edgecolor='none',
                    cmap='plasma')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_zlabel('$u(x,y)$')
    plt.savefig(name, bbox_inches='tight')

def plot(x_part, y_part, u, name, num_lines=20):
    xline = np.linspace(0, 1, x_part)
    yline = np.linspace(0, 1, y_part)
    X, Y = np.meshgrid(xline, yline)
    Z = getZ(X, Y, u)

    # Plotting
    fig = plt.figure()
    ax = plt.axes()
    pcm = ax.contourf(X, Y, Z, num_lines, cmap='plasma')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    fig.colorbar(pcm, ax=ax)
    plt.savefig(name, bbox_inches='tight')
