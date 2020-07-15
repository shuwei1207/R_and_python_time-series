# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 16:58:34 2020

@author: USER
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller
from statsmodels.tools.eval_measures import rmse, aic
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.vector_ar.vecm import coint_johansen

# Problem 2. VAR model and Cointegration

f = open(r'Dataset-VAR.txt')
content = f.readlines()
f.close()

rates = []

for i in range(len(content)):
    text = content[i].split(' ')
    text = list(filter(None, text))
    a = float(text[0])
    b = float(text[1])
    
    rates.append([a,b])

df = pd.DataFrame(data = rates, columns = ['1-year','3-year'])
print(df.shape)  # (612, 2)

# Fit a VAR model on this data.
def adfuller_test(series, signif=0.05, name='', verbose=False):
    r = adfuller(series, autolag='AIC')
    output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
    p_value = output['pvalue'] 
    def adjust(val, length= 6): return str(val).ljust(length)

    # Print Summary
    print(f'    Augmented Dickey-Fuller Test on "{name}"', "\n   ", '-'*47)
    print(f' Null Hypothesis: Data has unit root. Non-Stationary.')
    print(f' Significance Level    = {signif}')
    print(f' Test Statistic        = {output["test_statistic"]}')
    print(f' No. Lags Chosen       = {output["n_lags"]}')

    for key,val in r[4].items():
        print(f' Critical value {adjust(key)} = {round(val, 3)}')

    if p_value <= signif:
        print(f" => P-Value = {p_value}. Rejecting Null Hypothesis.")
        print(f" => Series is Stationary.")
    else:
        print(f" => P-Value = {p_value}. Weak evidence to reject the Null Hypothesis.")
        print(f" => Series is Non-Stationary.")    

for name, column in df.iteritems():
    adfuller_test(column, name=column.name)
    print('\n')

df_differenced = df.diff().dropna()

for name, column in df_differenced.iteritems():
    adfuller_test(column, name=column.name)
    print('\n')
    
model = VAR(df_differenced)

x = model.select_order(maxlags=20)
print(x.summary())

model_fitted = model.fit(19)
model_fitted.summary()


# Use the fitted VAR model to produce 1-step to 12-step ahead forecasts of the interest rates, assuming that the forecast origin is March 2004.
lag_order = model_fitted.k_ar

forecast_input = df_differenced.values[-lag_order:]
fc = model_fitted.forecast(y=forecast_input, steps=lag_order)
df_forecast = pd.DataFrame(fc, index=df.index[-lag_order:], columns=df.columns + '_2d')
print(df_forecast)

# Are the two interest rate series cointegrated? Use 5 % significance level to perform the test.
def cointegration_test(df, alpha=0.05): 
    out = coint_johansen(df,-1,5)
    d = {'0.90':0, '0.95':1, '0.99':2}
    traces = out.lr1
    cvts = out.cvt[:, d[str(1-alpha)]]
    def adjust(val, length= 6): return str(val).ljust(length)

    # Summary
    print('Name   ::  Test Stat > C(95%)    =>   Signif  \n', '--'*20)
    for col, trace, cvt in zip(df.columns, traces, cvts):
        print(adjust(col), ':: ', adjust(round(trace,2), 9), ">", adjust(cvt, 8), ' =>  ' , trace > cvt)

cointegration_test(df)