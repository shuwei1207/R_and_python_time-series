# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 15:38:21 2020

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

log_return = []

for i in range(len(n_return)):
    b = np.log(n_return[i]+1)
    log_return.append(b)
    
# build an SV model on this data instead
import pymc3 as pm

def make_stochastic_volatility_model(data):
    with pm.Model() as model:
        step_size = pm.Exponential('step_size', 5)
        volatility = pm.GaussianRandomWalk('volatility', sigma=step_size, shape=len(data))
        nu = pm.Exponential('nu', 0.1)
        returns = pm.StudentT('returns', nu=nu, lam=np.exp(-2*volatility), observed=data)
        
    return model

stochastic_vol_model = make_stochastic_volatility_model(log_return)

pm.model_to_graphviz(stochastic_vol_model)

# Based on the SV model you fit, compute 1-step to 5-step ahead volatility forecasts at the forecast origin December 2003.

with stochastic_vol_model:
    prior = pm.sample_prior_predictive(500)
    
with stochastic_vol_model:
    trace = pm.sample(1, tune=10, cores=1)
    
with stochastic_vol_model:
    posterior_predictive = pm.sample_posterior_predictive(trace)

print(posterior_predictive['returns'][1][-1])