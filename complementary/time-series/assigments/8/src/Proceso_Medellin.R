library(readxl)
library(MASS)
library(timeSeries)
library(tseries)
library(tidyverse)
library(forecast)
library(fUnitRoots)
library(feasts)

setwd("D:/EAFIT/Series de Tiempo")

Inflacion <- read_excel("1.2.4.IPC_Por ciudad_IQY.xlsx", skip=1044)

Inflacion <- Inflacion %>%
             rename(Medellin = Medellín ) %>%
             select(Medellin) %>%
             mutate(Medellin = as.numeric(Medellin)) %>%
             na.omit()

Medellin <- ts(Inflacion$Medellin,
               start = c(1979,12),
               end = c(2020,9),
               frequency = 12)

plot(Medellin)

Medellin <- window(Medellin, start = c(2000,1), end=c(2020,9))

plot(Medellin)

bc <- boxcox(Medellin ~ 1)

(lambda <- bc$x[which.max(bc$y)])

lnMedellin <- log(Medellin)
Medellin_bc <- BoxCox(Medellin, lambda)

plot(lnMedellin)
plot(Medellin_bc)

unitrootTest(Medellin)
unitrootTest(lnMedellin)
unitrootTest(Medellin_bc)

acf(diff(Medellin))
unitrootTest(Medellin, lags = 12)
unitrootTest(lnMedellin, lags = 12)
unitrootTest(Medellin_bc, lags = 12)

pp.test(Medellin)

kpss.test(Medellin)

diffMed <- diff(Medellin)

unitrootTest(diffMed)
pp.test(diffMed)
kpss.test(diffMed)

acf(diffMed)
pacf(diffMed)

(modelo1 <- arima(Medellin,order = c(2,1,2)))
(modelo2 <- arima(Medellin,order = c(12,1,12)))

BIC(modelo1)
BIC(modelo2)

acf(modelo1$residuals)
pacf(modelo1$residuals)

acf(modelo2$residuals)
pacf(modelo2$residuals)

plot(modelo1)
plot(modelo2)

Box.test(modelo1$residuals, lag=12, type = "Ljung",fitdf = 4)

Box.test(modelo2$residuals, lag=36, type = "Ljung",fitdf = 24)

modelo_auto <- auto.arima(Medellin, max.p = 24, max.q = 24, d=1,
                          seasonal = FALSE)

acf(modelo_auto$residuals)
pacf(modelo_auto$residuals)

modelo_auto2 <- auto.arima(Medellin, max.p = 12, max.q = 12, d=1,
                          seasonal = FALSE, stepwise = FALSE,
                          max.order = 15)

acf(modelo_auto2$residuals)
pacf(modelo_auto2$residuals)

Box.test(modelo2$residuals, lag=24, type = "Ljung",fitdf = 13)

modelo_bc <- auto.arima(Medellin_bc, max.p = 12, max.q = 12, d=1,
                           seasonal = FALSE, stepwise = FALSE,
                           max.order = 15)
modelo_bc

h <- 12

pred_modelo_lin <- forecast(modelo_auto2, h) 
pred_modelo_bc <- forecast(modelo_bc,h)

pred_modelo_bc_corregido <- InvBoxCox(pred_modelo_bc$mean, lambda,
                                      biasadj = TRUE,
                                      fvar = var(Medellin_bc))

Data_pred <- data.frame(cbind(pred_modelo_lin$mean,
                              pred_modelo_bc_corregido))
Data_pred <- Data_pred %>%
             mutate(t=seq(from = as.Date("2020/10/31"), 
                          to = as.Date("2021/09/30"), 
                          length.out = 12))

ggplot(Data_pred) +
  geom_line(aes(x=t, y = pred_modelo_lin.mean,
                colour = "Lineal"), size = 1) +
  geom_line(aes(x=t, y = pred_modelo_bc_corregido,
                colour = "Box-Cox"), size = 1) +
  scale_colour_manual("", 
                      breaks = c( "Lineal",  "Box-Cox"),
                      values = c("red", "blue")) +
  theme_minimal()


Medellin_cortado <- window(Medellin,
                           start = c(2000,1), 
                           end=c(2019,9))

Medellin_bc_cortado <- window(Medellin_bc,
                              start = c(2000,1), 
                              end=c(2019,9))

Modelo_cortado_lin <- arima(Medellin_cortado, order = c(12,1,1))

Modelo_cortado_bc <- arima(Medellin_bc_cortado,order = c(5,1,9))

pred_modelo_lin_cortado <- forecast(Modelo_cortado_lin, h=12)


pred_modelo_bc_cortado <- forecast(Modelo_cortado_bc,h)
pred_modelo_bc_cortado_corregido <- InvBoxCox(pred_modelo_bc_cortado$mean, lambda,
                                      biasadj = TRUE,
                                      fvar = var(Medellin_bc))

datos_reales <- window(Medellin, 
                       start = c(2019,10), 
                       end=c(2020,9))

Datos_validacion_pred <- data.frame(cbind(datos_reales,
                                      pred_modelo_lin_cortado$mean,
                                      pred_modelo_bc_cortado_corregido))

Datos_validacion_pred <- Datos_validacion_pred %>%
  mutate(t=seq(from = as.Date("2019/10/31"), 
               to = as.Date("2020/09/30"), 
               length.out = 12))

ggplot(Datos_validacion_pred) +
  geom_line(aes(x=t, y = pred_modelo_lin_cortado.mean,
                colour = "Lineal"), size = 1) +
  geom_line(aes(x=t, y = pred_modelo_bc_cortado_corregido,
                colour = "Box-Cox"), size = 1) +
  geom_line(aes(x=t, y = datos_reales,
                colour = "Inflacion"), size = 1) +
  scale_colour_manual("", 
                      breaks = c( "Lineal",  "Box-Cox", "Inflacion"),
                      values = c("red", "blue","black")) +
  theme_minimal()
