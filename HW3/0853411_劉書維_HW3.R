#Generate the first 1000 data points from the following ARMA(1,2)
arma<-arima.sim(model=list(ar = c(0.7), ma = c(-0.8, 0.1)),n=1000)+0.3
arma

#Pretend you don’t know the orders. Do the order estimation using EACF.
library(TSA)
eacf(arma)

#Do the parameter estimation using the order obtained above.
out<-arima(arma,order=c(0,0,2))
summary(out)
out[1]

#Simulate the first 1000 data points of an ARIMA(1,1,2)
arima1<-arima.sim(model=list(order = c(1,1,2), ar = c(0.7), ma = c(-0.8, 0.1)),n=1000)+0.3
arima1

#Do the augmented Dickey-Fuller test on your simulated data.
library(tseries)
library(forecast)
adf.test(arima1)
