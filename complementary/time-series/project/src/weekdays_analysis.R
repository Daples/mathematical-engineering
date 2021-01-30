## Libraries
library(readxl)
library(timeSeries)
library(tseries)
library(MASS)
library(tidyverse)
library(forecast)
library(fUnitRoots)

source("data_processing.R")

## Data preparation
file = "jnj.csv"
JNJ = get_data(file)
time = get_time(file)

# Separate data
weekday_data <- separate_weekdays(JNJ, time$Date)
monday <- weekday_data$Monday
tuesday <- weekday_data$Tuesday
wednesday <- weekday_data$Wednesday
thursday <- weekday_data$Thursday
friday <- weekday_data$Friday

acf(diff(tuesday), lag = 60)
pacf(diff(tuesday), lag = 60)

## Stationarity tests
l = 5
test_stationarity(diff(monday), l)
test_stationarity(diff(tuesday), l)
test_stationarity(diff(wednesday), l)
test_stationarity(diff(thursday), l)
test_stationarity(diff(friday), l)

## Fit auto.arimas
auto.arima(monday, d = 1)
auto.arima(tuesday) # Random-walk models
auto.arima(wednesday)
auto.arima(thursday)
auto.arima(friday)
