#!/usr/bin/env python3

import tools
from fenics import *

tol = DOLFIN_EPS

# Mesh
mesh = UnitSquareMesh(20, 20)
V = FunctionSpace(mesh, 'P', 1)

# Dirichlet boundary 1
def boundary(x, on_boundary):
    return on_boundary and (near(x[0], 0, tol) or (near(x[1], 1, tol)))

u0 = Constant(0.0)
bc1 = DirichletBC(V, u0, boundary)

# Dirichlet boundary 2
def boundary2(x, on_boundary):
    return on_boundary and near(x[1], 0, tol)

u0 = Expression("1 - exp(-x[0])", degree=2)
bc2 = DirichletBC(V, u0, boundary2)

# Dirichlet boundary 3
def boundary3(x, on_boundary):
    return on_boundary and near(x[0], 1, tol)

u0 = Expression("4 - exp(-x[1])", degree=2)
bc3 = DirichletBC(V, u0, boundary3)

# Variational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Expression("250 - pow(x[0], 2) - 6*pow(x[1], 2)", degree=2)

a = inner(grad(u), grad(v))*dx
L = f*v*dx

# Solution
u = Function(V)
solve(a == L, u, [bc1, bc2, bc3])

# Plotting
tools.plot3d(60, 60, u, "figs/exerc-8.pdf")
tools.plot(100, 100, u, "figs/exerc-8-2d.pdf", num_lines=60)
