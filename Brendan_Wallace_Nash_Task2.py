import os
import glob, os
import string
from Stemming.porter2 import stem
import sys
from contextlib import redirect_stdout
import re
import math


class BowColl:
   
    BowCollList = []

class BowDoc:

    def __init__(self, docID = int, term= {}, docLen = int):
        self.docID = docID
        self.term = term
        self.docLen = docLen


    def getDocInfo(doc, stop_words):
        start_end = False
        docDic = {}
        doc_len = 0
        for line in doc:
            line = line.strip()
            if(start_end == False):
                if line.startswith("<newsitem "):
                    for part in line.split():
                        if part.startswith("itemid="):
                            docID = part.split("=")[1].split("\"")[1]
                            break
                if line.startswith("<text>"):
                    start_end = True
            elif line.startswith("</text>"):
                break
            else:
                line = line.replace("<p>", "").replace("</p>", "")
                line = line.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
                line = line.replace("\\s+", " ")
                for term in line.split():
                    doc_len += 1
                    term = stem(term.lower())
                    if len(term) > 2 and term not in stop_words:
                        try:
                            docDic[term] += 1
                        except KeyError:
                            docDic[term] = 1
        return docID , docDic, doc_len

   
    def getDocId(doc):
        for line in doc:
            line = line.strip()
            if line.startswith("<newsitem "):
                    for part in line.split():
                        if part.startswith("itemid="):
                            docid = part.split("=")[1].split("\"")[1]
        return docid
    
    def addTerm(doc, stop_words):
        start_end = False
        curr_doc = {}
        word_count = 0
        for line in doc:
                    line = line.strip()
                    if(start_end == False):
                        pass
                        if line.startswith("<text>"):
                            start_end = True
                    elif line.startswith("</text>"):
                        break
                    else:
                        line = line.replace("<p>", "").replace("</p>", "")
                        line = line.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
                        line = line.replace("\\s+", " ")
                        for term in line.split():
                            word_count += 1
                            term = stem(term.lower())
                            if len(term) > 2 and term not in stop_words:
                                try:
                                    curr_doc[term] += 1
                                except KeyError:
                                    curr_doc[term] = 1
        return curr_doc, word_count

    
    def OrderDic(dictionary):
        sortedValues={k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}
        return sortedValues

    def RecursiveItems(dictionary):
        for key, value in dictionary.items():
            if type(value) is dict:
                yield from BowDoc.RecursiveItems(value)
            else:
                yield (key, value)

    def DicFormat(dictionary):
        sortedDic = dict()
        dic = BowDoc.OrderDic(dictionary)
        for key, value in BowDoc.RecursiveItems(dic):
            #print("{} : {}".format(key, value))
            sortedDic[key] = value
        return sortedDic

    def PrintDic(dictionary):
        for key, value in BowDoc.RecursiveItems(dictionary):
            print("{} : {}".format(key, value))

    def getDoc_len(self):
        return self.docLen

    doc_lenList = []

    def setDoc_len(self):
        BowDoc.doc_lenList.append(BowDoc.getDoc_len(self))
        return BowDoc.doc_lenList

    def avgDocLenght(self):
        totalDocLength = 0
        lenght = sum(BowDoc.setDoc_len(self))
        totalDocLength += lenght
        avgDocLenght = totalDocLength / len(BowDoc.doc_lenList)
        return avgDocLenght


def parse_rcv_coll(inputpath, stop_words):
    curr_doc = {}
    start_end = False
    word_count = 0
    document = []
    #bowDocDic = {'ID'}
    for filename in os.listdir(inputpath):
        f = os.path.join(inputpath, filename)
        myfile = open(f)
        file = myfile.readlines()
        document.append(file)
    for i in range(len(document)):
        dic2, count2 = BowDoc.addTerm(document[i], stop_words)
        docID2 = BowDoc.getDocId(document[i])
        doc2 = BowDoc(docID2, dic2, count2)
        BowColl.BowCollList.append([doc2.docID, doc2.term, doc2.docLen])
    BowDocColl = BowColl.BowCollList
    return BowDocColl

def parse_query(query, stop_words):
    curr_doc = {}
    for line in query.replace('-', ' ').split(' '):
        line = line.strip()
        line = line.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
        #print(line)
        #print('-----------')
        line = line.replace("\\s+", " ")
        #term = stem(term.lower()) ## for wk 4
        line = stem(line.lower()) #wk3
        if len(line) > 2 and line not in stop_words: #wk3
            try:
                curr_doc[line] += 1
            except KeyError:
                curr_doc[line] = 1
    return curr_doc

