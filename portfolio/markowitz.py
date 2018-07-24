# -*- coding: utf-8 -*-
"""
@author: QUAN YUAN
"""
import numpy as np

def portfolio_opt(mu, sigma, corr, target, rf):
    '''
    mu = np.array([0.04, 0.08, 0.12, 0.15])
    sigma = np.array([0.07, 0.12, 0.18, 0.26])
    corr = np.array([[1,0.2,0.5,0.3], [0.2,1,0.7,0.4],[0.5,0.7,1,0.9],[0.3,0.4,0.9,1]])
    target = 0.05
    rf = 0.03
    w, Sigma = portfolio_opt(mu = mu, sigma = sigma, corr = corr, \
                  target = target, rf = rf)
    print 'Weight: ', w
    
    '''
    S = np.diag(sigma)
    Sigma = np.dot(np.dot(S, corr), S)
    Sigma_inv = np.mat(Sigma).I
    lam = (target - rf)*1.0/np.dot(np.dot((mu - rf).T, Sigma_inv), mu - rf)
    w = lam*np.dot(Sigma_inv, (mu - rf))
    return w, Sigma
