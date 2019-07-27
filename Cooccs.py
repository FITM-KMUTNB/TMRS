import os
import sys
from natsort import natsorted #For retrieve list file from directory
import nltk #For Categorize And TaggingWord
from py2neo import Graph, Node, Relationship, NodeMatcher #Working with Neo4j


#Document Directory
path = "Document/Test/"
diseasedir = natsorted(os.listdir(path))
#Neo4j Database
print('Connect to database...', end="", flush=True)
graph = Graph(password = "tmrs_1234")
try:
    graph.run("Match () Return 1 Limit 1")
    print(' Success !')
except Exception:
    print(' Failed !')

matcher = NodeMatcher(graph)

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
    
    for name in diseasedir:
        print("-> Retrieve Document file")
        try:       
            with open(path+"/"+name, "r", encoding="latin-1") as f: # open txt file from directory and keep in f variable
                
                for text in f:
                    
                    VectorRow = []
                    sentence = nltk.word_tokenize(text) # Retrieve word from document per sentence
                    #print(text) # Retrieve word from document
                    
                    # Retrieve word from each sentence                
                    for word in sentence:
                        VectorRow.append(word)
                    # Store Sentence to list
                    SentenceVector.append(VectorRow)

                # Display Output
                """
                SentenceRow = 1
                for DisplaySV in SentenceVector:
                    print(SentenceRow, "::", DisplaySV)
                    SentenceRow += 1
                """
                print("Read text file [", name, "] ... Done") 
                
                CreateNodeAndRelation(SentenceVector)
        except IOError as exc:
            print("Error")
            if exc.errno != errno.EISDIR:
                raise
    main()

def CreateNodeAndRelation(SentenceVector):
    print("\n")
    print("-> Create Node And Relation")
    tx = graph.begin() 
    print("in transaction of database")    
    for Words in SentenceVector:
        # Seperate word|POS
        tempword = ""
        temppos = ""
        for word in Words:
            if "|" in word:
                tempword, temppos = word.split("|")
            else:
                tempword = word
            f_flag = 0
            # checking if the node is already present
            for record in matcher.match("SINGLE_NODE"):
                
                wordnode = record["name"]
                
                if wordnode == tempword:
                    occur = record["occur"]
                    occur += 1
                    record["occur"] = occur
                    tx.push(record)
                    f_flag = 1
                    print(wordnode, " node was already present. Count updated.")    
            
            if f_flag != 1:
                wordnode = Node("SINGLE_NODE", name=tempword, occur=1, pos=temppos) 
                tx.create(wordnode)
                print(wordnode, " node added.")  
          
            
    
    tx.commit()
    
    


if __name__ == "__main__":
    main()