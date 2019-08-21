from time import time, strftime, localtime
from datetime import timedelta
import networkx as nx
import operator


def main():
    query = input("Input Query or (E)xit ::")
    calcentroid(query)


def calcentroid(query):

    print("Read Graph ... ")
    Cooccs = nx.read_gml("GML/226.gml")
      
    while query != 'e':
        start = time()
        query = query.split()
        count = 1
        centroidcandidates = []
        centroid = dict()

        while True:
            centroidcandidates = []
            node2colors = dict()
            reachednode = {}
            words = []
            maxshortdistance = 0
            

            print("Activating round to execute :", count)
            # Check if query word exist in database.
            for qword in query:
                if qword in Cooccs:
                    words.append(qword)
            if not words:
                break
        
            # Find Max shortest path distance of set of query for calulate radius.
            reachednum = 1
            for i in range(len(words)):
                reachcount = 1
                for j in range(len(words)):

                    if words[i] == words[j]:
                        continue

                    try:
                        cost = nx.dijkstra_path_length(Cooccs, words[i], words[j], weight='cost')
                        path = nx.dijkstra_path(Cooccs , words[i], words[j], weight='cost')
                        reachcount += 1

                    except nx.NetworkXNoPath:
                        print("No Path Between :: ",words[i], " and ",words[j])
                    
                    # If words can be reached in the graph database from one another 
                    if reachcount == len(words):
                        reachednode[words[i]] = reachednum
                        reachednum += 1

                    # Find Max Distance Between words in query.
                    if maxshortdistance < cost:
                        maxshortdistance = cost
                        #print(maxshortdistance)
                    
   
            print("Reached Node :: ", reachednode)
            print("Max Shortest Path :: ", path)
            arearadius = (maxshortdistance/2.0)+1
            print("Radius::", arearadius)
        
            
            # Find which term can reached to all of activated term.
            for i in reachednode.keys():
                visited = nx.neighbors(Cooccs, i)
                print("Activating :: ", i)
                                
                for v in visited:
                
                    if v in node2colors:
                        node2colors[v].append(reachednode[i])
                    else:
                        node2colors[v] = [reachednode[i]]

                if count > 1:
                    visitedlist = list(nx.neighbors(Cooccs, i))
                    
                    for c in range(count-1):
                        print("Activating :: ", visitedlist[c])
                        
                        visited2 = nx.neighbors(Cooccs, visitedlist[c])
                        
                        for v in visited2:
                
                            if v not in node2colors:
                                node2colors[v] = [reachednode[i]]
                            

           
            for i in node2colors:
                if len(node2colors[i]) == len(reachednode):
                    
                    centroidcandidates.append(i)
            
            #print("Centroid Candidates (", len(centroidcandidates), ") :: ", centroidcandidates)
            print("Centroid Candidates (", len(centroidcandidates), ")")
            
            if len(centroidcandidates) > 10:
                break                     
            count +=1

        
        pathsum = dict()
        for cand in centroidcandidates:
            shortestp = 0
            
            for keyword in words:
                if cand != keyword: 
                    
                    shortestp += nx.dijkstra_path_length(Cooccs, cand, keyword, weight='cost')
            
            pathsum[cand] = shortestp
        
        averagesp = 1000000
        for s in pathsum:
            try:
                Cooccs.node[s]['disease']
            
                shortestp = pathsum[s]/len(words)
            
                if shortestp < averagesp:
                
                    centroid[s] = shortestp
            except:
                pass
                
                
                    
        print("Centroid :: ", sorted(centroid.items(), key=operator.itemgetter(1)))
        end = time()
        xtime = end - start
        print('Processing Time:', secondsToStr(xtime)) 

        query = input("Input Query or (E)xit ::")


def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))   

main()