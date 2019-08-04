from neo4j import GraphDatabase
import sys
from natsort import natsorted #For retrieve list file from directory
import nltk #For Categorize And TaggingWord
import os
import atexit
from time import time, strftime, localtime
from datetime import timedelta

#Document Directory
path = "Document/test/"
diseasedir = natsorted(os.listdir(path))

#Neo4j-Driver
driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'tmrs_2019'))
session = driver.session()

# Check if connect to database
print('Connect to database...', end="", flush=True)
try:
    session.run("Match () Return 1 Limit 1")
    print(' Success !')
except Exception:
    print(' Failed !')


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
        dbClose()
        sys.exit

def CreateCoocurrenceGraph():
    start = time() 
    print("\n")
    print("-> Start Create Co-Occurrence Graph")
    print("-> Retrieve Document file")
    
    for DocName in diseasedir:
        
        try:       
            with open(path+"/"+DocName, "r", encoding="latin-1") as f: # open txt file from directory and keep in f variable
                Sline = 1
                AllSline = len(open(path+"/"+DocName).readlines())
                for text in f: # Read Document of each line(Sentence) --> Store in text
                    text = text.rstrip('\n')
                    sentence = text.split(" ") # Seperate word from each line and store in sentence valiable {w1,w2,w3}
                                      
                    # Sent Sentence to Database 
                    CreateNodeAndRelation(sentence, DocName, Sline, AllSline)
                    Sline +=1
                print("Read text file [", DocName, "] ... Done!!")    
                 
            
        except IOError as exc:
            print("Error")
            if exc.errno != errno.EISDIR:
                raise
    # Update Dice and Cost of relation edge
    UpdateDiceandCost()
    end = time()
    xtime = end - start
    print('Execute Time:', secondsToStr(xtime)) 
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

        # if node already present --> Update Count!!
        nodeID = matchNode(tempword)    
        if nodeID:
            occur = getProps(nodeID,'occur')
            occur +=1
            props = {'occur':occur}
            setNodProperty(nodeID, props)
            f_flag = 1
            print("[", DocName," [",Sline,"/",AllSline,"] \"", tempword, "\" node was already present. Count updated.") 
        # Create new node   
        if f_flag != 1:
            createNode({'name':tempword, 'occur':1, 'pos':temppos})
            print("[", DocName," [",Sline,"/",AllSline,"] \"", tempword, "\" node added.")  
    
        # Add relationship between node.
    for p in range(len(tempS)):
        
        for q in range(p+1, len(tempS)):
                        
            rel_found = False
            # Check if node the same node
            if not (tempS[p] == tempS[q]):
                
                rel_found = False
                
                #Get Node ID
                nodeid1 = matchNode(tempS[p])
                nodeid2 = matchNode(tempS[q])
                
                # If Relationship already exist --> Update Count!!
                relID = matchRelationship(nodeid1, nodeid2)
                if relID:
                    count = getProps(relID,'count')
                    count +=1
                    setRelProperty(relID, {'count':count})
                               
                    print("[", DocName," [",Sline,"/",AllSline,"] Relation already existed between nodes \"", tempS[p], "\" and \"", tempS[q], "\" Count updated.")
                    rel_found = True
                        
                # Create new relationship
                if not rel_found:
                    createRelation(nodeid1, nodeid2,{'count':1, 'dice':0, 'cost':0})
                    print("[", DocName," [",Sline,"/",AllSline,"] Relation inserted with nodes \"", tempS[p], "\" and \"", tempS[q],"\"")
                

def UpdateDiceandCost():
    print("Update Dice and Cost ... ", end="", flush=True)
    nodelist = hashNext()
    tempRel = []
    
    for node1 in nodelist:
        countA = getProps(node1, 'occur')
        for node2 in findRelation(node1):
            relAB = matchRelationship(node1, node2)

            if relAB not in tempRel:
                tempRel.append(relAB)
                countB = getProps(node2, 'occur')
                countAB = getProps(relAB, 'count')

                helpk = 0
                if countB <= countA:
                    helpk = countB
                else:
                    helpk = countA
                if countAB >= helpk:
                    countAB = helpk
            
                dice = (2*countAB)/(countA+countB)

                if dice > 1:
                    dice = 1.0

                setRelProperty(relAB, {'dice': dice})
                setRelProperty(relAB, {'cost': 1/(dice+0.01)})

    print('Done!!')
    
def createNode(props):
    Label = 'SINGLE_NODE'
    return session.run("CREATE (a:"+Label+" {props}) "
                       "RETURN id(a)",  {'props':props}).single().value()
def createRelation(n1,n2,props):
    Label = 'SINGLE_NODE'
    return session.run("MATCH (a:"+Label+"),(b:"+Label+") WHERE id(a) = {n1} AND id(b) = {n2} "
                       "CREATE (a)-[rel:IS_CONNECTED {props}]->(b) RETURN rel",  {'n1':n1,'n2':n2,'props':props}).single().value()       
def matchNode(name):
    Label = 'SINGLE_NODE'
    try:
        return session.run("MATCH (a:"+Label+") WHERE a.name= $name " 
                            "RETURN id(a)", name=name).single().value()
    except Exception:
        return None
    
def matchRelationship(n1,n2):
    Label = 'SINGLE_NODE'
    try:
        return session.run("MATCH (a:"+Label+")-[rel:IS_CONNECTED]-(b:"+Label+") WHERE id(a)= $n1 and id(b)= $n2 " 
                           "RETURN id(rel)", n1=n1,n2=n2).single().value()
    except Exception:
        return None
    
def getProps(id, props):
    try:
        return session.run("MATCH (a) WHERE id(a)= {id} " 
                           "RETURN a."+props+"", {'id':id}).single().value()
    except:
        return session.run("MATCH ()-[r]-() WHERE id(r)= {id} " 
                           "RETURN r."+props+"", {'id':id}).value()[0]

def setNodProperty(id, props):
    Label = 'SINGLE_NODE'
    session.run("MATCH (a) WHERE id(a)= {id} " 
                "SET a+= {props}", {'id':id, 'props':props})
def setRelProperty(id, props):
    session.run("MATCH ()-[r]-() WHERE id(r)= {id} " 
                "SET r+= {props}", {'id':id, 'props':props})
def hashNext():
    Label = 'SINGLE_NODE'
    return session.run("MATCH (n:"+Label+") " 
                       "RETURN id(n)").value()

def findRelation(start_node):
    Label = 'SINGLE_NODE'
    return session.run("MATCH (a:"+Label+")-[rel:IS_CONNECTED]-(b:"+Label+") WHERE id(a)= $start_node " 
                       "RETURN id(b)", start_node=start_node).value()

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))   

def dbClose():
    driver.close()



if __name__ == "__main__":
    main()