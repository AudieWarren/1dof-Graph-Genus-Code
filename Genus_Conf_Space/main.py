"""
This is the main file.
It calls the algorithm and creates a picture and animation.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from randomnumbergenerators import *
import application
import networkx as nx
Edg = application.Edg
Vert = application.Vert


def randomprojection(set, k):
    """
    To create a picture, we will project the tropical curve
    to a random plane. This is done with the following function.
    """

    coeff1 = []
    coeff2 = []

    """Randomly define coefficients for the plane."""
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


"""We do not need the Y version of the coordinates."""
XVert = []
for vertex in Vert:
    XVert.append(vertex[0])

"""k is the number of variables."""
k = len(XVert[0])

"""We map down to two dimensions using the projection."""
ProjVert = randomprojection(XVert, k)

"""We plot the random projection of the tropical curve."""
for edge in Edg:
    xcoords = [ProjVert[edge[0]-1][0], ProjVert[edge[1]-1][0]]
    ycoords = [ProjVert[edge[0]-1][1], ProjVert[edge[1]-1][1]]
    plt.plot(xcoords, ycoords, 'k-')

for vertex in ProjVert:
    plt.plot(vertex[0], vertex[1], 'ro', markersize=1)

plt.axis('equal')
plt.show()

"""We now create the animation."""

G = nx.Graph()
G.add_edges_from(Edg)

vertices = {}
for i in range(len(ProjVert)):
    vertices.update({i + 1: (ProjVert[i][0], ProjVert[i][1])})


def step(frame):

    ax.clear()
    linesegments = list(G.edges())[:frame+1]
    nodes = [node for edge in linesegments for node in edge]
    nx.draw(G, pos=vertices, ax=ax, edgelist=linesegments, nodelist=nodes,
            edge_color='red', width=2, node_size=10)

    if frame > len(G.edges)-2:
        ani.event_source.stop()


drawing, ax = plt.subplots()

ani = FuncAnimation(drawing, step, frames=len(G.edges), interval=200)

plt.show()