#Calculate document frequency of terms
#this is the frequency of documents the word appears in
'''
Task 2.1

Assumption: reuters was appearing in the text of some of the articles and not other.
Reuters is the company that made all the articles and because they only had
their name in some text and not other (some times their name was in removed tags)
it would make sense to remove them, but this term was left in the examples
in the assignment sheet so they were left in.

the calc_df() function is passed the BowCollList and the loops through the range of documents in the coll
for each coll the terms are taken from each dictionary and added to the document frequency dictionary (df) as a key
 and the value is set to 1 or if the term is already in the dictionary the frequency is updataed by adding 1. The format dictionary function from
the BowDoc class is used to order the dictionary in decending order of frequency. The dictionary is then
returned.

I have commented out the part of the function that would return the output that was requested becuase
in task 2 it never ask for the output to be present in the main method and further on when this function is used
I need a return of the dictionary and not a print out.

'''
def calc_df(coll):
    res = dict()
    df_ = {}

    for i in range(len(coll)):
        for term in coll[i][1].keys():
            try:
                df_[term] += 1
            except KeyError:
                df_[term] = 1
    freqDic = BowDoc.DicFormat(df_)
    #print('There are 10 documents in this dataset\nThe following are the terms document-frequency:\n')
    #BowDoc.PrintDic(WordFreq)
    return freqDic

"""
Task 2.2 create a tfifg(doc, df (document freq from calc_df), ndocs (number of documents)) to calculate the tf*idf value of a term in a BowDoc object

An empty dictionary (tfidf = {}) is initialised and word count is set to the documents word count (doc[2]) (doc list is [id, termDic, wordCount])
the term frequency is then calculated by diciding the term frequency in the document by the word count of the

A dictionary for the inverse data fequency is intialised (idfDict) and then the terms(words) and document
frequency of those words are looped through from the document frequency list passed through from the calc_df functin,
the log10 of the number of documents divided by the document frequncy of the word is calculated and added to a
dictionary as the value with the term the key.
Lastly the TF-IDF is calulated by looping through the tfDict for word and values and then multiplying the tf value
by the idf value and decalring that as the value for the dictionary with the term as the keyword. and then returning a
dictionary of terms and TF-IDF values


"""
def tfidf(doc, df, ndocs):
    tfDict = {}
    wordCount = doc[2]
    for word, count in doc[1].items():
        tfDict[word] = count/float(wordCount)

    #inverse data frequency
    idfDict = {}
    for word, val in df.items():
            idfDict[word] = math.log10(ndocs / float(val))

    # Calculate the TF-IDF
    tfidfDic = {}
    for word, val in tfDict.items():
        tfidfDic[word] = val * idfDict[word]
    return tfidfDic

"""
Task 2.3 tf*idf IR model

the IR_model() is pased a query, which is a pre proscessed string witht the parse_query functions, and BowDocTFIDF
which is a list of document ID and a dictionary of its terms and TFIDF values (BowDocTFIDF [id, dic{term:tfidf}]).

The loop is intiatied for the range(len()) of the BowDocTFIDF and the ID from this list is appeneded to the valueList.
From here we loop through the parsed query taking its key and value. The key is used to find if the term in the query
is present in the BowDocTFIDF dictionary, if it is the BowDocTFIDF value is multiplied by the parsed query value (query term frequency).
If the query term is not in the BowDocTFIDF it is passed and not added. The valueList is then returned.


"""

def IR_model(query, BowDocTFIDF):
    valueList = []

    for i in range(len(BowDocTFIDF)):
        valueList.append([BowDocTFIDF[i][0]])
        for key, value in query.items():
            try:
                valueList[i].append(BowDocTFIDF[i][1][key]*value)
            except KeyError:
                pass
    return valueList
""""
outPutIR is just a function that gets the ir_resuts and the query string and formats them into a dictionary as was required by the 
assignment.
"""
def outPutIR(ir_result, queryString):
    print('\nThe Ranking Result for query: {}\n'.format(queryString))
    irDic = {}
    for i in range(len(ir_result)):
        irDic['{}'.format(ir_result[i][0])] = sum(ir_result[i][1:len(ir_result[i])])
        irDic = BowDoc.OrderDic(irDic)
    BowDoc.PrintDic(irDic)

