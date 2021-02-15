## Libraries
library(readxl)
library(timeSeries)
library(tseries)
library(MASS)
library(tidyverse)
library(forecast)
library(fUnitRoots)
library(dynlm)
library(astsa)

source("tools.R")

## Data preparation
# Reading
file = "jnj.csv"
JNJ = get_data_orig(file, 1238)
time = get_time(file)

# Fit ARIMAxSAR (0,1,9)x(1,0) period of 9
model_arimasar = sarima(JNJ, 0, 1, 9, P = 1, S = 9)


########## Validation
# White noise
Box.test(model_arimasar$fit$residuals, type = "Ljung") # melo
Box.test(model_arimasar$fit$residuals) # melo

# Stationarity
plot(model_arimasar$fit) # melo

# Coefficients significance
get_significance(model_arimasar$fit) # no melo
get_corr(model_arimasar$fit) # melo

# Linearity test
white.test(JNJ)

# Goodness-of-fit
get_R2(model_arimasar$fit, JNJ)
AIC(model_arimasar$fit)
BIC(model_arimasar$fit)
