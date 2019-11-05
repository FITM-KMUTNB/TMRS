import networkx as nx 
import math  
import glob

#----------------------- Coocurrence Graph ----------------------#
G = nx.Graph()
word_count = dict()
word_tag = dict()
link_count = dict()
link_dict = dict()
link_cost = dict()

#----------------------- Cluster --------------------------------#
# Area = Average Distance[cluster] + (3 * Standard Deviation[cluster])
# Standard Deviation[cluster] = Math.sqrt( (x-average)**2 / n-1 )
# First Centroid, Average distance = 1, Standard Deviation = 1/2
c_id = 1
cluster = dict() #{ cid : {n1 : dis_ct, n2 : dis_ct, n3 : dis_ct}, }
cluster_ct = dict() #{ cid : n, }
cluster_area = dict() #{ cid : area, }
has_cluster = set()

def read_document(path):
    
    for file in glob.glob(path+"*.txt"):
        print("file: ", file)
        
        # open file.
        Text_file = open(file, 'r', encoding='utf-8')
        create_graph(Text_file)
        graph_cluster()

    g_file = "Database/Pickle/221cluster.gpickle"
    _write_graph_to_gpickle_format(g_file)

def create_graph(doc):
    global G

    # word, link frequencies and link cost.
    for line in doc:
        _word_frequency(line)
        _link_frequency(line)

    _calculate_link_cost()

    # create graph object, node and edge.
    for node in word_count:
        G.add_node(node, occur=word_count[node], tag=word_tag[node])
    
    for edge in link_count:
        nodes = edge.split('|')
        G.add_edge(nodes[0], nodes[1], count=link_count[edge],
                   dice=link_dict[edge], cost=link_cost[edge])
    

def _word_frequency(line):
    global word_count
    global word_tag

    word_list = line.split()

    for word in word_list:
        if "|" in word:
            word, tag = word.split("|")
            word_tag[word] = tag

        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1


def _link_frequency(line):
    global link_count

    word_list = line.split()

    for source in range(len(word_list)):
        for target in range(source+1, len(word_list)):
            if word_list[source] == word_list[target]:
                continue

            source_word = None
            target_word = None
            # Remove tag
            if "|" in word_list[source]:
                source_word = word_list[source].split('|')[0]
            else:
                source_word = word_list[source]

            if "|" in word_list[target]:
                target_word = word_list[target].split('|')[0]
            else:
                target_word = word_list[target]

            # Sort the letters
            sort_word = sorted([source_word, target_word])
            pair_word = sort_word[0] + "|" + sort_word[1]

            if pair_word in link_count:
                link_count[pair_word] += 1
            else:
                link_count[pair_word] = 1

def _calculate_link_dice(wordlink, countab):
    global link_dict
    wordlist = wordlink.split('|')
    countA = word_count[wordlist[0]]
    countB = word_count[wordlist[1]]
    countAB = countab

    helpk = 0
    if countB <= countA:
        helpk = countB
    else:
        helpk = countA

    if countAB >= helpk:
        countAB = helpk

    dicevalue = (2*countAB)/(countA+countB)

    if dicevalue > 1:
        dicevalue = 1.0

    link_dict[wordlink] = dicevalue
    return dicevalue


def _calculate_link_cost():
    global link_cost
    for wordpair in link_count:
        dice = _calculate_link_dice(wordpair, link_count[wordpair])
        cost = 1/(dice+0.01)
        link_cost[wordpair] = cost

def graph_cluster():
    global cluster
    global cluster_ct
    global cluster_area
    global c_id
    global has_cluster

    for node in G.nodes:
        print("\n")
        print("node : ", node)
        # first node create cluster.
        if not cluster:
            if node not in has_cluster:
                has_cluster.add(node)

            cluster[c_id] = {node : 0}
            cluster_ct[c_id] = node
            cluster_area[c_id] = _cluster_area(cluster[c_id])

            #print("Create New cluster id : ", c_id)
            #print("member : ", len(cluster[c_id]))
            #print("area : ", cluster_area[c_id])
            #print("centroid : ", cluster_ct[c_id])

            c_id += 1

        # next node
        else:
            if node in has_cluster:
                continue
    
            # Not found any existing cluster that node could be enter.
            if not _add_to_exist_clsuter(node):
                if node not in has_cluster:
                    has_cluster.add(node)

                cluster[c_id] = {node : 0}
                cluster_ct[c_id] = node
                cluster_area[c_id] = _cluster_area(cluster[c_id])

                #print("Create New cluster id : ", c_id)
                #print("member : ", len(cluster[c_id]))
                #print("area : ", cluster_area[c_id])
                #print("centroid : ", cluster_ct[c_id])

                c_id += 1
   
