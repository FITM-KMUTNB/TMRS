import networkx as nx
import operator
import nltk

#G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
#print(nx.info(G))
#maxdistance2 = nx.single_source_dijkstra_path_length(G,'disease', weight='cost')
#print('max2 : ', G.edges['Year', 'Baby']['cost'])
#first2pairs = {k: cen[k] for k in list(cen.keys())[:10]}
#print(first2pairs)
#print(nx.dijkstra_path_length(G, 'migraine', 'confusion', weight = 'cost'))

#if target_word in nltk.corpus.words.words():
#    print(target_word)
#g2 = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
#word_allSP = dict(nx.floyd_warshall(g2, weight='cost'))

#maxdistance2 = nx.single_source_dijkstra_path_length(G,'depression', weight='cost')

#maxdistance = 0
#maxdistance = min(k for k,v in maxdistance2.items() if v != 0)
#allcentroid = sorted(maxdistance2.items(), key=operator.itemgetter(1))

#print(nx.dijkstra_path_length(G, 'man', 'fever', weight='cost'))
#print(nx.dijkstra_path(G, 'man', 'fever', weight='cost'))

#print(nx.single_source_dijkstra_path(G,'dengue_fever' ,weight='cost'))
lists = [['a','b']]
print(len(lists[0]))
#node_sp = nx.single_source_dijkstra_path_length(G, 'disease', weight='cost', cutoff=10)

