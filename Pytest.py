"""
import operator
c_file = open("Result1000(2).txt", 'r', encoding="latin-1")
file = open("Result1000(3).txt","w") 

for c in c_file: 
        text = c.translate(str.maketrans({"'":None}))
        #print(text)     
        text2 = text.split(":") 
        print(text2[1])    
        file.write(text2[1]) 
               
        
file.close() 

c_file.close()
"""
import Tokenization as tk
import chardet   

rawdata = open("Document/corpus 226/Lesch–NyhanSyndrome.txt.txt.s_nouns_sentences_untagged.txt", 'rb').read()
result = chardet.detect(rawdata)

print(result['encoding'])