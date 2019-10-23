import networkx as nx
import matplotlib.pyplot as plot
import operator

G = nx.Graph()

G.add_edges_from([('A', 'B'), ('A', 'M'), ('A', 'L'), ('B', 'C'), ('B', 'D'),
                  ('B', 'N'), ('B', 'O'), ('C', 'D'), ('D', 'E'), ('D', 'O'), ('E', 'F'), ('F', 'G'), ('F', 'N'), ('G', 'H'), ('H', 'N'), ('H', 'I'), ('H', 'P'), ('P', 'O'), ('P', 'I'), ('P', 'M'), ('I', 'J'), ('J', 'K'), ('K', 'M'), ('K', 'L')])

print('Shortest path from E to L is :',
      nx.shortest_path(G, source='E', target='L'))

final_avg = 999999999.99
final_key = ''
# find node shortest path to all nodes
node_allSP = dict(nx.shortest_path_length(G, weight='weight'))
print(node_allSP)
for key in node_allSP:
    avg_nodeSP = sum(node_allSP[key].values())/(len(node_allSP[key]))
    print('AverageSP to all nodes of :', key, ' is ', avg_nodeSP)
    if final_avg > avg_nodeSP:
        final_avg = avg_nodeSP
        final_key = key

print('The centroid is : ', final_key, 'the length is ', final_avg)

# Draw Graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_color='yellow', node_size=1500)
plot.show()


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
                #print("Activate [", index,"]:: ", act_node)

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
                            candidate[r] = node_sum[r] / len(keywords)
                        """if min_average > candidate[r]:
                            min_average = candidate[r]
                            centroid = r"""
        #print("Candidate : ", len(candidate))
        
        activate_round += 1
    
    return dict(sorted(candidate.items(), key=operator.itemgetter(1)))

# Example
G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
keywords = ['skin', 'itch', 'headache']
centroid = spreading_activation_centroid(G, keywords)

for c in list(centroid)[:10]:
    print(c)
  