"""
Task 2.3 Main method
The main method is simular to previous with creating a stop word file, path and using parse_rcv_coll. BowDocTFIDF list in intitiated to store BowDocId
and the the tfidfDic  made from the tfidf functon. document frequency is calculated with the calc_df function and assighed
to docFreq. 

a loop is used for the range of the BowDocColl and for each BowDocObject in the BowDocCOll the tfidf is 
calculated by passing the document, document frequency of words and total number of documents. the tfidf dictionary 
is declared to the tfidfDic variable and then the BowDoc object ID and tfidf ID is appended to the BowDocTFIDF list. 

The following code is repeated twice, once within the sys.stdout method for getting output into a text file and once
to just have the output. A loop for the range of BowDocTFIDF is created to print a document discription, sort the 
dictionary in the BowDocTFIDF list decsending unsing OrderDic() and output the top 12 keys and values by
converting the sorted dictionary into a list and limiting it to the first 12 instances of the list before looping
and printing the keys and values. 

lastly the IR model was used on three examples using the title as the query. The title were just copied and pasted 
from the files as it was not stated that it needed to be retrievied by code. the title was declared to a 
queryString valiable and then passed through the parse_query function with stop words list. The output from the parse
query and the BowDocTFIDF list are passed through the ir model and then the output is declared to the irList varaible
and passed through the outPutIR() function along with the query string (Headline) to format the output.


"""

if __name__ == "__main__":
    stopwords_f = open('common-english-words.txt', 'r')
    stopwordsList = stopwords_f.read().split(',')
    stopwords_f.close()
    path = "Rnews_v1/Rnews_v1"
    BowDocColl = parse_rcv_coll(path, stopwordsList)

    BowDocTFIDF = []
    docFreq = calc_df(BowDocColl)

    for i in range(len(BowDocColl)):
        tfidfDic = tfidf(BowDocColl[i], docFreq, 10)
        BowDocTFIDF.append([BowDocColl[i][0], tfidfDic])
    
    for i in range(len(BowDocTFIDF)):
        print('\nDocument {} contains {} terms\n'.format(BowDocTFIDF[i][0], len(BowDocTFIDF[i][1])))
        BowDocSortedDic = BowDoc.OrderDic(BowDocTFIDF[i][1])
        for key, values in list(BowDocSortedDic.items())[:12]:
            print('{} : {}'.format(key, values))
    #Document 741299
    queryString1 = "BELGIUM: MOTOR RACING-LEHTO AND SOPER HOLD ON FOR GT VICTORY"
    query1 = parse_query(queryString1, stopwordsList)
    irList = IR_model(query1, BowDocTFIDF)
    outPutIR(irList, queryString1)
    #Document 741309
    queryString2 = "UK: GOLF-BRITISH OPEN FOURTH ROUND LEADERBOARD."
    query2 = parse_query(queryString2, stopwordsList)
    irList2 = IR_model(query2, BowDocTFIDF)
    outPutIR(irList2, queryString2)
    #Document 780723
    queryString3 = "CANADA: Toronto stocks open mixed and directionless."
    query3 = parse_query(queryString3, stopwordsList)
    irList3 = IR_model(query3, BowDocTFIDF)
    outPutIR(irList3, queryString3)
    #following if for the text file, after that is for the print excute
    orig_stdout = sys.stdout
    f = open('Brendan_Wallace_Nash_Q2.txt', 'w')
    sys.stdout = f

    for i in range(len(BowDocTFIDF)):
        print('\nDocument {} contains {} terms\n'.format(BowDocTFIDF[i][0], len(BowDocTFIDF[i][1])))
        BowDocSortedDic = BowDoc.OrderDic(BowDocTFIDF[i][1])
        for key, values in list(BowDocSortedDic.items())[:12]:
            print('{} : {}'.format(key, values))
    #Document 741299
    queryString1 = "BELGIUM: MOTOR RACING-LEHTO AND SOPER HOLD ON FOR GT VICTORY"
    query1 = parse_query(queryString1, stopwordsList)
    irList = IR_model(query1, BowDocTFIDF)
    outPutIR(irList, queryString1)
    #Document 741309
    queryString2 = "UK: GOLF-BRITISH OPEN FOURTH ROUND LEADERBOARD."
    query2 = parse_query(queryString2, stopwordsList)
    irList2 = IR_model(query2, BowDocTFIDF)
    outPutIR(irList2, queryString2)
    #Document 780723
    queryString3 = "CANADA: Toronto stocks open mixed and directionless."
    query3 = parse_query(queryString3, stopwordsList)
    irList3 = IR_model(query3, BowDocTFIDF)
    outPutIR(irList3, queryString3)
    f.close()



    