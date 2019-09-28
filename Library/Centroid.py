import networkx as nx
import operator
import math  

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

# Area = Average Distance[cluster] + (3 * Standard Deviation[cluster])
# Standard Deviation[cluster] = Math.sqrt( (x-average)**2 / n-1 )
# First Centroid, Average distance = 1, Standard Deviation = 1/2
 
def graph_cluster(G):
    cluster_node = dict() # node with cluster id, {node : cluster_id}
    cluster_centroid = dict() # cluster id with centroid, {cluster_id : centroid}
    node_distance = dict() # node distance to centroid, {node : distance_to_centroid}
    cluster_area = dict() # cluster id with area., {cluster_id : area}
    cluster_id = 1 # first node, create cluster immediatly.
    node_no = 0
    fileResult = open("Result Centroid/cluster.txt", "w", encoding="utf-8")

    for node in G.nodes:

        if node in cluster_node:
            continue
 
        cluster_node[node] = cluster_id
        cluster_centroid[cluster_id] = node
        cluster_area[cluster_id] = _cluster_area(cluster_id, cluster_node, None)

        while True:
            node_sp = nx.single_source_dijkstra_path_length(G, 
                        cluster_centroid[cluster_id], weight='cost', cutoff=cluster_area[cluster_id])
            
            # If there are nodes that can enter the cluster.
            new_member = False
            if len(node_sp) != 1:
            
                for node2 in node_sp:
                    if node2 not in cluster_node:
                        cluster_node[node2] = cluster_id
                        node_distance[node2] = node_sp[node2]
                        new_member = True
                
                if new_member:
               
                    # check cluster centroid again.
                    new_centroid = _update_centroid(G, cluster_id, cluster_node)
                    # if centroid have change!
                    if new_centroid != cluster_centroid[cluster_id] and new_centroid != None:
                       
                        cluster_centroid[cluster_id] = new_centroid
                        update_distance = _update_distance_to_centroid(G, cluster_id, cluster_node, cluster_centroid[cluster_id])
                        
                        # update node distance to new centroid.
                        for exnode in update_distance:
                            node_distance[exnode] = update_distance[exnode]

                        cluster_area[cluster_id] = _cluster_area(cluster_id, cluster_node, node_distance)
                 

                    # if centroid not change!
                    else:
                   
                        cluster_area[cluster_id] = _cluster_area(cluster_id, cluster_node, node_distance)

                                    
                else:
                    member = []
                    for m in cluster_node:
                        if cluster_node[m] == cluster_id:
                            member.append(m)
                    print("\nCluseter no. ", cluster_id)
                    print("Area :: ", cluster_area[cluster_id])
                    print("Centroid :: ", cluster_centroid[cluster_id])
                    print("Member :: ", len(member))
                    fileResult.write("Cluster "+str(cluster_id)+"["+str(cluster_centroid[cluster_id])+"]"+str(member)+"\n") 
                    cluster_id += 1
                    break

            # no more node can enter the cluseter.
            else:
                member = []
                for m in cluster_node:
                    if cluster_node[m] == cluster_id:
                        member.append(m)
                print("\nCluseter no. ", cluster_id)
                print("Area :: ", cluster_area[cluster_id])
                print("Centroid :: ", cluster_centroid[cluster_id])
                print("Member :: ", len(member))
                fileResult.write("Cluster "+str(cluster_id)+"["+str(cluster_centroid[cluster_id])+"]"+str(member)+"\n") 
                cluster_id += 1
                break
            
 
     
