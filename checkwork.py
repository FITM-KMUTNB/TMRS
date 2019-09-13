


path = "C:/Users/Kaow/Documents/Project/TMRS/Document/corpus221/cleanword/ADHD.txt.txt.s_nouns_sentences_untagged.txt"
c_file = open(path, 'r', encoding="utf-8")

file1 = dict()
for line in c_file:
    wordlist = line.split()
    for w in wordlist:
        if w in file1:
            file1[w] += 1
        else:
            file1[w] = 1
    
path = "C:/Users/Kaow/Documents/Project/TMRS/Document/corpus221/cleanword2/test.txt"
c_file = open(path, 'r', encoding="utf-8")

file2 = dict()
for line in c_file:
    wordlist = line.split()
    for w in wordlist:
        if w in file2:
            file2[w] += 1
        else:
            file2[w] = 1
num = 0
for f1 in file1:
    if f1 not in file2:
        print(f1)
        num += 1

print(num)