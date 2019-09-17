import glob
import chardet

path1 = "Document/corpus221/"

def _text_list():

    for file in glob.glob(path1+"*.txt"):
        print("file name: ", file)
        _word_list(file)

def _word_list(file):
    #Detect file encoding type of file
    rawdata = open(file, 'rb').read()
    FileCode = chardet.detect(rawdata)
    Encode = FileCode['encoding']
    c_file = open(file, 'r', encoding=Encode)
    
    for line in c_file:
        word = line.split()
        

_text_list()