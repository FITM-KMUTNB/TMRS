import networkx as nx

Cooccs = nx.read_gml("GML/226.gml")
noded = 0
for n in Cooccs.nodes:
    try:
        Cooccs.node[n]['disease']
        noded += 1
    except:
        pass
print("Node :: ", noded, "(Disease)")
#nx.set_node_attributes(Cooccs, {"test": {'disease':222}} )
#nx.write_gml(Cooccs, "C:/Users/Kaow/Documents/Project/TMRS/GML/test.gml")

#neighbor = nx.single_source_dijkstra_path_length(Cooccs, words[i], weight='cost',cutoff = arearadius) // IF Weight < cutoff
#nx.write_edgelist(g, 'relations.edgelist', delimiter='|')