library(hash)
library(fUnitRoots)
library(readxl)
library(MASS)
library(timeSeries)
library(tseries)
library(tidyverse)
library(forecast)
library(feasts)
library(ggplot2)

separate_weekdays <- function(ts, dates) {
  days <- c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
  weekdays_data <- weekdays(dates)
  separated_data <- hash()
  for (i in 1:5) {
    separated_data[[weekdays_data[i]]] <- c(ts[i])
  }
  
  for (i in 6:length(weekdays_data)) {
    day = weekdays_data[i]
    separated_data[[day]] <- c(separated_data[[day]], ts[i])
  }
  
  for (day in days) {
    separated_data[[day]] <- ts(separated_data[[day]])
  }
  return(separated_data)
}

test_stationarity <- function(ts, l) {
  ADF = unitrootTest(ts, lags = l)
  pADf = ADF@test$p.value[2]
  KPSS = kpss.test(ts)
  pKPSS = KPSS$ p.value
  return(c(pADf, pKPSS))
}

create_dummies <- function(dates) {
  days <- c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
  weekdays_data <- weekdays(dates)
  dummies <- hash()
  for (day in days) {
    dummies[[day]] <- as.integer(weekdays_data == day)
  }
  return(dummies)
}

get_data_orig <- function(file, h) {
  data <- read.csv(file)
  JNJ <- data %>%
    select(Close) %>%
    mutate(Close = as.numeric(Close)) %>%
    na.omit()
  JNJ <- ts(JNJ)
  JNJ <- JNJ[1:h]
  return(JNJ)
}

get_data_new <- function(file, h) {
  data <- read.csv(file)
  JNJ <- data %>%
    select(Close) %>%
    mutate(Close = as.numeric(Close)) %>%
    na.omit()
  JNJ <- ts(JNJ)
  JNJ <- JNJ[(h+1):length(JNJ)]
  return(JNJ)
}

get_data <- function(file) {
  data <- read.csv(file)
  JNJ <- data %>%
    select(Close) %>%
    mutate(Close = as.numeric(Close)) %>%
    na.omit()
  JNJ <- ts(JNJ)
  return(JNJ)
}

get_time <- function(file) {
  data <- read.csv(file)
  time <- data %>%
    select(Date) %>%
    mutate(Date = as.Date(Date, format = "%Y-%m-%d"))
  return(time)
}

get_time_orig <- function(file, h) {
  data <- read.csv(file)
  time <- data %>%
    select(Date) %>%
    mutate(Date = as.Date(Date, format = "%Y-%m-%d"))
  time <- head(time, h)
  return(time)
}

get_time_new <- function(file, h) {
  data <- read.csv(file)
  time <- data %>%
    select(Date) %>%
    mutate(Date = as.Date(Date, format = "%Y-%m-%d"))
  time <- tail(time, (dim(time)[1] - h))
  return(time)
}

get_significance <- function(model, bool=FALSE) {
  coeffs <- model$coef
  for (i in 1:length(coeffs)) {
    val <- abs(coeffs[i])/sqrt(model$var.coef[i,i])
    if (bool) {
      print(val > 1.96)
    } else {
      print(val)
    }
  }
}

get_corr <- function(model, val=0.6) {
  print(abs(cov2cor(model$var.coef)) > val)
}

get_R2 <- function(model, ts) {
  print(1 - model$sigma2/var(ts))
}