import networkx as nx
import operator
import nltk

#G = nx.read_gpickle("Database/Pickle/221clean.gpickle")
#print(nx.info(G))
#maxdistance2 = nx.single_source_dijkstra_path_length(Cooccs,'disease', weight='cost')
#print('max2 : ', Cooccs.edges['Year', 'Baby']['cost'])
#first2pairs = {k: cen[k] for k in list(cen.keys())[:10]}
#print(first2pairs)
#print(nx.dijkstra_path_length(G, 'migraine', 'confusion', weight = 'cost'))

target_word = "canadian"
#if target_word in nltk.corpus.words.words():
#    print(target_word)
#g2 = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)
#word_allSP = dict(nx.floyd_warshall(g2, weight='cost'))

tag = {'DS' : ['fever', 'acne', 'migrain'], 'ST' : ['itch', 'fever','cough'], 'DT' : ('DS', 'ST')}
default = "kaow"

if default != None:
    print("hello")