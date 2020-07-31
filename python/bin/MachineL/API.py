# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:51:24 2020

@author: Aldo
"""


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
#import seaborn as sns
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from pathlib import Path

import pickle
import os

class MLAPI(object):

    vectorizer3 = None
    k_model = None
    mytokenizer = RegexpTokenizer(r'[a-zA-Z\']+')
    stemmer = SnowballStemmer('english')

    def tokenizeText(self,text):
        return [self.stemmer.stem(word) for word in self.mytokenizer.tokenize(text.lower())]

    def __init__(self):
        documents = []
        path = Path("python/bin/files/")
        for x in path.iterdir():
             data = ""
             with open(x, encoding="utf8", errors='ignore') as myfile:
                data = myfile.read()
        #print(data)
             documents.append(data)
   
        punc = ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}',"%"]
        stop_words = text.ENGLISH_STOP_WORDS.union(punc)
    
        vectorizer3 = TfidfVectorizer(stop_words = stop_words, tokenizer = self.tokenizeText, max_features = 1000)
        X3 = vectorizer3.fit_transform(documents)
        words = vectorizer3.get_feature_names()

        #print(len(words))

        kmeans = KMeans(n_clusters = 5, n_init = 20, n_jobs = 2) # n_init(number of iterations for clsutering) n_jobs(number of cpu cores to use)
        kmeans.fit(X3)


        self.vectorizer3 = vectorizer3
        self.k_model = kmeans
        
        # We look at 3 the clusters generated by k-means.
        common_words = kmeans.cluster_centers_.argsort()[:,-1:-35:-1]
        for num, centroid in enumerate(common_words):
            print(str(num) + ' : ' + ', '.join(words[word] for word in centroid))

    def getPrediction(self,message):
        #print(message)
        Y = self.vectorizer3.transform([message])
        prediction = self.k_model.predict(Y)
        #print(type(prediction.flat[0]))
        return prediction.flat[0].item()


def main():
    
    
    k_model=MLAPI()
    Pkl_Filename = "kmodel.pkl"
    with open(os.path.join('./python/bin/MachineL',Pkl_Filename), 'wb') as file:  
        pickle.dump(k_model,file)

if __name__=='__main__':
    main()        
