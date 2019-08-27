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

def calcentroid(inputq):
    
    query = inputq.split()
    neighbor = dict()
    maxp = 0
    candidate = []
    global centroid
    centroid = dict()

    # Examine if keywords existing in db
    for q in query:
        if q in Cooccs:
            pass
        else:
            query.remove(q)

    print("query : ", query)

    # Find largest length between keywords
    for wp in query:
        for wn in query:
            if wp == wn:
                continue
            try:
                cost = nx.dijkstra_path_length(Cooccs, wp, wn, weight='cost')
                if cost > maxp:
                    maxp = cost
            except nx.NetworkXNoPath:
                print("No Path Between :: ", wp, " and ", wn)
             
    arearadius = (maxp / 2.0) + 1
    round = 1
    
    # Find Related node within keywords radius
    while len(candidate) < 10:
        print("Radius : ", arearadius)
        if round > 1:
            arearadius = arearadius + (arearadius/2)
            candidate = []
            neighbor = dict()

        for q in query:
                            
            rel_link = nx.single_source_dijkstra_path_length(Cooccs, q, weight = 'cost', cutoff = arearadius)

            for r in rel_link:
                try:
                    Cooccs.node[r]['disease']
                    if r != q:
                        if r in neighbor:
                            neighbor[r] += 1
                        else:
                            neighbor[r] = 1
                except:
                    pass
        
        # Find node that related to all keywords (Candidate Centroid)
        print("Neighbor : ", len(neighbor))
        for n in neighbor:
            if neighbor[n] == len(query) :
                candidate.append(n)

        if round > 10 and len(candidate > 0):
            break
        round += 1
        print("Cadidate : ", len(candidate))

    #Find node that have most minimun average distance. (Centroid)     
    Shortestaveragedistance(query, candidate)
    findDoc(sorted(centroid.items(), key=operator.itemgetter(1)))
    print("Centroid :: ", centroid)
    return(centroid)

def Shortestaveragedistance(query, candidate):
    
    for cd in candidate:
        sum = 0
        for wd in query:
            sum += nx.dijkstra_path_length(Cooccs, cd, wd, weight='cost')
        
        average = sum / len(query)
        centroid[cd] = average
       

def findDoc(getcentroid):
    global centroid
    path = dir_path+"/Document/corpus 226/Wiki"
    os.chdir(path)
    
    for c in range(len(getcentroid)):
        for TextName in glob.glob("*.txt"):
            docname = TextName.replace(".txt", "")
        
            ratio = fuzz.ratio(docname.lower(), getcentroid[c][0].lower())
            
            if ratio > 80 and len(getcentroid[c]) != 3:
                
                getcentroid[c] = (*getcentroid[c], TextName)
        if len(getcentroid[c]) == 2:
            getcentroid[c] = (*getcentroid[c], "None")
                
    print(getcentroid)
    centroid = getcentroid

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))   

