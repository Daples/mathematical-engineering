## Libraries
library(readxl)
library(timeSeries)
library(tseries)
library(MASS)
library(tidyverse)
library(forecast)
library(fUnitRoots)

source("tools.R")

## Data preparation
# Reading
N = 1259
t = 1238
file = "jnj.csv"
JNJ = get_data_orig(file, t)
time_orig = get_time_orig(file, t)
time_new = get_time_new(file, t)
JNJ_new = get_data_new(file, t)

# Create dummies
dummies = create_dummies(time_orig$Date)
dumm_monday = dummies$Monday
dumm_tuesday = dummies$Tuesday
dumm_wednesday = dummies$Wednesday
dumm_thursday = dummies$Thursday
dumm_friday = dummies$Friday

# Fit ARIMAX (3,1,2) with 4 eXogenous variables
xreg = c(dumm_monday, dumm_tuesday, dumm_wednesday, dumm_thursday)
xreg = matrix(xreg, ncol = 4, nrow = t)
model_arimax = Arima(JNJ, order=c(3,1,2), xreg=xreg)

########## Validation
# White noise
Box.test(model_arimax$res, type = "Ljung") # melo
Box.test(model_arimax$res) # melo

# Stationarity
plot(model_arimax) # melo

# Coefficients significance
get_significance(model_arimax) # no melo
get_corr(model_arimax) # no melo

# Linearity test
white.test(JNJ)

# Goodness-of-fit
get_R2(model_arimax, JNJ)
AIC(model_arimax)
BIC(model_arimax)

### Forecast
# Create dummies
dummies_new = create_dummies(time_new$Date)
dumm_monday_new = dummies_new$Monday
dumm_tuesday_new = dummies_new$Tuesday
dumm_wednesday_new = dummies_new$Wednesday
dumm_thursday_new = dummies_new$Thursday

# Fit ARIMAX (3,1,2) with 4 eXogenous variables
xreg_new = c(dumm_monday_new, dumm_tuesday_new, dumm_wednesday_new, dumm_thursday_new)
xreg_new = matrix(xreg_new, ncol = 4, nrow = (N - t))

