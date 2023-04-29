from collections import defaultdict
from pathlib import Path
from math import log10, sqrt
from typing import Dict, List, Set
import math
import numpy as np
import PreProcessor
import Stemmer

class VectorSpaceModel:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(list))
        self.DocSource = {}
        self.DocumentMapData = {}
        self.QueryTermFreq = {}
        self.Qvector = {}
        self.RelavanceFeedBack = {}

    def IndexBuilding(self, linksMap):
        WebpagesPath = "webpages/"
        self.index = {}
        self.DocSource = {}
        self.DocumentMapData = {}
        for DocID, filepath in enumerate(sorted(Path(WebpagesPath).glob("*"))):
            try:
                #print(f"Processing file: {filepath}")
                filename = str(filepath)
                link = linksMap.get(filename)
                if link is None:
                    print(f"Error: No link found for file {filename}")
                with filepath.open("r", encoding="utf-8") as f:
                    DocText = f.read()
                    self.DocSource[DocID] = link 
                    Preprocessor = PreProcessor.PreProcessor()
                    stemmer = Stemmer.Stemmer()
                    KUDocs = stemmer.StemmerInput(Preprocessor.DocumentClean(DocText))
                    textArray = ' '.join(KUDocs).split()
                    self.DocumentMapData[DocID] = textArray
                    for j, word in enumerate(textArray):
                        positions = self.index.setdefault(word, {}).setdefault(DocID, [])
                        positions.append(j)
            except (FileNotFoundError, Exception) as e:
                print(f"Error processing file {filepath}: {e}")
        return self.index


    def QueryIndex(self, query: str):
        self.QueryTermFreq = {} 
        InitialQuery = query.lower()
        Preprocessor = PreProcessor.PreProcessor()
        stemmer=Stemmer.Stemmer()
        InitialQuery = Preprocessor.DocumentClean(InitialQuery)
        InitialQuery= stemmer.StemmerInput(InitialQuery)
        WholeQuery = ' '.join(InitialQuery).split()
        for word in WholeQuery:
            word = word.lower()
            if word in self.QueryTermFreq:
                self.QueryTermFreq[word] += 1
            else:
                self.QueryTermFreq[word] = 1
        self.QueryEncoding() 

    def TermFreq(self, word: str, DocID: int) -> int:
        return len(self.index[word][DocID])
        

    def DF(self, word: str) -> int:
        return len(self.index[word])

    def IDF(self, word: str) -> float:
        if word not in self.index:
            return 0.0
        DocFreq = self.DF(word)
        if DocFreq > 0:
            idf = math.log10(len(self.DocSource) / DocFreq)
            if idf >= 0:
                return idf
        return 0.0

    def TF_IDF(self, word: str, DocID: int) -> float:
        if word not in self.index:
            return 0.0
        if DocID not in self.index[word]:
            return 0.0
        return self.IDF(word) * self.TermFreq(word, DocID)


    def DocumentVectors(self) -> Dict[int, List[float]]:
        DocumentVectors = {}
        for DocID, k in self.DocSource.items():
            DocumentVectors[DocID] = [self.TF_IDF(word, DocID) for word in self.index.keys()]
        return DocumentVectors

    def QueryEncoding(self) -> None:
        self.QVector = {term: 0.0 for term in self.index.keys()}
        for term, freq in self.QueryTermFreq.items():
            if term in self.index:
                self.QVector[term] = freq * self.IDF(term)
        return self.QVector


    def SearchResultsRanking(self) -> Dict[str, float]:
        SimilarityResult = {}
        for DocID, source in self.DocSource.items():
            DocVector = np.array([self.TF_IDF(term, DocID) for term in self.index.keys()])
            Normalize = np.linalg.norm(list(self.QVector.values())) * np.linalg.norm(DocVector)
            if Normalize == 0.0:
                CosineSimilarity = 0.0
            else:
                CosineSimilarity = np.dot(list(self.QVector.values()), DocVector) / Normalize
            SimilarityResult[source] = CosineSimilarity
        return {source: score for source, score in sorted(SimilarityResult.items(), key=lambda x: x[1], reverse=True) if score != 0.0}






