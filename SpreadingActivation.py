import networkx as nx
from time import time, strftime, localtime
from datetime import timedelta
import operator
#Cooccs = nx.read_gpickle("Database/Pickle/man.gpickle")
#print(nx.info(Cooccs))
from networkx.algorithms import approximation as approx
def MaxDistance(Cooccs, query):
    
    start = time()
    maxdistance = 0
    word = query
  
    for w in range(len(word)):
        for nx in range(w+1, len(word)):
         
            print('max 1 :', nx.efficiency(Cooccs, word[w], word[nx]))
   

  
    end = time()
    xtime = end - start
    print('Processing Time:', secondsToStr(xtime)) 

#Covert Time from second to HH.MM.SS format
def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))  
#MaxDistance()