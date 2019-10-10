import networkx as nx
import operator
import nltk

G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
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


def spreading_activation_centroid(G, keywords):
    centroid = ''
    key_point = [] # node point to activate and find neighbors.
    activate_round = 1
    candidate = dict()
    
    node_count = dict() # node count to all keywords
    node_sum = dict() # node sum distance to all keywords
    node_distance = [] # distance from node to each keywords

    for key in keywords:
            initial = dict()
            # initail distance 
            initial[key] = 0
            node_distance.append(initial)
            key_point.append([key])

    while len(candidate) < 10:
        #print("Activation round : ", activate_round)
        min_average = 999999
        centroid = ''
              

        for index in range(len(key_point)):
            activate_size = 1
            # initail point.
            for a in range(activate_size):
                act_node = key_point[index].pop(0)
                #print("Activate :: ", act_node)

                # Activate
                related_node = nx.neighbors(G, act_node)

                # iterate neighbors.
                for r in related_node:
                    if r not in key_point[index]:
                        # append node for next activation.
                        key_point[index].append(r)
                        distance_dict = node_distance[index]
                        
                        # distance from neightbor to activate node.
                        distance_dict[r] = distance_dict[act_node] + G[act_node][r]['cost']
                        if r in node_count:
                            node_count[r] += 1
                            node_sum[r] += distance_dict[r]
                        else:
                            node_count[r] = 1
                            node_sum[r] = distance_dict[r]
                    
                    if node_count[r] == len(keywords):
                        if G.node[r]['tag'] == 'DS':
                            print(r, node_count[r])
                            candidate[r] = node_sum[r] / len(keywords)
                            print(candidate[r])
                        """if min_average > candidate[r]:
                            min_average = candidate[r]
                            centroid = r"""
        #print("Candidate : ", len(candidate))
       
        activate_round += 1
    
    return dict(sorted(candidate.items(), key=operator.itemgetter(1))) 

"""keywords = ["headache", "infertility", "nausea", "miscarriage", "edema"]
result = spreading_activation_centroid(G, keywords)

print(result)"""

for i in range(3):
    print(i)