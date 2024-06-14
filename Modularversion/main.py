import graphgeneration
Tri = graphgeneration.Tri
from StartingPoint import *
from algorithm import *
from graphgeneration import *


if Tri < 4:
    xchoices, ychoices, n = listcreation(cyc,n)
    Vert, Edg, Ray, InfDires, InfDiresmultset = graph(movetovertex(pointcreation(xchoices, ychoices, n))) 
else: 
    Vert, Edg, Ray, InfDires, InfDiresmultset = graph(movetovertex(startingpoint(edges, graphvertices)))
    
genus = len(Edg)-len(Vert)+1

print(f"There are {len(Vert)} vertices")
print(f"There are {len(Edg)} bounded edges")
print(f"There are {len(Ray)} infinite rays")
print(f"There are {len(InfDires)} infinite ray directions")
print(f"The genus of (one component of) the curve is {genus}")
# print(f"The infinite ray directions are {InfDires}")
# print(f"The vertices are {Vert}")
# print(f"The bounded edges are {Edg}")