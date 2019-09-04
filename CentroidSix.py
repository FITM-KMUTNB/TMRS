import networkx as nx
import operator
import random
import os
import glob

Cooccs = None
nodes = dict()
words = []
centroid = ""
candidatesum = dict()
writetextline = ""

docfile = dict() # Keep word from document to dict {1:[w1,w2,w3,..], 2:[w1,w2,..] ,..}
fileindex = [] # For Randommixfile [ file1/file2, file1/file3, file1/file4, file2/file3 .... ]
def ReadG():
    global Cooccs
    print("Read Graph...")
    Cooccs = nx.read_gpickle("Database/Pickle/226pic.gpickle")
    print("Find High Frequency Range")
    #Findhighfrequency()
    listdoc()
    
def listdoc():
    global fileindex
    os.chdir("Document/4file/")
    docnum = 1
    for file in glob.glob("*.txt"):

        print(docnum, " file name: ", file)
        listline(file, docnum)
        fileindex.append(docnum)
        docnum += 1

    fileResult = open("Result/1million.txt", "w") 
    #Randomthesamefile(2, fileResult)
    #Randommix2file(2, fileResult)
    #Randomthesamefile(5, fileResult)
    #Randommix5file(fileResult)
    #Random3wordfrom4doc(fileResult)
    #RandomSecondword(fileResult)
    #Random5wordfromDB(fileResult)
    Random100(fileResult)
    fileResult.close()

def listline(fname, filenum):
    global docfile
    c_file = open(fname, 'r', encoding="latin-1")
    num = 1
    for line in c_file:
        #print(line)
        wordlist = line.split()
        #Put Word from text file to dictionary --> {1:[w1,w2,w3...], 2:[w1,w2..], ...}
        if num == 1:
            docfile[filenum] = wordlist
            num = 2
        else:
            docfile[filenum] += wordlist
def Random100(file):
    global writetextline
    listcentroid = {}
    query = []
    largest_component = max(nx.connected_components(Cooccs), key=len)
    node = list(largest_component)
    writetextline += "{"
    for r in range(100):
        while True:
            randword = random.randint(0, len(node)-1)
            inputnode = node[randword]
            if inputnode not in listcentroid:
                listcentroid[inputnode] = Cooccs.node[inputnode]['occur']
                writetextline += inputnode + ":"+str(listcentroid[inputnode])+ ", "
                query.append(inputnode)
                break
    print(len(listcentroid))

    Calcentroid(query, file)

# W1, Random(W2) : C | x 10
def RandomSecondword(file):
    global writetextline
    pair_list = []
    
    # Generate connected components and select the largest:
    largest_component = max(nx.connected_components(Cooccs), key=len)
    node = list(largest_component)
    if len(node) >= 2000:
        print("Node amount :: ", len(node))
    else:
        print("Node amount :: ", len(node), " Less than 2000 !!!")
        
    #Loop first word from 1-2000
    for word1 in range(2000):

        #Random second word pair with first word 10 time
        for r in range(10):
            while True:
                pair_word = []
                writetextline = ""
                randword = random.randint(0, len(node)-1)
                word2 = node[randword]
                pair_word = [node[word1], word2]
                rpair_word = [word2, node[word1]]

                #Check duplicate pair word in list
                if pair_word[0] != pair_word[1]:
                    if (pair_word not in pair_list) and (rpair_word not in pair_list):
                        try:
                            nx.dijkstra_path_length(Cooccs, pair_word[0], pair_word[1], weight='cost')
                            pair_list.append(pair_word)
                            writetextline += str(pair_word[0])+", "+str(pair_word[1])
                            Calcentroid(pair_word, file)
                            break
                        except nx.NetworkXNoPath:
                            print("No Link Random Word Again!!")
                            pass

