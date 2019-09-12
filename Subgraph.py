import networkx as nx
import glob
import os
import chardet

Cooccs = nx.read_gpickle("Database/Pickle/221clean.gpickle")
fileResult = open("Result Centroid/subgraph.txt", "w") 
dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path+"/Document/corpus 221/cleanword/"

Node = dict()
centroid = None

def document(fileResult):
    print("List Text File In Directory")
    os.chdir(path)
    for file in glob.glob("*.txt"):
        word(file)
        print("file name: ", file)
        Subgraphcentroid()
        output = file," - "+centroid
        print(output)
        fileResult.write(str(output)+"\n") 
        Node = dict()

def word(file):
    
    #Detect file encoding type of file
    rawdata = open(file, 'rb').read()
    FileCode = chardet.detect(rawdata)
    Encode = FileCode['encoding']
    #Open and read
    Text_file = open(file, 'r', encoding=Encode)      
    print("Read...")
    for line in Text_file:
        sentence = line.split()
        WordCount(sentence)

#Add Word Frequency {W1 : occur, W2 : occur} 
def WordCount(sentence):
    global Node

    for word in sentence:
        if word in Node:
                Node[word] += 1
        else:
                Node[word] = 1    

def Subgraphcentroid():
    global centroid
    nbunch = set()
    
    for n in Node:
        nbunch.add(n)
    
    subg = nx.subgraph(Cooccs, nbunch)
    print(len(subg))

    final_avg = 999999999.99
    word_allSP = dict(nx.shortest_path_length(subg, weight='cost'))
    for key in word_allSP:
        avg_nodeSP = sum(word_allSP[key].values())/(len(word_allSP[key]))
        if final_avg > avg_nodeSP:
            final_avg = avg_nodeSP
            centroid = key


def Centroid():
    global centroid
    minaveragedistance = 999999999.99
    print(len(Node))
    for n in Node:
        sumdistance = 0
        distance = nx.single_source_dijkstra_path_length(Cooccs, n, weight='cost')

        for target in distance:
            if target in Node:
                sumdistance += distance[target]
        average = sumdistance/len(Node)
        if average < minaveragedistance:
            minaveragedistance = average
            centroid = n


document(fileResult)