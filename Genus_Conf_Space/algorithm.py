""" Contains the main definitions for the traversing algorithm. """

import math
import copy
import randomnumbergenerators
import graphgeneration
from transversalitytest import transversalitytest

"""
We call some values from the other modules.
graphgenerations.py to create the cycles and the number of vertices.
randomnumbergenerators.py to generate random numbers.
"""

cyc = graphgeneration.cyc
n = graphgeneration.n
size = randomnumbergenerators.size


def minpairs(P):
    """
    Finds pairs of indices in a cycle where the minimum value is attained.
    Input: A point P on the tropical curve.
    Output: A list of pairs of indices where each cycle minimum is attained.
    """
    Mxy = []

    for cc in cyc:

        mx = min(P[0][T] for T in cc)
        pair = [T for T in cc if P[0][T] == mx]

        if len(pair) == 2:
            Mxy += [pair]

        elif len(pair) == 1:
            raise ValueError("not on curve")

        my = min(P[1][T] for T in cc)
        pair = [T for T in cc if P[1][T] == my]

        if len(pair) == 2:
            Mxy += [pair]

        elif len(pair) == 1:
            raise ValueError("not on curve")

    return Mxy


def trans2(prs):
    """
    This calculates the transitive closure of a relation.
    In our case the relation is where minima are attained in each cycle.
    Input: Output of the minpairs function.
    Output: Transitive closure of the minpairs list.
    """
    if len(prs) > 1:

        bubble = prs[0]
        common = []

        for i in range(len(prs)-1):
            if bool(set(bubble) & set(prs[i+1])):
                common.append(i+2)

        if len(common) > 0:
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


def stopp(pt, dir):
    """
    Given a point on the tropical curve, and a direction, calculates the
    distance to travel.
    Input: A point pt on the curve and a direction dir.
    Output: A value goal, which is the distance able to travel.
    goal is initialised as infinity.
    """
    goal = float('inf')

    for cc in cyc:

        mx = min([pt[0][T] for T in cc])
        Mp = [T for T in cc if pt[0][T] == mx]
        stay = set(Mp) - set(dir)

        if len(stay) == 0:  # we may go until next smallest value is reached
            if len(set(cc)-set(dir)) > 0:
                tres = min(pt[0][T] for T in set(cc) - set(dir)) - mx
                goal = min(goal, tres)

        elif len(stay) == 1:  # cannot even start going
            goal = 0

        cdir = list(set(range(n+1)) - set(dir))
        my = min([pt[1][T] for T in cc])
        Mp = [T for T in cc if pt[1][T] == my]
        stay = set(Mp) - set(cdir)

        if len(stay) == 0:
            if len(set(cc) - set(cdir)) > 0:
                tres = min(pt[1][T] for T in set(cc) - set(cdir)) - my
                goal = min(goal, tres)

        elif len(stay) == 1:
            goal = 0

    return goal


def dirs(P):
    """
    Given a point (vertex) on the tropical curve
    calculates possible directions and distances to travel.
    Input: A single point P on the curve.
    Output: A pairs of lists; pairs of entries
    corresponding the same index give a distance and a direction.
    """

    bubbles = trans2(minpairs(P))

    for i in range(n+1):

        j = 0

        for x in bubbles:
            if i in x:
                j = j + 1

        if j == 0:
            bubbles.append([i])

    nb = len(bubbles)
    dires = []

    for pob in range(1, (2 ** nb)-1):

        dir = []

        for i in range(nb):

            if pob % 2 == 1:
                for x in bubbles[i]:
                    dir.append(x)
                pob = pob-1

            pob = pob / 2  # cut off last binary digit

        dires.append(dir)

    # compute distances and throw away zero distance candidates
    fdires = []
    fdists = []

    for dir in dires:

        ds = stopp(P, dir)

        if ds > 0:
            fdires.append(dir)
            fdists.append(ds)

    return fdires, fdists


