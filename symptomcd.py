import networkx as nx
import random
import Library as ctd


Main_G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
largest_component = max(nx.connected_components(Main_G), key=len)
G = Main_G.subgraph(largest_component)
print(nx.info(G))

fileResult = open("Result Centroid/symptomcd.txt", "w") 

def randomsymptom():

    allsymptom = _get_symptom() # Get all symptom from graph
    tuple_size = 100000
    symptomset = dict()
    duplicate_check = []
    symptomset_size = 5
    result = ""

    for tup in range(tuple_size):
        print("No.", tup+1)
        result = "{"
        while True:
            symptom = random.choice(list(allsymptom.keys()))
            if symptom not in symptomset:
                symptomset[symptom] = allsymptom[symptom] # Keep symptom:frequency
                result += "\""+ symptom + "\" : " + str(allsymptom[symptom]) + ", "
            if len(symptomset) == symptomset_size:
                # if symptom set not duplicate prevoius set.
                if dict(sorted(symptomset.items())) not in duplicate_check:
                    print(symptomset)
                    duplicate_check.append(symptomset)
                    disease = list(centroid(symptomset))[0]
                    print("Centroid : ", disease)
                    result += "\""+ disease + "\" : " + str(G.node[disease]['occur']) + "}"
                    fileResult.write(str(result)+"\n")
                    symptomset = dict()
                    break

                # clear and random symptom set again.
                else:
                    symptomset = dict()
                    result = "{"

def _get_symptom():
    symptom = dict()
    for node in G.nodes:
        if G.node[node]['tag'] == 'ST':
            symptom[node] = G.node[node]['occur']

    return symptom

def centroid(symptom_set):
    keywords = []
 

    for key in symptom_set:
        keywords.append(key)
    
    centroid = ctd.spreading_activation_centroid(G, keywords)

    
    return centroid

def spreading_activation(symptom_set):
    neighbor_count = dict()
    disease_candidate = dict()
    range_n = 2
    while True:
        neighbor_count = dict()
        disease_candidate = dict()

        for key in symptom_set:
            print(key)
            neighbors = nx.single_source_dijkstra_path_length(G, key, cutoff=range_n)
            for n in neighbors:
                if n in neighbor_count:
                    neighbor_count[n] += 1
                else:
                    neighbor_count[n] = 1
        
        for n in neighbor_count:
            try:
                if G.node[n]['tag'] == 'DS' and neighbor_count[n] == len(symptom_set):
                    disease_candidate[n] =  G.node[n]['occur']
            except:
                pass

        if len(disease_candidate) > 10:
            break
        else:
            range_n += 1
    
    min_average = 9999999
    centroid_disease = ''
    for candidate in disease_candidate:
        sum_distance = 0
        for s in symptom_set:
            sum_distance += ctd.distance_measure(G, candidate, s)
        
        average = sum_distance / len(symptom_set)
        if average < min_average:
            min_average = average
            centroid_disease = candidate
    print("Centroid : ", centroid_disease, " : ", min_average)

randomsymptom()
