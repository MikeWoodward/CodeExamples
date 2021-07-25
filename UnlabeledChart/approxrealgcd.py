#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 15:21:54 2021

@author: mikewoodward
"""

import numpy as np
import pandas as pd

# %%
MAX_ERROR = 3
STEP = 0.01
ERROR_THRESHOLD = 0.01
    
def mse(y, div):
    """Means square error calculation."""
    return sum([(round(_y/div) - _y/div)**2 for _y in y])/len(y)

def find_divider(y):
    """Return the non-integer that minimizes the error function."""
    error_list = []  
    for _div in np.arange(1 + STEP, 
                          min(y) + 2*MAX_ERROR, 
                          STEP):
        error_list.append({"divider": _div, 
                           "error":mse(y, _div)})
    df_error = pd.DataFrame(error_list)
    df_error.plot(x='divider', y='error', kind='scatter')
    
    _slice = df_error[df_error['error'] == df_error['error'].min()]
    divider = _slice['divider'].to_list()[0]
    error = _slice['error'].to_list()[0]
    
    if error > ERROR_THRESHOLD:
        raise ValueError('The estimated error is {0} which is '
                          'too large for a reliable result.'.format(error))
    
    return divider

def find_estimate(y, y_extent):
    """Make an estimate of the underlying data."""
    
    if (max(y_measured) - min(y_measured))/y_extent < 0.1:
        raise ValueError('Too little range in the data to make an estimate.')
         
    m = find_divider(y)
        
    return [round(_e/m) for _e in y_measured], m

# %%
def example_1():
    """Poisson distributed data."""
    
    _y = [4, 6, 5, 6, 3, 4, 8, 8, 4, 5]
    print("Original numbers: {0}".format(_y))

    df = pd.DataFrame({'x':range(len(_y)), 'y':_y})
    df.plot(x='x', y='y', kind='bar', legend=None)

    # Measurements from chart
    _y_measured = [519, 295, 408, 297, 631, 519, 72, 73, 519, 406]
    
    # Position of upper and lower y axis (plot y borders)
    _start = 963
    _stop = 30

    return [_start - _y_m for _y_m in _y_measured], _start - _stop
    
def example_2():
    """Prime number data."""
    _y = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23] 
    print("Original numbers: {0}".format(_y))

    df = pd.DataFrame({'x':range(len(_y)), 'y':_y})
    df.plot(x='x', y='y', kind='bar', legend=None)

    _y_measured = [539, 515, 492, 446, 399, 306, 260, 167, 120, 27]
    _start = 563
    _stop = 3

    return [_start - _y_m for _y_m in _y_measured], _start - _stop

def example_3():
    """Data set that blows up the algorithm."""
    _y = [490, 491, 488, 495, 497, 480, 492, 489, 493, 496]
    print("Original numbers: {0}".format(_y))

    df = pd.DataFrame({'x':range(len(_y)), 'y':_y})
    df.plot(x='x', y='y', kind='bar', legend=None)

    _y_measured = [66, 67, 71, 56, 53, 83, 62, 71, 61, 56]
    _start = 943
    _stop = 12

    return [_start - _y_m for _y_m in _y_measured], _start - _stop


def example_4():
    """Random data set - should yield an error."""
    _y = [131, 342, 104, 53, 351, 50, 90, 73, 194, 210]
    
    print("Original numbers: {0}".format(_y))

    df = pd.DataFrame({'x':range(len(_y)), 'y':_y})
    df.plot(x='x', y='y', kind='bar', legend=None)

    _y_measured = [396, 108, 432, 502, 95, 505, 36, 474, 308, 287]
    _start = 573
    _stop = 10
    return [_start - _y_m for _y_m in _y_measured], _start - _stop


def example_5():
    """Random data set - gives a good result."""
    _y = [33, 30, 32, 23, 32, 26, 18, 59, 47]
    
    print("Original numbers: {0}".format(_y))

    df = pd.DataFrame({'x':range(len(_y)), 'y':_y})
    df.plot(x='x', y='y', kind='bar', legend=None)

    _y_measured = [482, 500, 489, 541, 489, 523, 571, 329, 399]
    _start = 677
    _stop = 187
    return [_start - _y_m for _y_m in _y_measured], _start - _stop
    

# %%
# Get the measured result and the extent of the y axis
y_measured, y_extent = example_5()
# Estimate the 'gcd' and m
estimate, m = find_estimate(y_measured, y_extent)
# Show the results
print("Measured y values: {0}".format(y_measured))
print("Divider (m) estimate: {0}".format(m))
print("Estimated original numbers: {0}".format(estimate))

    