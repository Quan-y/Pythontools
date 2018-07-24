# -*- coding: utf-8 -*-
"""
@author: QUAN YUAN
"""
#import numpy as np
#from scipy.optimize import fsolve
#from scipy.optimize import linprog

# solve equation
'''
# DEMO
def p11_merton(x):
    # initialization
    v0 = x[0]
    sigma_v = x[1]
    
    d1 = 1.0*(np.log(v0*1.0/debt) + (rf + 1.0*sigma_v**2/2)*T)/(sigma_v*np.sqrt(T))
    d2 = d1 - sigma_v*np.sqrt(T)
    
    # equity and sigma of equity
    # norm.cdf default mean = 0, vol = 1
    equ1 = v0*norm.cdf(d1) - debt*np.exp(-rf*T)*norm.cdf(d2)
    sigma_equ1 = sigma_v*norm.cdf(d1)*v0*1.0/equ1
    
    # loss function
    return [equ0 - equ1, sigma_equ0 - sigma_equ1]

if __name__ == '__main__':
    equ0 = 3 # million
    sigma_equ0 = 0.5 # 50%
    debt = 5 # million
    T = 1 # year
    rf = 0.02 # 2%
    
    print 'Solution to this equation: '
    print fsolve(p11_merton, x0 = [3.79, 0.55])
'''

# linear programming
'''
DEMO 1
minmize -7x1 + 7x2 - 2x3 - x4 - 6x5
s.t.
    3x1 - x2 + x3 - 2x4 = -3
    2x1 + x2 + x4 + x5 = 4
    -x1 + 3x2 - 3x4 + x6 = 12
'''
#c = np.array([-7, 7, -2, -1, -6, 0])
#a = np.array([[3, -1, 1, -2, 0, 0], [2, 1, 0, 1, 1, 0], [-1, 3, 0, -3, 0, 1]])
#b = np.array([-3, 4, 12])
#
#res = linprog(c, A_eq = a, b_eq = b, bounds = ((0, None), (0, None), \
#                       (0, None), (0, None), (0, None), (0, None)))
#print res

'''
DEMO 2
minmize -x1 + 4x2
s.t.
    -3x1 + x2 <= 6
    x1 + 2x2 <= 4
    x1 >= -3
'''
#c = [-1, 4]
#A = [[-3, 1], [1, 2]]
#b = [6, 4]
#x1_bound = (None, None)
#x2_bound = (-3, None)
#res = linprog(c, A_eq = A, b_eq = b, bounds = (x1_bound, x2_bound), options = {'disp': True})
#print res

