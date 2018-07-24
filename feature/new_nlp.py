# -*- coding: utf-8 -*-
'''
=================================== MLQuant ===================================
================================ New NLP Module ===============================
@Eric Yuan
'''
# import packages
import numpy as np
import pandas as pd
import re
import wordcloud as wc
from collections import Counter

# Sklearn
#from sklearn.feature_extraction import DictVectorizer
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import HashingVectorizer

# Textblob
#from textblob import TextBlob
#from textblob import Word

# Gensim
#import gensim
#from gensim import corpora, models, similarities

# NLTK
from nltk.corpus import stopwords

# matplotlib
import matplotlib.pyplot as plt
from PIL import Image

class Wordclean(object):
    '''
    Function: help to keep only English words and remove stopwords
    Input: txt, string like
    Output: clean txt, string like
    '''
    def __init__(self):
        pass
        
    @staticmethod
    def nlp_clean(sen):
        '''
        Input: sentence
        Output: sentence
        '''
        return filter(lambda ch: ch in 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ', sen.lower())
    
    def get(self, sen):
        # clean
        clean_txt = self.nlp_clean(sen)
        # remove stopwords
        stopwordlist = stopwords.words('english')
        clean_txt = ' '.join([word for word in clean_txt.split() if word not in stopwordlist])
        return clean_txt
    
class Wordvisual(Wordclean):
    '''
    Input: txt, string type
    Output:
        method1: wordcloud
        method1: freq
    '''
    def __init__(self, txt):
        self.txt = txt

    def nlp_cut(self, txt):
        '''
        Function: cut sentences to words
        Input: txt, string like
        Output: words combination
        '''
        txt = self.nlp_clean(txt)
        pat = '[a-z]+'
        return re.findall(pat, txt)
    
    @staticmethod
    def nlp_count(word_list, n):
        freq_dict = Counter(word_list).most_common(n)
        word = [each[0] for each in freq_dict]
        freq = [each[1] for each in freq_dict]
        freq_df = pd.DataFrame({'word': word, 'freq': freq})
        return freq_df
    
    def freq(self, n = 10):
        '''
        n, the top n most common word
        '''
        # clean words
        clean_txt = self.get(self.txt)
        # cut words
        word_list = self.nlp_cut(clean_txt)
        # frequency
        freq_df = self.nlp_count(word_list, n)
        # visualization
        label = freq_df['word']
        idx = np.arange(len(freq_df))
        plt.figure(figsize = (12, 8))
        plt.title('Description of word frequency')
        plt.barh(idx, freq_df['freq'])
        plt.yticks(idx + 0.4, label)
        plt.show()
        return freq_df
    
    def wordcloud(self, picture = None):
        '''
        wordcloud visualization
        txt: string or dict
        picture: None, picture path
        '''
        if picture == None:
            stopwords = set(wc.STOPWORDS)
            wordcloud = wc.WordCloud(background_color = "white", \
                                     width = 1000, height = 860, margin = 20, \
                                     max_words = 2000, stopwords = stopwords).generate(self.txt)
            
            plt.figure(figsize=(9,9))
            plt.imshow(wordcloud)
            plt.axis("off")
        else:
            im = Image.open(picture)
            im_array = np.array(im)
            stopwords = set(wc.STOPWORDS)
            if type(self.txt) == str:
                wordcloud = wc.WordCloud(background_color = "white", \
                                         max_words = 2000, mask = im_array, \
                                         stopwords = stopwords).generate(self.txt)
            plt.figure(figsize=(9,9))
            plt.imshow(wordcloud)
            plt.axis("off")

class Wordresearch(Wordvisual):
    '''
    function: sentimental analysis, Tf-idf, Count, LDA, LSA
    '''
    def __init__(self, txt):
        Wordvisual.__init__(self, txt)
    
    # visualization
    def plot(self, n = 10, picture = None):
        self.freq(n)
        self.wordcloud(picture)
    
    # modeling
    
    
    
    
    
    
    
    
    