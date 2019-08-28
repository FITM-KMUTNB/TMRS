from time import time, strftime, localtime
from datetime import timedelta
import networkx as nx
import glob
import operator
import os
from fuzzywuzzy import fuzz

dir_path = os.path.dirname(os.path.realpath(__file__))

print("Read Graph ... ")
Cooccs = nx.read_gml(dir_path+"/GML/226.gml")
centroid = dict()
candidatesum = dict()

def calcentroid(inputq):
    
    query = inputq.split()
    neighbor = dict()
    maxp = 0
    candidate = []
    global centroid
    global candidatesum
    centroid = dict()

    # Examine if keywords existing in db
    for q in query:
        if q in Cooccs:
            pass
        else:
            query.remove(q)

    print("query : ", query)

    # Find largest length between keywords
    for wp in range(len(query)):
        for wn in range(wp+1, len(query)):
            if wn > len(query):
                break
            try:
                cost = nx.dijkstra_path_length(Cooccs, query[wp], query[wn], weight='cost')
                if cost > maxp:
                    maxp = cost
            except nx.NetworkXNoPath:
                print("No Path Between :: ", query[wp], " and ", query[wn])
             
    arearadius = (maxp / 2.0) + 1
    round = 1
    
    # Find Related node within keywords radius
    while len(candidate) < 10:
        print("Activat round::", round)
        
        if round > 1:
            arearadius = arearadius + (arearadius/2)
            candidate = []
            neighbor = dict()
            candidatesum = dict()
        print("Radius : ", arearadius)
        for q in query:
                            
            rel_link = nx.single_source_dijkstra_path_length(Cooccs, q, weight = 'cost', cutoff = arearadius)

            for r in rel_link:
                try:
                    Cooccs.node[r]['disease']
                    if r != q:
                        if r in neighbor:
                            neighbor[r] += 1
                            candidatesum[r] += rel_link[r]
                        else:
                            neighbor[r] = 1
                            candidatesum[r] = rel_link[r]
                except:
                    pass
        
        # Find node that related to all keywords (Candidate Centroid)
        
        for n in neighbor:
            if neighbor[n] == len(query):
                candidate.append(n)

        if round > 10 and len(candidate > 0):
            break
        round += 1
        print("Cadidate : ", len(candidate))
    
    #Find node that have most minimun average distance. (Centroid)     
    Shortestaveragedistance(query, candidate)
    findDoc(sorted(centroid.items(), key=operator.itemgetter(1)))
    #print("Centroid :: ", centroid[:10])
    return(centroid[:10])

#Find Average Distance --> Sum/N
def Shortestaveragedistance(query, candidate):
    global candidatesum
    
    for cd in candidate:
        average = candidatesum[cd] / len(query)
        centroid[cd] = average
       
#Find Disease Document
def findDoc(getcentroid):
    global centroid
    path = dir_path+"/Document/corpus 226/Wiki"
    os.chdir(path)
    
    for c in range(len(getcentroid)):
        maxratio = 0
        diseasebook = ""
        for TextName in glob.glob("*.txt"):
            docname = TextName.replace(".txt", "")
        
            ratio = fuzz.ratio(docname.lower(), getcentroid[c][0].lower())
            
            if ratio > maxratio:
                maxratio = ratio
                diseasebook = TextName

        if diseasebook != "":    
            getcentroid[c] = (*getcentroid[c], diseasebook)

        if len(getcentroid[c]) == 2:
            getcentroid[c] = (*getcentroid[c], "None")
    
    centroid = getcentroid

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))   

