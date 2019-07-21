import os
from natsort import natsorted
import nltk

path = "diseasesfulltextswiki/"
diseasedir = natsorted(os.listdir(path))

def CategorizeAndTaggingWord():
    for name in diseasedir:
        try:       
            with open(path+"/"+name, "r", encoding="latin-1") as f:
                text = nltk.word_tokenize(f.read())
                result = nltk.pos_tag(text)
                print(result)
                print("\n")
                print(name) 
            
        except IOError as exc:
            print("Error")
            if exc.errno != errno.EISDIR:
                raise
    

CategorizeAndTaggingWord()