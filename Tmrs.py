import networkx as nx
import Library as ct
import operator
import glob
import chardet
import os


def disease(G, keywords):
    # Return disease proximity to keywords

    return disease_hop_activate(G, keywords)

def disease_hop_activate(G, keywords):
    activate_list = []
    candidate = dict()
    disease = dict()
    current_hop = 0
    node_count = dict()
    node_distance = []
    sum_distance = dict()

    for key in keywords:
        activate_list.append([key])
        node_distance.append({key : 0})
               
    while len(disease) <= 10:
        for circle in range(len(activate_list)):
            activate_node = activate_list[circle][current_hop]
            
            for neighbors in nx.neighbors(G, activate_node):
                if neighbors in keywords:
                    continue

                # distance from initial point.
                if neighbors not in node_distance[circle]:
                    
                    node_distance[circle][neighbors] = node_distance[circle][activate_node] + G[activate_node][neighbors]['cost']

                    # sum distance to all keywords.
                    if neighbors in sum_distance:
                        sum_distance[neighbors] += node_distance[circle][neighbors]
                    else:
                        sum_distance[neighbors] = node_distance[circle][neighbors]
                
                # check intersect
                if neighbors in node_count:

                    if neighbors not in activate_list[circle]:
                        activate_list[circle].append(neighbors)
                        node_count[neighbors] += 1
                    
                    # if found node intersect, calculate average distance.
                    if node_count[neighbors] == len(keywords):
                        candidate[neighbors] = sum_distance[neighbors] / len(keywords)
                        if G.node[neighbors]['tag'] == 'DS':
                            disease[neighbors] = sum_distance[neighbors] / len(keywords)
            
                else:
                    activate_list[circle].append(neighbors)
                    node_count[neighbors] = 1
                     

        current_hop += 1
    
    return dict(sorted(disease.items(), key=operator.itemgetter(1))), dict(sorted(candidate.items(), key=operator.itemgetter(1)))    

def disease_by_hop(G, keywords):
    disease = dict()
    diseasehop = dict()
    centroid, hop = ct.centroid_by_hop(G, keywords)

    for word in centroid:
        try:
            if G.node[word]['tag'] == 'DS' or G.node[word]['tag'] == 'DT':

                disease[word] = centroid[word]
                diseasehop[word] = format(hop[word]/len(keywords), '.2f')
        except:
            pass
    allcentroid = dict(
        sorted(centroid.items(), key=operator.itemgetter(1))[:50])
    return(disease, allcentroid, diseasehop)


def disease_by_distance(G, keywords):
    disease = dict()
    centroid = ct.centroid_by_distance(G, keywords)

    for word in centroid:
        try:
            if G.node[word]['tag'] == 'DS' or G.node[word]['tag'] == 'DT':
                disease[word] = centroid[word]
        except:
            pass
    allcentroid = dict(
        sorted(centroid.items(), key=operator.itemgetter(1))[:50])
    return(disease, allcentroid)


def disease_document(G, disease):
    document = dict()
    # Get document name.
    for word in disease:
        try:
            document[word] = G.node[word]['document']
        except:
            pass
    return document


def disease_neighbors_old(G, centroid, hop=1):

    neighbors = ct.centroid_neighbors(G, centroid, hop)
    node_no = dict()
    node = []
    node_link = []
    path_list = []
    number = 0
    
    # Set node number.
    for n in neighbors:
        temp_path = []

        for p in neighbors[n]:
            node_name = dict()
            try:
                if G.node[p]['tag'] == 'ST' or p == centroid or G.node[p]['tag'] == 'DS':
                    if p not in node_no:
                        node_no[p] = number
                        node_name['name'] = p
                        node.append(node_name)
                        
                        number += 1
                    temp_path.append(p)
            except:
                pass

        if len(temp_path) > 1 and temp_path not in path_list:
            path_list.append(temp_path)
    
    # Set pair_node list by node using number.
    for path in path_list:
        for link in range(len(path)):
            source_target = dict()
            if link+1 < len(path):
                source_target["source"] = node_no[path[link]]
                source_target["target"] = node_no[path[link+1]]
                node_link.append(source_target)

    return(node, node_link)

def disease_neighbors(G, centroid):
    neighbors, neighbors_dis = ct.centroid_neighbors(G, centroid)
    disease_dis = dict()
    path_list = []
    hop_distance = dict()
    node_tag = dict()
    for p in neighbors:
        temp_path = []
        hop = 0
        try:
            if G.node[p]['tag'] == 'ST' or G.node[p]['tag'] == 'DS':
                for n in neighbors[p]:
                    hop += 1
                    temp_path.append(n)
                    if n not in node_tag:
                        node_tag[n] = G.node[n]['tag']
                    if G.node[p]['tag'] == 'ST' or G.node[p]['tag'] == 'DS':
                        disease_dis[n] = neighbors_dis[n]
                    if n not in hop_distance:
                        hop_distance[n] = hop - 1 # not count centroid. path ['centroid', 'neighbors']
                    
                if len(temp_path) > 1 and temp_path not in path_list:
                    path_list.append(temp_path)
        except:
            pass
    return(path_list, hop_distance, node_tag, dict(sorted(disease_dis.items(), key=operator.itemgetter(1))))

