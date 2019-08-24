import networkx as nx
import matplotlib.pyplot as plt

g=nx.read_edgelist('Document\Test\TEST2.txt',create_using=nx.Graph(),nodetype=int)

print nx.info(g)

nx.draw(g)


plt.show()