# -*- coding: utf-8 -*-
"""
===============================================================================
=============================== PYTHON EDA API ==============================
===============================================================================
## FRAMEWORK MLSOLVER ##
## EXPLORATORY DATA ANALYSIS ##
## AUTHOR: QUAN YUAN ##
"""

#import numpy as np
import pandas as pd
from scipy import interpolate
import numpy as np
# over sampling
from imblearn.over_sampling import RandomOverSampler
# under sampling
from imblearn.under_sampling import RandomUnderSampler

class Outlier(object):
    def __init__(self, data, up_bound, low_bound):
        '''
        data: dataframe
        '''
        self.data = data
        # x std
        self.up_bound = up_bound
        # x std
        self.low_bound = low_bound
    
    def __transform(self, x, mean, std):
        '''
        transform
        '''
        if x >= self.up_bound:
            return self.up_bound*std + mean
        elif x <= self.low_bound:
            return self.low_bound*std + mean
        else:
            return x*std + mean
        
    def remove(self, col):
        '''
        data: dataframe object
        col: columns' name, list
        '''
        for each_col in col:
            # mean
            mean = self.data[each_col].mean()
            # std
            std = self.data[each_col].std()
            self.data['help'] = self.data[each_col].map(lambda x: \
                     (x - mean)*1.0/std)
            self.data[each_col] = self.data['help'].map(lambda x: \
                     self.__transform(x, mean, std))
        del self.data['help']
        return self.data
    
class Missing(object):
    def __init__(self, data):
        '''
        data: dataframe (alter object df)
        '''
        self.data = data
    # fill missing data
    def fill(self, col, method, value):
        '''
        col: column, list
        method: method, list (ffill, bfill, value)
        value: Series/Dataframe(according to index) or value, list
        '''
        for each_col, each_method, each_value in zip(col, method, value):
            if each_method == 'value':
                self.data[each_col].fillna(value = each_value, inplace = True)
            else: 
                self.data[each_col].fillna(method = each_method, inplace = True)
        return self.data
    
    def interpolate(self, x, col, method):
        '''
        default: x_new is the same for all columns
        x: list like
        col: list like
        method: list like, 'nearest', 'zero','linear','quadratic'
        return: dataframe only for interpolate columns
        '''
        y_new = []
        y_new.append(x)
        for each_col, each_method in zip(col, method):
            f = interpolate.interp1d([i for i in range(len(self.data))], \
                                      self.data[each_col], kind = each_method)
            y_new.append(f(x))
        result = pd.DataFrame(y_new).T
        result.columns = ['new_x'] + col
        return result

class Detect:
    def __init__(self, data):
        self.data = data
    def run(self):
        try:
            detect_row = self.data.iloc[0]
        except:
            print 'ERROR'
        for each in self.data.columns:
            print 'col '+ each + ' '+ str(type(detect_row[each]))

class Balance:
    def __init__(self, data):
        self.data = data
    
    def oversample(self, x, y, method = 'random'):
        '''
        x: list, [string]
        y: string
        '''
        if method == 'random':
            balancer = RandomOverSampler(random_state = 0)
            y = list(self.data[y])
            col_list = x
            if len(x) == 1:
                x = np.array(self.data[x]).reshape(1, -1)
            else:
                x = np.array(self.data[x])
            x_resampled, y_resampled = balancer.fit_sample(x, y)
            result = pd.DataFrame(x_resampled.reshape(len(col_list), -1)).T
            result['y'] = y_resampled
            result.columns = col_list + ['y']
            return result
    
    def undersample(self, x, y, method = 'random'):
        if method == 'random':
            rus = RandomUnderSampler(random_state = 0)
            y = list(self.data[y])
            col_list = x
            if len(x) == 1:
                x = np.array(self.data[x]).reshape(1, -1)
            else:
                x = np.array(self.data[x])
            x_resampled, y_resampled = rus.fit_sample(x, y)
            result = pd.DataFrame(x_resampled.reshape(len(col_list), -1)).T
            result['y'] = y_resampled
            result.columns = col_list + ['y']
            return result
            
class Compact:
    '''
    #[1,0,0,2]
    #[0,0,3,4]
    #[4,5,6,0]
    #[6,0,3,0]
    ## after compact
    #value =  [1,2,3,4,4,5,6,6,3]
    #cloumn = [0,3,2,3,0,1,2,0,2]
    #row = [0,0,1,1,2,2,2,3,3,]
    '''
    def __init__(self, data):
            pass


class Clean(Outlier, Missing, Detect, Balance):
    def __init__(self, data, up_bound, low_bound):
        Outlier.__init__(self, data, up_bound, low_bound)
    
        
        
        
        
    