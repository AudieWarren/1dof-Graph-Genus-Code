import random
import math
import copy
from itertools import combinations
import networkx as nx

#Notice - edge indexing starts from zero!
#Just uncomment the value of n and the cycle list and run the programme. 
#If no starting point is found, you can input a starting point manually at the bottom of the code. Uncomment the 'graph' function and comment out the 'list creation' function.

#INPUT - n the number of edges minus one, and the list of edges

edges = [(0,1),(0,2),(0,4),(1,5),(1,3),(4,5),(4,6),(2,6),(2,3),(3,7),(7,6),(5,7)]
n = len(edges)-1
calligraph = nx.Graph(edges)
vertcyc = list(nx.simple_cycles(calligraph))
#print(vertcyc)

#H6 graph - similar to cube graph but inner square is half flipped, genus

#3prism - genus 10
# n = 7
# cyc = [[0,1,2],[1,3,4,5],[2,4,5,6,7],[0,3,6,7], [0,2,3,4,5], [0,1,4,5,6,7],[1,2,3,6,7]]

# 4cycle - genus 1
# n=3
# cyc = [[0,1,2,3]]

#cycle with triangles stuck on - genus 1
# n=7
# cyc=[[0,1,2,3],[0,4,5],[1,6,7],[2,3,4,5,6,7],[1,2,3,4,5],[0,3,2,7,6]]

#K2,m - genus (m-2)2^(m-1)+1
# m=4
# n = 2*m - 1
# cyc = []
# for i in range(1, m):
#     for j in range(i+1, m+1):
#         cyc += [[2*i-2,2*i-1,2*j-2,2*j-1]]

#calligraph example from Georg/Niels paper - hard to find starting point
# n=9
# cyc=[[0,1,2],[1,3,4,5],[5,6,7],[2,7,8,9],[0,3,4,6,8,9],[0,2,3,4,5],[1,3,4,6,7],[5,6,2,8,9]]

#cube graph - genus 247
# n = 11
# cyc = [[0,1,2,3],[4,5,6,7],[0,9,4,8],[9,1,5,10],[2,6,10,11],[3,7,8,11],[3,11,6,5,4,8],[0,9,5,6,7,8],[1,9,4,7,6,10],[2,10,5,4,7,11],[2,10,6,7,8,3],[11,7,4,9,0,3],[8,4,5,10,1,0],[1,9,5,6,11,2],[3,11,6,10,1,9,4,8],[2,10,5,9,0,8,7,11],[3,11,6,5,9,0],[3,2,10,5,4,8],[2,1,9,4,7,11],[1,0,8,7,6,10],[1,2,3,8,7,6,5,9],[0,1,2,11,6,5,4,8],[0,1,10,5,4,7,11,3],[0,3,2,10,6,7,4,9],[2,10,5,9,0,3],[8,4,9,1,2,3],[11,7,8,0,1,2],[11,6,10,1,0,3]]

#Wagner graph - genus 225
# n=11
# cyc = [[0,1,2,3,4,5,6,7],[0,8,4,11],[1,9,5,8],[2,10,6,9],[3,10,11,7],[0,1,2,3,11],[1,2,3,4,8],[2,3,4,5,9],[3,4,5,6,10],[4,5,6,7,11],[5,6,7,0,8],[6,7,0,1,9],[7,0,1,2,10],[0,1,9,4,5,11],[1,2,10,6,5,8],[2,3,11,7,6,9],[3,4,8,0,7,10],[0,1,2,10,6,5,4,11],[1,2,3,11,7,6,5,8],[2,3,4,8,0,7,6,9],[3,4,5,9,1,0,7,10],[0,1,9,6,10,3,11],[1,2,10,7,11,4,8],[2,3,11,0,8,5,9],[3,4,8,1,9,6,10],[4,5,9,2,10,7,11],[5,6,10,3,11,0,8],[6,7,11,4,8,1,9],[7,0,8,5,9,2,10]]

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

#Find positions for minima in starting point
def listcreation(cyc,n):
  for j in range(n // 2):
    numberoftriangles = len([triangle for triangle in cyc if len(triangle)==3])
    choices = [list(x) for i in range(n // 2 - j, n + 1) for x in combinations(range(n+1), i)]
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
            return graph(movetovertex(pointcreation(x,y,n)))    
  print("No starting point found")  
  return

#Starting point may not be a vertex - we move to a vertex before starting the main algorithm
def movetovertex(startingpoint):
 Direction, Distance = dirs(startingpoint)
 return go(startingpoint, Direction[0], Distance[0])
 
#From minima positions, we create the starting point
def pointcreation(xchoice,ychoice,n):
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

#Random number generator
size = 1000
def arb():
  return random.randint(1,size)

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
  edges,dists = dirs(pt)
  nbs = []
  for i in range(1,len(edges)+1):
    if not math.isfinite(dists[i-1]):
      dir = edges[i-1]
      pt_copy = copy.deepcopy(pt)
      nbs.append(go(pt_copy, dir, size // 4))
  return nbs

def graph(pt):
  # complete connected graph
  Vert = []
  Edg = []
  Ray = []
  PVert = [pt]
  InfVert = []
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
    ry = rays(pick)
    if len(ry) > 0:
      for ray in ry:
        InfVert += [ray]
        Ray.append([src,len(InfVert)])
  #Ray = [[T[0], T[1] + len(Vert)] for T in Ray]
  #Vert += InfVert
  genus = len(Edg)-len(Vert)+1
  print(f"There are {len(Vert)} vertices")
  print(f"There are {len(Edg)} bounded edges")
  print(f"There are {len(Ray)} rays")
  #print(f"The vertices are {Vert}")
  #print(f"The bounded edges are {Edg}")
  print(f"The genus of (one component of) the curve is {genus}")
  return Vert,Edg,Ray


t1 = arb()
t2 = arb()
#for inputting manual starting point
#graph(movetovertex([[arb(),0,0,arb(),arb(),0,arb(),0,arb(),arb()],[0,0,t1 + t2 + arb(),0,arb(),t1,t1,t1 + t2,t1+t2, t1+t2 + arb()]]))

listcreation(cyc,n)