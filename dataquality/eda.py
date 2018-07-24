# -*- coding: utf-8 -*-
"""
===============================================================================
=============================== PYTHON EDA API ==============================
===============================================================================
## FRAMEWORK MLSOLVER ##
## EXPLORATORY DATA ANALYSIS ##
## AUTHOR: QUAN YUAN ##

outlier
missing data
corr f-f
corr f-obj
balance
distribution
type
iid

"""

import pandas as pd
import numpy as np
import statistics
import statsmodels.api as sm

import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

class Eda:
    # EXPLORATORY DATA ANALYSIS IN MLSOLVER
    def __init__(self, data):
        self.data = data
        sns.set(font = 'times new roman', font_scale = 1.5, rc={"figure.figsize": (12,8)})
        
    # DISSTRIBUTION ANALYSIS
    def distribution(self, col, qqplot = True):
        '''
        INPUT: series(continuous variable), data from class and one column of data
        '''
        dist = statistics.Distribution(self.data[col])
        dist.analysis()
        
    def outliers(self, xcol, method = 'inner'):
       '''
       INPUT: series, col
       '''
       f_l = np.percentile(self.data[xcol], 25)
       f_u = np.percentile(self.data[xcol], 75)
       f_m = np.median(self.data[xcol])
       if method == 'inner':
           lower = f_l - 1.5*f_l
           upper = f_u + 1.5*f_l
       elif method == 'outer':
           lower = f_l - 3*f_l
           upper = f_u + 3*f_l
       print 'the typical value is ', f_m
       print 'the upper value is ', upper
       print 'the lower value is ', lower
       print 'the percentage of outliers is %', round((1 - \
             len(self.data[xcol][(self.data[xcol] <= upper)\
             &(self.data[xcol] >= lower)])*1.0/len(self.data[xcol]))*100, 3)
    
    def missdata(self, xcol):
        # column: True or False, which column has missing data
        # row: True or False, which row has missing data
        # alldata: True or False, display all the missing data in the dataframe
        print 'MISSING DATA IN {0}'.format(xcol)
        print len(self.data[self.data[xcol] != self.data[xcol]])*1.0/len(self.data)
    
    # BALANCE TEST
    def balance(self, ycol):
        '''
        ycol = target column
        '''
        length = len(self.data)
        perc = []
        for each in set(self.data[ycol]):
            print "CATEGORY ", each
            each_perc = round(len(self.data[self.data[ycol] == each])*1.0/length, 4)
            perc.append(each_perc)
            print each_perc
        plt.figure(figsize = (8, 8))
        mpl.rc('font',family='Times New Roman')
        plt.title('BALANCE DATA TEST', fontsize = 16)
        plt.xlabel('CATEGORY', fontsize = 16)
        plt.ylabel('PERCENTAGE', fontsize = 16)
        plt.plot(perc)
        plt.show()
        
    # TYPE TEST
    def typetest(self):
        for each in self.data.columns:
            print each, ":", type(self.data[each].iloc[0])

    def causal_analysis(self, xcol, ycol):
        '''
        data: dataframe, xcol:string, ycol:string
        '''
        collect = []
        for i in list(set(self.data[xcol])):
            collect.append(self.data[self.data[xcol] == i][ycol].describe())
        collect_df = pd.concat(collect, axis = 1)
        collect_df.columns = [xcol + str(i) for i in list(set(self.data[xcol]))]
        collect_df.loc['count_rate'] = (collect_df.iloc[0]/sum(collect_df.iloc[0].tolist())).tolist()
        
        plt.figure(figsize = (12, 8))
        mpl.rc('font',family = 'Times New Roman')
        plt.title('RELATIONSHIP BETWEEN {0} AND {1}'.format(xcol, ycol), fontsize = 16)
        plt.xlabel('{0}'.format(xcol), fontsize = 16)
        plt.ylabel('{0}'.format(ycol), fontsize = 16)
        sns.boxplot(x = self.data[xcol], y = self.data[ycol])
        return collect_df
    
    def pair_corr(self):
        '''
        correlation analysis
        '''
        sns.set(font = 'times new roman', font_scale = 1.5, rc={"figure.figsize": (12,8)})
        sns.pairplot(self.data)
        plt.show()
    
    def corr(self, xcol1, xcol2):
        sns.jointplot(xcol1, xcol2, self.data, kind = 'reg')       
        plt.show()
        
    def autocorr(self, xcol):
        fig = plt.figure(figsize=(12,8))
        ax1 = fig.add_subplot(211)
        fig = sm.graphics.tsa.plot_acf(self.data[xcol], lags = 40, ax = ax1)
        ax2 = fig.add_subplot(212)
        fig = sm.graphics.tsa.plot_pacf(self.data[xcol], lags = 40, ax = ax2)
    
# resistance regression
def resist_reg(x, y):
    data = pd.DataFrame({'x':x,'y':y})
    data = data.loc[data['x'].sort_values().index]

    x = data['x']
    x.index = range(len(x))
    y = data['y']
    y.index = range(len(y))
    x_l = np.median(x.loc[:int(len(data)*1.0/3)-1])
    y_l = np.median(y.loc[:int(len(data)*1.0/3)-1])
    x_m = np.median(x.loc[int(len(data)*1.0/3):int(len(data)*2.0/3)-1])
    y_m = np.median(y.loc[int(len(data)*1.0/3):int(len(data)*2.0/3)-1])
    x_r = np.median(x.loc[int(len(data)*2.0/3):])
    y_r = np.median(y.loc[int(len(data)*2.0/3):])
    
    b0 = (y_r - y_l)*1.0/(x_r - x_l)
    a0 = 1.0*(y_l - b0*(x_l - x_m) + y_m + y_r - b0*(x_r - x_m))/3
    
    count = 0
    while 1:
        count += 1
        if count > 1000:
            return b0, a0
        b_init = b0
        a_init = a0
        
        e = y - (a_init + b_init*(x - x_m))
        
        y_l = np.median(e.loc[:int(len(data)*1.0/3)-1])
        y_m = np.median(e.loc[int(len(data)*1.0/3):int(len(data)*2.0/3)-1])
        y_r = np.median(e.loc[int(len(data)*2.0/3):])
        
        b0 = b_init + (y_r - y_l)*1.0/(x_r - x_l)
        a0 = a_init + 1.0*(y_l - b0*(x_l - x_m) + y_m + y_r - b0*(x_r - x_m))/3
        
        if abs(b_init - b0) < 0.01*b_init:
            print "y = {0}(x - {1}) + {2}".format(b0, x_m, a0)
            return {b0, a0, x_m}
        else:
            continue
        
        
        
        
        
        
        