from json.tool import main
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

    """
    Task 3.1.1

    The following are the get and Set methods for task 3.1. getDoc_len returns the docLen variable and setDocLen
    appends it to the class list declared doc_lenList. once the the doc lenght is appended to the doc_lenList it
    intiates the avgDocLenght() function which declares the setDoc_len() to the leght variable then adds it to
    total length (i noticed going over this that it might be redundent but it works and I dont want to risk
    changing it). totaldocLenght is divided by the len(BowDoc.doc_lenList to get the average doc lenght), avgDocLenght
    is then returned.
    """

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
        
"""
Task 3.1

the avg_doc_len() function is passed a bowdoc collection and loops though each one document in the collection
passing them again through the BowDoc class to intiate the previous functions discussed in the BowDoc class. 
the BowDoc.avgDocLength() is used to store and create the average doc length
"""

def avg_doc_len(coll):
    for doc in coll:
        bd = BowDoc(doc[0], doc[1], doc[2])
        avgDocLen = BowDoc.avgDocLenght(bd)
    return avgDocLen

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
Task 3.2 

the score_BM25() function is passed a Bowdoc collection(coll), a query in string form (q), and document frequencies
of the terms (df). the score_BM25() uses the BM25 ranking algorithim to rank the documents on the likely relation 
they have to the query that is passed through it. The function returns print statements  demonstrating the query
and the BM25 score, with the higher score meaning it is more likely that the document is relevant to that query.

The function startes by creating a stop word list and declaring an empty query result list (query_result).
Varaibles like K1, K2, b, ect. where set to either their predetermined values or in the case of K2 set to K2=100 (range 0-100).

Assumption: the output is not the same as the assignment sheet but the answers seem to scale to the same as the 
example solutions so it my be a factor of log chosen or the setting of parameters like K2.

qf (query frequency) is calculated by using the parse_query function on the query pased though and similarly average
doc lenght (avdl) is calculated passing BowDoc coll through avg_doc_len().

a loop is then made to loop through each document in the BowDoc collection followed by a loop to for terms in query
frequency. n (number of ducements the term is in) is calculated by using the term as the key in the df dictionary, if 
the word is present then it will define n as the value if not then n=0. Similarly this is done with f (terms frequency in doc)
using term as the key for the dictionary in the bowdoc coll dictionary(doc[1]).

K is calcualted using the compute_K() which gets passed document lenght (doc[2]) and average document lenght (avdl).
Commenting for compute_k() can be found above the functions' decleration.

All the varaibales decalred are then used to calculate the the BM23 score using the equation provided. the three 
chunks of multiplecation are calculated serperatly and declared to the values first, second and third. 
these thre vareiables are then all multiplied and declared as the value to the query_result dictionary 
with the document id (doc[0]) set as the dictioanry key, this is then repeated for all docs.

Lastly once the qf terms loop completes the query_results is looped through for key and values which are then used to
in the print statements for document ID, doc lenght, and BM25 score, similar loop is condicted again BowDoc.orderDictionary
is used to order the dictionary by values before printing the most relevant documents to the query. 


"""    

def score_BM25(coll, q, df):
    stopwords_f = open('common-english-words.txt', 'r')
    stop_words = stopwords_f.read().split(',')
    stopwords_f.close()
    query_result = dict()
    k1 = 1.2
    k2 = 100
    b = 0.75
    R = 0.0
    N = len(coll)
    r = 0.0
    
    qf = parse_query(q, stop_words)
    avdl = avg_doc_len(coll)
    for doc in coll:
        for term in qf.keys():
            try:
                n = df[term]
            except KeyError:
                n= 0
            try:
                f = doc[1]['{}'.format(term)]
            except KeyError:
                f = 0
            K = compute_K(doc[2], avdl)
            first = math.log10( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
            second = ((k1 + 1) * f) / (K + f)
            third = ((k2+1) * qf[term]) / (k2 + qf[term])
            score = first * second * third

            if doc[0] in query_result: #this document has already been scored once
                query_result[doc[0]] += score
            else:
                query_result[doc[0]] = score
        

    for key, values in query_result.items():
        print("Document ID: {}, Doc Lenght: {} -- BM25 Score: {}".format(key, doc[2], values))
    print("\nThe following are possibly relevant documents retrieved -")
    for key, values in BowDoc.OrderDic(query_result).items():
        print("{} {}".format(key, values))

""""
compute_K is called in the score_BM25() function, document lenght and avg doc lenght are passed and the formula
discussed in the lecture is applied to them.
K is returned.
"""

def compute_K(dl, avdl):
	return 1.2 * ((1-0.75) + 0.75 * (float(dl)/float(avdl)) )

"""
Task 3.3

similar to previous main methods the stopwordsList is defined so to the BowDocColl and calc_df() is used to get terms
document frequecnies. 

the four queires are defined and them added to a Queries list.

A loop then loops through the queries. the first print line states the average document lenght and using avg_doc_len()
to calculate the average lenght of the BowDocColl. the next print line states the query that is being used and the following
one details the the following, score_BM25 function is used to get the scores for that query. this is then completed
for all queries

Again the sys.stdout methods is used to create an output textfile so the same method is repreated again within this 
sys method
"""

if __name__ == "__main__":
    stopwords_f = open('common-english-words.txt', 'r')
    stopwordsList = stopwords_f.read().split(',')
    stopwords_f.close()
    path = "Rnews_v1/Rnews_v1"
    BowDocColl = parse_rcv_coll(path, stopwordsList)
    df = calc_df(BowDocColl)
    query1 = 'This British fashion'
    query2 = 'All fashion awards'
    query3 = 'The stock markets'
    query4 = 'The British-Fashion Awards'
    Queries = [query1, query2, query3, query4]
    for query in Queries:
        print("\nAverage document lenght for this collection is: {}".format(avg_doc_len(BowDocColl)))
        print("The Query is: {}".format(query))
        print("The following are the BM25 score for each document:")
        score_BM25(BowDocColl, query, df)
        
    orig_stdout = sys.stdout
    f = open('Brendan_Wallace_Nash_Q3.txt', 'w')
    sys.stdout = f
    for query in Queries:
        print("\nAverage document lenght for this collection is: {}".format(avg_doc_len(BowDocColl)))
        print("The Query is: {}".format(query))
        print("The following are the BM25 score for each document:")
        score_BM25(BowDocColl, query, df)
    f.close()

