library(readxl)
library(timeSeries)
library(tseries)
library(tidyverse)

# Read data
inflation <- read_excel("inflation.xlsx", skip=1044)

inflation <- inflation %>%
  select(Cali) %>%
  mutate(Cali = as.numeric(Cali)) %>%
  na.omit()

Cali <- ts(inflation$Cali,
           start = c(1979,12),
           end = c(2020,9),
           frequency = 12)

Cali <- window(Cali, start = c(2000,1), end=c(2020,9))

# First Model: AR(1)xSAR(1)
first_model<- arima(Cali, order =c(1,0,0), seasonal = c(1,0,0))
BIC(first_model)

# Second Model: AR(13)
second_model<- arima(Cali, order = c(13,0,0))
BIC(second_model)
