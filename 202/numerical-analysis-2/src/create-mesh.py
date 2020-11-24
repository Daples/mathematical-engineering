#!/usr/bin/env python3

from fenics import *
from mshr import *

# Create mesh
channel = Rectangle(Point(0, 0), Point(2.2, 0.41))
cylinder = Circle(Point(0.2, 0.2), 0.05)
domain = channel - cylinder
mesh = generate_mesh(domain, 64)

# Save mesh to file (for use in reaction_system.py)
File('cylinder.xml.gz') << mesh
