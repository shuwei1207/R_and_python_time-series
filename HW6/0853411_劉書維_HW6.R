#Generate a 2-dimensional process from a VAR(1)
library(tsDyn)
library(mnormt)

cof = matrix(c(0.2,-0.6,0.3,1.1),2,2)
trend = c(0.2, 0.4)
cov.mat = matrix(c(2,1,1,1),2,2)

data =VAR.sim(cof, n=200, include = c("none"), innov=rmnorm(200, mean=0,varcov = cov.mat))

#Fit an VARMA model on it, and check the adequacy of your result.
library(MTS)

Eccm(data)
mod <- VARMA(data)
