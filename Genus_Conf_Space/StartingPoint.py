"""
This file contains the algorithms for generating a
starting point for the main algorithm. This involves
calculating a single point on the tropical curve.
"""

from itertools import combinations
from randomnumbergenerators import *
from algorithm import dirs, go


def listcreation(cyc, n):
    """
    This finds the positions where the minima must be attained.
    Input: cyc the cycles of the graph, n the number of vertices.
    Output: x, the starting point in terms of the X variables.
            y, the starting point in terms of the Y variables.
            also outputs the number n for convenience.
    """

    for j in range(n//2):

        """We brute force the search, and check intersections."""
        choices = [list(x) for i in range(n//2 - j, n + 1)
                   for x in combinations(range(n+1), i)]
        continue_x = False

        for x in choices:

            if continue_x is True:
                continue_x = False
                continue

            for y in choices:
                continue_y = False

                if continue_x is True:
                    break

                for cycle in cyc:
                    if len(set(x).intersection(set(cycle))) < 2:
                        continue_x = True
                        break
                    if len(set(y).intersection(set(cycle))) < 2:
                        continue_y = True
                        break

                if continue_x is True:
                    continue

                if continue_y is True:
                    continue

                if len(set(x).intersection(set(y))) < 2:
                    return x, y, n

    """If this search fails:"""
    print("No starting point found")

    return


def pointcreation(xchoice, ychoice, n):
    """
    This is the naive version of the algorithm.
    The more complex one is below.
    Given the minima positions, we generate a starting point.
    """

    """Initialise the point as an empty list."""
    mins = [0]
    xcoords = []
    ycoords = []

    for i in range(n+1):
        xcoords += [arb()]
        ycoords += [arb()]

    """In this naive version, minima values are always 0."""
    for j in xchoice:
        xcoords[j] = 0

    for k in ychoice:
        ycoords[k] = 0

    print(f"starting point is {[xcoords, ycoords]}")

    return [xcoords, ycoords]


def startingpoint(edges, graphvertices):
    """
    Want two random functions on the vertex set, one increasing,
    one decreasing. These are stored in two lists, Vinc and Vdec.
    """

    Vinc = []
    Vdec = []

    for i in range(len(graphvertices)):
        """We generate increasing values randomly."""

        if Vinc == []:
            Vinc.append(arbsp())

        else:
            Vinc.append(Vinc[i-1] + arbsp())

        if Vdec == []:
            Vdec.append(arbsp())

        else:
            Vdec.append(Vdec[i-1] - arbsp())

    """Vinc and Vdec are now defined."""
    # print(f"Vinc = {Vinc}")
    # print(f"Vdec = {Vdec}")

    """Initialise the coordinate lists."""
    px = []
    py = []

    for i in range(len(edges)):
        px.append(min(Vinc[edges[i][0]], Vinc[edges[i][1]]))
        py.append(min(Vdec[edges[i][0]], Vdec[edges[i][1]]))

    px0 = px[0]
    pyend = py[len(py)-1]

    """Translate the values for simplicity."""
    for i in range(len(px)):
        px[i] = px[i] - px0
        py[i] = py[i] - pyend

    for i in range(len(px)):
        px[i] = px[i] + py[0]

    """Print the starting point."""
    print(f"Starting point is {px,py}")

    """We can now generate the weights."""
    weights = []

    for i in range(len(px)):
        weights.append(px[i]+py[i])

    """We also find the weight differences."""
    weightsdiffs = []

    for i in range(len(weights)):
        for j in range(i+1, len(weights)):
            weightsdiffs.append(weights[i]-weights[j])

    """Options for printing the weights."""
    # print(f"Weights are {weights}")
    # print(f"Weight differences are {weightsdiffs}")
    # print(f"weight differences len is {len(weightsdiffs)}")
    # print(f"weightdifferences set is {len(set(weightsdiffs))}")

    if len(weightsdiffs) != len(set(weightsdiffs)):
        print(f"there are repeated weight differences")

    return [px, py]


def movetovertex(startingpoint):
    """
    Starting point may not be a vertex.
    We move to a vertex before starting the main algorithm.
    This prevents an artificial extra edge and vertex being counted.
    """

    xcoords = startingpoint[0]
    ycoords = startingpoint[1]
    weights = []

    for i in range(len(xcoords)):
        weights.append(xcoords[i] + ycoords[i])

    if len(weights) == len(set(weights)):
        print("This starting point has distinct weights")

    else:
        print("Warning! This starting point does not have distinct weights.")

    Direction, Distance = dirs(startingpoint)

    return go(startingpoint, Direction[0], Distance[0])
