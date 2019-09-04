import networkx as nx
import os
import glob
from fuzzywuzzy import fuzz

path = "Document/corpus 226/Tag"


def listfile(path):
    
    os.chdir(path)
    doc_no = 1
    for DocName in glob.glob("*.txt"):
        print(doc_no," :: "+DocName)
        listsentence(DocName)
        doc_no+=1
     
    

def listsentence(fname):
    c_file = open(fname, 'r', encoding="latin-1")
    diseasep = dict()
    for sents in c_file:
        nline = sents.replace("{", "")
        pline = nline.replace("}", "")
        pline = pline.rstrip('\n')
        words = pline.split(",")
        for d in words:
            n, s = d.split("=")
            diseasep[n.lower()] = s
        
    print(diseasep)    
    diseasetag(diseasep)
    c_file.close()

def diseasetag(dtag):
    Cooccs = nx.read_gml("C:/Users/Kaow/Documents/Project/TMRS/GML/226.gml")
    num = 0
    for n in Cooccs.nodes:
        for t in dtag:
            ratio = fuzz.ratio(n.lower(), t.lower())
            if ratio > 90:
                print("Node : ", n, " ,Tag : ", t , "| Matching ratio :: ", ratio)
                nx.set_node_attributes(Cooccs, {n: {'disease' : dtag[t]}})
                num += 1
    nx.write_gml(Cooccs, "C:/Users/Kaow/Documents/Project/TMRS/GML/226.gml")
    print("Node :: ", num," Tag")

listfile(path)
    