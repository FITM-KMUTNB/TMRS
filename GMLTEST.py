import networkx as nx
import operator
import nltk


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


dicts = [['a','b','c']]

for a in range(len(dicts[0])):
    dicts[0].pop(0)
    if 'd' not in dicts[0]:
        dicts[0].append('d')
print(dicts)
#node_sp = nx.single_source_dijkstra_path_length(G, 'disease', weight='cost', cutoff=10)

