from neo4j import GraphDatabase
import sys
import os
import glob
import atexit
from time import time, strftime, localtime
from datetime import timedelta
import networkx as nx

MyBrain = dict() 
BrainLink = dict()
BrainLinkDice = dict()
BrainLinkCost = dict()
start = 0
#driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'tmrs_2019'))
wordbatch = []
relbatch = []

def main():
    
    print("===============================================")
    print("Thai Traditional Medical Recommendation System.")
    print("===============================================")
    choice = input("""

(T)he Co-Occurrence Graph
(E)xit
\n
Please Enter Your Choice :: """)

    if choice == "T" or choice == "t":
        start = time() 
        listfile("Document/corpus 226/")
        end = time()
        xtime = end - start
        print('Processing Time:', secondsToStr(xtime)) 
        #dbClose()
    
    elif choice == "E" or choice == "e":
        #dbClose()
        sys.exit
    

 # ======================================== Text Processing ==================================================== #
def listfile(path):
    
    os.chdir(path)
    doc_no = 1
    for DocName in glob.glob("*.txt"):
        print(doc_no," :: "+DocName)
        listsentence(DocName)
        doc_no+=1
    calcost()    
    creatgraphX()
    #addBatch()
    
    

def listsentence(fname):
    c_file = open(fname, 'r', encoding="latin-1")
    
    for sents in c_file:
        nline = sents.replace("|NN", "")
        pline = nline.replace("|NP", "")
        # process line
        processline(pline)
    
    
    
    c_file.close()


def processline(w_line):
    global MyBrain
    global BrainLink
    
    wordlists = w_line.split()
    # remove duplicate words
    wordlists = list(dict.fromkeys(wordlists))
    
    # count word frequencies
    for word in wordlists:
        if word in MyBrain.keys():
            MyBrain[word] += 1
        else:
            MyBrain[word] = 1
    # Count word_pairs frequencies
    for i in range(len(wordlists)):
        if i+1 == len(wordlists):
            break
        for j in range(i, len(wordlists)):
            if j+1 == len(wordlists):
                break
            if wordlists[i] == wordlists[j+1]:
                continue
            # create link pair with the less value word first
            if wordlists[i] < wordlists[j+1]:
                word_pair = wordlists[i]+'|' + wordlists[j+1]
            else:
                word_pair = wordlists[j+1]+'|' + wordlists[i]

            if word_pair in BrainLink:
                BrainLink[word_pair] += 1
            else:
                BrainLink[word_pair] = 1

    
        


# calculate Dice-coefficien using formular
# 2*co-occurences count / count of word a + count of word b
def caldice(wordlink, coocvalue):
    global MyBrain
    global BrainLink
    global BrainLinkDice
    
    wordlist = wordlink.split('|')
    countA = MyBrain[wordlist[0]]
    countB = MyBrain[wordlist[1]]
    countAB = coocvalue
 
    helpk = 0
    if countB <= countA:
        helpk = countB
    else:
        helpk = countA

    if countAB >= helpk:
        countAB = helpk
            
    dicevalue = (2*countAB)/(countA+countB)

    if dicevalue > 1:
        dicevalue = 1.0
    
    BrainLinkDice[wordlink] = dicevalue
    return dicevalue
    pass

# Calculate relationships Cost / Cost = 1/(Dice + 0.01)
def calcost():
    # Dice and Cost Calculation
    for wordpair in BrainLink:
        dice = caldice(wordpair, BrainLink[wordpair])
        cost = 1/(dice+0.01)
        BrainLinkCost[wordpair] = cost

# ======================================== NetworkX Graph ==================================================== #
def creatgraphX():
    
    G = nx.Graph()
       
    for word in MyBrain:
        G.add_node(word, occur=MyBrain[word])
       
    for word_pair in BrainLinkCost:
        words = word_pair.split('|')
        
        G.add_edge(words[0], words[1], count= BrainLink[word_pair], dice = BrainLinkDice[word_pair], cost= BrainLinkCost[word_pair])
    
    nx.write_gml(G, "CooccsDB.gml")    
    
    
 
# ======================================== Neo4j Graph ==================================================== #

 # createGraph ----> Create per Session
def creategraph():
    for word in MyBrain:
        createNode({'name': word, 'occur': MyBrain[word]})
    for word_pair in BrainLink:
        words = word_pair.split('|')
        createRelation(words[0], words[1], {
                       'count': BrainLink[word_pair], 'dice': 0.5})


def createNode(props):
    Label = 'SINGLE_NODE'
    with driver.session() as session:
        return session.run("CREATE (a:"+Label+" {props}) "
                           "RETURN id(a)",  {'props': props}).single().value()


def createRelation(n1, n2, props):
    Label = 'SINGLE_NODE'
    with driver.session() as session:
        return session.run("MATCH (a:"+Label+"),(b:"+Label+") WHERE a.name = {n1} AND b.name = {n2} "
                           "CREATE (a)-[rel:IS_CONNECTED {props}]->(b) RETURN rel",  {'n1': n1, 'n2': n2, 'props': props})

# createGraph ----> Unwind Batch
def addBatch():
    global wordbatch
    global relbatch
    # Add word from MyBrain(dic) to wordbatch(list) )
    print("Add Word...Batch")
    for word in MyBrain:
        wordbatch.append({"name":word, "occur":MyBrain[word]})
        if (len(wordbatch) % 50000) == 0:
            print("wordbatch size ", len(wordbatch), " Add to DB")
            createNodeGraph()
            wordbatch = []
    if len(wordbatch) > 0:
        createNodeGraph()

    print("Add relations...Batch")
    # Add relations from 
    for word_pair in BrainLink:
        words = word_pair.split('|')
        relbatch.append({"from":words[0], "to":words[1],"properties":{ "count":BrainLink[word_pair], "dice":0.5, "cost":0}})
        if(len(relbatch) % 50000) == 0:
            print("relbatch size ", len(relbatch), " Add to DB")
            createLinkGraph()
            relbatch = []
    if len(relbatch) > 0:
        createLinkGraph()

def createNodeGraph():
    
    with driver.session() as session:
        query = """
        UNWIND {{wordbatch}} as row
        CREATE (n:SINGLE_NODE)
        SET n += row
        """.format(wordbatch=wordbatch)
        result = session.run(query, wordbatch=wordbatch)
        if result:
            print("Add Node ... Done")
   
    
def createLinkGraph():

    with driver.session() as session:
        query = """
        UNWIND {{relbatch}} as row
        MATCH (from:SINGLE_NODE {{name:row.from}})
        MATCH (to:SINGLE_NODE {{name:row.to}})
        MERGE (from)-[rel:IS_CONNECTED]->(to)
        ON CREATE SET rel += row.properties
        """.format(relbatch=relbatch)
        result = session.run(query, relbatch=relbatch)
        if result:
            print("Add Relationship ... Done")

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))   

def dbClose():
    driver.close()



main()