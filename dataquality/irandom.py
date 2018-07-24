# -*- coding: utf-8 -*-
"""
@author: QUAN
"""
import random

class Generator:
    def __init__(self, dist):
        # distribution
        self.dist = dist
    def get(self, num, mu = 0, sigma = 1, lambd = 1, alpha = 0, beta = 1):
        if self.dist == 'normal':
            return [random.normalvariate(mu, sigma) for i in range(num)]
        elif self.dist == 'lognormal':
            return [random.lognormvariate(mu, sigma) for i in range(num)]
        elif self.dist == 'exp':
            return [random.expovariate(lambd) for i in range(num)]
        elif self.dist == 'gamma':
            return [random.expovariate(alpha, beta) for i in range(num)]
        elif self.dist == 'beta':
            return [random.betavariate(alpha, beta) for i in range(num)]
        elif self.dist == 'weibull':
            return [random.weibullvariate(alpha, beta) for i in range(num)]
            
            