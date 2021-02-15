library(readr)
library(forecast)
library(tseries)

data <- read.csv("data.csv")
data <- data[2]
attach(data)
x <- as.ts(data)

fit = auto.arima(data, ic="aic")
ts.plot(fit[["residuals"]])

# residuales correlacionados
acf(fit[["residuals"]])
pacf(fit[["residuals"]])
Box.test(x)

# invertibilidad/estacionariedad
plot(fit)

# coeficientes correlacionados
cov2cor(fit[["var.coef"]])

# es lineal
white.test(x)