def disease_related(G, centroid):

    distance = nx.single_source_dijkstra_path_length(G, centroid, weight='cost')
    path = nx.single_source_dijkstra_path(G, centroid, weight='cost')
    hop = dict()
  
    for p in path:
        
        if p == centroid:
            continue
        
        hop[p] = len(path[p]) - 1 
    
    return(distance, path, hop)

def get_all_graph(G):
    node = []
    node_link = []
    node_no = dict()
    number = 0
    
    for n in G.nodes:
        node_name = dict()
        node_name['name'] = n
        node_no[n] = number
        number += 1
        node.append(node_name)
        if number == 1000:
            break

    for e in G.edges:
        if e[0] not in node_no or e[1] not in node_no:
            continue
        pair_word = dict()
        pair_word['source'] = node_no[e[0]]
        pair_word['target'] = node_no[e[1]]
        node_link.append(pair_word)
    return(node, node_link)

def _get_disease_name():
    readpath = "Document/corpus221/Wiki/"
    textoutput = open("Document/corpus221/Tag/diseaselist.txt",
                      "w", encoding='utf-8')
    for file in glob.glob(readpath+"*.txt"):

        print("file : ", file)
        # Detect file encoding type of file
        rawdata = open(file, 'rb').read()
        FileCode = chardet.detect(rawdata)
        Encode = FileCode['encoding']

        Text_file = open(file, 'r', encoding=Encode)
        firstLine = Text_file.readline()
        textoutput.write(str(firstLine))
    textoutput.close()


def disease_text_tokenization():
    text_disease_dir = "Document/corpus221/Tag/diseaselist.txt"
    text_disease_list = open(text_disease_dir, 'r', encoding="utf-8")
    disease_symptom = []

    # Disease list -> [['acne'], ['yellow', 'ferver'], ...]
    for disease in text_disease_list:
        disease_name = disease.lower().split()
        if disease_name not in disease_symptom:
            disease_symptom.append(disease_name)

    text_symptom_dir = "Document/corpus221/Tag/symptomlist.txt"
    text_symptom_list = open(text_symptom_dir, 'r', encoding="utf-8")

    # Symptom list -> [['fever'], ['back', 'pain'], ...]
    for symptom in text_symptom_list:
        symptom_name = symptom.lower().split()
        if symptom_name not in disease_symptom:
            disease_symptom.append(symptom_name)

    # Text tokenization
    input_text_dir = "Document/corpus221/cleanword/"
    os.chdir(input_text_dir)
    for file in glob.glob("*.txt"):
        output_text_dir = "../cleantag/"+file
        ct.text_tokenized(file, output_text_dir, disease_symptom)


def disease_text_tag():
    text_disease_dir = "Document/corpus221/Tag/diseaselist.txt"
    text_disease_list = open(text_disease_dir, 'r', encoding="utf-8")
    disease_tag = []

    # Disease list -> [['acne'], ['yellow_ferver'], ...]
    for disease in text_disease_list:
        disease_name = disease.lower().replace("\n", "")
        disease_name = disease_name.replace(" ", "_")
        if disease_name not in disease_tag:
            disease_tag.append(disease_name)

    text_symptom_dir = "Document/corpus221/Tag/symptomlist.txt"
    text_symptom_list = open(text_symptom_dir, 'r', encoding="utf-8")
    symptom_tag = []

    # Symptom list -> [['fever'], ['back_pain'], ...]
    for symptom in text_symptom_list:
        symptom_name = symptom.lower().replace("\n", "")
        symptom_name = symptom_name.replace(" ", "_")

        if symptom_name not in symptom_tag:
            symptom_tag.append(symptom_name)

    tag_dict = {'DS': disease_tag, 'ST': symptom_tag, 'DT': ('DS', 'ST')}
    # Text tagged
    input_text_dir = "Document/corpus221/cleanword/"
    os.chdir(input_text_dir)
    for file in glob.glob("*.txt"):
        output_text_dir = "../cleantag/"+file
        ct.word_tagged(file, output_text_dir, tag_dict, default="NN")


def create_tmrs_graph():
    input_text_dir = "Document/corpus221/cleantag/"
    g_file = "Database/Pickle/221tag.gpickle"
    ct.create_graph(input_text_dir, g_file)


def tmrs_graph_add_document_attr():
    text_disease_dir = "Document/corpus221/Wiki/"
    disease_doc = dict()

    os.chdir(text_disease_dir)
    for file in glob.glob("*.txt"):
        # Detect file encoding type of file
        rawdata = open(file, 'rb').read()
        FileCode = chardet.detect(rawdata)
        Encode = FileCode['encoding']
        print(Encode)
        # For Check Disease Name In Sentence
        Text_file = open(file, 'r', encoding=Encode)

        disease_name = Text_file.readline()
        disease_name = disease_name.lower().replace("\n", "")
        disease_name = disease_name.replace(" ", "_")
        if disease_name not in disease_doc:
            disease_doc[disease_name] = file
    print(disease_doc)
    os.chdir('../../..')
    G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
    for node in G.nodes:
        if node in disease_doc:
            print(node)
            nx.set_node_attributes(G, {node: {'document': disease_doc[node]}})

    nx.write_gpickle(G, "Database/Pickle/221tag.gpickle")

def tmrs_graph_clustering():
    G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
    print(nx.info(G))
    ct.graph_cluster(G)
"""
G = nx.read_gpickle("Database/Pickle/221tag.gpickle")
keywords = ['skin', 'headache', 'itch']
disease, centroid = disease_hop_activate(G, keywords)
"""