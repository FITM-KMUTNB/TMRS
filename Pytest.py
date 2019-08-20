import os
import glob
from fuzzywuzzy import fuzz

path = "Document/corpus 226/Tag"

a = fuzz.ratio("new y YANKEES".lower(), "NEW YORK YANKEES".lower())
print(a)

def listfile(path):
    
    os.chdir(path)
    doc_no = 1
    for DocName in glob.glob("*.txt"):
        print(doc_no," :: "+DocName)
        listsentence(DocName)
        doc_no+=1
     
    

def listsentence(fname):
    c_file = open(fname, 'r', encoding="latin-1")
    disease = {}
    for sents in c_file:
        nline = sents.replace("{", "")
        pline = nline.replace("}", "")
        pline = pline.rstrip('\n')
        words = pline.split(",")
        for d in words:
            n, s = d.split("=")
            disease[n.lower()] = s
        
    #print(disease)    
    
    c_file.close()

listfile(path)
    