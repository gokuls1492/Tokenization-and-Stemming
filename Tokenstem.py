import glob
import re
import string
import time
import sys
from _collections import defaultdict
import operator
from operator import itemgetter
from audioop import reverse
from string import replace
import porter2
#from nltk.stem import PorterStemmer

def Tokenize(text):
    text = re.sub(r'\.(?![a-zA-Z]{3})', '', text)
    text = text.replace("\'s","")
    words =re.sub('[^a-zA-Z]+', ' ', text).split()# re.split(r'[-=\.,?!:$;_()\[\]\`\'*"/\t\n\r\d+ \x0b\x0c]+', text)##re.sub(r"\p{P}+", "", text.lower()).split()#
    return [word.strip() for word in words if word.strip() != '']
    
def buildDictionary():
    filesList = glob.glob(dirPath)    
    global listWord
    global noScanDocs,noWords
    #log= open("E:\output.txt","w") 
    for files in filesList:
        noScanDocs += 1
        textFile = open(files,"r")
        words = textFile.read().lower()
        plainWord = re.sub('<[^>]*>','', words)
        listWord = Tokenize(plainWord)
        #print listWord
        for word in listWord:
            #print word
            #log.write(word + '\n')
            noWords += 1
            dictWord[word]+=1
            
        textFile.close()
        
def Stemming():
    filesList = glob.glob(dirPath)    
    #ps = PorterStemmer()
    global listWord
    global noScanDocs,noStems
    for files in filesList:
        noScanDocs += 1
        textFile = open(files,"r")
        words = textFile.read().lower()
        plainWord = re.sub('<[^>]*>','', words)
        listWord = Tokenize(plainWord)    
        for w in listWord:
            noStems += 1
            stemWord[porter2.stem(w)]+= 1    
    #json.dump(stemWord, open("E:\output1.txt","w") )


dirPath  = sys.argv[1]+"/*"#"/people/cs/s/sanda/cs6322/Cranfield/*"##"F:/UTD/IR/Home work/Cranfield/*" #
noScanDocs = 0
noWords = 0
noStems = 0
noSingleStems = 0
noSingleWords = 0
dictWord = defaultdict(int)
stemWord = defaultdict(int)
startTime = int(round(time.time() * 1000))
buildDictionary()
endTime = int(round(time.time() * 1000))
for key in dictWord:        
    if (dictWord[key] == 1):
        noSingleWords +=1        
avgWord = noWords/noScanDocs
print "Time taken : "+ str(endTime-startTime) + " milliseconds"
print "Number of tokens  in the Cranfield text collection : "+ str(noWords)
print "Number of unique words : "+ str(len(dictWord.keys()))
print "Number of words that occur only once : "+ str(noSingleWords)
print "The average number of word tokens per document: "+ str(avgWord)
print "The 30 most frequent words :"
#for i in range(0,30):
#    print sortWord[i] 
for w in sorted(dictWord, key = dictWord.get, reverse = True)[:30]:
    print w + " = "+ str(dictWord[w])
noScanDocs = 0    
Stemming()

for sKey in stemWord.iterkeys():
    if (stemWord[sKey] == 1):
        noSingleStems +=1

avgStem = noStems/noScanDocs
        
print "\n"+ "Number of distinct stems in the Cranfield text collection: "+ str(stemWord.__len__())
print "Number of stems that occur only once in the Cranfield text collection :"+ str(noSingleStems) 
print "Average number of word stems per document :"+ str(avgStem) 
print "30 most frequent stems in the Cranfield text collection :"
for w in sorted(stemWord, key = stemWord.get, reverse = True)[:30]:
    print w + " = "+ str(stemWord[w])
 