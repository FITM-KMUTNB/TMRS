import networkx as nx
import operator

Cooccs = nx.read_gpickle("Database/Pickle/221.gpickle")


# Generate connected components and select the largest:
largest_component = max(nx.connected_components(Cooccs), key=len)

# Create a subgraph of G consisting only of this component:
LargestGraph = Cooccs.subgraph(largest_component)

for n in Cooccs:
    try:
        Cooccs.node[n]['document']
        print(n, " Doc ::",Cooccs.node[n]['occur'])
       
    except:
        pass

def findcentroid():

    global LargestGraph

    final_avg = 999999999.99
    final_key = ''
    # find node shortest path to all nodes
    word_allSP = dict(nx.shortest_path_length(LargestGraph, weight='cost'))

    for key in word_allSP:
        avg_nodeSP = sum(word_allSP[key].values())/(len(word_allSP[key]))
        if final_avg > avg_nodeSP:
            final_avg = avg_nodeSP
            final_key = key

    print('The centroid is : ', final_key, final_avg)
#findcentroid()
#nx.set_node_attributes(Cooccs, {"test": {'disease':222}} )
#nx.write_gml(Cooccs, "C:/Users/Kaow/Documents/Project/TMRS/GML/test.gml")

#neighbor = nx.single_source_dijkstra_path_length(Cooccs, words[i], weight='cost',cutoff = arearadius) // IF Weight < cutoff
#nx.write_edgelist(g, 'relations.edgelist', delimiter='|')