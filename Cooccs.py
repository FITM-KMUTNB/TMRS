import os
import sys
from natsort import natsorted #For retrieve list file from directory
import nltk #For Categorize And TaggingWord
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher #Working with Neo4j


#Document Directory
path = "Document/output_allWords_/"
diseasedir = natsorted(os.listdir(path))
#Neo4j Database
print('Connect to database...', end="", flush=True)
graph = Graph(password = "tmrs_2019")
try:
    graph.run("Match () Return 1 Limit 1")
    print(' Success !')
except Exception:
    print(' Failed !')

matcher = NodeMatcher(graph)
relmatcher = RelationshipMatcher(graph)

#Main menu
def main():
    
    print("===============================================")
    print("Thai Traditional Medical Recommendation System.")
    print("===============================================")
    choice = input("""
(C)ategorize And Tagging Word
(T)he Co-Occurrence Graph
(E)xit
\n
Please Enter Your Choice :: """)

    if choice == "C" or choice == "c":
        CategorizeAndTaggingWord()
    elif choice == "T" or choice == "t":
        CreateCoocurrenceGraph()
    elif choice == "E" or choice == "e":
        sys.exit

def CategorizeAndTaggingWord():
    for name in diseasedir:
        try:       
            with open(path+"/"+name, "r", encoding="latin-1") as f: # open txt file from directory and keep in f variable
                text = nltk.word_tokenize(f.read()) # Retrieve word from document
                result = nltk.pos_tag(text) # Tagging word Pos
                print(result)
                print("\n")
                print(name) 
            
        except IOError as exc:
            print("Error")
            if exc.errno != errno.EISDIR:
                raise
    main()

def CreateCoocurrenceGraph():
    print("\n")
    print("-> Start Create Co-Occurrence Graph")
    SentenceVector = []
    
    for DocName in diseasedir:
        print("-> Retrieve Document file")
        try:       
            with open(path+"/"+DocName, "r", encoding="latin-1") as f: # open txt file from directory and keep in f variable
                Sline = 1
                AllSline = len(open(path+"/"+DocName).readlines())
                for text in f: # Read Document of each line(Sentence) --> Store in text
                    
                    VectorRow = []
                    sentence = text.split(" ") # Seperate word from each line and store in sentence valiable {w1,w2,w3}
                                       
                    
                    # Retrieve word from each sentence               
                    for word in sentence:
                        VectorRow.append(word) # Words form each sentence store to VectorRow[] {Word|POS}
                    
                    # Sent Sentence to Database 
                    CreateNodeAndRelation(VectorRow, DocName, Sline, AllSline)
                    Sline +=1
                    

                print("Read text file [", DocName, "] ... Done\n") 
                
                
        except IOError as exc:
            print("Error")
            if exc.errno != errno.EISDIR:
                raise
    main()

def CreateNodeAndRelation(SentenceVector, DocName, Sline, AllSline):
        
    tempS = []
    # Seperate word|POS
    tempword = ""
    temppos = ""
    for word in SentenceVector:
        if "|" in word:
            tempword, temppos = word.split("|")
        else:
            tempword = word
            temppos = None
        f_flag = 0
        tempS.append(tempword)
        # checking if the node is already present
        for record in matcher.match("SINGLE_NODE"):
               
            wordnode = record["name"]
            # if node already present --> Update Count!!    
            if wordnode == tempword:
                occur = record["occur"]
                occur += 1
                record["occur"] = occur
                tx = graph.begin() 
                tx.push(record)
                tx.commit()
                f_flag = 1
                print("[", DocName," [",Sline,"/",AllSline,"] \"", tempword, "\" node was already present. Count updated.")    
        # Create new node   
        if f_flag != 1:
            if temppos != None:
                wordnode = Node("SINGLE_NODE", name=tempword, occur=1, pos=temppos) 
                tx = graph.begin() 
                tx.create(wordnode)
                tx.commit()
                print("[", DocName," [",Sline,"/",AllSline,"] \"", tempword, "\" node added.")  
            else:
                wordnode = Node("SINGLE_NODE", name=tempword, occur=1) 
                tx = graph.begin() 
                tx.create(wordnode)
                tx.commit()
                print("[", DocName," [",Sline,"/",AllSline,"] \"", tempword, "\" node added.")  

      

    # Add relationship between node.
    for p in range(len(tempS)):
        
        for q in range(p+1, len(tempS)):
                        
            rel_found = False
            # Check if node the same node
            if not (tempS[p] == tempS[q]):
                rel_found = False
                
                #Get Node ID
                nodeid1 = 0
                for nid in graph.run("match (n:SINGLE_NODE {name: '"+tempS[p]+"'}) return id(n) as NODEID"):
                     nodeid1 = nid["NODEID"]
                     
                nodeid2 = 0
                for nid in graph.run("match (n:SINGLE_NODE {name: '"+tempS[q]+"'}) return id(n) as NODEID"):
                    nodeid2 = nid["NODEID"]
                
                n1 = graph.nodes[nodeid1]
                n2 = graph.nodes[nodeid2]
                
                # If Relationship already exist --> Update Count!!
                if relmatcher.match(nodes=(n1, n2), r_type="IS_CONNECTED"):
                    for rel in relmatcher.match(nodes=(n1, n2), r_type="IS_CONNECTED"):
                        count = rel["count"]
                        count += 1
                        rel["count"] = count
                        tx = graph.begin()
                        tx.push(rel)
                        tx.commit()
                        print("[", DocName," [",Sline,"/",AllSline,"] Relation already existed between nodes \"", tempS[p], "\" and \"", tempS[q], "\" Count updated.")
                    rel_found = True

                if relmatcher.match(nodes=(n2, n1), r_type="IS_CONNECTED"):
                    for rel in relmatcher.match(nodes=(n2, n1), r_type="IS_CONNECTED"):
                        count = rel["count"]
                        count += 1
                        rel["count"] = count
                        tx = graph.begin()
                        tx.push(rel)
                        tx.commit()
                        print("[", DocName," [",Sline,"/",AllSline,"] Relation already existed between nodes \"", tempS[p], "\" and \"", tempS[q], "\" Count updated.")
                    rel_found = True
                        
                # Create new relationship
                if not rel_found:
                    n1id = 0
                    n2id = 0
                    for nid in graph.run("match (n:SINGLE_NODE {name: '"+tempS[p]+"'}) return id(n) as NODEID"):
                        n1id = nid["NODEID"]
                        
                    for nid in graph.run("match (n:SINGLE_NODE {name: '"+tempS[q]+"'}) return id(n) as NODEID"):
                        n2id = nid["NODEID"]
                        
                    n1 = graph.nodes[n1id]
                    n2 = graph.nodes[n2id]
                    relationship = Relationship(n1, "IS_CONNECTED", n2, count=1, dice=0, cost=0)
                    tx = graph.begin()
                    tx.create(relationship)
                    tx.commit()
                    print("[", DocName," [",Sline,"/",AllSline,"] Relation inserted with nodes \"", tempS[p], "\" and \"", tempS[q],"\"")
                    


    
if __name__ == "__main__":
    main()