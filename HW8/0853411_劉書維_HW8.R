#Generate the first 200 data points from the following AR(3):

ar3<-arima.sim(model=list(ar=c(0.1, 0,-0.1)+0.01),n=200)
ar3

#Suppose you observe R(t) for t=1~200 EXCEPT t=100.  Fit the model using the Gibbs sampling approach for a missing data
library(LaplacesDemon)
armiss <- ar3
armiss[100] <- NA

Fit <- MISS( matrix(armiss,40), Iterations=100, Algorithm="GS", verbose=TRUE)
Fit
summary(Fit)


#Suppose you observe R(t) for t=1~200 EXCEPT t=100~110.  Fit the model using the Gibbs sampling approach for a missing data
library(LaplacesDemon)

armiss2 <- ar3
armiss2[100:110] <- NA

Fit2 <- MISS( matrix(armiss2,40), Iterations=100, Algorithm="GS", verbose=TRUE)
Fit2
summary(Fit2)

