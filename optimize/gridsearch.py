# -*- coding: utf-8 -*-
"""
===============================================================================
============================= PYTHON OPTIMIZER API ============================
===============================================================================
@author: QUAN YUAN
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

class Optimizer:
    def __init__(self, fun):
        # function for calculate the objective value
        self.fun = fun
        # the number of parameter
        # n = self.fun.__code__.co_argcount
        # self.n = n
        
    def gridsearch(self, *para_range):
        # example input: (1,2,3,4), (2,3,4,5)
        # change the para_range format [[one group parameter(para1, para2 ...)]]
        # product function
        para_all = []
        
        pools = map(tuple, para_range)
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            para_all.append(prod)
        
        para_all = np.array(para_all).T
        # para_range
        para_range_zip = zip(*para_all)
        # optimization result
        result = {}
        count = 1
        
        # calculate value
        for each_group_para in para_range_zip:
            
            # get parameters name in fun
            para_name = iter(self.fun.__code__.co_varnames)
            para_dict = {}
            
            # use iter
            each_iter = iter(each_group_para)
            
            # iteration
            while True:
                try:
                    # Next vale
                    x = next(para_name)
                    # para dict
                    para_dict[x] = next(each_iter)
                except StopIteration:
                    break
            para_dict['result'] = self.fun(**para_dict)
            result[count] = para_dict
            count += 1

        # find optimize result
        # the max and min
        value = []
        result_value = result.values()
        for i in range(len(result)):
            value.append(result_value[i]['result'])
        print 'The Max: ', result_value[value.index(max(value))]
        print 'The Min: ', result_value[value.index(min(value))]        
        
        result = pd.DataFrame(result).T
        self.result = result
        # all the result
        return  result
    
    def visual(self):
        # visual only for two-dim
        x, y = np.meshgrid(sorted(set(self.result['x'])), \
                           sorted(set(self.result['y'])))
        z = np.reshape(self.result['result'].values, x.shape)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap = cm.YlGnBu_r)
        ax.set_xlabel(r'x')
        ax.set_ylabel(r'y')
        ax.set_zlabel(r'z')
        plt.show()
            
        
    