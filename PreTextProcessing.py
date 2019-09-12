import os
import glob
import Tokenization as tk
import chardet
Taglist = [] #[[Disease1], [Disease2/1, Disease2/2], .... N ]
Node = dict() #{ W1 : occur, W2 : occur, W3 : occur, .... N }
Link = dict() #{ W1|W2 : count, W1|W3 : count, W2|W3 : count ... N}
LinkDice = dict() #{ W1|W2 : dict, W1|W3 : dict, W2|W3 : dict ... N}
LinkCost = dict() #{ W1|W2 : cost, W1|W3 : cost, W2|W3 : cost ... N}
DiseaseName = dict() #{Disease1 : doc, Disease2/1_Desease2/2 : doc}

dir_path = os.path.dirname(os.path.realpath(__file__))
path = dir_path+"/Document/corpus 221/cleanword/"

#List file in directory
def ListTextFile(path):
    print("List Text File In Directory")
    os.chdir(path)
    for file in glob.glob("*.txt"):
        ReadTextFile(file)
        print("file name: ", file)
 
#Read file 
def ReadTextFile(file):
    global Taglist
    #Detect file encoding type of file
    rawdata = open(file, 'rb').read()
    FileCode = chardet.detect(rawdata)
    Encode = FileCode['encoding']
    #Open and read
    Text_file = open(file, 'r', encoding=Encode, )      
    print("Read...")
    if Taglist:
        for line in Text_file:
                sentence = tk.TokenizeMultiWord(line, Taglist)
                WordCount(sentence)
                LinkCount(sentence)
    else:
        for line in Text_file:
                sentence = line.split()
                WordCount(sentence)
                LinkCount(sentence)

    print("Add Word And Link Done !")

#Add Word Frequency {W1 : occur, W2 : occur} 
def WordCount(sentence):
    global Node

    for word in sentence:
        if word in Node:
                Node[word] += 1
        else:
                Node[word] = 1     

#Add Word Frequency {W1|W2 : count, W1|W3 : count} 
def LinkCount(sentence):
    global Link

    for fw in range(len(sentence)):
        for nw in range(fw+1, len(sentence)):
            if sentence[fw] == sentence[nw]:
                continue
            #Sort the letters
            sort_word = sorted([sentence[fw], sentence[nw]])
            pair_word = sort_word[0] + "|" + sort_word[1]

            if pair_word in Link:
                Link[pair_word] += 1
            else:
                Link[pair_word] = 1
        
#Prepare keyword to matching with word in text file
def WordTags():
    global Taglist
    global DiseaseName
    os.chdir("Document/corpus 221/Wiki")
    print("Prepare Disease Name Tags.")
    for file in glob.glob("*.txt"): 
        #Detect file encoding type of file
        rawdata = open(file, 'rb').read()
        FileCode = chardet.detect(rawdata)
        Encode = FileCode['encoding']
        print(Encode)
        #For Check Disease Name In Sentence
        Text_file = open(file, 'r', encoding=Encode) 
        firstLine = Text_file.readline() # Read first line in each disease document to get disease name.
        removen = firstLine.replace("\n", "")
        DiseaseTag = removen.lower().split()
        Taglist.append(DiseaseTag)
        #For Tag Disease Node
        replaceu = removen.lower().replace(" ", "_")
        DiseaseName[replaceu] = file
    return Taglist

# calculate Dice-coefficien using formular
# 2*relations count / count of word a + count of word b
def CalDice(wordlink, countab):
    global LinkDice
    wordlist = wordlink.split('|')
    countA = Node[wordlist[0]]
    countB = Node[wordlist[1]]
    countAB = countab
 
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
    
    LinkDice[wordlink] = dicevalue
    return dicevalue
    
# Calculate relationships Cost / Cost = 1/(Dice + 0.01)
def CalLinkCost():
    # Dice and Cost Calculation
    for wordpair in Link:
        dice = CalDice(wordpair, Link[wordpair])
        cost = 1/(dice+0.01)
        LinkCost[wordpair] = cost

def GetPreGraph():
    WordTags()
    ListTextFile(path)
    CalLinkCost()

    return(Node, Link, LinkDice, LinkCost, DiseaseName)
