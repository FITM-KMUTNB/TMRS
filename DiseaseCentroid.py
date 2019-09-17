import networkx as nx
import Centroid as ct
import operator

def disease(G, keywords):
      
    return diseasebydistance(G, keywords)

def diseasebyhop(G, keywords):
    disease = dict()
    diseasehop = dict()
    centroid, hop = ct.centroid_by_hop(G, keywords)
   
    for word in centroid:
        try:
            G.node[word]['disease']
            disease[word] = centroid[word]
            diseasehop[word] = hop[word]
        except:
            pass
    allcentroid = dict(sorted(centroid.items(), key=operator.itemgetter(1))[:50])  
    return(disease, allcentroid, diseasehop)

def diseasebydistance(G, keywords):
    disease = dict()
    centroid = ct.centroid_by_distance(G, keywords)
   
    for word in centroid:
        try:
            G.node[word]['disease']
            disease[word] = centroid[word]
        except:
            pass
    allcentroid = dict(sorted(centroid.items(), key=operator.itemgetter(1))[:50])  
    return(disease, allcentroid)

def diseasedocument(G, disease):
    document = dict()

    for word in disease:
        try:
            document[word] = G.node[word]['document']
        except:
            pass
    return document

def disease_neighbors(G, centroid, hop=1):
    
    neighbors = ct.centroid_neighbors(G, centroid, hop)
    node_no = dict()
    node = []
    node_link = []
    path_list = []
    number = 0
 
    #Set node number.
    for n in neighbors:
        temp_path = []
    
        for p in neighbors[n]:
            node_name = dict()
            try:
                G.node[p]['disease']
              
                if p not in node_no:
                    node_no[p] = number
                    node_name['name'] = p
                    node.append(node_name)
                    number += 1
                temp_path.append(p)
            except:
                pass
       
        if len(temp_path) > 1 and temp_path not in path_list:
            path_list.append(temp_path)
    
    for path in path_list:
        for link in range(len(path)):
            source_target = dict()
            if link+1 < len(path):
                source_target["source"] = node_no[path[link]]
                source_target["target"] = node_no[path[link+1]]
                node_link.append(source_target)

    return(node, node_link)

"""G = nx.read_gpickle("Database/Pickle/221clean.gpickle")
centroid = "dengue_fever"
disease_neighbors(G, centroid, 10)"""
