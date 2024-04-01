import random
import math
import copy
import sys
import ast
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import tkinter as tk
import subprocess

#Notice - edge indexing starts from zero!
#Just uncomment the value of n and the cycle list and run the programme. 
#If no starting point is found, you can input a starting point manually at the bottom of the code. Uncomment the 'graph' function and comment out the 'list creation' function.

#INPUT - the list of edges

#k23 edges
# edges = [(0,2),(0,3),(0,4),(1,2),(1,3),(1,4)]

#C4 edges
# edges = [(0,1),(  1,2),(2,3),(3,0)]

#prism edges
# edges = [(0,1),(0,2),(0,4),(1,2),(1,5),(2,3),(3,4),(4,5)]

#prism on 4 cycle edges
# edges = [(0,1),(0,2),(0,4),(1,2),(1,5),(2,3),(3,4),(4,5), (3,5), (6,0),(6,7),(7,4)]

#Wagner Graph
# edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0),(0,4),(1,5),(2,6),(3,7)]

#cube graph
# edges = [(0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(7,4)]

#Georg/Paul/Niels example
# edges = [(0,1),(1,6),(6,4),(4,3),(3,5),(5,0),(0,2),(1,2),(2,3),(2,4)]

edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(1,6),(3,6),(4,6)]
print(f"edges before = {edges}")
# edges = edges.split()
# edges = [arg.strip() for arg in ' '.join(edgesinput).split()]
# print(f"edges are {edges}")
n = len(edges)-1
calligraph = nx.Graph(edges)
vertices = len(list(calligraph.nodes))
vertcyc = list(nx.simple_cycles(calligraph))
size = 10000
smallsize = 3
#print(vertcyc)

#3prism minus internal triangle edge - genus 10 (two components of genus 5)
# n = 7
# cyc = [[0,1,2],[1,3,4,5],[2,4,5,6,7],[0,3,6,7], [0,2,3,4,5], [0,1,4,5,6,7],[1,2,3,6,7]]

# 4cycle - genus 1
# n=3
# cyc = [[0,1,2,3]]

#cycle with triangles stuck on - genus 1
# n=7
# cyc=[[0,1,2,3],[0,4,5],[1,6,7],[2,3,4,5,6,7],[1,2,3,4,5],[0,3,2,7,6]]

#K2,m - genus (m-2)2^(m-1)+1
# m=3
# n = 2*m - 1
# cyc = []
# for i in range(1, m):
#     for j in range(i+1, m+1):
#         cyc += [[2*i-2,2*i-1,2*j-2,2*j-1]]

#calligraph example from Georg/Paul/Niels paper - hard to find starting point
# n=9
# cyc=[[0,1,2],[1,3,4,5],[5,6,7],[2,7,8,9],[0,3,4,6,8,9],[0,2,3,4,5],[1,3,4,6,7],[5,6,2,8,9]]

#cube graph - genus 247
# n = 11
# cyc = [[0,1,2,3],[4,5,6,7],[0,9,4,8],[9,1,5,10],[2,6,10,11],[3,7,8,11],[3,11,6,5,4,8],[0,9,5,6,7,8],[1,9,4,7,6,10],[2,10,5,4,7,11],[2,10,6,7,8,3],[11,7,4,9,0,3],[8,4,5,10,1,0],[1,9,5,6,11,2],[3,11,6,10,1,9,4,8],[2,10,5,9,0,8,7,11],[3,11,6,5,9,0],[3,2,10,5,4,8],[2,1,9,4,7,11],[1,0,8,7,6,10],[1,2,3,8,7,6,5,9],[0,1,2,11,6,5,4,8],[0,1,10,5,4,7,11,3],[0,3,2,10,6,7,4,9],[2,10,5,9,0,3],[8,4,9,1,2,3],[11,7,8,0,1,2],[11,6,10,1,0,3]]

#Wagner graph - genus 225
# n=11
# cyc = [[0,1,2,3,4,5,6,7],[0,8,4,11],[1,9,5,8],[2,10,6,9],[3,10,11,7],[0,1,2,3,11],[1,2,3,4,8],[2,3,4,5,9],[3,4,5,6,10],[4,5,6,7,11],[5,6,7,0,8],[6,7,0,1,9],[7,0,1,2,10],[0,1,9,4,5,11],[1,2,10,6,5,8],[2,3,11,7,6,9],[3,4,8,0,7,10],[0,1,2,10,6,5,4,11],[1,2,3,11,7,6,5,8],[2,3,4,8,0,7,6,9],[3,4,5,9,1,0,7,10],[0,1,9,6,10,3,11],[1,2,10,7,11,4,8],[2,3,11,0,8,5,9],[3,4,8,1,9,6,10],[4,5,9,2,10,7,11],[5,6,10,3,11,0,8],[6,7,11,4,8,1,9],[7,0,8,5,9,2,10]]

