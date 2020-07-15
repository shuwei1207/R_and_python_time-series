# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:40:06 2020

@author: USER
"""

import numpy as np

# Generate a local-trend model
y = []
mu = []
start_point = 0

y.append(start_point)
mu.append(start_point)

for i in range(200):
    if i == 0:
        temp = start_point
    else:
        data = temp + np.random.normal(0,1)
        y.append(data)
        next_temp = temp + np.random.normal(0, 2)
        mu.append(next_temp)
        temp = next_temp

#Perform Kalman filter and smoothing on it.
#Plot your results 
from pydlm import dlm, trend, seasonality

linear_trend = trend(degree=1, discount=0.95, name='linear_trend', w=10)
simple_dlm = dlm(y)+ linear_trend
simple_dlm.fit()

simple_dlm.turnOff('data points')
simple_dlm.plot()