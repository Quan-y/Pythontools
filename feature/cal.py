# -*- coding: utf-8 -*-
"""
@QUAN
"""
import numpy as np
from sklearn import preprocessing

def cal_z(data, index, col):
    '''
    功能：计算z_aplha
    输入：data需要处理的数据（dataframe），col为需要处理的列（string）
    输出：表中第一个数据相对表中其他数据的z_alpha
    '''

    # 避免分母为0
    if len(data[col]) == 1:
        return 0
    # 取出需要处理的数据
    mu = data.loc[index][col]
    mean = data[col].mean()
    std = data[col].std()
    z = (mu - mean)*1.0/std
    return z

def cal_diff(data, index, col):
    '''
    功能：计算与均值之间的差
    输入：data需要处理的数据（dataframe），col为需要处理的列（string）
    输出：表中第一个数据相对表中其他数据均值的差异
    '''
    # 取出需要处理的数据
    mu = data.loc[index][col]
    mean = data[col].mean()
    return mu - mean

def cal_std(data, index, col):
#    min_max_scaler = preprocessing.MinMaxScaler()
#    X_scaled = min_max_scaler.fit_transform(np.array(data[col]).reshape(-1, 1))
    return np.std(data[col])

def cal_quantile(data, index, col):
    # 计算分位数，越高越好
    # 先按升序排列
    data = data.sort_values(by = col, ascending = True)
    data['count'] = range(len(data))
    i = data.loc[index]['count']
    return i*1.0/len(data)

def cal_mean(data, index, col):
    # 计算均值，越高越好
    value = data.loc[index][col]
    mean = data[col].mean()
    return value - mean

def cal_turnover(data, index, col):
    # 计算均值，越高越好
    turnover = len(data[data['sub_signal'] != data['signal']])
    return turnover

def cal_obj_mean(data, col):
    # 计算均值，越高越好
    mean = data[col].mean()
    return mean

class Cal:
    '''功能：算子类，提供计算函数'''    
    def __init__(self, data, index, col):
        # 选出的同期数据
        self.data = data
        # 需要处理的数据在同期数据中是第几个
        self.index = index
        # 需要处理的列
        self.col = col
    
    def cal_z(self):
        '''
        功能：计算z_aplha
        输入：data需要处理的数据（dataframe），col为需要处理的列（string）
        输出：表中第一个数据相对表中其他数据的z_alpha
        '''
        data = self.data
        # 避免分母为0
        if len(data[self.col]) == 1:
            return 0
        # 取出需要处理的数据
        mu = data.loc[self.index][self.col]
        mean = data[self.col].mean()
        std = data[self.col].std()
        z = (mu - mean)*1.0/std
        return z
    
    def cal_diff(self):
        '''
        功能：计算与均值之间的差
        输入：data需要处理的数据（dataframe），col为需要处理的列（string）
        输出：表中第一个数据相对表中其他数据均值的差异
        '''
        data = self.data
        # 取出需要处理的数据
        mu = data.loc[self.index][self.col]
        mean = data[self.col].mean()
        return mu - mean
    
    def cal_quantile(self):
        # 计算分位数，越高越好
        # 先按升序排列
        data = self.data.sort_values(by = self.col, ascending = True)
        data['count'] = range(len(data))
        i = data.loc[self.index]['count']
        return i*1.0/len(data)
