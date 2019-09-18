import networkx as nx
import operator

def centroid_by_hop(G, keywords):
    """Find centroid of keywords by find node that have path 
    and have minimum hop and average distance to all keyword
    ***sorted by hop first than followed by average distance
    
    Parameters
    ----------
    G : NetworkX graph
    keywords : Set of word want to find centroid

    Returns
    -------
    centroid : dictionary
        Key is a centroid name, value is a average distance to keywords.
    
    Examples
    --------
    >>> G = nx.read_gpickle(path)
    >>> keywords = 'headache fever itch'
    >>> centroid = ct.centroidbyhop(G, keywords)
    {'dengue_ferver : 9.38160, 'shingles : 10.16122, 'chickenpox', 12.00171, 'rhinitis' : 14.605624}

    """
    return _sorted_hop_distance(G, keywords)

def _sorted_hop_distance(G, keywords):
    targetcount = dict()
    targetdistance = dict()
    targethop = dict()
    centroid = dict()
    
    for source in keywords:
        distance, hop = nx.single_source_dijkstra(G, source, weight='cost')
        for target in distance:
            if target in keywords:
                continue
            if target in targetcount:
                targetcount[target] += 1
                targetdistance[target] += distance[target]
                targethop[target] += len(hop[target])-1
            else:
                targetcount[target] = 1
                targetdistance[target] = distance[target]
                targethop[target] = len(hop[target])-1

    for target in targetcount:
        if targetcount[target] == len(keywords):
            centroid[target] = targetdistance[target] / len(keywords)  

    centroid = _sorted_hop(centroid, targethop)

    return(centroid, targethop)  

def _sorted_hop(centroid, targethop):
    centroidsortedbyhop = dict()
    targethop = dict(sorted(targethop.items(), key=operator.itemgetter(1)))
    minhopkey = min(targethop, key=targethop.get)
    minhop = targethop[minhopkey]
    tempcentroidhop = dict()

    for target in targethop:

        if minhop < targethop[target]:
            minhop = targethop[target]
            tempcentroidhop = dict(sorted(tempcentroidhop.items(), key=operator.itemgetter(1)))
            for temp in tempcentroidhop:
                centroidsortedbyhop[temp] = tempcentroidhop[temp]
            tempcentroidhop = dict()

        tempcentroidhop[target] = centroid[target]
    
    return centroidsortedbyhop


def centroid_by_distance(G, keywords):
    """Find centroid of keywords by find node that have path 
    and have minimum average distance to all keyword
    
    Parameters
    ----------
    G : NetworkX graph
    keywords : Set of word want to find centroid

    Returns
    -------
    centroid : dictionary
        Key is a centroid name, value is a average distance to keywords.
    
    Examples
    --------
    >>> G = nx.read_gpickle(path)
    >>> keywords = 'headache fever itch'
    >>> centroid = ct.centroidbydistance(G, keywords)
    {'dengue_ferver : 9.38160, 'shingles : 10.16122, 'chickenpox', 12.00171, 'rhinitis' : 14.605624}

    """
    return _sorted_average_distance(G, keywords)

def _sorted_average_distance(G, keywords):
    targetcount = dict()
    targetdistance = dict()
    centroid = dict()
    
    for source in keywords:
        distance = nx.single_source_dijkstra_path_length(G, source, weight='cost')
        for target in distance:
            if target in keywords:
                continue
            if target in targetcount:
                targetcount[target] += 1
                targetdistance[target] += distance[target]
            else:
                targetcount[target] = 1
                targetdistance[target] = distance[target]

    for target in targetcount:
        if targetcount[target] == len(keywords):
            centroid[target] = targetdistance[target] / len(keywords)  

    return dict(sorted(centroid.items(), key=operator.itemgetter(1)))  

def centroid_neighbors(G, centroid, hop):
    """Find neighbors of centroid node by hop distance. 

     Parameters
    ----------
    G : NetworkX graph
    centroid : Node of centroid.
    hop : Distance to neighbors.

    Returns
    -------
    neighbors: dictionary
        Key is a node destination, value is a list of node from centroid to destination.
    
    Examples
    --------



    """
    
    neighbors = nx.single_source_dijkstra_path(G, centroid, cutoff=hop)
    
    return neighbors

def checkgraphnode(G, keywords):
    keywords = keywords.split()
    node = []
    for word in keywords:
        if G.has_node(word):
            node.append(word)
    return node

"""G = nx.read_gpickle("Database/Pickle/man.gpickle")
centroid = "Year"
centroid_neighbors(G, centroid, 1)"""