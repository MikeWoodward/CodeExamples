#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 18:15:22 2021

@author: mikewoodward
"""

import pandas as pd
from scipy.stats.kde import gaussian_kde

from bokeh.plotting import figure, show

def violin(data=None,
           steps=100,
           range_extension=0.5,
           pdf_min_cutoff=0.001,
           title=None,
           y_axis_label=None,
           y_axis_max=None,
           y_axis_min=None,
           fill_color='#1F77B4'):
    
    """Function to plot a violin plot."""

    # Calculate maximum, minimum
    _min = data.min()
    _max = data.max()
    
    # Don't build the chart if the minimum and maximum are the same.
    if _max == _min:
        _str = ("""violin plot function error. """
                """Maxmimum and minimum values of the input data series """
                """are the same.""")
        raise ValueError(_str)

    # Train the KDE
    pdf = gaussian_kde(data)
    
    # Extend the range of the data by range_extension - doing this to prevent
    # the pdf from truncation when plotted using the y value range
    _e_range = (1 + range_extension)*(_max - _min)        
    _e_min = (_min + _max - _e_range)/2

    # Build the y values
    y = [_e_min + (step*_e_range)/steps for step in range(steps+1)]  
    # Calculate the pdf at each of the y values
    x = pdf.evaluate(y) 

    # Now remove any values past the minimum and maximum that are too small 
    # to plot
    _too_small = max(x)*pdf_min_cutoff
    df = pd.DataFrame({'x': x, 'y': y})
    df = df[((df['y'] <= _max) & (df['y'] >= _min)) |
            ((df['y'] > _max) & (df['x'] > _too_small)) | 
            ((df['y'] < _min) & (df['x'] > _too_small))]
    
    chart = figure(title=title,
                   y_axis_label=y_axis_label)
    
    chart.harea(y=df['y'],
                x1=df['x'],
                x2=-df['x'],
                fill_color=fill_color)
    
    chart.xaxis.visible = False
    chart.xgrid.grid_line_color = None
    
    if y_axis_max is not None and df['y'].max() > y_axis_max:
        chart.y_range.end = y_axis_max
        
    if y_axis_min is not None and df['y'].min() < y_axis_min:
        chart.y_range.start = y_axis_min
    
    return chart
    

dataframe = pd.read_csv("gapminder_full.csv", 
                        error_bad_lines=False, 
                        encoding="ISO-8859-1")

chart = violin(data=dataframe['life_exp'],
               title="Violin example",
               y_axis_label="Age at death")

show(chart)

