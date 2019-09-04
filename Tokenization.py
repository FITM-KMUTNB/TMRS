import nltk

# input sentence -> This is multi word
# prepare tags -> (multi,word)
# output -> {This, is, multi_word}
def TokenizeMultiWord(sentence, multi__word_list):
    tokenized_string = sentence.split()
    mwe = multi__word_list
    mwe_tokenizer = nltk.tokenize.MWETokenizer(mwe)
    tokenized_string = mwe_tokenizer.tokenize(tokenized_string)
    return tokenized_string

