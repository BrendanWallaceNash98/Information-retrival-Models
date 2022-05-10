import os
import glob, os
import string
from Stemming.porter2 import stem
import sys
from contextlib import redirect_stdout
import re
import math

'''
The complete BowDoc Class will be present in every question instead of importing.
Where parts of the BowDoc Class are relevant to questions they will be commented with explanation.
'''
class BowColl:
    """
    Task 1.1, Step 2

    This is a list that is called from the the BowColl Class to store BowDoc objects.
    While the work sheet examples used a dictionary with docID as key and the BowDoc object as
    the value, i will be using a list structure of [docID, docDic, docLen]

    often i will be refering to doc[0], doc[1], doc[2], this is reference to this list 
    structure and while I would of liked to change then to variable names i ran out of
    time

    """
    BowCollList = []

class BowDoc:

    """
    Task 1.1, Step 1.1 and Step 1.2
    I did not have a class variable for docID that wich I assumed was what being asked in Step
    1.1 as I did not need this in my method and initiated docID variable in the __init__ dunction 
    bellow in part 2.

    The BowDoc class is intiatated with a the docID (int of document ID), term (dictionary of
    terms and frequencies) and DocLen (int of total words in a document)
    """

    def __init__(self, docID = int, term= {}, docLen = int):
        self.docID = docID
        self.term = term
        self.docLen = docLen

    """
    Question 1, Step 1.3
    getDocInfo was the intial function to get the docID, term, docLen. I was unsure per Step 1.3
    weather we needed to create individual functions for each varaible so their are also
    fucntions for the docID(getDocID(doc)) and for the term and docLen (addTerm(doc)). These two
    functions are basically getDocInfo split into seperate functions to cover myself if that was
    required.

    getDocInfo is passed an individual xml(doc) File and a list of stop words. The function
    identifies the "itemid=" tag to get the document ID and further more identifies the
    "</text>" tags the instract the terms from the article body and to start the document word count.
    If the terms are not in the stopwordlist and have more then two letters (len(term)>2) the term is 
    made the docDic key and the value is either set to 1 or 1 is added if the term is already in 
    the dictionary.

    docId, docTerm and doc_len are then returned 

    ASSUMPTIONS: General assumptions through out phrasing and stemming were that some none-words
    that were found in the assingment were stock tickers. These where left in as they would be
    important terms if stoke analysis was the goal. Further more in the quering part of the assingment some of the words in
    the title were hyphenated, these words were split because the hyphenated words
    were not hyphenated in the documents so it seemed impractical to keep them this way.

    """

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

    """
    Question 1.1, Step 1,3
    getDocId is passed an individual xml file and returns the docid by identifing the "itemdid="
    tag in the "<newsitem" and stripping the surrounding elemnts around in the id and storing it
    in the docid varaible before returning it
    """
    def getDocId(doc):
        for line in doc:
            line = line.strip()
            if line.startswith("<newsitem "):
                    for part in line.split():
                        if part.startswith("itemid="):
                            docid = part.split("=")[1].split("\"")[1]
                            return docid
    """
    Question 1.1 Step 3.2 addTerm() also included the creation of the term dictionary seeing that the
    two dunctions would be very simular

    addTerm is passed an individual xml doc and a list of stop words. Text tags are again used
    to identify the terms of the document. Tags are removed and str.maketrans is used to remove
    digits and puntuation. Once text is reduced to terms the word count variable is added by 1
    for each term. It should be noted that word count includes all words and not only words that
    passed the stop words list, this was because it seemed nesseary  for the document lenght to
    incoperate the whole word count. From here terms are made into lowercased and stemmed
    with the porter2 algorithim. If the lenght of the term is greater then 2 (greater then 2 because
    acronyms like AU and US can be removed, 3 letter words lise AUS would end up removing relevant
    words) and not in the stop word list the term becomes the key in the curr dictionary and the
    frequency is made one or added by 1 dependent on if its first instance or not.

    (question 1.1 step 3) The removal of unimportant tags and stop words and trimming the document
    down to key terms is an example of tokenisation.
    """
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

    """
    the following functions (OrderDic(), RecursiveItems(), DicFormat()) are used to convert the BowDoc
    object dictionary into a the required format for presentation. the DicFormat() function was used
    in the parse_rvc_coll() function. the DicFormat() uses the OrderDic() function to order the dictionary
    by values and then RecursiveItems() to interrate through the dictionary.
    """
    def OrderDic(dictionary):
        #Sort dictionary based on key items in decending order
        sortedValues={k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}
        return sortedValues
    #the recursion was really only needed for nested dictionaries (which i didnt use) but the else fucntion allows it 
    # to work for normal dicitonaries to
    def RecursiveItems(dictionary):
        for key, value in dictionary.items():
            if type(value) is dict:
                yield from BowDoc.RecursiveItems(value)
            else:
                yield (key, value)
    #this function basically combines the last two functions into one
    def DicFormat(dictionary):
        sortedDic = dict()
        dic = BowDoc.OrderDic(dictionary)
        for key, value in BowDoc.RecursiveItems(dic):
            #print("{} : {}".format(key, value))
            sortedDic[key] = value
        return sortedDic
    #this function outputs the BowDoc coll dictionaries as required
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



