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
    c_update = []
    node_no = 1
    for node in G.nodes:
        
        print("\n[", node_no,"]Read node :: ", node)
        # first cluster.
        if cluster_id == 1:
            cluster_node[node] = cluster_id
            cluster_centroid[cluster_id] = node

            # find second member by select node that have shortest distance.
            node_sp = nx.single_source_dijkstra_path_length(G, node, weight='cost')
            next_node = 1
            while True:
                
                second_node, dis = sorted(node_sp.items(), key=operator.itemgetter(1))[next_node]
                # if seconde member already have cluster, find the next one.
                if second_node not in cluster_node:
                    cluster_node[second_node] = cluster_id
                    node_distance[second_node] = dis
                    break
                else:
                    next_node += 1

            cluster_area[cluster_id] = _cluster_area(cluster_id, cluster_node, node_distance)
            print("Cluster id :: ", cluster_id)
            print("Cluster area :: ", cluster_area[cluster_id])
            print("Cluster centroid :: ", cluster_centroid[cluster_id])
            cluster_id += 1

        # next node find cluster.
        else:
            min_distance = 999999999.99
            temp_cluster = None
            node_distance = nx.single_source_dijkstra_path_length(G, node, weight='cost')
            
            # find cluster.
            for c_id, cent in cluster_centroid.items():
                if cent in node_distance:
                    if node_distance[cent] < cluster_area[c_id]:
                        if node_distance[cent] < min_distance:
                            min_distance = node_distance[cent]
                            temp_cluster = c_id
            # found cluster.
            if temp_cluster:
                print("To cluster id :: ", temp_cluster)
                print("Cluster area :: ", cluster_area[temp_cluster])
                print("Distance to centroid :: ", min_distance)
                print("Cluster centroid :: ", cluster_centroid[temp_cluster])
                cluster_node[node] = temp_cluster
                update_centroid = _update_centroid(G, temp_cluster, cluster_node)
                
                # if centroid changed.
                if update_centroid != cluster_centroid[temp_cluster] and update_centroid != None:
                    
                    cluster_centroid[temp_cluster] = update_centroid
                    update_distance = _update_distance_to_centroid(G, temp_cluster, cluster_node, update_centroid)

                    # update node distance to centroid.
                    for m in update_distance:
                        node_distance[m] = update_distance[m]
                    
                    # delete if centroid in node_distance.
                    if update_centroid in node_distance:
                        node_distance.pop(update_centroid)

                    print("New cluster centroid :: ", cluster_centroid[temp_cluster])

                # if centroid no changed.
                else:
                    node_distance[node] = min_distance

                if temp_cluster not in c_update:
                    c_update.append(temp_cluster)
                    cluster_area[temp_cluster] = _cluster_area(temp_cluster, cluster_node, node_distance)
                    print("Update cluster area :: ", cluster_area[temp_cluster])
                if node_no % 10 == 0:
                    c_update.clear()

                
            # not found, create new cluster
            else:
                
                cluster_node[node] = cluster_id
                cluster_centroid[cluster_id] = node
                # find second member by select node that have shortest distance.
                node_sp = nx.single_source_dijkstra_path_length(G, node, weight='cost')
                next_node = 1
                while True:
                    
                   
                    second_node, dis = sorted(node_sp.items(), key=operator.itemgetter(1))[next_node]
                    # if seconde member already have cluster, find the next one.
                    if second_node not in cluster_node:
                        cluster_node[second_node] = cluster_id
                        node_distance[second_node] = dis
                        break
                    else:
                        next_node += 1

                cluster_area[cluster_id] = _cluster_area(cluster_id, cluster_node, node_distance)
                print("Cluster id :: ", cluster_id)
                print("Cluster area :: ", cluster_area[cluster_id])
                print("Cluster centroid :: ", cluster_centroid[cluster_id])
                cluster_id += 1
        node_no += 1

    sorted_x = sorted(cluster_node.items(), key=operator.itemgetter(1))
    sorted_y = sorted(cluster_centroid.items())
    print(sorted_x)
    print(sorted_y)
  
def graph_cluster2(G):
    cluster_node = dict() # node with cluster id, {node : cluster_id}
    cluster_centroid = dict() # cluster id with centroid, {cluster_id : centroid}
    node_distance = dict() # node distance to centroid, {node : distance_to_centroid}
    cluster_area = dict() # cluster id with area., {cluster_id : area}
    cluster_id = 1 # first node, create cluster immediatly.

    for node in G.nodes:
        if node in cluster_node:
            continue

        else:
            print("\nCluster ID :: ", cluster_id)
            cluster_node[node] = cluster_id
            cluster_centroid[cluster_id] = node
            print("Centroid :: ", cluster_centroid[cluster_id])
            cluster_area[cluster_id] = _cluster_area(cluster_id, cluster_node, None)
            print("Cluster Area :: ", cluster_area[cluster_id])
            node_sp = nx.single_source_dijkstra_path_length(G, node, weight='cost')
            close_node = sorted(node_sp.items(), key=operator.itemgetter(1))

            ck_cent = 0

            for cn in close_node:
                c_node, c_dis = cn
            
                if c_dis < cluster_area[cluster_id] and c_dis > 0:
                    cluster_node[c_node] = cluster_id

                    update_centroid = None
                    if ck_cent > 10:
                        break                
                    update_centroid = _update_centroid(G, cluster_id, cluster_node)
                
                    # if centroid changed.
                    if update_centroid != cluster_centroid[cluster_id] and update_centroid != None:
                        
                        cluster_centroid[cluster_id] = update_centroid
                        update_distance = _update_distance_to_centroid(G, cluster_id, cluster_node, update_centroid)

                        # update node distance to centroid.
                        for m in update_distance:
                            node_distance[m] = update_distance[m]
                        
                        # delete if centroid in node_distance.
                        if update_centroid in node_distance:
                            node_distance.pop(update_centroid)

                        print("New cluster centroid :: ", cluster_centroid[cluster_id])

                    # if centroid no changed.
                    else:
                        node_distance[c_node] = c_dis
                        ck_cent += 1

                    cluster_area[cluster_id] = _cluster_area(cluster_id, cluster_node, node_distance)
                    #print("Update Area :: ", cluster_area[cluster_id])
             
            cluster_member = []
           
            # node in cluster id.
            for n in cluster_node:
                if cluster_node[n] == cluster_id:
                    cluster_member.append(n)
            print("Update Area :: ", cluster_area[cluster_id])
            print("Member :: ", len(cluster_member))
            cluster_id += 1

    
def _standard_deviation_and_average_distance(c_id, cluster_node, node_distance):
    cluster_member = []
    average_distance = None
    standard_deviation = None

    for node in cluster_node:
        if cluster_node[node] == c_id:
            cluster_member.append(node)

    # cluster amount == 1
    if len(cluster_member) == 1:
        distance = 1
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
    #print("Member :: ", len(cluster_member))

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

G = nx.read_gpickle("../Database/Pickle/221tag.gpickle")
graph_cluster2(G)
