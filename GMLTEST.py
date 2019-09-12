import networkx as nx
import operator

G = nx.read_gpickle("Database/Pickle/221clean.gpickle")
print(nx.info(G))
#maxdistance2 = nx.single_source_dijkstra_path_length(Cooccs,'disease', weight='cost')
#print('max2 : ', Cooccs.edges['Year', 'Baby']['cost'])
#first2pairs = {k: cen[k] for k in list(cen.keys())[:10]}
#print(first2pairs)

print(nx.dijkstra_path_length(G, 'migraine', 'confusion', weight = 'cost'))

