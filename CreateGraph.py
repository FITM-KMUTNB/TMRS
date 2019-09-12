import networkx as nx
import PreTextProcessing as pt

Node, Link, LinkDice, LinkCost, DiseaseName = pt.GetPreGraph()
Tags = 0

def CreatGraphX():
    global Tags
    G = nx.Graph()
    wordlist = []
    for word in Node:
        G.add_node(word, occur=Node[word])
        
        if word in DiseaseName:
            wordlist.append(word)
            nx.set_node_attributes(G, {word: {'disease' : 1, 'document' : DiseaseName[word]}})
            Tags += 1
       
    for word_pair in LinkCost:
        words = word_pair.split('|')
        G.add_edge(words[0], words[1], count= Link[word_pair], dice = LinkDice[word_pair], cost= LinkCost[word_pair])
    
    print(nx.info(G))
    #print(sorted(wordlist))
    nx.write_gpickle(G, "C:/Users/Kaow/Documents/Project/TMRS/Database/Pickle/221clean.gpickle")  
  
CreatGraphX()
print("Tags ", Tags)



