#!/usr/bin/env python3

import tools
from fenics import *

tol = DOLFIN_EPS

# Mesh
mesh = UnitSquareMesh(20, 20)
V = FunctionSpace(mesh, 'P', 1)

# Dirichlet boundary
def boundary(x, on_boundary):
    return on_boundary and (near(x[0], 1, tol) or (near(x[1], 1, tol)))

u0 = Constant(0.0)
bc = DirichletBC(V, u0, boundary)

# Variational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Expression("1", degree=0)
g = Expression("0", degree=0)

a = inner(grad(u), grad(v))*dx
L = f*v*dx + g*v*ds

# Solution
u = Function(V)
solve(a == L, u, bc)

# Plotting
tools.plot3d(60, 60, u, "figs/exerc-5.pdf")
tools.plot(100, 100, u, "figs/exerc-5-2d.pdf", num_lines=60)

# Values
print(u(0.5, 0.5))
