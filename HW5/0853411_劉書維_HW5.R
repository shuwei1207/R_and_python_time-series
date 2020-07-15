#Generate the first 200 data points from the following GARCH model
library(fGarch)

spec = garchSpec(model = list(ar = c(0.03,-0.03)+0.01, cond.dist = "snorm"))
data1 = garchSim(spec, n = 200)
data1


#Perform a RESET test on the simulated data.
library(fRegression)

x = c(1:200)
lmTest(data1  ~ x , "reset", power =2, type = "regressor")


#Generate the first 200 data points from the following GARCH model
library(fGarch)

spec = garchSpec(model = list(ar = c(0.03,-0.03)+0.01 , (ar = c(0.1))^2, cond.dist = "snorm"))
data2 = garchSim(spec, n = 200)
data2


#Perform a RESET test on the simulated data.
library(fRegression)

x = c(1:200)
lmTest(data2  ~ x , "reset", power = 2, type = "regressor")
