#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 18:15:22 2021

@author: mikewoodward
"""
import numpy as np
import pandas as pd
from scipy.stats.kde import gaussian_kde

from bokeh.plotting import figure, show

def vioin(series=None,
          steps=100,
          extension=0.1,
          title=None,
          y_axis_label=None):
    
    """Function to plot a violin plo.t"""
    
    # Kernel density estimation 
    pdf = gaussian_kde(series)
    
    # Make the plot extend beyond the minimim and maximum data points
    _min = series.min()
    _max = series.max()
    _step = (_max - _min)/steps
    y = np.arange(_min - steps*extension*_step, 
                  _max + (steps+1)*extension*_step,
                  _step)
    
    chart = figure(title=title,
                   y_axis_label=y_axis_label)
    
    chart.harea(y=y,
                x1=pdf(y),
                x2=-pdf(y))
    
    chart.xaxis.visible = False
    chart.xgrid.grid_line_color = None
    
    return chart
    

dataframe = pd.read_csv("gapminder_full.csv", 
                        error_bad_lines=False, 
                        encoding="ISO-8859-1")

chart = vioin(series=dataframe['life_exp'],
              title="Violin example",
              y_axis_label="Age at death")

show(chart)


