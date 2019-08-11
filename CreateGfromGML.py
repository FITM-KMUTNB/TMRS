import networkx as nx

g = nx.read_gml('GML/CooccsDB40.gml')
shortest = nx.dijkstra_path(g , 'disease', 'lyme')
print(shortest)
nx.write_edgelist(g, 'relations.edgelist', delimiter='|')