# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 21:13:25 2020

@author: USER
"""
import numpy as np
import matplotlib.pyplot as plt
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

# Problem 1. GARCH and SV models 

f = open(r'Dataset-GARCH.txt')
content = f.readlines()
f.close()

n_return = []
date = []

for i in range(1,len(content)):
    a = float(content[i][-9]+content[i][-8]+content[i][-7]+content[i][-6]+content[i][-5]+content[i][-4]+content[i][-3]+content[i][-2])
    text = content[i].split(' ')
    d = int(text[0])
    
    n_return.append(a)
    date.append(d)

# Transform the returns into log-return, and plot-out the time series of the log-return
log_return = []

for i in range(len(n_return)):
    b = np.log(n_return[i]+1)
    log_return.append(b)

plt.plot(log_return)
plt.show()

# Build a GARCH model on this data.
import arch

low_aic = 0
for i in range(1,11):
    for j in range(1,11):
        model = arch.arch_model(log_return,vol='Garch', p=i, o=0, q=j, dist='Normal') 
        result = model.fit(update_freq=0) 
        if result.aic < low_aic:
            low_aic = result.aic
            best_p = i
            best_q = j
        

model = arch.arch_model(log_return,vol='Garch', p= best_p, o=0, q= best_q, dist='Normal') 
result = model.fit(update_freq=0) 
print(result.summary())

# Based on the GARCH model you fit, compute 1-step to 5-step ahead volatility forecasts at the forecast origin December 2003.

forecasts = result.forecast(horizon=5)
print(forecasts.mean.iloc[-1:])