if (2*vertices - 4 != n+1):
  print("This does not look like a calligrah - does not satisfy edge count")
  exit()

#this function converts the cycles in terms of vertices to cycles in terms of edges
def vertexedgeconvert(Vcyc):
  cyc = []
  for vcycle in Vcyc:
    cycle = []
    for i in range(len(vcycle)):
      for j in range(len(edges)):
        if i < len(vcycle)-1:
          if {vcycle[i],vcycle[i+1]} == set(edges[j]):
            cycle.append(j)
        elif i == len(vcycle)-1:
          if {vcycle[i],vcycle[0]} == set(edges[j]):
            cycle.append(j)
    #print(cycle)
    cyc.append(cycle)
    #print(cyc)
  return cyc

#Define the cycles of the graph
cyc = vertexedgeconvert(vertcyc)
triangles = [triangle for triangle in cyc if len(triangle)==3]
numberoftriangles = len([triangle for triangle in cyc if len(triangle)==3])
#Find positions for minima in starting point
def listcreation(cyc,n):
  for j in range(n//2):
    choices = [list(x) for i in range(n//2 - j, n + 1) for x in combinations(range(n+1), i)]
    continue_x = False
    for x in choices:
      if continue_x == True:
        continue_x = False
        continue
      for y in choices:
          continue_y = False
          if continue_x == True:
            break
          for cycle in cyc:
            if len(set(x).intersection(set(cycle))) < 2:
              continue_x = True
              break
            if len(set(y).intersection(set(cycle))) < 2:
              continue_y = True
              break
          if continue_x == True:
            continue
          if continue_y == True:
            continue
          if len(set(x).intersection(set(y)))< 2:
            return x,y,n   
  print("No starting point found")  
  return

#Starting point may not be a vertex - we move to a vertex before starting the main algorithm
def movetovertex(startingpoint):
  xcoords = startingpoint[0]
  ycoords = startingpoint[1]
  weights = []
  for i in range(len(xcoords)):
    weights.append(xcoords[i]+ycoords[i])
  if len(weights) == len(set(weights)):
    print("This starting point is generic")
  else:
    print("Warning! This starting point is not generic. Proceed at own risk.")
  Direction, Distance = dirs(startingpoint)
  return go(startingpoint, Direction[0], Distance[0])
 
#From minima positions, we create the starting point
def pointcreation(xchoice,ychoice,n):  
    mins = [0]
    xcoords = []
    ycoords = []
    for i in range(n+1):
      xcoords += [arb()]
      ycoords += [arb()]
    for j in xchoice:
      xcoords[j] = 0
    for k in ychoice:
      ycoords[k] = 0
    print(f"starting point is {[xcoords,ycoords]}")
    return [xcoords,ycoords]

#Random number generators
def arb():
  return random.randint(1,size)

def smallarb():
  return random.randint(-smallsize,smallsize)

def minpairs(P):
  # for each cycle such that the minimum is reached twice, the list of these pairs
  Mxy = []
  for cc in cyc:
    mx = min(P[0][T] for T in cc)
    pair = [T for T in cc if P[0][T] == mx]
    if len(pair)==2:
      Mxy += [pair]
    elif len(pair)==1:
      raise ValueError("not on curve")
    my = min(P[1][T] for T in cc)
    pair =  [T for T in cc if P[1][T] == my]
    if len(pair)==2:
      Mxy += [pair]
    elif len(pair)==1:
      raise ValueError("not on curve")
  return Mxy

def havecommon(L1,L2):
  return bool(set(L1) & set(L2))

def trans2(prs):
  if len(prs) > 1:
    bubble = prs[0]
    common = []
    for i in range(2, len(prs)+1):
      if havecommon(bubble,prs[i-1]):
        common.append(i)
    if len(common)>0:
      disj = prs[1:]
      for i in common:
        bubble = list(set(bubble + prs[i-1]))
        disj = prs[1:i-1] + prs[i:]
      return trans2([bubble] + disj)
    else:
      others = trans2(prs[1:])
      return [bubble] + others 
  else:
    return prs 

def stopp(pt,dir):
  # how far can we go starting at pt heading dir?
  goal = float('inf')
  for cc in cyc:
    mx = min([pt[0][T] for T in cc])
    Mp = [T for T in cc if pt[0][T] == mx]
    stay = set(Mp) - set(dir)
    if len(stay) == 0: # we may go until next smallest value is reached
      if len(set(cc)-set(dir)) > 0:
        tres = min(pt[0][T] for T in set(cc) - set(dir)) - mx
        goal = min(goal,tres)
    elif len(stay) == 1: # cannot even start going
      goal = 0
    cdir = list(set(range(n+1)) - set(dir))
    my = min([pt[1][T] for T in cc])
    Mp = [T for T in cc if pt[1][T]==my]
    stay = set(Mp) - set(cdir)
    if len(stay) == 0:
        if len(set(cc) - set(cdir))>0:
          tres = min(pt[1][T] for T in set(cc) - set(cdir)) - my
          goal = min(goal,tres)
    elif len(stay) == 1:
      goal = 0
  return goal

def dirs(P):
# directions and distances to next vertex
  # list "dires" of candidates obtained by necessary equalities
  bubbles = trans2(minpairs(P))
  for i in range(n+1):
    j = 0
    for x in bubbles:
      if i in x:
        j=j+1
    if j == 0:
      bubbles.append([i])
  nb = len(bubbles)
  dires = []
  for pos in range(1,(2 ** nb)-1):
    dir = []
    pob = pos # binary digits
    for i in range(1,nb+1):
      if pob % 2 == 1:
        for x in bubbles[i-1]:
          dir.append(x)
        pob = pob-1
      pob = pob / 2 # cut off last binary digit
    dires.append(dir)
  # compute distances and throw away zero distance candidates
  fdires = []
  fdists = []
  for dir in dires:
    ds = stopp(P,dir)
    if ds > 0:
      fdires.append(dir)
      fdists.append(ds)
  return fdires,fdists

def gofar(pt,dir,distance):
  # go to the next point
  cdir = list(set(range(n+1)) - set(dir))
  qt = pt
  if 0 in dir:
    for k in cdir:
      qt[0][k] = qt[0][k]-distance
      qt[1][k] = qt[1][k]+distance
  else:
    for k in dir:
      qt[0][k] = qt[0][k]+distance
      qt[1][k] = qt[1][k]-distance
  return qt

def go(pt,dir,dist):
  # go to the next point
  cdir = list(set(range(n+1)) - set(dir))
  qt = pt
  if 0 in dir:
    for k in cdir:
      qt[0][k] = qt[0][k] - dist
      qt[1][k] = qt[1][k] + dist
  else:
    for k in dir:
      qt[0][k] = qt[0][k] + dist
      qt[1][k] = qt[1][k] - dist
  return qt

def neighbors(pt):
  # neighbor vertices
  edges,dists = dirs(pt)
  nbs = []
  for i in range(len(edges)):
    if math.isfinite(dists[i]):
      dir = edges[i]
      pt_copy = copy.deepcopy(pt)
      nbs.append(go(pt_copy, dir, dists[i]))
  return nbs

def rays(pt):
  # infinite rays from vertex
  directions,dists = dirs(pt)
  # print(f"directions = {directions}")
  nbs = []
  infdires = set()
  for i in range(len(directions)):
    if not math.isfinite(dists[i]):
      dir = directions[i]
      # print(f"dir = {dir}")
      infdires.add(tuple(sorted(dir)))
      # print(f"infdires is {infdires}")
      # print(f"Infinite ray direction is {dir}")
      pt_copy = copy.deepcopy(pt)
      nbs.append(go(pt_copy, dir, size // 4))
  return nbs, infdires

def graph(pt):
  # complete connected graph
  Vert = []
  Edg = []
  Ray = []
  PVert = [pt]
  InfVert = []
  InfDiresmultset = []
  InfDires = set()
  while len(PVert) > 0:
    pick = PVert[0]
    PVert = PVert[1:]
    #print(f"Found vertex {pick}")
    Vert = Vert + [pick]
    src = len(Vert)
    nxt = neighbors(pick)
    nxt = [list(x) for x in nxt if x not in Vert]
    nnxt = [list(x) for x in nxt if x not in PVert]
    PVert = PVert +  nnxt 
    for i in range(1,len(PVert)+1):
      if PVert[i-1] in nxt:
        Edg.append([src,len(Vert)+i])
    ry, infdir = rays(pick)
    # print(f"inf dir is {infdir}")
    if len(ry) > 0:
      # print(f"infdir = {infdir}")
      InfDires.update(infdir)
      for i in range(len(ry)):
        InfDiresmultset.append(list(infdir)[i])
      for ray in ry:
        InfVert += [ray]
        Ray.append([src,len(InfVert)])
    # if len(Vert) > 400:
    #   return Vert,Edg,Ray,InfDires, InfDiresmultset
  #Ray = [[T[0], T[1] + len(Vert)] for T in Ray]
  #Vert += InfVert
  return Vert,Edg,Ray,InfDires, InfDiresmultset


t1 = arb()
t2 = arb()
t3 = arb()
t4 = arb()
t5 = arb()
t6 = arb()
t7 = arb()
t8 = arb()
t0 = arb()
t9 = arb()
s1 = arb()
s2 = arb()
s3 = arb()
s4 = arb()
s5 = arb()
s6 = arb()
s7 = arb()
s8 = arb()
s0 = arb()
s9 = arb()
#for inputting manual starting point
#k23 with cycle of form a,a,b,b - non-generic and non-transverse intersection
# px = [0,t2,t2,t1,0,0]
# py = [t3,t4,t4,0,0,0]

#generic starting point for k23
# px = [0,arb(),0,arb(),0,arb()]
# py = [0,0,arb(),0,arb(),0]

# Example non-generic starting point from k23 which draws out a face
# px = [0,0,0,0,0,1]
# py = [0,0,0,0,1,0]

#Zero starting point
# px = [0 for i in range(n+1)]
# py = [0 for i in range(n+1)]

px = [t0,t1,min(t0,t1,t6,t9),min(t8,t9),0,0,t6,min(t0,t6),t9,t8]
py = [0,min(s2,s3,s7,s8),s2,s3,s4,0,0,s7,min(s3,s8),s8]
Vert, Edg, Ray, InfDires, InfDiresmultset = graph(movetovertex([px,py]))

# xchoices, ychoices, n = listcreation(cyc,n)
# Vert, Edg, Ray, InfDires, InfDiresmultset = graph(movetovertex(pointcreation(xchoices, ychoices, n))) 

genus = len(Edg)-len(Vert)+1
print(f"There are {len(Vert)} vertices")
print(f"There are {len(Edg)} bounded edges")
print(f"There are {len(Ray)} infinite rays")
print(f"There are {len(InfDires)} infinite ray directions")
# print(f"The infinite ray directions are {InfDires}")
# print(f"The vertices are {Vert}")
# print(f"The bounded edges are {Edg}")
mults = []
for dir in InfDires:
  count = 0
  for test in InfDiresmultset:
    # print(f"dir is {dir}")
    # print(f"test is {test}")
    if dir == test:
      count = count + 1
  mults.append(count)
sum = 0
for i in mults:
  sum = sum + i
  
dirswithmult = []
for i in range(len(InfDires)):
  dirswithmult.append([list(InfDires)[i],mults[i] ])
print(f"The mults alone are {mults}")
# print(f"The multiplicity list is {dirswithmult}")
print(f"length of the mult list is {len(mults)}")
print(f"the sum of mults is {sum}")
print(f"The genus of (one component of) the curve is {genus}")

#Vert = [[1,2,3,4,5,8],[7,8,9,6,1,0],[0,6,4,3,3,1]
#Edg = [[0,1],[1,2],[0,2]]

#we define a random projection on k variables. The input set must be a list of lists, each list having k entries
def randomprojection(set, k):
  coeff1= []
  coeff2 = []
  for i in range(k):
    coeff1.append(smallarb())
    coeff2.append(smallarb())
  images = []
  for input in set:
    output1 = np.dot(coeff1, input)
    output2 = np.dot(coeff2, input)
    output = [output1, output2]
    images.append(output)
  return images

#We now throw away y coords for vertices
XVert = []
for vertex in Vert:
  XVert.append(vertex[0])
#print(f"XVert is {XVert}")

#k is the number of variable
k = len(XVert[0])

#We now map down to two dimensions
ProjVert = randomprojection(XVert, k)
# print(f"lenProjVert is {len(ProjVert)}")
# We now plot the random projection of the tropical curve
for edge in Edg:
    xcoords = [ProjVert[edge[0]-1][0],ProjVert[edge[1]-1][0]]
    ycoords = [ProjVert[edge[0]-1][1],ProjVert[edge[1]-1][1]]
    #print(f"start = {start}")
    #print(f"end = {end}")
    plt.plot(xcoords,ycoords,'k-')
for vertex in ProjVert:
    plt.plot(vertex[0],vertex[1],'ro')
plt.axis('equal')
plt.show() 

# HERE BEGINS THE ANIMATION STUFF

G = nx.Graph()
G.add_edges_from(Edg)

vertices = {}
for i in range(len(ProjVert)):
  vertices.update({i+1 : (ProjVert[i][0],ProjVert[i][1])})


def step(frame):
    ax.clear() 
    linesegments = list(G.edges())[:frame+1]
    nodes = [node for edge in linesegments for node in edge]
    nx.draw(G, pos=vertices, ax=ax, edgelist=linesegments, nodelist=nodes, edge_color='red',width = 2, node_size=10)
    if frame > len(G.edges)-2:
        ani.event_source.stop()
drawing, ax = plt.subplots()

ani = FuncAnimation(drawing, step, frames=len(G.edges), interval=200)

plt.show()
