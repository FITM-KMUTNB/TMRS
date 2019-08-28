import nltk
from nltk.corpus import words
import operator
import os
import glob

def dir():
    path = "Document/4file/"
    os.chdir(path)
    for file in glob.glob("*.txt"):
        print("file name: ", file)
        readline(file)

def readline(file):
    
    c_file = open(file, 'r', encoding="latin-1")
    file = open("cleanword/"+ file,"w")
    for c in c_file:
        cleantxt(c, file)
    file.close()     
    c_file.close()   

def cleantxt(line, cleanfile):
    text = []
    word_list = line.split()
    word_list = list(dict.fromkeys(word_list))
    for word in word_list:
        if word in words.words() and len(word) > 1:
                cleanfile.write(word)
        cleanfile.write(" ")
    cleanfile.write("\n") 
    

dir()