# Random 5 word from DB -> W1, W2, W3, W4, W5:C
def Random5wordfromDB(file):
    global writetextline
    
    # Generate connected components and select the largest:
    largest_component = max(nx.connected_components(Cooccs), key=len)
    node = list(largest_component)
    print("Graph Node amount :: ", len(node))
    #Loop find centroid of 5 word 10,000 tuples
    for r in range(10000):
        query = []
        writetextline = ""
        while True:
            randword = random.randint(0, len(node)-1)
            word = node[randword]
            if word not in query:
                query.append(word)
                writetextline += word
                if len(query) != 5:
                    writetextline +=", "
            if len(query) == 5:
                break
                
                
        Calcentroid(query, file)
     
# Random Document -> D(R(W1)), D(R(W2)), D(R(W3)) : C
def Random3wordfrom4doc(file):
    global docfile
    global fileindex
    global writetextline
    
    for all in range(1000):
        lists3doc = []
        
        #Random file
        while len(lists3doc) != 3:
            randdoc = random.randint(0, len(fileindex)-1)
            docfilekey = fileindex[randdoc]
            if docfilekey not in lists3doc:
                lists3doc.append(docfilekey)

        #Random word in file
        while True:
            query = []
            writetextline = ""
            for doc in lists3doc:
                while True:
                    randword = random.randint(0, len(docfile[doc])-1)
                    word = docfile[doc][randword]
                    
                    if word not in query:
                        query.append(word)
                        writetextline += word
                        if len(query) != 3:
                            writetextline += ", "
                        break
            try:
                for q in range(len(query)):
                    for nq in range(q+1, len(query)):
                        nx.dijkstra_path_length(Cooccs, query[q], query[nq], weight='cost')
                
                Calcentroid(query, file)
                break
            except nx.NetworkXNoPath:
                print("No Link Random Word Again!!")
                pass
        print(query)

# D(R(W1)), ..... N: C
def Randomthesamefile(word_amount, file):
    global docfile
    global writetextline
    output = ""
    tuples = 0
        
    for f in docfile:
        for allword in range(250):
            while True:
                
                query = []
                writetextline = ""
                while len(query) != word_amount:
                    randword = random.randint(0, len(docfile[f])-1)
                    word = docfile[f][randword]
                    if word not in query:
                        query.append(word)
                        writetextline += word
                        if len(query) != word_amount:
                            writetextline += ", "
                # Check all word have link to each other
                try:
                    for i in range(len(query)):
                        for n in range(i+1, len(query)):
                            nx.dijkstra_path_length(Cooccs, query[i], query[n], weight='cost')
                    Calcentroid(query, file)
                    tuples += 1
                    break
                        
                except nx.NetworkXNoPath:
                    pass

    output = word_amount, " words -> ", tuples, " tuples"
    print(output)
    
# D1(R(W1)), D2(R(W2))... N : C
# D1(R(W1)), D3(R(W2))... N : C
def Randommix2file(word_amount, file):
    global fileindex
    global docfile
    global writetextline
    output = ""
    tuples = 0

    # First  file
    for f in range(len(fileindex)):
        # Next file
        for nf in range(f+1, len(fileindex)):
            #print("File :: ", fileindex[f], "|", fileindex[nf])

            # Do 200 time to random word from pair file 
            for allword in range(200):
                while True:
                    tuples += 1
                    query = []
                    writetextline = ""
                    while len(query) != word_amount:
                        randword1 = random.randint(0, len(docfile[fileindex[f]])-1)
                        word1 = docfile[fileindex[f]][randword1]
                        randword2 = random.randint(0, len(docfile[fileindex[nf]])-1)
                        word2 = docfile[fileindex[nf]][randword2]

                        if word1 != word2:
                            query.append(word1)
                            query.append(word2)
                            writetextline += word1 + ", " + word2

                    # Check two word have link to each other
                    try:
                        nx.dijkstra_path_length(Cooccs, query[0], query[1], weight='cost')
                        Calcentroid(query, file)
                        break
                        
                    except nx.NetworkXNoPath:
                        pass
                    

    output = word_amount, " words -> ", tuples, " tuples"
    print(output)

