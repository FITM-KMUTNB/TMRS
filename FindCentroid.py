from time import time, strftime, localtime
from datetime import timedelta
import networkx as nx
import operator
import os

Cooccs = None

def Centroid(keywords):
    start = time()
    keywords = keywords.split()
  
    print("Input Keyword : ", keywords)
    node = CheckNodeExist(keywords)
    print("Node in DB : ", node)
   
    print("Calculate sum distance")
    costsum = SumDistance(node)
    
    print("Calculate average distance")
    nodeaverage = AverageDistance(costsum, node)
    #print(sorted(nodeaverage.items(), key=operator.itemgetter(1))[:20])
    print("Calculate hop sum")
    hopsum, nodereach = Sumhop(node)
    candidate = []
    for n in nodereach:
        if nodereach[n] == len(node):
            candidate.append(n)
    #print(sorted(hopsum.items(), key=operator.itemgetter(1))[:20])
    allcentroid, diseasecentroid = SortCentroid(nodeaverage, hopsum, candidate)

    print("Centroid :", allcentroid)
    print("Disease :", diseasecentroid)

    topdisease = dict()
 
    
    for index in range(len(diseasecentroid)):
        for tuples in range(len(diseasecentroid[index])):
            topdisease[diseasecentroid[index][tuples][0]] = diseasecentroid[index][tuples][1]
    
    end = time()
    xtime = end - start
    print('Processing Time:', secondsToStr(xtime)) 
    return(node, allcentroid[:10], list(topdisease.items())[:5])


def SortCentroid(nodeaverage, hopsum, candidate):
    allcentroid = []
    diseasecentroid = []
    minhopkey = min(hopsum, key=hopsum.get)
    minhop = hopsum[minhopkey]
    calround = 1

    while len(diseasecentroid) < 2:
        centroid = dict()
        disease = dict()
        if calround > 1:
            minhop += 1
        for c in candidate:
            if hopsum[c] == minhop:
                try:
                    Cooccs.node[c]['disease']
                    disease[c] = nodeaverage[c]
                except:
                    pass
                centroid[c] = nodeaverage[c]
        if len(centroid) > 0:
            allcentroid.append(sorted(centroid.items(), key=operator.itemgetter(1)))
                    
        if len(disease) > 0:
            diseasecentroid.append(sorted(disease.items(), key=operator.itemgetter(1)))
        calround += 1

    return(allcentroid, diseasecentroid)
    
#Find sum hop to input keyword
def Sumhop(node):
    hopsum = dict()
    nodereach = dict()
    for n in node:
        hop_link = nx.single_source_dijkstra_path_length(Cooccs, n)
        for c in hop_link:
            if c in node:
                continue
            if c in hopsum:
                hopsum[c] += hop_link[c]
                nodereach[c] += 1
            else:
                hopsum[c] = hop_link[c]
                nodereach[c] = 1
    return(hopsum, nodereach)

#Find average distance to input keyword  
def AverageDistance(nodesum, query):
    nodeaverage = dict()

    for n in nodesum:
        average = nodesum[n]/len(query)   
        nodeaverage[n] = average                                                                          
    return nodeaverage

#Find sum distance to input keyword
def SumDistance(node):
    costsum = dict()
    for n in node:
        cost_link = nx.single_source_dijkstra_path_length(Cooccs, n, weight="cost")
        for c in cost_link:
            if c in node:
                continue
            if c in costsum:
           
                costsum[c] += cost_link[c]
            else:
            
                costsum[c] = cost_link[c]
    return costsum

#Check if have input word in database -> Has = True, Not Has = False
def CheckNodeExist(keywords):
    node = []
    for word in keywords:
        if NodeExist(word):
            node.append(word)
    return node

def NodeExist(word):
    hasnode = Cooccs.has_node(word)
    return hasnode
#Check Node Can Reach To Each Other -> Reached = True, Unreached = False
def NodeReach(source, target):
    reach = nx.has_path(Cooccs, source, target)
    return reach

#Read Graph from gpickle file and stored in Cooccs variable
def ReadGraph():
    global Cooccs
    dir_path = os.path.dirname(os.path.realpath(__file__))
    Cooccs = nx.read_gpickle(dir_path+"/Database/Pickle/221.gpickle")
    print("Read Graph ... Done.")
    print(nx.info(Cooccs))

#Covert Time from second to HH.MM.SS format
def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))   

ReadGraph()

#keywords = "itch vomit muscle pain"
#Centroid(keywords)
