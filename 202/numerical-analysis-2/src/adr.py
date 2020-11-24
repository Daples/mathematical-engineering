from fenics import *
from navier_stokes import get_navier_stokes_sol
from matplotlib.animation import FuncAnimation

import matplotlib.pyplot as plt
import numpy as np

# Do not print
set_log_level(False)

# Parameters
T = 5.0                        # final time
num_steps = 500                # number of time steps
dt = T / num_steps             # time step size
eps = 0.01                     # diffusion coefficient
K = 10.0                       # reaction rate
nu = 0.1                       # Kinematic Viscosity
mesh = Mesh("cylinder.xml.gz") # Mesh

# Define function space for velocity
W = VectorFunctionSpace(mesh, 'P', 2)

# Define function space for system of concentrations
P1 = FiniteElement('P', triangle, 1)
element = MixedElement([P1, P1, P1])
V = FunctionSpace(mesh, element)

# Define test functions
v_1, v_2, v_3 = TestFunctions(V)

# Define functions for velocity and concentrations
w = Function(W)
u = Function(V)
u_n = Function(V)

# Split system functions to access components
u_1, u_2, u_3 = split(u)
u_n1, u_n2, u_n3 = split(u_n)

# Define source terms
f_1 = Expression('pow(x[0]-0.1,2)+pow(x[1]-0.1,2)<0.05*0.05 ? 0.1 : 0',
                 degree=1)
f_2 = Expression('pow(x[0]-0.1,2)+pow(x[1]-0.3,2)<0.05*0.05 ? 0.1 : 0',
                 degree=1)
f_3 = Constant(0)

# Define expressions used in variational forms
k = Constant(dt)
K = Constant(K)
eps = Constant(eps)

# Define variational problem
F = ((u_1 - u_n1) / k)*v_1*dx + dot(w, grad(u_1))*v_1*dx \
  + eps*dot(grad(u_1), grad(v_1))*dx + K*u_1*u_2*v_1*dx  \
  + ((u_2 - u_n2) / k)*v_2*dx + dot(w, grad(u_2))*v_2*dx \
  + eps*dot(grad(u_2), grad(v_2))*dx + K*u_1*u_2*v_2*dx  \
  + ((u_3 - u_n3) / k)*v_3*dx + dot(w, grad(u_3))*v_3*dx \
  + eps*dot(grad(u_3), grad(v_3))*dx - K*u_1*u_2*v_3*dx + K*u_3*v_3*dx \
  - f_1*v_1*dx - f_2*v_2*dx - f_3*v_3*dx

# Create time series for reading velocity data
timeseries_w = get_navier_stokes_sol(dt, T, nu, mesh)
timeseries_u = []

# Time-stepping
t = 0
for n in range(num_steps):
    # Update current time
    t += dt

    # Read velocity from file
    w.assign(timeseries_w[n][0])

    # Solve variational problem for time step
    solve(F == 0, u)

    # Update previous solution
    timeseries_u.append(u.copy(deepcopy=True))
    u_n.assign(u)

# Cylinder parameters
center = np.array([0.2, 0.2])
radius = 0.05

def get_animation():
    # Plot animation
    fig = plt.figure(figsize=(12, 5))
    ax = plt.axes()
    circle = plt.Circle(center, radius, facecolor="w", edgecolor="w")
    ax.add_artist(circle)

    # Meshgrid
    xl = np.linspace(0, 2.2, 50)
    yl = np.linspace(0, 0.41, 50)
    xx, yy = np.meshgrid(xl, yl)

    # Calculate zs
    zs = []
    for u in timeseries_u:
        zs.append([np.zeros(xx.shape), np.zeros(xx.shape), np.zeros(xx.shape)])
        for i in range(xx.shape[0]):
            for j in range(xx.shape[1]):
                x = xx[i, j]
                y = yy[i, j]
                if (x - center[0]) ** 2 + (y - center[1]) ** 2 >= radius ** 2:
                    zs[-1][0][i, j] = u(x, y)[0]
                    zs[-1][1][i, j] = u(x, y)[1]
                    zs[-1][2][i, j] = u(x, y)[2]

    # Animations
    def animate(i, uj=0):
        cont = plt.contourf(xx, yy, zs[i][uj], 50, cmap="plasma")
        return cont

    animate1 = lambda i : animate(i, uj=0)
    animate2 = lambda i : animate(i, uj=1)
    animate3 = lambda i : animate(i, uj=2)

    # Extract each mp4
    desired_time = 10
    ani = FuncAnimation(fig, animate1, frames=range(len(timeseries_u)),
                        interval=int(dt*1000*desired_time/T))
    ani.save("a-chemical.mp4")

    ax.clear()
    circle = plt.Circle(center, radius, facecolor="w", edgecolor="w")
    ax.add_artist(circle)
    ani = FuncAnimation(fig, animate2, frames=range(len(timeseries_u)),
                        interval=int(dt*1000*desired_time/T))
    ani.save("b-chemical.mp4")

    ax.clear()
    circle = plt.Circle(center, radius, facecolor="w", edgecolor="w")
    ax.add_artist(circle)
    ani = FuncAnimation(fig, animate3, frames=range(len(timeseries_u)),
                        interval=int(dt*1000*desired_time/T))
    ani.save("c-chemical.mp4")

get_animation()
