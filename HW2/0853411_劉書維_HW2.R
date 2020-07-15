#Generate the first 500 data points from the following AR(3):
ar3<-arima.sim(model=list(ar=c(0.1, 0,-0.1)+0.01),n=500)
ar3


#Compute and draw the autocorrleation plot.
index <- acf(ar3)
index


#Pretend you do not know the order. Do the order estimation using PACF
index2 <- pacf(ar3)
index2


#Pretend you do not know the order. Do the order estimation using the AIC.
library('forecast')
auto.arima(ar3, ic='aic')


#Use the order obtained by 4. to do the parameter estimations.
coef <- arima(ar3, order=c(2,0,2))
coef


#Check the adequacy of your estimated model by checking whether the estimated residuals forms a white-noise process.
tsdisplay(residuals(coef))
