from functools import reduce
from collections import Counter
from gensim import models
import numpy as np
import string
import json
from scipy.spatial.distance import cosine
import random
import heapq
from operator import itemgetter


class Recommender(object):

    def __init__(self,
                 model_path = 'data/embeddings/mdl',
                 user_path = 'data/user.json',
                 title_path  ='data/news.json',#news path is for title only
                 recom_path ='data/recom.json',
                 ids_path   ='data/ids.json',
                 embed_dimension=100,
                 use_google = False,
                 only_title = True,
                 summary_path = None,#for all the summary
                 ):

        self.summary_path = summary_path
        self.title_path = title_path
        self.user_path = user_path
        self.model_path = model_path

        if only_title:
            self.news_path = self.title_path
        else:
            self.news_path = self.summary_path

        self.recom_path = recom_path
        self.ids_path = ids_path
        self.dimension = embed_dimension

        if use_google:
            self.model = models.KeyedVectors.load_word2vec_format(model_path,binary=True)
        else:
            self.model = models.Word2Vec.load(self.model_path)

        self.user = self.__readfile(self.user_path)

        self.news = self.__readfile(self.news_path)
        self.recom = self.__readfile(self.recom_path)
        self.ids = self.__readfile(self.ids_path)

        self.__getnews = lambda user,news:map(lambda x:news.get(x),user)
        self.__clean = lambda x:x.translate(str.maketrans("","", string.punctuation)).strip()
        self.__V = lambda x:self.model.wv.get_vector(x)

        self.getrecomvec(self.recom,self.news)
        self.getuservec(self.user,self.news)

    def use_title(self):
        self.news_path = self.title_path
        self.news = self.__readfile(self.news_path)

    def use_summary(self):
        self.news_path = self.summary_path
        self.news = self.__readfile(self.news_path)

    def updaterecom(self):
        self.recom = self.__readfile(self.recom_path)
        self.getrecomvec(self.recom,self.news)

    def updateuser(self,**kwargs):
        self.user = self.__readfile(kwargs.get('user_path',self.user_path))
        self.getuservec(self.user,self.news)


    def getrecomvec(self,recom,news):
        self.recomvec = self.__weightedAvgEmbedding(self.__computetfidfmap(self.__getnews(recom,news)))


    def getuservec(self,user,news):
        self.uservec = self.__avgofAll(self.__weightedAvgEmbedding(self.__computetfidfmap(self.__getnews(user,news))))



    def __weightedAvgEmbedding(self, wdict):
        try:
            rt = [*map(lambda X: np.stack(map(lambda x: self.__getembedding(x[0]) * x[1], X.items())).mean(0), wdict)]
        except:
            rt = [*map(lambda X: np.array(map(lambda x: self.__getembedding(x[0]) * x[1], X.items())), wdict)]
        return rt

    def __getembedding(self,word):
        try:
            vec = self.__V(self.__clean(word))
        except:
            vec = np.zeros(self.dimension)
        return vec

    def __avgofAll(self,wavgemb):
        try:
            rt = np.stack(wavgemb).mean(0)
        except:
            rt = wavgemb
        return rt

    def __computetfidfmap(self,docx):
        corpus = [*map(lambda x: x.split(), docx)]
        wordset = reduce(lambda x, y: set(x).union(set(y)), corpus)
        initdict = [dict.fromkeys(wordset, 0) for i in range(len(corpus))]
        [*map(lambda x: x[0].update(Counter(x[1])), zip(initdict, corpus))]
        tfbow = [*map(lambda x: self.__computeTF(*x), zip(initdict, corpus))]
        idfs = self.__computeIDF(initdict)
        topicweight = [*map(lambda x: self.__computeTFIDF(x, idfs), tfbow)]
        return [*map(lambda X: dict(filter(lambda x: x[1] > 0, X.items())), topicweight)]

    def __computeTF(self,wordDict, bow):
        tfDict = dict()
        bowCount = len(bow)
        for word, count in wordDict.items():
            tfDict[word] = count / float(bowCount)
        return tfDict

    def __computeIDF(self,docList):
        import math
        idfDict = {}
        N = len(docList)

        idfDict = dict.fromkeys(docList[0].keys(), 0)
        for doc in docList:
            for word, val in doc.items():
                if val > 0:
                    idfDict[word] += 1

        for word, val in idfDict.items():
            idfDict[word] = math.log10(N / float(val))

        return idfDict

    def __computeTFIDF(self,tfBow, idfs):
        tfidf = {}
        for word, val in tfBow.items():
            tfidf[word] = val * idfs[word]
        return tfidf

    def getrecommendation(self,n=10):
        dist = [*map(lambda x:cosine(x,self.uservec),self.recomvec)]
        recindex = heapq.nsmallest(len(dist), range(len(dist)), dist.__getitem__)[:n]
        return itemgetter(*recindex)(self.recom)


    def __readfile(self,fname):
        with open(fname, "r") as f:
            d = json.load(f)
        return d

    def __writefile(self,fname, data):
        with open(fname, 'w') as f:
            json.dump(data, f)



    def randomToRecommendList(self, n = 50):
        subset = list(set(self.ids) - set(self.recom) - set(self.user))
        self.__writefile(self.recom_path, random.sample(subset, n))
        self.updaterecom()

    def updateuserreadlist(self,read = []):
        self.user.extend(read)
        self.__writefile(self.user_path,self.user)
        self.updateuser()

if __name__ == '__main__':
    r = Recommender()
    print(r.getrecommendation())
    r.randomToRecommendList()
    print(r.getrecommendation())



