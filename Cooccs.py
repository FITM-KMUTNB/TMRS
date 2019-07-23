import os
from natsort import natsorted
import nltk
import sys

path = "diseasesfulltextswiki/"
diseasedir = natsorted(os.listdir(path))

def main():
    print("===============================================")
    print("Thai Traditional Medical Recommendation System.")
    print("===============================================")
    choice = input("""
    (C) ategorize And Tagging Word
    (E) xit
    Please Enter Your Choice :: """)

    if choice == "C" or choice == "c":
        CategorizeAndTaggingWord()
    elif choice == "E" or choice == "e":
        sys.exit

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
    main()

if __name__ == "__main__":
    main()