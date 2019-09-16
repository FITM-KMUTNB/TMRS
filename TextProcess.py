import glob
import chardet
import nltk

def word_tagged(inputtext, outputtext, tag, default=None):
    """ Specify word type by tag.

    Parameter
    ---------
    inputtext : String, file name or path of text file.
    outputtext : String, file name or path of output text file.
    tag : dict, key is a tag name, value is a word list of tag key.
    default : String, for default tagged, if default is none, 
            empty tagged for word that not in any tag list. 

    Returns
    --------
    textresult : Text file encode with UTF-8
            With words tagged.
    
    Examples
    ---------
    >>> inputtext = "inputtext.txt"
    >>> outputtext = "outputtext.txt"
    >>> tag = "{'DS' : ['fever', 'acne', 'migrain'], 'ST' : ['itch', 'fever','cough'], 'DT' : ['DS', 'ST']}"
    >>> word_tagged(inputtext, outputtext, tag, default = "|NN")

    fever|DT acne|DS migrain|DS itch|ST cough|ST germany|NN 

    """
    inputtext = open(inputtext, 'r', encoding=_encode_type(inputtext))
    fileResult = open(outputtext, "w", encoding="utf-8")

    if default != None:
        for sentence in inputtext:
            sentence = sentence.split()
            for word in sentence:
                taglabel = ""
       
                for t in tag:
                    if type(tag[t]) is not tuple:
                        if word in tag[t]:
                            taglabel = "|" + t
                    else:
                        inalltag = True
                        for tp in tag[t]:
                            if word not in tag[tp]:
                                inalltag = False
                           
                        if inalltag:
                            taglabel = "|" + t

                if taglabel == "":
                    taglabel = "|" + default

                
                word = word + taglabel
                fileResult.write(word)
                fileResult.write(" ")
            fileResult.write("\n")

    if default == None:
        for sentence in inputtext:
            sentence = sentence.split()
            for word in sentence:
                taglabel = ""
                for t in tag:
                    if type(tag[t]) is not tuple:
                        if word in tag[t]:
                            taglabel = "|" + t
                    else:
                        inalltag = False
                        for tp in tag[t]:
                            if word in tag[tp]:
                                inalltag = True
                            else:
                                inalltag = False
                        if inalltag:
                            taglabel = "|"+tag[t]

                word = word + taglabel
                fileResult.write(word)
                fileResult.write(" ")
            fileResult.write("\n")

    inputtext.close()
    fileResult.close()

def text_tokenized(inputtext, outputtext, wordlist):
    """ Tokenization text file.

    Parameter
    ---------
    inputtext : String, file name or path of text file.
    outputtext : String, file name or path of output text file.
    wordlist : list, contain word list for do word tokenization.

    Returns
    --------
    textresult : Text file encode with UTF-8
            With complete tokenization of words.

    Examples
    ---------
    >>> inputtext = "inputtext.txt"
    >>> outputtext = "outputtext.txt"
    >>> wordlist = "[["mercedes", "benz"], ["super", "car"]]"
    >>> text_tokenized(inputtext, outputtext, wordlist)

    before
    >>> inputtext = open("inputtext.txt", 'r', encoding=Encode)
    >>> inputtext.readline()

    This super car come from mercedes benz motor company.

    after do text_tokenized
    >>> outputtext = open("outputtext.txt", 'r', encoding=Encode)
    >>> outputtext.readline()

    This super_car come from mercedes_benz motor company.
    
    """
    inputtext = open(inputtext, 'r', encoding=_encode_type(inputtext))      
    fileResult = open(outputtext, "w", encoding="utf-8") 
    for sentence in inputtext:
        for token in tokenization(sentence, wordlist):
            fileResult.write(token)
            fileResult.write(" ")
        fileResult.write("\n")  
    inputtext.close()
    fileResult.close()

def tokenization(sentence, wordlist):
    """ Match a string with serveral words.

    Parameter
    ---------
    sentence : string, text read from document per line.
    wordlist : list, contain word list for do word tokenization.

    Returns
    ---------
    tokenized : list
            Return list variable contain word of sentences
            and words that have several word will be represented as one.

    Examples
    ---------
    >>> sentence = "This is new york and it's one of the world biggest cities"
    >>> wordlist = [["new","york"], ["biggest", "cities"]]
    >>> tokenized = tokenization(sentence, wordlist)
    ["This", "is", "new_york", "and", "it's", "one", "of", "the", "world", "biggest_cities"]

    """
    sentence = sentence.split()
    mwe_tokenizer = nltk.tokenize.MWETokenizer(wordlist)
    tokenized = mwe_tokenizer.tokenize(sentence)

    return tokenized

def _encode_type(file):
    
    rawdata = open(file, 'rb').read()
    FileCode = chardet.detect(rawdata)
    
    return FileCode['encoding']

def _get_disease_name():
    readpath = "Document/corpus221/Wiki/"
    textoutput = open("Document/corpus221/Tag/diseaselist.txt", "w", encoding='utf-8') 
    for file in glob.glob(readpath+"*.txt"): 

        print("file : ", file)
        #Detect file encoding type of file
        rawdata = open(file, 'rb').read()
        FileCode = chardet.detect(rawdata)
        Encode = FileCode['encoding']
       
        Text_file = open(file, 'r', encoding=Encode) 
        firstLine = Text_file.readline() 
        textoutput.write(str(firstLine)) 
    textoutput.close()


inputtext = "Document/Test/New Text Document.txt"
outputtext = "Document/Test/New Text Document2.txt"
tag = {'g':['Woman','Man','Kaow'], 't':['Year','Kaow'], 's':('g','t')}
word_tagged(inputtext, outputtext, tag, default="NN")