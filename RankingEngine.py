"""
about:
This code was written by Mostafa El-Marzouki @iSuperMostafa
Occupation: Faculty of computer science and information Helwan university.
Related course: information storage and retrieval
------------------------------------------------------------
summery:
This project is a Tiny Ranking Engine, that do searching in
unlimited number of files in directory called data and calculate Terms weighting.
The input is query like Term Term | Term.
The output the weighting of each term per document
"""
import os, math
from collections import defaultdict


class RankingEngine:
    def __init__(self):
        self.DocumentsFrequency = {}
        self.Files = []

    # Get all Files in Directory
    # we can also return it's subdirectories
    def AllocateAllFiles(self, Directory):
        AllFilles = []
        for Root, Dirs, Files in os.walk(Directory):
            for File in Files:
                if File.endswith('.txt') or File.endswith('.docx') or File.endswith('.rtf'):
                    AllFilles.append(File)
        return AllFilles

    # the function is loaded one time to ini DocumentFrequency and the files
    # before the user input his query to reduce the run time of the program!
    def EngineIni(self):
        AllFiles = self.AllocateAllFiles('data')
        self.DocumentsFrequency = self.DocumentFrequency(AllFiles)
        self.Files = AllFiles

    # create a binary matrix for the search operation
    def IncidenceMatrix(self, Query):
        TermsBinaryVectors = {}
        Terms = Query.split()
        TermsBinaryDictionary = defaultdict(list)
        TermsByOrder = []
        for Term in Terms:
            if not Term in TermsBinaryVectors:
                # this's a problem the term can be added to the array without appending the new value
                # just placing it randomly
                TermsBinaryVectors[Term] = {}
            # the previous problem solved by this list selector
            TermsByOrder.append(Term)
            for File in self.Files:
                with open('data/' + File) as Lines:
                    for Line in Lines:
                        if Term in Line:
                            TermsBinaryVectors[Term][File] = True
                        else:
                            if not File in TermsBinaryVectors[Term] or not TermsBinaryVectors[Term][File] is True:
                                TermsBinaryVectors[Term][File] = False
        return TermsBinaryVectors, TermsBinaryDictionary, TermsByOrder

    # get the term frequency
    def TermCount(self, File, Term):
        TermCount = 0
        with open('data/' + File) as Lines:
            for Line in Lines:
                if Term in Line:
                    for Word in Line.split():
                        if Word == Term:
                            TermCount += 1
        return TermCount

    # count matrix
    def CountMatrix(self, TermsBinaryVectors, TermsByOrder):
        for Term in TermsByOrder:
            for File in self.Files:
                TermCount = 0
                if TermsBinaryVectors[Term][File] is not False:
                    TermCount = self.TermCount(File, Term)
                TermsBinaryVectors[Term][File] = TermCount
        return TermsBinaryVectors

    # get the max of words in query
    def TermFrequency(self, TermsByOrder):
        Words = {}
        Max = 0
        for Term in TermsByOrder:
            if Term not in Words:
                Words[Term] = 1
            else:
                Words[Term] += 1
        for Term in TermsByOrder:
            if Words[Term] > Max:
                Max = Words[Term]
        return Max

    # get the max of words in every document
    def DocumentFrequency(self, Files):
        Words = []
        WordsOccurrence = {}
        MaxWordsOccurrence = {}
        for File in Files:
            with open('data/' + File) as Lines:
                for Line in Lines:
                    for Word in Line.split():
                        if Word not in WordsOccurrence:
                            WordsOccurrence[Word] = {}
                            Words.append(Word)
                        if File not in WordsOccurrence[Word]:
                            WordsOccurrence[Word][File] = 1
                        elif File in WordsOccurrence[Word]:
                            WordsOccurrence[Word][File] += 1
        for File in Files:
            MaxWordOccurrence = 0
            for Word in Words:
                if File in WordsOccurrence[Word]:
                    if WordsOccurrence[Word][File] > MaxWordOccurrence:
                        MaxWordOccurrence = WordsOccurrence[Word][File]
            MaxWordsOccurrence[File] = MaxWordOccurrence
        return MaxWordsOccurrence

    # wight matrix
    def WeightMatrix(self, TermsCountVectors, TermsByOrder):
        # Term Frequency: tfij = tfij / maxi{fij}
        TermFrequency = {}
        # print("TermFrequency ", TermFrequency))
        MaxOfTermsCountVectors = self.TermFrequency(TermsByOrder)
        # print(MaxOfTermsCountVectors)
        for Term in TermsByOrder:
            if not Term in TermFrequency:
                TermFrequency[Term] = {}
            for File in self.Files:
                if TermsCountVectors[Term][File] > 0:
                    TermFrequency[Term][File] = TermsCountVectors[Term][File]/MaxOfTermsCountVectors
                else:
                    TermFrequency[Term][File] = 0
        # Inverse Document Frequency: idf = log10(N/df)
        DocumentFrequency = self.DocumentsFrequency
        InverseDocumentFrequency = {}
        for Term in TermsByOrder:
            if not Term in InverseDocumentFrequency:
                InverseDocumentFrequency[Term] = {}
            for File in self.Files:
                InverseDocumentFrequency[Term][File] = math.log10(len(self.Files)/DocumentFrequency[File])
        # tf-idf weighting: w = (1+log10(tf))*idf   >>>>>>>>>>>>>>>>>>>>> commented
        # tf-idf weighting: w = tf*idf
        Weighting = {}
        for Term in TermsByOrder:
            if not Term in Weighting:
                Weighting[Term] = {}
            for File in self.Files:
                # Weighting[Term][File] = (1+math.log10(TermFrequency[Term][File]))*InverseDocumentFrequency[Term]
                Weighting[Term][File] = TermFrequency[Term][File]*InverseDocumentFrequency[Term][File]
        return Weighting

    # Search for the terms of the query in files
    def Search(self, Query):
        TermsBinaryVectors, TermsBinaryDictionary, TermsByOrder = self.IncidenceMatrix(Query)
        return self.WeightMatrix(self.CountMatrix(TermsBinaryVectors, TermsByOrder), TermsByOrder)
