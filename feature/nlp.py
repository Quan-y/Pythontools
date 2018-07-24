# -*- coding: utf-8 -*-
'''
=================================== MLQuant ===================================
================================== NLP Module =================================
@ QUAN YUAN
'''
# import packages
import numpy as np
import pandas as pd
import re
import wordcloud as wc
from collections import Counter
# Sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
# Textblob
from textblob import TextBlob
from textblob import Word
# Gensim
import gensim
from gensim import corpora, models, similarities
# NLTK
from nltk.corpus import stopwords
# matplotlib
import matplotlib.pyplot as plt
from PIL import Image

# -------------------------------- WordCloud -------------------------------- #
def nlp_wordcloud(txt, picture = None):
    '''
    wordcloud visualization
    txt: string or dict
    picture: None, picture path
    '''
    
    if picture == None:
        stopwords = set(wc.STOPWORDS)
        if type(txt) == str:
            wordcloud = wc.WordCloud(background_color = "white", \
                                     width = 1000, height = 860, margin = 20, \
                                     max_words = 2000, stopwords = stopwords).generate(txt)
        elif type(txt) == dict:
            wordcloud = wc.WordCloud(background_color = "white", \
                                     width = 1000, height = 860, margin = 20, \
                                     max_words = 2000, stopwords = stopwords).fit_words(txt)
        else:
            return "Don't support this type"
        plt.figure(figsize=(9,9))
        plt.imshow(wordcloud)
        plt.axis("off")
        return plt
    else:
        im = Image.open(picture)
        im_array = np.array(im)
        stopwords = set(wc.STOPWORDS)
        if type(txt) == str:
            wordcloud = wc.WordCloud(background_color = "white", \
                                     max_words = 2000, mask = im_array, \
                                     stopwords = stopwords).generate(txt)
        elif type(txt) == dict:
            wordcloud = wc.WordCloud(background_color = "white", \
                                     max_words = 2000, mask = im_array, \
                                     stopwords = stopwords).fit_words(txt)
        else:
            return "Don't support this type"
        plt.figure(figsize=(9,9))
        plt.imshow(wordcloud)
        plt.axis("off")
        return plt

# --------------------------------- Sklearn --------------------------------- #
def nlp_tovec(txt, method = 'idf', n_features = 10):
    '''
    txt: dict or string
    method: 'idf' or 'freq' or 'hash'
    n_features: output n features
    return: toarray() or get_feature_names()
    
    Demo:
        
    '''
    if type(txt[0]) == dict:
        vec = DictVectorizer()
        return [vec.fit_transform(txt), vec.get_feature_names()]
    elif type(txt[0]) == str:
        if method == 'idf':
            vec = TfidfVectorizer(min_df = 0.05, max_df = 0.95, \
                                  stop_words = 'english', analyzer = 'word')
            return [vec.fit_transform(txt), vec.get_feature_names()]
        elif method == 'hash':
            vec = HashingVectorizer(n_features = n_features, \
                                    stop_words = 'english', analyzer = 'word')
            return [vec.fit_transform(txt), vec.get_feature_names()]
    else:
        print 'error'
    
