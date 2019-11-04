import networkx as nx
import operator
import nltk

G = nx.read_gpickle("Database/Pickle/man.gpickle")
print(nx.info(G))
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

#print(nx.single_source_dijkstra_path(G,'dengue_fever', weight='cost', cutoff=15))

#node_sp = nx.single_source_dijkstra_path_length(G, 'disease', weight='cost', cutoff=10)


x = [1, 2, 3, 4]

def addition(array):
    if len(array) == 0:
        return 0
    else:
        return array[0] + addition(array[1:])

x = [[1,2], [[3], 4, [5,6]], [7,[8]]]
def addition2(array):
    total = 0
   
    for num in array:
        print(num)
        if type(num) != list:
            total += num
        else:
            total += addition2(num)
    print('total:', total)
    return total

#addition2(x)


min_average = 999999.999
centroid = ''
for n in G.nodes:
    sp_distance = nx.single_source_dijkstra_path_length(G, n, weight='cost')
    sum_distance = 0

    for dis in sp_distance:
        sum_distance += sp_distance[dis]
    
    average = sum_distance / len(sp_distance)
    if min_average > average:
        min_average = average
        centroid = n
print(centroid)