import graphgeneration
Tri = graphgeneration.Tri
from StartingPoint import *
from algorithm import *
from graphgeneration import *

print(f"cycles are {cyc}")
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
# print(f"The infinite ray direction mult set are {InfDiresmultset}")
# print(f"The vertices are {Vert}")
# print(f"The bounded edges are {Edg}")

# print(Edg)
# print(Vert)
# Area = 0
# for pair in Edg:
#     edgearea = math.dist(Vert[pair[0]-1][0],Vert[pair[1]-1][0])
#     Area = Area + edgearea
    
# print(f"The area of the curve is {Area}")


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