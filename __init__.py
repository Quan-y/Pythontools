# -*- coding: utf-8 -*-
"""
# --------------------------------------------------------------------------- #
# --------------------------- Welcome to MLQUANT ---------------------------- #
# --------------------------------------------------------------------------- #
@author: QUAN YUAN
"""
# necessary package check

# for judging whether MLQuant has been import
# bloomberg and wind apis are not required
flag = 0

try:
    import blpapi
except ImportError:
    print 'Package required: bloomberg python package(optional)'

try:
    from WindPy import *
    w.start()
except ImportError:
    print 'Package required: Wind python package(optional)'

# some welcome print
print '''# --------------------------------------------------------------------------- #
# --------------------------- Welcome to MLQUANT ---------------------------- #
# --------------------------------------------------------------------------- #'''