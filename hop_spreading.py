import networkx as nx
import operator

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

    next_act = 0
    while len(candidate) < 10:
        print("Activation round : ", activate_round)
        min_average = 999999
        centroid = ''
        for index in range(len(key_point)):
            activate_size = 1
            # initail point.
            for a in range(activate_size):
                act_node = key_point[index][next_act]
                print("Activate [", index,"]:: ", act_node)

                # Activate
                related_node = nx.neighbors(G, act_node)

                # iterate neighbors.
                for r in related_node:
                    if r in keywords:
                        continue

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
        next_act += 1
    
    return dict(sorted(candidate.items(), key=operator.itemgetter(1)))

def spreading_activation_centroid2(G, keywords):
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

    next_act = 0
    while len(candidate) < 1:
        print("Activation round : ", activate_round)
        min_average = 999999
        centroid = ''
        for index in range(len(key_point)):
            activate_size = 1
            # initail point.
            for a in range(activate_size):
                act_node = key_point[index][next_act]
                print("Activate [", index,"]:: ", act_node)

                # Activate
                related_node = nx.neighbors(G, act_node)

                # iterate neighbors.
                for r in related_node:
                    if r in keywords:
                        continue

                    if r not in key_point[index]:
                        # append node for next activation.
                        key_point[index].append(r)
                        distance_dict = node_distance[index]
                        
                        # distance from neightbor to activate node.
                        distance_dict[r] = distance_dict[act_node] + 1
                        if r in node_count:
                            node_count[r] += 1
                            node_sum[r] += distance_dict[r]
                        else:
                            node_count[r] = 1
                            node_sum[r] = distance_dict[r]
                    
                    if node_count[r] == len(keywords):
                        
                        candidate[r] = node_sum[r] / len(keywords)
                        """if min_average > candidate[r]:
                            min_average = candidate[r]
                            centroid = r"""
        #print("Candidate : ", len(candidate))
        print(node_count)
        print(key_point)
        activate_round += 1
        next_act += 1
    
    return dict(sorted(candidate.items(), key=operator.itemgetter(1)))

# Example
G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
keywords = ["hematochezia", "headache", "cataplexy", "hemoptysis", "apraxia"]
centroid = spreading_activation_centroid(G, keywords)

for c in list(centroid.items())[:10]:
    print(c)

  