# --------------------------------- TextBlob -------------------------------- #
# filter string
def nlp_clean(sen):
    '''
    Input: sentence
    Output: sentence
    '''
    return filter(lambda ch: ch in 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ', sen.lower())

# sentimental analysis
def nlp_sen(txt):
    '''
    Input: [sentence, sentence, ...]
    Output: dataframe
    The polarity score is a float within the range [-1.0, 1.0]. 
    The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
    '''
    txt = pd.Series(txt).map(nlp_clean)
    polar = []
    subj = []
    for each_txt in txt:
        testimonial = TextBlob(each_txt)
        polarity = testimonial.sentiment[0]
        if polarity > 0:
            polar.append('pos')
        elif polarity == 0:
            polar.append('med')
        else:
            polar.append('neg')
        subjectivity = testimonial.sentiment[1]
        subj.append(subjectivity)
    return pd.DataFrame({'polar':polar, 'subj':subj})

# return speech
def nlp_phrase(txt):
    '''
    input: sentence eg: 'an apple'
    output: eg: [('an', u'DT'), ('apple', u'NN')]
    '''
    phrase = TextBlob(txt)
    return phrase.tags

# to original
def nlp_origin(txt):
    '''
    Input: [single word, single word, ...]
    Output: [single word, single word, ...]
    '''
    origin = []
    for each_txt in txt:
        each_txt = Word(each_txt)
        origin.append(each_txt.singularize().lemmatize('v'))
    return origin

# correct
def nlp_correct(txt):
    '''
    Input: [sentence, sentence, ...]
    Output: [sentence, sentence, ...]
    '''
    correct = []
    for each_txt in txt:
        try:
            each_txt = TextBlob(each_txt)
            correct.append(str(each_txt.correct()))
            #print each_txt + ' yes'
        except:
            #print each_txt + ' no'
            correct.append(each_txt)
    return correct
        
# --------------------------------- Gensim ---------------------------------- #
def nlp_cut(sen):
    '''
    Input: cut sentences to words
    Output: words combination
    '''
    sen = nlp_clean(sen)
    pat = '[a-z]+'
    return re.findall(pat, sen)
    
# LDA and LSI
def nlp_lda(txt_matrix, method = 'lda', num_topics = 3):
    '''
    Input: txt_matrix, method: lda or lsi
           eg:
          [['human', 'interface', 'computer'],
           ['survey', 'user', 'computer', 'system', 'response', 'time'],
           ['eps', 'user', 'interface', 'system'],
           ['system', 'human', 'system', 'eps'],
           ['user', 'response', 'time'],
           ['trees'],
           ['graph', 'trees'],
           ['graph', 'minors', 'trees'],
           ['graph', 'minors', 'survey']]
    Output：df
    
    Demo:
        test = [['human', 'interface', 'computer'],
            ['survey', 'user', 'computer', 'system', 'response', 'time'],
            ['eps', 'user', 'interface', 'system'],
            ['system', 'human', 'system', 'eps'],
            ['user', 'response', 'time'],
            ['trees'],
            ['graph', 'trees'],
            ['graph', 'minors', 'trees'],
            ['graph', 'minors', 'survey']]
        f_nlp_lda(test, method = 'lda')
    
    '''
    dictionary = corpora.Dictionary(txt_matrix)
    txt_matrix = [dictionary.doc2bow(text) for text in txt_matrix]
    tfidf = models.TfidfModel(txt_matrix)
    txt_matrix = tfidf[txt_matrix]
    if method == 'lsi':
        lsi = models.LsiModel(txt_matrix, num_topics = num_topics)
        corpus_lsi = lsi[txt_matrix]
    elif method == 'lda':
        lda_model = gensim.models.LdaModel(txt_matrix, num_topics = num_topics)
        corpus_lsi = lda_model[txt_matrix]
    all_txt = []
    for num in range(len(corpus_lsi[0])):
        each_txt = []
        for each in corpus_lsi:
            each_txt.append(each[num][1])
        all_txt.append(each_txt)
    all_txt_df = pd.DataFrame(all_txt).T
    if method == 'lda':
        all_txt_df.columns = ['LD_'+str(i) for i in range(len(corpus_lsi[0]))]
        return all_txt_df
    elif method == 'lsi':
        all_txt_df.columns = ['LS_'+str(i) for i in range(len(corpus_lsi[0]))]
        return all_txt_df
    else:
        return None
    
# similarity
def f_nlp_similar(origin, new):
    '''
    Input: data after model
        eg:lsi(corpus), format[(0, 0.76576841), (1, 0.12116003), (2, 0.11307155)]
    Output: similarity
    '''
    index = similarities.MatrixSimilarity(origin)
    sims = index[new]
    return list(enumerate(sims))

# handel [string, string, ...] to wordlist
def map_str(test):
    test = pd.Series(test).map(nlp_clean)
    test = nlp_correct(test)
    all_sen = []
    for each_sen in test:
        zen = TextBlob(each_sen)
        all_sen.append(zen.words)
    return all_sen

# --------------------------- One Function to Final -------------------------- #
def f_nlp(txt, method, n_features = 5, num_topics = 3):
    if method == 'wordcloud':
        return nlp_wordcloud(txt, picture = None)
    elif method == 'idf':
        return nlp_tovec(txt, method = 'idf', n_features = n_features)
    elif method == 'sentimental':
        return nlp_sen(txt)
    elif method == 'lda':
        return nlp_lda(map_str(txt), method = 'lda', num_topics = num_topics)