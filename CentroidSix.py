import networkx as nx
import operator
import random

Cooccs = None
nodes = dict()
words = []
centroid = ""
candidatesum = dict()
writetextline = ""

def ReadG():
    global Cooccs
    print("Read Graph...")
    Cooccs = nx.read_gml("GML/DB40.gml")
    print("Find High Frequency Rang")
    Findhighfrequency()
    

def Findhighfrequency():
    global Cooccs
    global nodes
    for n in Cooccs.nodes:
        occur = Cooccs.node[n]['occur']
        nodes[n] = occur
    
    descend = sorted(nodes.items(), key=operator.itemgetter(1), reverse=True)

    for n in range(0, 2000):
        words.append(descend[n][0])
    
    Randomsixword()

def Randomsixword():
    global words
    global writetextline
    r = 1
    file = open("Result.txt","w") 
    while r < 1000:
        query = []
        writetextline = ""
        while len(query) < 6:
            rand = random.randint(0, 1499)
            w = words[rand]
            if w not in query:
                query.append(w)
                writetextline += w+", "
        print(r, " : ", query)
        
        #file.write(str(r)+" : ""%s\n" % query +"\n") 
        Calcentroid(query, file)
        r += 1
    file.close() 

def Calcentroid(query, file):
    
    neighbor = dict()
    maxp = 0
    candidate = []
    global centroid
    global candidatesum
    global writetextline
    centroid = ""

    # Examine if keywords existing in db
    for q in query:
        if q in Cooccs:
            pass
        else:
            query.remove(q)

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
                
                if r != q:
                    if r in neighbor:
                        neighbor[r] += 1
                        candidatesum[r] += rel_link[r]
                    else:
                        neighbor[r] = 1
                        candidatesum[r] = rel_link[r]
     
        
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
    print("Centroid :: ", centroid)
    writetextline += centroid
    file.write(str(writetextline)+"\n") 

#Find Average Distance --> Sum/N
def Shortestaveragedistance(query, candidate):
    global candidatesum
    global centroid
    minaverage = 1000
    for cd in candidate:
        average = candidatesum[cd] / len(query)
        if average < minaverage:
            minaverage = average
            centroid = cd

ReadG()