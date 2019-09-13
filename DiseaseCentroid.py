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