def Randommix5file(file):
    global fileindex
    global docfile
    global writetextline
    tuples = 0
    output = ""
    for r in range(500):
        while True:
            query = []
            writetextline = ""
            #Random word from each 1-4 file
        
            for d in docfile:
                word = ""

                while True:
                    randword = random.randint(0, len(docfile[d])-1)
                    word = docfile[d][randword]
                    if word not in query:
                        break
                query.append(word)
                writetextline += word + ", "

            #Random one in 4 file
            word = ""
            while True:
                randfile = random.randint(0, len(fileindex)-1)
                randword = random.randint(0, len(docfile[fileindex[randfile]])-1)
                word = docfile[fileindex[randfile]][randword]
                if word not in query:
                    break
            query.append(word)
            writetextline += word
            # Check all word have link to each other
            try:
                for i in range(len(query)):
                    for n in range(i+1, len(query)):
                        nx.dijkstra_path_length(Cooccs, query[i], query[n], weight='cost')
                Calcentroid(query, file)
                tuples += 1
                break
                        
            except nx.NetworkXNoPath:
                pass
            

    output = 5, " words -> ", 500, " tuples"
    print(output)

           
def Findhighfrequency():
    global Cooccs
    global nodes
    for n in Cooccs.nodes:
        occur = Cooccs.node[n]['occur']
        nodes[n] = occur
    
    descend = sorted(nodes.items(), key=operator.itemgetter(1), reverse=True)

    for n in range(0, 2000):
        words.append(descend[n][0])
    
    Randomsixword()

def Randomsixword():
    global words
    global writetextline
    r = 1
    file = open("Result.txt","w") 
    while r < 1000:
        query = []
        writetextline = ""
        while len(query) < 6:
            rand = random.randint(0, 1499)
            w = words[rand]
            if w not in query:
                query.append(w)
                writetextline += w+", "
        print(r, " : ", query)
        
        #file.write(str(r)+" : ""%s\n" % query +"\n") 
        Calcentroid(query, file)
        r += 1
    file.close() 

def Calcentroid(query, file):
    
    neighbor = dict()
    maxp = 0
    candidate = []
    global centroid
    global candidatesum
    global writetextline
    centroid = ""

    # Examine if keywords existing in db
    for q in query:
        if q in Cooccs:
            pass
        else:
            query.remove(q)

    # Find largest length between keywords
  
    for wp in range(len(query)):
        for wn in range(wp+1, len(query)):
            if wn > len(query):
                break
            try:
                cost = nx.dijkstra_path_length(Cooccs, query[wp], query[wn], weight='cost')
                if cost > maxp:
                    maxp = cost
            except nx.NetworkXNoPath:
                print("No Path Between :: ", query[wp], " and ", query[wn])
             
    arearadius = (maxp / 2.0) + 1
    
    round = 1
    
    # Find Related node within keywords radius
    while len(candidate) < 10:
        print("Activat round::", round)
        
        if round > 1:
            arearadius = arearadius + (arearadius/2)
            candidate = []
            neighbor = dict()
            candidatesum = dict()
        #print("Radius : ", arearadius)
    
        for q in query:
     
            rel_link = nx.single_source_dijkstra_path_length(Cooccs, q, weight = 'cost',cutoff=arearadius)

            for r in rel_link:
                
                if r != q:
                    if r in neighbor:
                        neighbor[r] += 1
                        candidatesum[r] += rel_link[r]
                    else:
                        neighbor[r] = 1
                        candidatesum[r] = rel_link[r]
     
        # Find node that related to all keywords (Candidate Centroid)
        
        for n in neighbor:
            if neighbor[n] == len(query):
                candidate.append(n)

        if round > 10 and len(candidate) > 0:
            break
        round += 1
        print("Cadidate : ", len(candidate))
    
    #Find node that have most minimun average distance. (Centroid)     
    Shortestaveragedistance(query, candidate)
    print("Centroid :: ", centroid)
    writetextline += "t : "+centroid+" }"
    file.write(str(writetextline)+"\n") 

#Find Average Distance --> Sum/N
def Shortestaveragedistance(query, candidate):
    global candidatesum
    global centroid
    minaverage = 1000
    for cd in candidate:
        average = candidatesum[cd] / len(query)
        if average < minaverage:
            minaverage = average
            centroid = cd

ReadG()