from time import time, strftime, localtime
from datetime import timedelta
import networkx as nx

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))  


G = nx.read_gpickle("Database/Pickle/221clean.gpickle")
print(nx.info(G))
print("---------------------")
start = time()


targetcount = dict() #store number of reach to given node.
targetdistance = dict() #sum of distance to all of given node.

givennode = ['headache', 'fever', 'itch']

#first ,find node that given node can reach by using single_source_dijkstra_path_length()
for source in givennode:
    reachnode = nx.single_source_dijkstra_path_length(G, source, weight='cost')

    #than store target node and distance from reachnode variable to dictionary.
    for target in reachnode:
        if target in targetcount:
            targetcount[target] += 1
            targetdistance[target] += reachnode[target]
        else:
            targetcount[target] = 1
            targetdistance[target] = reachnode[target]

minaverage = 999999999.99
finalword = ''

#find average distance only node that can reach to all of given word.
for target in targetcount:
    #if node have reach number equal to givennode amount.
    if targetcount[target] == len(givennode):
        averagedistance = targetdistance[target] / len(givennode)
        if (averagedistance < minaverage) and (target not in givennode):
            minaverage = averagedistance
            finalword = target

print("Min average distance word :"+finalword)


end = time()
xtime = end - start
print('Processing Time:', secondsToStr(xtime)) 


