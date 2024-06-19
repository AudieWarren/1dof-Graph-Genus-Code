import networkx as nx

#Notice - edge indexing starts from zero!
#Just uncomment the value of n and the cycle list and run the programme. 
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
edges = [(0,1),(0,3),(0,4),(3,4),(2,3),(1,2),(1,5),(4,5)]

#prism edges -genus 5
# edges = [(0,1),(0,2),(0,4),(1,2),(1,5),(2,3),(3,4),(4,5)]

#prism on 4 cycle edges
# edges = [(0,1),(0,2),(0,4),(1,2),(1,5),(2,3),(3,4),(4,5), (3,5), (6,0),(6,7),(7,4)]

#Wagner Graph - genus 225
# edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0),(0,4),(1,5),(2,6),(3,7)]

#cube graph - genus 247
# edges = [(0,1),(1,2),(2,3),(3,0),(0,4),(1,5),(2,6),(3,7),(4,5),(5,6),(6,7),(7,4)]

#Georg/Paul/Niels example
# edges = [(0,1),(1,6),(6,4),(4,3),(3,5),(5,0),(0,2),(1,2),(2,3),(2,4)]

#Josef example on nine vertices
# edges = [(0,1),(0,2),(0,3),(0,4),(5,1),(5,4),(6,1),(6,2),(7,2),(7,3),(8,3),(8,4),(5,8),(6,7)]

#Example of Sitharam,Wang,Gao - genus 129
# edges = [(0,2),(2,1),(1,3),(0,3),(4,5),(5,6),(6,7),(7,4),(2,4),(1,5),(3,6),(3,4)]

# edges = [(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(0,5),(1,5)]
# edges = [(0,3),(0,4),(0,5),(0,6),(1,3),(1,4),(1,6),(2,5),(2,6),(1,2)]


n = len(edges)-1
calligraph = nx.Graph(edges)
vertices = len(list(calligraph.nodes))
vertcyc = list(nx.simple_cycles(calligraph))
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

