from collections import defaultdict
import networkx as nx

G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
# Generate connected components and select the largest:
largest_component = max(nx.connected_components(G), key=len)

# Create a subgraph of G consisting only of this component:
LargestGraph = G.subgraph(largest_component)

def shortest_path(G, source):
       
    shortest_distance = dict()
    previous_vertex = dict()
    visited = []
    unvisited = [source]

    for sv in unvisited:
       
        if sv == source:
          
            visited.append(sv)
            for v in G.neighbors(sv):
                if v not in visited:
                    distance = G[sv][v]['cost']
                    shortest_distance[v] = distance
                    previous_vertex[v] = sv
            next_visit = min(shortest_distance, key=shortest_distance.get)
           
            unvisited.append(next_visit)
        else:
            min_distance = 99999999
            for v in G.neighbors(sv):
                distance = G[sv][v]['cost']

                if v not in visited and v in shortest_distance:
                    distance = distance + shortest_distance[sv]
                    
                    if distance < shortest_distance[v]:
                        shortest_distance[v] = distance
                        previous_vertex[v] = sv

                    if min_distance > distance:
                        min_distance = distance
                        next_visit = v

                elif v not in visited and v not in shortest_distance:
                
                    shortest_distance[v] = distance
                    previous_vertex[v] = sv

                    if min_distance > distance:
                        min_distance = distance
                        next_visit = v

            visited.append(sv)      
            
            print("Next2 : ", next_visit)
            unvisited.append(next_visit)

    print(shortest_distance)


    



num = 0

for n in G.nodes:
    print("Source :: ", n)
    print(shortest_path(G, n))
    num += 1

    if num > 10:
        break