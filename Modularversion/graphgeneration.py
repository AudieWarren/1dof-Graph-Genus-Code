import networkx as nx

#Notice - edge indexing starts from zero!
#Uncomment/write the cycles of your graph and run main. 
#If no starting point is found, you can input a starting point manually at the bottom of the code. Uncomment the 'graph' function and comment out the 'list creation' function.

#INPUT - the list of edges

# K24-genus 17
# 3prism without int triangle edge - genus 5

#k23 edges - genus 5
# edges = [(0,2),(0,3),(0,4),(1,2),(1,3),(1,4)]

#k24 - genus 17
# edges = [(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(0,5),(1,5)]

#k33 minus an edge - genus 17
# edges = [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4)]

#C4 edges - genus 1
# edges = [(0,1),(1,2),(2,3),(3,0)]

#Two 4-cycles with a triangle
# edges = [(0,1),(0,3),(0,4),(3,4),(2,3),(1,2),(1,5),(4,5)]

#7-cycle with 3 diagonals
# edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,0),(1,5),(2,6),(0,4)]

#6cycle with degree 4 vertex
# edges = [(0,1),(1,2),(2,3),(3,5),(5,6),(6,0),(0,4),(1,4),(3,4),(5,4)]

#1-ext on 3prism, applied to side edge, connect to inner vert. 
# edges = [(0,1),(1,2),(2,0),(0,3),(1,4),(3,4),(4,5),(3,5),(2,6),(5,6)]

#Housespider
# edges = [(0,1),(1,4),(1,2),(2,3),(3,4),(4,0),(0,6),(1,7),(2,8),(3,9),(4,5),(5,6),(6,7),(7,8),(8,9),(9,5)]

#Diamond graph
# edges = [(0,1),(1,2),(2,3),(3,4),(4,0),(0,6),(6,3),(4,5),(5,6),(5,2)]

#Open envelope graph
# edges = [(0,1),(1,2),(2,3),(3,4),(4,0),(4,5),(3,5),(5,6),(6,1),(6,2)]

#prism edges -genus 5
# edges = [(0,1),(0,2),(0,4),(1,2),(1,5),(2,3),(3,4),(4,5)]

#prism on 4 cycle edges
# edges = [(0,1),(0,2),(0,4),(1,2),(1,5),(2,3),(3,4),(4,5), (3,5), (6,0),(6,7),(7,4)]

#Wagner Graph - genus 225
edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0),(0,4),(1,5),(2,6),(3,7)]

#cube graph - genus 247
# edges = [(0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(7,4)]

#3-reg on 8 vertices
# edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0),(0,4),(1,7),(2,5),(3,6)]

#Spider graph 3
# edges = [(0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(7,4),(8,4),(9,5),(10,6),(11,7),(8,9),(9,10),(10,11),(11,8)]

#double house spider
# edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,2),(3,5)]
# edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,2),(3,5),(0,6),(1,7),(2,8),(3,9),(4,10),(5,11),(6,7),(7,8),(8,9),(9,10),(10,11),(11,6)]

#Omn graph
# m,n = 3,3
# edges = [(0,1),(1,2),(2,3),(3,0)]
# for i in range(4,m+4):
#   edges.append((1,i))
#   edges.append((3,i))
# for j in range(m+4,m+n+4):
#   edges.append((0,j))
#   edges.append((2,j))


n = len(edges)-1
calligraph = nx.Graph(edges)

H = calligraph.to_directed()

precyc = list(nx.simple_cycles(H))
precyc = [cycle for cycle in precyc if len(cycle)>2]
vertcyc = []
setcyc = []
for cycle in precyc:
    if set(cycle) not in setcyc:
        vertcyc.append(list(cycle))
        setcyc.append(set(cycle))

# print(f"vertcyc is {vertcyc}")

vertices = len(list(calligraph.nodes))
graphvertices = list(calligraph)

if (2*vertices - 4 != n+1):
  print("This does not look like a calligrah - does not satisfy edge count")
  exit()

Tridict = nx.triangles(calligraph, None)    
Tri = sum(Tridict.values())

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
    cyc.append(cycle)
  return cyc

#Define the cycles of the graph
cyc = vertexedgeconvert(vertcyc)

