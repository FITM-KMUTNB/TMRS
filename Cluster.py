import networkx as nx
import math  

# Area = Average Distance[cluster] + (3 * Standard Deviation[cluster])
# Standard Deviation[cluster] = Math.sqrt( (x-average)**2 / n-1 )
# First Centroid, Average distance = 1, Standard Deviation = 1/2

cluster = dict() #{ cid : {n1 : dis_ct, n2 : dis_ct, n3 : dis_ct}, }
cluster_ct = dict() #{ cid : n, }
cluster_area = dict() #{ cid : area, }

def graph_cluster(G):
    global cluster
    global cluster_ct
    global cluster_area
    
    c_id = 1

    for node in G.nodes:
        print("\n")
        # first node create cluster.
        if not cluster:
            
            cluster[c_id] = {node : 0}
            cluster_ct[c_id] = node
            cluster_area[c_id] = _cluster_area(cluster[c_id])

            print("Create New cluster id : ", c_id)
            print("member : ", len(cluster[c_id]))
            print("area : ", cluster_area[c_id])
            print("centroid : ", cluster_ct[c_id])

            c_id += 1

        # next node
        else:
            min_distance = 999999
            final_cluster = 0
            check_cluster = []
            neighbors = nx.neighbors(G, node)
            
            # check node with existing cluster
            for rel in neighbors: # current checking node.
                for c in cluster: # existing cluster.

                    # if aready check with this cluster id, not do again.
                    if c in check_cluster:
                        continue
                    
                    # if connected with this cluster id, check distance to the cluster centroid.
                    if rel in cluster[c]:
                        check_cluster.append(c)
                        distance = distance_to_centroid(G, cluster[c], node, cluster_ct[c])

                        if distance < cluster_area[c]:

                            if distance < min_distance:
                                min_distance = distance
                                final_cluster = c
            # Found existing cluster that node could be enter.
            if final_cluster != 0:
                print("To Existing Cluster : ", final_cluster)
                # add node to cluster.
                cluster[final_cluster][node] = min_distance

                # if cluster amount more than 2, re-check cluster centroid.
                if len(cluster[final_cluster]) > 2:
                    new_centroid = _update_centroid(G, cluster[final_cluster])

                    if new_centroid != cluster_ct[final_cluster]:
                        cluster_ct[final_cluster] = new_centroid
                        cluster[final_cluster] = _update_distance_to_centroid(G, cluster[final_cluster], cluster_ct[final_cluster])
                        

                # update cluster area.
                cluster_area[final_cluster] = _cluster_area(cluster[final_cluster])
                for n_distance in cluster[final_cluster]:
                    if cluster[final_cluster][n_distance] > cluster_area[final_cluster]:
                        print("Over lenght")

                print("member : ", len(cluster[final_cluster]))
                print("area : ", cluster_area[final_cluster])
                print("centroid : ", cluster_ct[final_cluster])
            # Not found any existing cluster that node could be enter.
            else:
                
                cluster[c_id] = {node : 0}
                cluster_ct[c_id] = node
                cluster_area[c_id] = _cluster_area(cluster[c_id])

                print("Create New cluster id : ", c_id)
                print("member : ", len(cluster[c_id]))
                print("area : ", cluster_area[c_id])
                print("centroid : ", cluster_ct[c_id])

                c_id += 1
   


def distance_to_centroid(G, cluster, node, centroid):
    cluster_list = list(cluster)
    cluster_list.append(node)
    cluster_G = nx.subgraph(G, cluster_list)

    return nx.dijkstra_path_length(cluster_G, node, centroid, weight='cost')


def _standard_deviation_and_average_distance(cluster_node):

    average_distance = None
    standard_deviation = None


    # cluster amount == 1
    if len(cluster_node) == 1:
   
        sum_distance = 1
        # average distance  
        average_distance = sum_distance / len(cluster_node)
        # standard deviation  
        standard_deviation = sum_distance / 2

    # cluster amount == 2
    elif len(cluster_node) == 2:
        sum_distance = 0

        # find sum distance of cluster
        for member in cluster_node:
            sum_distance += cluster_node[member]

        # average distance  
        average_distance = sum_distance / len(cluster_node)
        # standard deviation     
        standard_deviation = sum_distance / 2
    
    # cluster amount > 2
    elif len(cluster_node) > 2:
        sum_distance = 0

         # find sum distance of cluster
        for member in cluster_node:
            sum_distance += cluster_node[member]

        # find average distance of cluster
        average_distance = sum_distance / len(cluster_node)

        sd = 0 # (x - average)^2, x = distance to centroid

        for member in cluster_node:
            sd += (cluster_node[member] - average_distance)**2
        
        # standard deviation     
        standard_deviation = math.sqrt(sd / (len(cluster_node) - 1) ) 
        
    return average_distance, standard_deviation
   
def _cluster_area(cluster_node):
    # Area = Average Distance[cluster] + (3 * Standard Deviation[cluster])
    multiply = 3
    average, standard_deviation = _standard_deviation_and_average_distance(cluster_node)
    return average + (multiply * standard_deviation)

def _update_centroid(G, cluster_node):
    # when cluster have new member, calculate node average distance again to find centroid.
    new_centroid = None
    min_avg = 999999999.99
    subg = nx.subgraph(G, cluster_node)
    word_allSP = dict(nx.floyd_warshall(subg, weight='cost'))
    for key in word_allSP:
        avg_nodeSP = sum(word_allSP[key].values())/(len(word_allSP[key]))
        if min_avg > avg_nodeSP:
            min_avg = avg_nodeSP
            new_centroid = key
     
    return new_centroid
           
def _update_distance_to_centroid(G, cluster_node, centroid):

    # create subgraph of cluster.        
    cluster = nx.subgraph(G, cluster_node)

    # shortest path from centroid to member of cluster.
    return dict(nx.single_source_dijkstra_path_length(cluster, centroid, weight='cost'))
    
G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
graph_cluster(G)

for c in cluster:
    print("Cluster id : ", c)
    print("member : ", len(cluster[c]))
    print("area : ", cluster_area[c])
    print("centroid : ", cluster_ct[c])