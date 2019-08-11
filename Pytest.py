import networkx as nx
G = nx.Graph()

G.add_node("String1" occur = 3)
G.add_node("String2")
G.add_edge("String1", "String2", weight = 1)

nx.write_gml(G, "test.gml")