def _add_to_exist_clsuter(node):
    global cluster
    global cluster_ct
    global cluster_area
    global c_id
    global has_cluster

    min_distance = 999999
    final_cluster = 0
    check_cluster = []
    neighbors = nx.neighbors(G, node)
    found_cluster = False

    # check node with existing cluster
    for rel in neighbors: # current checking node.
        for c in cluster: # existing cluster.

            # if aready check with this cluster id, not do again.
            if c in check_cluster:
                continue
                    
            # if connected with this cluster id, check distance to the cluster centroid.
            if rel in cluster[c]:
                check_cluster.append(c)
                distance = distance_to_centroid(cluster[c], node, cluster_ct[c])

                if distance < cluster_area[c]:

                    if distance < min_distance:
                        min_distance = distance
                        final_cluster = c
                        found_cluster = True
    # Found existing cluster that node could be enter.
    if final_cluster != 0:
        #print("To Existing Cluster : ", final_cluster)
        #print("distance : ", min_distance)
        if node not in has_cluster:
            has_cluster.add(node)
        # add node to cluster.
        cluster[final_cluster][node] = min_distance

        # if cluster amount more than 2, re-check cluster centroid.
        if len(cluster[final_cluster]) > 2:
            new_centroid = _update_centroid(cluster[final_cluster])

            if new_centroid != cluster_ct[final_cluster]:
                cluster_ct[final_cluster] = new_centroid
                cluster[final_cluster] = _update_distance_to_centroid(cluster[final_cluster], cluster_ct[final_cluster])
                        

        # update cluster area.
        cluster_area[final_cluster] = _cluster_area(cluster[final_cluster])

        # check node distance to centroid, if out of range will find new cluster.
        for n_distance in cluster[final_cluster].copy():
            if cluster[final_cluster][n_distance] > cluster_area[final_cluster]:
                #print("Over lenght!!")
                # find new cluster.
                
                cluster[final_cluster].pop(n_distance)
                # if can't enter to any exist cluster, create new cluster
                if not _add_to_exist_clsuter(n_distance):
                   
                    cluster[c_id] = {node : 0}
                    cluster_ct[c_id] = node
                    cluster_area[c_id] = _cluster_area(cluster[c_id])

                    #print("Create New cluster id : ", c_id)
                    #print("member : ", len(cluster[c_id]))
                    #print("area : ", cluster_area[c_id])
                    #print("centroid : ", cluster_ct[c_id])

                    c_id += 1
    
        #print("member : ", len(cluster[final_cluster]))
        #print("area : ", cluster_area[final_cluster])
        #print("centroid : ", cluster_ct[final_cluster])

    return found_cluster

def distance_to_centroid(cluster, node, centroid):
  
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

def _update_centroid(cluster_node):
    # when cluster have new member, calculate node average distance again to find centroid.
    
    new_centroid = None
    min_avg = 999999999.99
    subg = nx.subgraph(G, cluster_node)

    word_allSP = dict(nx.shortest_path_length(subg, weight='cost', method='dijkstra'))

    for key in word_allSP:
        avg_nodeSP = sum(word_allSP[key].values()) / (len(word_allSP[key]))
        if min_avg > avg_nodeSP:
            min_avg = avg_nodeSP
            new_centroid = key
     
    return new_centroid
           
def _update_distance_to_centroid(cluster_node, centroid):

    # create subgraph of cluster.        
    cluster = nx.subgraph(G, cluster_node)

    # shortest path from centroid to member of cluster.
    return dict(nx.single_source_dijkstra_path_length(cluster, centroid, weight='cost'))

def _write_graph_to_gpickle_format(g_file):
    G = nx.Graph()

    for node in word_count:
        cid = 0
        cent = 0
        for c_id in cluster:
            if node in cluster[c_id]:
                cid = c_id
                break
        if cluster_ct[cid] == node:
            cent = 1
            
        G.add_node(node, occur=word_count[node], tag=word_tag[node], cluster=cid, centroid = cent)
      

    for edge in link_count:
        nodes = edge.split('|')
        G.add_edge(nodes[0], nodes[1], count=link_count[edge],
                   dice=link_dict[edge], cost=link_cost[edge])

    print(nx.info(G))
    nx.write_gpickle(G, g_file)


def clustering():
    path = "Document/corpus221/cleantag/"
    read_document(path)

    print("\n\n######### Result ###########")
    for c in cluster:
        print("\n")
        print("Cluster id : ", c)
        print("member : ", len(cluster[c]))
        print("area : ", cluster_area[c])
        print("centroid : ", cluster_ct[c])
    

clustering()