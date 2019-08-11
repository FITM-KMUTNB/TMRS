# This program uses the for loop to read
# all of the .txt file.
# MyBrain = {'man': 3, 'woman': 4, 'year': 1, 'baby': 2}
# BrainLink = {'man-woman': 3, 'man-baby': 1, 'man-year': 1}
import glob
import os
import datetime
from neo4j import GraphDatabase  # pip install neo4j

MyBrain = dict()
BrainLink = dict()
BrainLinkDice = dict()
xcount = 0
ycount = 0

# Main function process file in directoty


# Neo4j-Driver --> connect via bolt protocol
driver = GraphDatabase.driver(
    'bolt://localhost:7687', auth=('neo4j', 'tmrs_2019'))
session = driver.session()



def main():
    listfile("Document/test/")
    print("="*20, 'Summaries', "="*20)
   # print(MyBrain)
   # print(BrainLink)
    print("="*20, 'Summaries', "="*20)
    print("The size of is", MyBrain.__sizeof__(),
          'with :', len(MyBrain), 'words')
    print("The size of is", BrainLink.__sizeof__(),
          'with :', len(BrainLink), 'links')
    print('Top keyword is ', max(MyBrain, key=MyBrain.get),
          'with the value ', max(MyBrain.values()))
    print('Top keyword is ', max(BrainLink, key=BrainLink.get),
          'with the value ', max(BrainLink.values()))
    
    print(xcount)
    print(ycount)

    now = datetime.datetime.now()
    print("Current date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S"))

    creategraph()

    #now = datetime.datetime.now()
    #print("Current date and time : ")
    #print(now.strftime("%Y-%m-%d %H:%M:%S"))
    driver.close()


# List all the text file in the directory
def listfile(fstr):
    os.chdir(fstr)
    numfile = 0
    for file in glob.glob("*.txt"):
        print("file name: ", file)
        listline(file)
        numfile += 1
        print("-"*20, numfile, "-"*20)
    print(BrainLink)

# Open each file and process line by line
def listline(fname):

    c_file = open(fname, 'r', encoding="latin-1")
    # Read all the lines from the file.
    for line in c_file:
        # remove |NN and |NP
        #print(line)
        nline = line.replace("|NN", "")
        pline = nline.replace("|NP", "")
        # process line
        processline(pline)

    c_file.close()
    

# Processing line
def processline(w_line):
    global MyBrain
    global BrainLink
    #global xcount
    #global ycount
    wordlists = w_line.split()
    # remove duplicate words
    wordlists = list(dict.fromkeys(wordlists))
    # count specific words
    #xcount += wordlists.count('disease')
    #ycount += wordlists.count('lyme')
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
    dicevalue = 2*coocvalue / MyBrain[wordlist[0]] + MyBrain[wordlist[1]]
    return dicevalue
    pass


# Neo4j - Create graph database

def creategraph():
    for word in MyBrain:
        createNode({'name': word, 'occur': MyBrain[word]})
    for word_pair in BrainLink:
        words = word_pair.split('|')
        createRelation(words[0], words[1], {
                       'count': BrainLink[word_pair], 'dice': 0.5})


def createNode(props):
    Label = 'SINGLE_NODE'
    return session.run("CREATE (a:"+Label+" {props}) "
                       "RETURN id(a)",  {'props': props}).single().value()


def createRelation(n1, n2, props):
    Label = 'SINGLE_NODE'
    return session.run("MATCH (a:"+Label+"),(b:"+Label+") WHERE a.name = {n1} AND b.name = {n2} "
                       "CREATE (a)-[rel:IS_CONNECTED {props}]->(b) RETURN rel",  {'n1': n1, 'n2': n2, 'props': props})


# Call the main function.
main()
