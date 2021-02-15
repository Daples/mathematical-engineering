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

model_ar9 = Arima(JNJ, order=c(9, 1, 9))
model_sar1 = Arima(JNJ, order=c(0, 1, 9), seasonal=list(order=c(1, 0, 0), period=9))
