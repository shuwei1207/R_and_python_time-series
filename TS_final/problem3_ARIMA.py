# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 18:28:10 2020

@author: USER
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import pyflux as pf
from pydlm import dlm, trend, seasonality

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# Problem 3. ARIMA model and Kalman Filter

f = open(r'Dataset-ARIMA.txt')
content = f.readlines()
f.close()

returns = []

for i in range(len(content)):
    text = content[i].split(' ')
    text = list(filter(None, text))
    a = float(text[0])
    
    returns.append(a)
    
# Fit an ARIMA(0, 1, 1) model on this data.
model = ARIMA(returns, order=(0,1,1))
model_fit = model.fit(disp=0)
print(model_fit.summary())
    
# Estimate the local trend model in Equations (11.1) and (11.2) in the slide Week 11-1.
np_returns = np.array(returns)
model = pf.LocalTrend(data=np_returns, family=pf.Normal())
result = model.fit()
print(result.summary())

# Obtain time plots for the filtered variables with pointwise 95 % confidence interval.
# Obtain time plots for the smoothed variables with pointwise 95 % confidence interval.
linear_trend = trend(degree=1, discount=0.95, name='linear_trend', w=10)
simple_dlm = dlm(returns)+ linear_trend
simple_dlm.fit()

simple_dlm.turnOff('data points')
simple_dlm.plot()