def _standard_deviation_and_average_distance(c_id, cluster_node, node_distance):
    cluster_member = []
    average_distance = None
    standard_deviation = None

    for node in cluster_node:
        if cluster_node[node] == c_id:
            cluster_member.append(node)

    # cluster amount == 1
    if len(cluster_member) == 1:
   
        sum_distance = 1
        # average distance  
        average_distance = sum_distance / len(cluster_member)
        # standard deviation  
        standard_deviation = sum_distance / 2

    # cluster amount == 2
    elif len(cluster_member) == 2:
        sum_distance = 0

        # find sum distance of cluster
        for member in cluster_member:
            if member in node_distance:
                sum_distance += node_distance[member]

        # average distance  
        average_distance = sum_distance / len(cluster_member)
        # standard deviation     
        standard_deviation = sum_distance / 2
    
    # cluster amount > 2
    elif len(cluster_member) > 2:
        sum_distance = 0

         # find sum distance of cluster
        for member in cluster_member:
            if member in node_distance:
                sum_distance += node_distance[member]

        # find average distance of cluster
        average_distance = sum_distance / len(cluster_member)+1 # member + centroid

        sd = 0 # (x - average)^2, x = distance to centroid

        for member in cluster_member:
            if member in node_distance:
                sd = sd + (node_distance[member] - average_distance)**2
        
        # standard deviation     
        standard_deviation = math.sqrt(sd / len(cluster_member)) 
    
    return average_distance, standard_deviation
   
def _cluster_area(c_id, cluster_node, node_distance):
    # Area = Average Distance[cluster] + (3 * Standard Deviation[cluster])
    multiply = 3
    average, standard_deviation = _standard_deviation_and_average_distance(c_id, cluster_node, node_distance)
    return average + (multiply * standard_deviation)

def _update_centroid(G, c_id, cluster_node):
    # when cluster have new member, calculate node average distance again to find centroid.
    cluster_member = []
    new_centroid = None

    # node in cluster id.
    for node in cluster_node:
        if cluster_node[node] == c_id:
            cluster_member.append(node)
    
    # if node member > 2, calulate node average distance
    if len(cluster_member) > 2:

        min_avg = 999999999.99
        subg = nx.subgraph(G, cluster_member)
        word_allSP = dict(nx.floyd_warshall(subg, weight='cost'))
        for key in word_allSP:
            avg_nodeSP = sum(word_allSP[key].values())/(len(word_allSP[key]))
            if min_avg > avg_nodeSP:
                min_avg = avg_nodeSP
                new_centroid = key
    # if node member < 2
    else:
        new_centroid = None
   
    return new_centroid
           
def _update_distance_to_centroid(G, c_id, cluster_node, centroid):
    cluster_member = []
    update_distance = dict()

    # node in cluster id.
    for node in cluster_node:
        if cluster_node[node] == c_id:
            cluster_member.append(node)

    node_distance = nx.single_source_dijkstra_path_length(G, centroid, weight='cost')
    
    # node distance to centroid.
    for target in node_distance:
        if target in cluster_member:
            update_distance[target] = node_distance[target]

    return update_distance

def distance_measure(G, source, target):
    pair_distance = dict()
    start_point = []
    found_target = False
    distance = 0
    start_point.append(source)

    # find node neighbors from source to target
    for point in start_point:
        neighbor = G.neighbors(point)
        for n in neighbor:
            if n not in start_point:
                start_point.append(n)

            node_pair = (point, n)
            pair_distance[node_pair] = G[point][n]['cost']

            if n == target:
                found_target = True
                break
        
        if found_target:
            break
    
    path = []
    targets = target
    found_soucre = False
    # find sum distance from source to target
    while True:
        for s, t in pair_distance:
            print(s,t)
            if t == targets:
                if s == source:
                    path.append(s)
                path.append(t)
                targets = s
                distance += pair_distance[(s,t)]
            if targets == source:
                found_soucre = True
        if found_soucre:
            break
    print(path, " : ", distance)

def min_distance_measure(G, u, v):
    pair_distance = dict()
    start_point = []
    found_target = False
    distance = 0
    start_point.append(source)

    # find node neighbors from source to target
    for point in start_point:
        neighbor = G.neighbors(point)
        for n in neighbor:
            if n not in start_point:
                start_point.append(n)

            node_pair = (point, n)
            pair_distance[node_pair] = G[point][n]['cost']

            if point == target:
                found_target = True
                break
        
        if found_target:
            break

    #print(pair_distance)

#source = 'man'
#target = 'fever'
#min_distance_measure(G, source, target)