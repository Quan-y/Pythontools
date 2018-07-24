# -*- coding: utf-8 -*-
"""
Resistence Reg

@author: QUAN
"""
import numpy as np
import pandas as pd

# resistance regression
def resist_reg(x, y):
    '''
    x = [109, 113, 115, 116, 119, 120, 121, 124, 126, \
         129, 130 ,133, 134, 135, 137, 139, 141, 142]
    y = [137.6, 147.8, 138.8, 140.7, 132.7, 145.4, 135.0, \
         133.0, 148.5, 148.3, 147.5, 148.8, 133.2, 148.7, \
         152.0, 150.6, 165.3, 149.9]
    
    # test
    from numpy import random
    np.random.seed(0)
    x = np.array(random.rand(200)*10)
    np.random.seed(123)
    y = x*1.3 + np.array(random.rand(200))
    resist_reg(x, y)
    '''
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
