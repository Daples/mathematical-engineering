#!/usr/bin/env python3

import tools
from fenics import *

tol = DOLFIN_EPS

# Triangular elements
mesh = UnitSquareMesh(32, 32)

V = FunctionSpace(mesh, "Lagrange", 1)

# Dirichlet boundary (With equal dirichlet conditions)
def boundary(x, on_boundary):
    return on_boundary

u0 = Constant(0.0)
bc = DirichletBC(V, u0, boundary)

# Variational problem definition
u = TrialFunction(V)
v = TestFunction(V)
f = Expression("2*pi*sin(pi*x[0])*sin(pi*x[1])", degree=2)

a = inner(grad(u), grad(v))*dx
L = f*v*dx

# Solution
u = Function(V)
solve(a == L, u, bc)

# Plotting
tools.plot3d(60, 60, u, "figs/exerc-6a.pdf")
tools.plot(500, 500, u, "figs/exerc-6a-2d.pdf", num_lines=60)