"""
Question 1.1 create a function called parse_rcv_coll

This function takes in the path for the xml folder (inputpath) and a list of stop words. The function
loops through the folder of the xml files and appends the documents to a list named document. A loop
is then used to pass each document through both the addTerm() and getDocId() functions. The output
of these functions are declared to variables and passed through passed though the BowDoc() class function
to intiate the class. The BowDoc object is then stored in the BowColl class list BowCollList. The
BowCollList is then returned 

"""
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

"""
Question 1.2 Define a query prasing function parse_query()
queries(strings) and a stop words list are passed through the function. Simillar preprocessing was
used in prase querying that was in the parse_rcv_coll for tokenising, the only difference is the
splitting of the hyphen from words. This was done as i found that one of the later questions used
this function and the queries being passed through had hyphenated words that were not hyphenated in
the document, also it was exclueded from parse_rcv_coll because there were no hyphenated words in the
documents, just the titles.

the example of use case of the parse_query() is in the main method but commented out as it was not
asked for in the assignment.

"""

def parse_query(query, stop_words):
    curr_doc = {}
    for line in query.replace('-', ' ').split(' '):
        line = line.strip()
        line = line.translate(str.maketrans('','', string.digits)).translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
        line = line.replace("\\s+", " ")
        line = stem(line.lower())
        if len(line) > 2 and line not in stop_words:
            try:
                curr_doc[line] += 1
            except KeyError:
                curr_doc[line] = 1
    return curr_doc


"""
Task 1.3

in the main method the stop words list (stopwordsList) is defined based on opening, then reading (read()) and spliting the commas (split(",")) from the common-english-words.txt doc

The path for the Rnews_v1 is defined.

A BowDoc collection is declared (BowDocColl) by pasing the path and the stopwordsList through the parse_rcv_coll() function.

a loop is then initidated for the docs in the BowDocColl. doc[0] represents the documents ID, doc[1] represntes the term:frequency 
dictionary, and doc[2] represents the document lenght. theses are passed into the print string using f.strings.

the BowDoc.Print() function gets the BowDoc.formatfunction passed through it with the doc dictionary (doc[1]), this outputs the dictionary
in decsending order and in the required format.

the same loop in conducted again but inside a sys.stdout method so the output can be saved in a .txt file

For some reason when I use VS code it cuts the first print statement and couple of terms off only the first documents output. it is 
saved in the .txt file properly but it outputs strangly. this does not happen in Atom editor or jupyter notebook and may be a limitation on how much 
text the VS code can output but i dont know.
"""

if __name__ == "__main__":
    stopwords_f = open('common-english-words.txt', 'r')
    stopwordsList = stopwords_f.read().split(',')
    stopwords_f.close()
    path = "Rnews_v1/Rnews_v1"
    BowDocColl = parse_rcv_coll(path, stopwordsList)

    for doc in BowDocColl:
        print("Document {} contains {} terms and a total of {} words".format(doc[0], len(doc[1]), doc[2]) )
        BowDoc.PrintDic(BowDoc.DicFormat(doc[1]))

    orig_stdout = sys.stdout
    f = open('Brendan_Wallace_Nash_Q1.txt', 'w')
    sys.stdout = f

    for doc in BowDocColl:
        print("Document {} contains {} terms and a total of {} words".format(doc[0], len(doc[1]), doc[2]) )
        BowDoc.PrintDic(BowDoc.DicFormat(doc[1]))
    sys.stdout = orig_stdout
    f.close()
    #my understanding is that we did not need to output this but its here if needed
    #string1 = 'CANADA: Sherritt to buy Dynatec, spin off unit, canada.'
    #dictionary = parse_query(string1, stopwordsList)