def go(pt, dir, distance):
    """
    This simply travels on the tropical curve
    from a certain point, in a certain distance and direction.
    Input: pt a point on the curve, dir a direction,
    and distance a distance to travel.
    Note that directions are 01 lists,
    and we must try to move in both directions.
    """

    cdir = list(set(range(n+1)) - set(dir))

    """Creates a copy of the point to travel on."""
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


def neighbors(pt):
    """
    Given a vertex, finds the neighbours.
    Input: pt a point on the tropical curve.
    Output: A list of the points which are neighbours.
    """

    edges, dists = dirs(pt)
    nbs = []

    for i in range(len(edges)):
        if math.isfinite(dists[i]):
            dir = edges[i]
            pt_copy = copy.deepcopy(pt)
            nbs.append(go(pt_copy, dir, dists[i]))

    return nbs


def rays(pt):
    """
    This function can be used to find infinite rays
    It travels a certain distance, and creates an
    artificial vertex on the ray.
    Input: A point pt on the curve.
    Output: A pair of lists nbs, infdires. nbs contains
    the artificial vertices, infdires the corr. directions.
    """

    directions, dists = dirs(pt)
    nbs = []
    infdires = set()

    for i in range(len(directions)):
        if not math.isfinite(dists[i]):
            dir = directions[i]
            infdires.add(tuple(sorted(dir)))
            pt_copy = copy.deepcopy(pt)
            nbs.append(go(pt_copy, dir, size // 4))

    return nbs, infdires


def graph(pt):
    """
    This is the main function.
    It applies previous definitions to create a graph of the tropical curve.
    Some functionalities are not currently used - namely the rays.
    Input: pt a point on the curve.
    Output: A pair of lists Vert, Edg. Vert contains positions for the
    vertices of the tropical curve. Edg contains pairs of vertices
    which are connected. There are further listed outputs which
    are currently unused.
    """
    weights = []

    for i in range(len(pt[0])):
        weights.append(pt[0][i]+pt[1][i])

    """"We use transversalitytest.py to check for a transverse intersection"""
    if transversalitytest(pt, weights, cyc) is False:
        print("Non-transverse intersection found")
        exit()

    """We initialise all our lists."""
    Vert = []
    Edg = []
    Ray = []
    PVert = [pt]
    InfVert = []
    InfDiresmultset = []
    InfDires = set()

    while len(PVert) > 0:
        """
        Main while loop: PVert is a list of the found but
        not yet traversed from vertices. See further comments for details.
        """

        """ Take the first unchecked vertex."""
        pick = PVert[0]

        """ Transversality test at the new vertex. """
        if transversalitytest(pick, weights, cyc) is False:
            print("Non-transverse intersection found")
            print(f"non-transverse intersection point is {pick}")
            print(f"We found {len(Edg)} edges and {len(Vert)} vertices")
            exit()

        """
        Here we update some of our lists, and
        find neighbours of the chosen vertex.
        Any newly found vertices are added to PVert.
        """
        PVert = PVert[1:]
        Vert = Vert + [pick]
        src = len(Vert)
        nxt = neighbors(pick)
        nxt = [list(x) for x in nxt if x not in Vert]
        nnxt = [list(x) for x in nxt if x not in PVert]
        PVert = PVert + nnxt

        for i in range(1, len(PVert) + 1):
            if PVert[i-1] in nxt:
                Edg.append([src, len(Vert)+i])

        ry, infdir = rays(pick)

        if len(ry) > 0:

            InfDires.update(infdir)

            for i in range(len(ry)):
                InfDiresmultset.append(list(infdir)[i])

            for ray in ry:
                InfVert += [ray]
                Ray.append([src, len(InfVert)])

    """Commented out commands for ray calculations."""
    # Ray = [[T[0], T[1] + len(Vert)] for T in Ray]
    # Vert += InfVert

    return Vert, Edg, Ray, InfDires, InfDiresmultset
