""" This file calls the main algorithm and prints the results. """

import graphgeneration
from StartingPoint import *
from algorithm import *
from graphgeneration import *
Tri = graphgeneration.Tri

"""Optional printing of list of cycles."""
# print(f"cycles are {cyc}")

"""Depending on the number of triangles in G, choose different alg."""
if Tri < 4:
    xchoices, ychoices, n = listcreation(cyc, n)
    Vert, Edg, Ray, InfDires, InfDiresmultset = graph(
        movetovertex(pointcreation(xchoices, ychoices, n)))
else:
    Vert, Edg, Ray, InfDires, InfDiresmultset = graph(
        movetovertex(startingpoint(edges, graphvertices)))

genus = len(Edg) - len(Vert) + 1

"""Optional printing of further information."""
print(f"There are {len(Vert)} vertices")
print(f"There are {len(Edg)} bounded edges")
print(f"There are {len(Ray)} infinite rays")
print(f"There are {len(InfDires)} infinite ray directions")
print(f"The genus of (one component of) the curve is {genus}")
# print(f"The infinite ray direction mult set are {InfDiresmultset}")
# print(f"The vertices are {Vert}")
# print(f"The bounded edges are {Edg}")
# print(Edg)
# print(Vert)

"""
The comments below can print a list of the infinite ray directions
and also their multiplicities.
"""
# mults = []
# for dir in InfDires:
#   count = 0
#   for test in InfDiresmultset:
#     # print(f"dir is {dir}")
#     # print(f"test is {test}")
#     if dir == test:
#       count = count + 1
#   mults.append(count)
# sum = 0
# for i in mults:
#   sum = sum + i

# dirswithmult = []
# for i in range(len(InfDires)):
#   dirswithmult.append([list(InfDires)[i],mults[i] ])
# print(f"The mults alone are {mults}")
# print(f"The multiplicity list is {dirswithmult}")
# print(f"length of the mult list is {len(mults)}")
