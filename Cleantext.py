import nltk
from nltk.corpus import words
import operator
import os
import glob
import chardet
import PreTextProcessing as pt
import Tokenization as tk
import inflect
p = inflect.engine()
Taglist = []
DiseaseName = []
def dir():
    path = "C:/Users/Kaow/Documents/Project/TMRS/Document/corpus221/"
    os.chdir(path)
    for file in glob.glob("*.txt"):
        print("file name: ", file)
        readline(file)

def readline(file):
    #Detect file encoding type of file

    rawdata = open(file, 'rb').read()
    FileCode = chardet.detect(rawdata)
    Encode = FileCode['encoding']
    
    c_file = open(file, 'r', encoding=Encode)
    file = open("C:/Users/Kaow/Documents/Project/TMRS/Document/corpus221/cleanword2/"+file,"w", encoding="utf-8")
    for c in c_file:
        cleantxt(c, file)
    file.close()     
    c_file.close()   

def cleantxt(line, cleanfile):
  
    word_list = tk.TokenizeMultiWord(line, Taglist)
    
    for word in word_list:
  
        if (not word.isnumeric() and len(word) > 1 and word in words.words()) or (word in DiseaseName):
            cleanfile.write(word)
            cleanfile.write(" ")
        else:
            if p.singular_noun(word):
                cleanfile.write(word)
                cleanfile.write(" ")


    cleanfile.write("\n") 
#Prepare keyword to matching with word in text file
def WordTags():
    global Taglist
    
    os.chdir("Document/corpus221/Wiki")
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
        DiseaseName.append(replaceu)
      
#WordTags()
#dir()