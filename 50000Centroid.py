import networkx as nx
import random
import operator
import SpreadingActivation as sa
fileResult = open("Result Centroid/50000.txt", "w") 
Cooccs = nx.read_gpickle("Database/Pickle/221clean.gpickle")
print(nx.info(Cooccs))
centroid = ""
candidatesum = dict()


def Random100(file):
    global writetextline
    queryset = []                                                                      
    largest_component = max(nx.connected_components(Cooccs), key=len)
    node = list(largest_component)

    for t in range(1):
        print("Tuples ",t+1)
        query = []
        writetextline = ""
        if t+1 == 1:
            writetextline += "{"
        writetextline += str(t+1)+"{"
        while True:
            while True:
                randword = random.randint(0, len(node)-1)
             
                inputnode = node[randword]
                if inputnode not in query:
                    writetextline += "'"+inputnode + "':"+str(Cooccs.node[inputnode]['occur'])+", "
                    query.append(inputnode)
                    break

            if len(query) == 25:
                checkqueryset = sorted(query)
                if checkqueryset not in queryset:
                    queryset.append(checkqueryset)
                    break
                else:
                    query = []
                    writetextline = ""
                    writetextline += str(t+1)+"{"
       
        #Calcentroid(query, file,t+1)
        sa.MaxDistance(Cooccs, query)

def Calcentroid(query, file, roundnum):
    
    neighbor = dict()
    maxp = 0
    candidate = []
    global centroid
    global candidatesum
    global writetextline
    centroid = ""

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

    for n in neighbor:
        if neighbor[n] == len(query):
            candidate.append(n)
  
    Shortestaveragedistance(query, candidate)

    writetextline += "'t' : '"+centroid+"' }"
    if roundnum == 1:
        writetextline += "}"
    else:
        writetextline += ","
    file.write(str(writetextline)+"\n") 
          
#Find Average Distance --> Sum/N
def Shortestaveragedistance(query, candidate):
    global candidatesum
    global centroid
    minaverage = 999999999.99

    for cd in candidate:
   
        average = candidatesum[cd] / len(query)
        if minaverage > average:
            minaverage = average    
            centroid = cd

Random100(fileResult)