#Generate the first 200 data points from the following GARCH model
library(fGarch)

spec = garchSpec(model = list(ar = c(0.3,-0.3)+0.1 , alpha = c(0.12)+0.1, beta = c(0.09)), cond.dist = "snorm")
data = garchSim(spec, n = 200)
data

#Draw the ACF graphs for the simulated.
library(TSA)

acf(data)
acf(data^2)
acf(abs(data))

#Suppose you know the mean function is in an ARMA(p,q) form, but you don’t know p and q. Fit the mean function.
library(forecast)
auto.arima(data, trace=TRUE) 

#Now, based on the mean function you obtained in 3., fit the GARCH model
spec <- ugarchspec(variance.model = list( submodel = NULL, 
                                          external.regressors = NULL, 
                                          variance.targeting = FALSE), 
                   
                   mean.model     = list(armaOrder = c(3, 1), 
                                         external.regressors = NULL, 
                                         distribution.model = "norm", 
                                         start.pars = list(), 
                                         fixed.pars = list()))

garch <- ugarchfit(spec = spec, data , solver.control = list(trace=0))
garch

#Do a forecasting of 𝑟_𝑡 and 𝜎_𝑡^2 for t = 201 to 210.
library(fGarch)
model = garchFit(formula = ~ garch(1, 1), data = data, cond.dist = "norm", include.mean = TRUE)
fcst= predict(model,n.ahead=10)
mean.fcst=fcst$meanForecast
