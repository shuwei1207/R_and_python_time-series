#Simulate X(t) from:N(0,1) for t=1 to 100 and N(1,1) for t=101 to 200
x1 <- ts(rnorm( 100,mean= 0,sd= 1 ),1,100)
x2 <- ts(rnorm( 100,mean= 1,sd= 1 ),101,200)

x <- ts(c(x1, x2),start = start(x1),frequency = frequency(x1))

plot(x,type="p")


#Fit X with a single normal distribution.
library(MASS)

fit <- fitdistr(x, "normal")

para <- fit$estimate
print(para)

hist(x, prob = TRUE)
curve(dnorm(x, para[1], para[2]), col = 2, add = TRUE)


#Fix X with a mixture of normal when you know there are two mixture components
library(mclust, quietly=TRUE)

mixmdl = Mclust(x, G=2, model="V")
summary(mixmdl)


#What would you do if you do not know the number of mixture components
library(mixtools)

mixmd2 = normalmixEM(x)
summary(mixmd2)
plot(mixmd2,which=2)
lines(density(x), lty=2, lwd=2)


#suppose you know that the data actually comes from two different model, but you don¡¦t know the cutting point 100. How can you fit the model?
log_lik = function(cutpoint) {
  part1 = x[1:cutpoint]
  part2 = x[(cutpoint + 1):length(x)]
  sum(dnorm(part1, mean = 0, log = TRUE)) +
    sum(dnorm(part2, mean = 1, log = TRUE))
}

res = sapply(1:length(x), log_lik)
plot(res)
which.max(res)


#What if you don¡¦t know how many cutting points are there?
library(strucchange)

set.seed(666)
bp <- breakpoints(x ~ 1, breaks = NULL) # unknown number of breakpoints
bp$breakpoints