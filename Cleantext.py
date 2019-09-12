import nltk
from nltk.corpus import words
import operator
import os
import glob
import chardet
import PreTextProcessing as pt
import Tokenization as tk
def dir():
    path = "C:/Users/Kaow/Documents/Project/TMRS/Document/corpus221/cleanword/ADHD.txt.txt.s_nouns_sentences_untagged.txt"
    #os.chdir(path)
    #for file in glob.glob("*.txt"):
        #print("file name: ", file)
    readline(path)

def readline(file):
    #Detect file encoding type of file
    rawdata = open(file, 'rb').read()
    FileCode = chardet.detect(rawdata)
    Encode = FileCode['encoding']
    
    c_file = open(file, 'r', encoding=Encode)
    file = open("C:/Users/Kaow/Documents/Project/TMRS/Document/corpus221/cleanword2/test.txt","w", encoding="utf-8")
    for c in c_file:
        cleantxt(c, file)
    file.close()     
    c_file.close()   

def cleantxt(line, cleanfile):
  
    #word_list = tk.TokenizeMultiWord(line, Taglist)
    word_list = line.split()
    for word in word_list:
        if not word.isnumeric() and len(word) > 1 and word in words.words():
            cleanfile.write(word)
        cleanfile.write(" ")
    cleanfile.write("\n") 
    

dir()