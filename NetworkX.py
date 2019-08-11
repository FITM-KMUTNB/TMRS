import networkx as nx
import matplotlib.pyplot as plt

g = nx.Graph()

g.add_node(1)
g.add_node(3)

g.add_node(2)
g.add_node(5)

g.add_edge(2, 5 ,weight=0.9)
g.add_edge(5, 1,weight=0.9)
g.add_edge(1, 3,weight=0.9)

elist = [(2,5),(5,1),(1,3),(3,2)]

g.add_edges_from(elist)

elist = [('a', 'b', 1.0), ('b', 'c', 9.0), ('a', 'c', 5.0), ('c', 'd', 7.3)]
g.add_weighted_edges_from(elist)


nx.draw(g)

plt.show()




