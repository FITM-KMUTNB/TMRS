import networkx as nx
import matplotlib.pyplot as plot
import operator

G = nx.Graph()

G.add_edges_from([('A', 'B'), ('A', 'M'), ('A', 'L'), ('B', 'C'), ('B', 'D'),
                  ('B', 'N'), ('B', 'O'), ('C', 'D'), ('D', 'E'), ('D', 'O'), ('E', 'F'), ('F', 'G'), ('F', 'N'), ('G', 'H'), ('H', 'N'), ('H', 'I'), ('H', 'P'), ('P', 'O'), ('P', 'I'), ('P', 'M'), ('I', 'J'), ('J', 'K'), ('K', 'M'), ('K', 'L')])

#print('Shortest path from E to L is :',
      #nx.shortest_path(G, source='E', target='L'))

final_avg = 999999999.99
final_key = ''
# find node shortest path to all nodes
node_allSP = dict(nx.shortest_path_length(G, weight='weight'))
#print(node_allSP)
for key in node_allSP:
    avg_nodeSP = sum(node_allSP[key].values())/(len(node_allSP[key]))
    #print('AverageSP to all nodes of :', key, ' is ', avg_nodeSP)
    if final_avg > avg_nodeSP:
        final_avg = avg_nodeSP
        final_key = key

print('The centroid is : ', final_key, 'the length is ', final_avg)

# Draw Graph
#pos = nx.spring_layout(G)
#nx.draw(G, pos, with_labels=True, font_color='yellow', node_size=1500)
#plot.show()


def spreading_activation_centroid(G, keywords):
    activate_list = []
    candidate = []
    current_hop = 0
    node_count = dict()
    node_distance = []

    for key in keywords:
        activate_list.append([key])
        node_distance.append({key : 0})
               
    while len(candidate) <= 0:
        for circle in range(len(activate_list)):
            activate_node = activate_list[circle][current_hop]
            
            for neighbors in nx.neighbors(G, activate_node):
                if neighbors in keywords:
                    continue

                # distance from initial point.
                if neighbors not in node_distance[circle]:
                    
                    node_distance[circle][neighbors] = node_distance[circle][activate_node] + 1
                
                # check intersect
                if neighbors in node_count:

                    if neighbors not in activate_list[circle]:
                        activate_list[circle].append(neighbors)
                        node_count[neighbors] += 1

                    if node_count[neighbors] == len(keywords):
                        candidate.append(neighbors)
            
                else:
                    activate_list[circle].append(neighbors)
                    node_count[neighbors] = 1
          
            

        current_hop += 1
    
    print(candidate)       
     

# Example
keywords = ['I', 'A', 'E']
spreading_activation_centroid(G, keywords)

