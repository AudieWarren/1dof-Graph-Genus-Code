from itertools import combinations
from randomnumbergenerators import *
from algorithm import dirs, go

#Starting point generation starts here - commented out for new improved version
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

# #From minima positions, we create the starting point
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

#Want two random functions on the vertex set, one increasing, one decreasing. These are stored in two lists, Vinc and Vdec
def startingpoint(edges, graphvertices):
  Vinc = []
  Vdec = []
  for i in range(len(graphvertices)):
    if Vinc == []:
      Vinc.append(arbsp())
    else:
      Vinc.append(Vinc[i-1] + arbsp())
    if Vdec == []:
      Vdec.append(arbsp())
    else:
      Vdec.append(Vdec[i-1] - arbsp())
  #Vinc and Vdec are now defined
  print(f"Vinc = {Vinc}")
  print(f"Vdec = {Vdec}")
  px = []
  py = []
  for i in range(len(edges)):
    px.append(min(Vinc[edges[i][0]], Vinc[edges[i][1]]))
    py.append(min(Vdec[edges[i][0]], Vdec[edges[i][1]]))
  # print(f"px before is {px}")
  # print(f"py before is {py}")
  px0 = px[0]
  pyend = py[len(py)-1]
  for i in range(len(px)):
    px[i] = px[i]-px0
    py[i] = py[i]-pyend
  for i in range(len(px)):
    px[i] = px[i] + py[0]
  print(f"Starting point is {px,py}")
  weights = []
  for i in range(len(px)):
    weights.append(px[i]+py[i])
  weightsdiffs = []
  for i in range(len(weights)):
    for j in range(i+1,len(weights)):
      weightsdiffs.append(weights[i]-weights[j])
  # print(f"Weights are {weights}")
  # print(f"Weight differences are {weightsdiffs}")
  # print(f"weight differences len is {len(weightsdiffs)}")
  # print(f"weightdifferences set is {len(set(weightsdiffs))}")
  if len(weightsdiffs) != len(set(weightsdiffs)):
    print(f"there are repeated weight differences")
  return [px, py]

#Starting point may not be a vertex - we move to a vertex before starting the main algorithm
def movetovertex(startingpoint):
  xcoords = startingpoint[0]
  ycoords = startingpoint[1]
  weights = []
  for i in range(len(xcoords)):
    weights.append(xcoords[i]+ycoords[i])
  if len(weights) == len(set(weights)):
    print("This starting point has distinct weights")
  else:
    print("Warning! This starting point does not have distinct weights. Proceed at own risk.")
  Direction, Distance = dirs(startingpoint)
  return go(startingpoint, Direction[0], Distance[0])