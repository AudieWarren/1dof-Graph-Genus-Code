import networkx as nx

def transversalitytest(point, weights, cyc):
    #Note: point is a pairs with the x and y coordinates in the two entries
    n = len(point[0])
    Gp = nx.empty_graph(n)
    Gq = nx.empty_graph(n)
    xpoint = point[0]
    ypoint = point[1]
    for i in range(n):
        for j in range(n):
            if j > i:
                if xpoint[i] == xpoint[j]:
                    Gp.add_edge(i,j)
                if ypoint[i] == ypoint[j]:
                    Gq.add_edge(i,j)
    ncGp = nx.number_connected_components(Gp)
    ncGq = nx.number_connected_components(Gq)
    Gpq = Gp
    for edge in Gq.edges:
        Gpq.add_edge(*edge)
    ncGpq = nx.number_connected_components(Gpq)
    if ncGp + ncGq - ncGpq == n:
        return True
    else:
        return False
            
    