import networkx as nx
import random
import operator

fileResult = open("Centroid Result/1million.txt", "w") 
Cooccs = nx.read_gpickle("Database/Pickle/221.gpickle")
print(nx.info(Cooccs))
centroid = ""
candidatesum = dict()
writetextline = ""

def Random100(file):
    global writetextline
    queryset = []                                                                      
    largest_component = max(nx.connected_components(Cooccs), key=len)
    node = list(largest_component)

    for t in range(3):
        query = []
        writetextline += "{"
        while True:
            while True:
                randword = random.randint(0, len(node)-1)
             
                inputnode = node[randword]
                if inputnode not in query:
                    writetextline += inputnode + ":"+str(Cooccs.node[inputnode]['occur'])+", "
                    query.append(inputnode)
                    break

            if len(query) == 100:
                checkqueryset = sorted(query)
                if checkqueryset not in queryset:
                    queryset.append(checkqueryset)
                    break
       
        Calcentroid(query, file)


def Calcentroid(query, file):
    
    neighbor = dict()
    maxp = 0
    candidate = []
    global centroid
    global candidatesum
    global writetextline
    centroid = ""
    print(query)
    for q in query:
           
        rel_link = nx.single_source_dijkstra_path_length(Cooccs, q, weight = 'cost')
           
        for r in rel_link:
                
            if r not in query:
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
  
    print("Cadidate : ", len(candidate))
    #print(sorted(candidatesum.items(), key=operator.itemgetter(1))[:50])
    #Find node that have most minimun average distance. (Centroid)     
    Shortestaveragedistance(query, candidate)
    #print("Centroid :: ", centroid)
    writetextline += "t : "+centroid+" }"
    #file.write(str(writetextline)+"\n") 
          
#Find Average Distance --> Sum/N
def Shortestaveragedistance(query, candidate):
    global candidatesum
    global centroid
    minaverage = 999999999.99
    diseaselist = {}

    print("Check average")
    for cd in candidate:
        try:
            Cooccs.node[cd]['disease']
            average = candidatesum[cd] / len(query)
            
            diseaselist[cd]=average
      
        except:
            pass
   
    #print(sorted(diseaselist.items(), key=operator.itemgetter(1))[:10])
    print("Check hop")
    check_hop = {}
    for q in query:
        hop_link = nx.single_source_dijkstra_path_length(Cooccs, q)
        for h in hop_link:
            if  h in diseaselist and h in check_hop:
                check_hop[h] += hop_link[h]
            if h in diseaselist and h not in check_hop:
                check_hop[h] = hop_link[h]
    print(sorted(check_hop.items(), key=operator.itemgetter(1))[:30])   

    hopkey = min(check_hop, key = check_hop.get)
    hop = check_hop[hopkey]
    increaseround = 1
    candidatecentroid = {}
    centroidhop  = []
    while len(centroidhop) < 2:
        if increaseround > 1:
            hop += 1
            candidatecentroid = {}
        print("Round:", increaseround," Hop:", hop)
        for d in diseaselist:
            for h in check_hop:
                if check_hop[h] == hop:
                    if d == h and d not in candidatecentroid:
                        candidatecentroid[d] = diseaselist[d]
        if len(candidatecentroid) > 1:
            centroidhop.append(sorted(candidatecentroid.items(), key=operator.itemgetter(1)))

        increaseround += 1
    print(len(centroidhop))
    print(centroidhop)                                                                                                                                                          

query = ["pain","breathlessness","cough"]
Calcentroid(query, None)
#Random100(fileResult)