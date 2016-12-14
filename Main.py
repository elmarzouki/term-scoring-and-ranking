"""
about:
This code was written by Mostafa El-Marzouki @iSuperMostafa
Occupation: Faculty of computer science and information Helwan university.
Related course: information storage and retrieval
------------------------------------------------------------
summery:
This project is a Tiny Ranking Engine, that do searching in
unlimited number of files in directory called data.
The input is query like Term Term | Term.
The output the weighting of each term per document
"""
import RankingEngine


RankingEngine = RankingEngine.RankingEngine()
# ini documents frequency
RankingEngine.EngineIni()
while True:
    Query = input("Search: ")
    result = RankingEngine.Search(Query)
    for key, value in result.items():
        print(key)
        for doc, w in value.items():
            print(doc, " : ", w)
