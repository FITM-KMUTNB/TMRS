import networkx as nx
import operator
import random

Cooccs = None
nodes = dict()
words = []
centroid = dict()

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
        words.append([descend[n][0], descend[n][1]])
    print(words)
    #Randomsixword()

def Randomsixword():
    global words
    #print(words)
    r = 1
    file = open("Result.txt","w") 
    while r < 1000:
        query = []

        while len(query) < 6:
            rand = random.randint(0, 1499)
            w = words[rand]
            if w not in query:
                query.append(w)
        print(r, " : ", query)
        file.write(str(r)+" : ""%s\n" % query +"\n") 
        Calcentroid(query, file)
        r += 1
    file.close() 
def Calcentroid(query, file):

    neighbor = dict()
    maxp = 0
    candidate = []
    global centroid
    centroid = dict()
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
    
    while len(candidate) < 10:
        if round > 1:
            arearadius = arearadius + (arearadius/2)
            candidate = []

        for q in query:
            rel_link = nx.single_source_dijkstra_path_length(Cooccs, q, weight = 'cost', cutoff = arearadius)

            for r in rel_link:
                if r != q:
                    if r in neighbor:
                        neighbor[r] += 1
                    else:
                        neighbor[r] = 1
    
        for n in neighbor:
            if neighbor[n] == len(query) and len(candidate) < 30:
                candidate.append(n)
        round += 1

    Shortestaveragedistance(query, candidate)
    print("Centroid :: ", centroid)
    file.write("Centroid :: ""%s\n" % centroid +"\n") 

def Shortestaveragedistance(query, candidate):
    
    for cd in candidate:
        sum = 0
        for wd in query:
            sum += nx.dijkstra_path_length(Cooccs, cd, wd, weight='cost')
        
        average = sum / len(query)
        centroid[cd] = average

ReadG()