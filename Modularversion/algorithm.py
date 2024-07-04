import math
import copy
import randomnumbergenerators
import graphgeneration
from transversalitytest import transversalitytest
cyc = graphgeneration.cyc
n = graphgeneration.n
size = randomnumbergenerators.size


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
  weights = []
  for i in range(len(pt[0])):
    weights.append(pt[0][i]+pt[1][i])
  if transversalitytest(pt, weights, cyc) == False:
    print("Non-transverse intersection found")
    exit()
  Vert = []
  Edg = []
  Ray = []
  PVert = [pt]
  InfVert = []
  InfDiresmultset = []
  InfDires = set()
  while len(PVert) > 0:
    pick = PVert[0]
    if transversalitytest(pick, weights, cyc) == False:
      print("Non-transverse intersection found")
      exit()
    PVert = PVert[1:]
    # print(f"Found vertex {pick}")
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
  #Ray = [[T[0], T[1] + len(Vert)] for T in Ray]
  #Vert += InfVert
  return Vert,Edg,Ray,InfDires, InfDiresmultset