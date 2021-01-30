library(quantmod)
library(rugarch)
library(forecast)
library(car)
library(FinTS)
library(PerformanceAnalytics)
library(ggplot2)
library(zoo)

source("tools.R")

## Data preparation
# Reading
t = 1238
file = "jnj.csv"
JNJ = zoo(get_data_orig(file, t))
time_orig = get_time_orig(file, t)
time_new = get_time_new(file, t)

JNJ_diff = diff(JNJ)

garch11.spec = ugarchspec(variance.model = variance.model=list(model="gjrGARCH",
                                                               garchOrder=c(1,1)), 
                              mean.model = list(armaOrder=c(1,0)))

garch_model <- ugarchfit(spec=garch11.spec, data=JNJ_diff)

garch_model
plot(garch_model, which=12)
