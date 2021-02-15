## Libraries
library(readxl)
library(timeSeries)
library(tseries)
library(MASS)
library(tidyverse)
library(forecast)
library(fUnitRoots)
library(astsa)

source("tools.R")

## Data preparation
# Reading
t = 1238
file = "jnj.csv"
JNJ = get_data_orig(file, t)
time_orig = get_time_orig(file, t)
time_new = get_time_new(file, t)
JNJ_complete = get_data(file)
time_complete = get_time(file)

## Preliminary analysis
pdf(file='figs/ts.pdf',  width=10)
  tsplot(time_complete, JNJ_complete, xlab = "Tiempo", ylab = "JNJ")
dev.off()

pdf(file='figs/acf_og.pdf',  width=10)
  acf2(JNJ, plot = TRUE)
dev.off()

unitrootTest(JNJ)
kpss.test(JNJ)

# Diff
JNJ_diff <- diff(JNJ)

pdf(file='figs/ts_diff.pdf',  width=10)
  tsplot(time_orig$Date[2:length(time_orig$Date)], diff(JNJ), xlab = "Tiempo", ylab = "diff(JNJ)")
dev.off()

pdf(file='figs/acf_diff.pdf',  width=10)
  acf2(diff(JNJ), plot = TRUE)
dev.off()

unitrootTest(JNJ_diff)
kpss.test(JNJ_diff)

# 

model_auto = auto.arima(JNJ, d = 1) # <- ARIMA(3,1,2)

########## Validation
# White noise
Box.test(model_auto$res, type = "Ljung") # melo
Box.test(model_auto$res) # melo

# Stationarity
plot(model_auto) # melo

# Coefficients significance
get_significance(model_auto) # melo
get_corr(model_auto) # no melo

# Linearity test
white.test(JNJ)

# Goodness-of-fit
get_R2(model_auto, JNJ)
AIC(model_auto)
BIC(model_auto)
