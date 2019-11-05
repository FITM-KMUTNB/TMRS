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

def centroid_neighbors(G, centroid):
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
   

    """
    
    neighbors = nx.single_source_dijkstra_path(G, centroid, weight='cost')
    distance = nx.single_source_dijkstra_path_length(G, centroid, weight='cost')
    
    return neighbors, dict(sorted(distance.items(), key=operator.itemgetter(1)))  

def checkgraphnode(G, keywords):
    keywords = keywords.split()
    node = []
    for word in keywords:
        if G.has_node(word):
            node.append(word)
    return node

def distance_measure(G, source, target):
    neigbor_distance = dict()
    neigbor_distance[source] = 0
    point = []
    point.append(source)

    for current in point:
        related_node = nx.neighbors(G, current)
        for node in related_node:
            if node not in neigbor_distance:
                neigbor_distance[node] = neigbor_distance[current] + G[current][node]['cost']
                point.append(node)
            
            if node == target:
                break
    #print(nx.dijkstra_path(G, source, target))
    #print(target, " : ", neigbor_distance[target])
    return neigbor_distance[target]


def spreading_activation_centroid(G, keywords):
    centroid = ''
    key_point = [] # node point to activate and find neighbors.
    activate_round = 1
    candidate = dict()
    
    node_count = dict() # node count to all keywords
    node_sum = dict() # node sum distance to all keywords
    node_distance = [] # distance from node to each keywords

    for key in keywords:
            initial = dict()
            # initail distance 
            initial[key] = 0
            node_distance.append(initial)
            key_point.append([key])

    while len(candidate) < 10:
        #print("Activation round : ", activate_round)
        min_average = 999999
        centroid = ''
        
        

        for index in range(len(key_point)):
            activate_size = 1
            # initail point.
            for a in range(activate_size):
                act_node = key_point[index].pop(0)
                #print("Activate [", index,"]:: ", act_node)

                # Activate
                related_node = nx.neighbors(G, act_node)

                # iterate neighbors.
                for r in related_node:
                    if r not in key_point[index]:
                        # append node for next activation.
                        key_point[index].append(r)
                        distance_dict = node_distance[index]
                        
                        # distance from neightbor to activate node.
                        distance_dict[r] = distance_dict[act_node] + G[act_node][r]['cost']
                        if r in node_count:
                            node_count[r] += 1
                            node_sum[r] += distance_dict[r]
                        else:
                            node_count[r] = 1
                            node_sum[r] = distance_dict[r]
                    
                    if node_count[r] == len(keywords):
                        if G.node[r]['tag'] == 'DS':
                            candidate[r] = node_sum[r] / len(keywords)
                        """if min_average > candidate[r]:
                            min_average = candidate[r]
                            centroid = r"""
        #print("Candidate : ", len(candidate))
        
        activate_round += 1
    
    return dict(sorted(candidate.items(), key=operator.itemgetter(1))) 

def hop_activate_centroid(G, keywords):
    activate_list = []
    candidate = dict()
    current_hop = 0
    node_count = dict()
    node_distance = []
    sum_distance = dict()

    for key in keywords:
        activate_list.append([key])
        node_distance.append({key : 0})
               
    while len(candidate) <= 0:
        for circle in range(len(activate_list)):
            activate_node = activate_list[circle][current_hop]
            
            for neighbors in nx.neighbors(G, activate_node):
                if neighbors in keywords:
                    continue

                # distance from initial point.
                if neighbors not in node_distance[circle]:
                    
                    node_distance[circle][neighbors] = node_distance[circle][activate_node] + G[activate_node][neighbors]['cost']

                    # sum distance to all keywords.
                    if neighbors in sum_distance:
                        sum_distance[neighbors] += node_distance[circle][neighbors]
                    else:
                        sum_distance[neighbors] = node_distance[circle][neighbors]
                
                # check intersect
                if neighbors in node_count:

                    if neighbors not in activate_list[circle]:
                        activate_list[circle].append(neighbors)
                        node_count[neighbors] += 1
                    
                    # if found node intersect, calculate average distance.
                    if node_count[neighbors] == len(keywords):
                        candidate[neighbors] = sum_distance[neighbors] / len(keywords)
            
                else:
                    activate_list[circle].append(neighbors)
                    node_count[neighbors] = 1
        current_hop += 1
    
    return dict(sorted(candidate.items(), key=operator.itemgetter(1)))   

"""
G = nx.read_gpickle("../Database/Pickle/221tag.gpickle")
#graph_cluster2(G)
keywords = ['skin', 'itch', 'headache']
centroid = hop_activate_centroid(G, keywords)
for c in centroid:
    print(c, " : ", centroid[c])
"""   

