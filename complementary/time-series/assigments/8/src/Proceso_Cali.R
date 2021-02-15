library(readxl)
library(MASS)
library(timeSeries)
library(tseries)
library(tidyverse)
library(forecast)
library(fUnitRoots)
library(feasts)

# Leer datos
Inflacion <- read_excel("1.2.4.IPC_Por ciudad_IQY.xlsx", skip=1044)

Inflacion <- Inflacion %>%
             select(Cali) %>%
             mutate(Cali = as.numeric(Cali)) %>%
             na.omit()

Cali <- ts(Inflacion$Cali,
               start = c(1979,12),
               end = c(2020,9),
               frequency = 12)

# Serie de tiempo
plot(Cali)

# Truncar a después del 2000
Cali <- window(Cali, start = c(2000,1), end=c(2020,9))

plot(Cali)

# Transformación Box-Cox para varianza
bc <- boxcox(Cali ~ 1)
(lambda <- bc$x[which.max(bc$y)])
Cali_bc <- BoxCox(Cali, lambda)

plot(Cali_bc)

# Pruebas estacionariedad
unitrootTest(Cali) # no
unitrootTest(Cali_bc) # no

unitrootTest(Cali, lags = 12) # no
unitrootTest(Cali_bc, lags = 12) # no

pp.test(Cali) # no
pp.test(Cali_bc) # no
kpss.test(Cali) # no
kpss.test(Cali_bc) # no

# Diferenciar
diff_cali <- diff(Cali)
diff_cali_bc <- diff(Cali_bc)

unitrootTest(diff_cali) # si
unitrootTest(diff_cali_bc) # si

unitrootTest(diff_cali, lags = 12) # no
unitrootTest(diff_cali_bc, lags = 12) # no

pp.test(diff_cali) # si
pp.test(diff_cali_bc) # si
kpss.test(diff_cali) # si
kpss.test(diff_cali_bc) # si

# Estimar modelo
# Modelo 1
modelo1 <- auto.arima(Cali, max.p = 12, max.q = 12, d=1,
                      seasonal = FALSE)
# Ruido blanco
acf(modelo1$residuals) # no
pacf(modelo1$residuals) # no

Box.test(modelo1$residuals, lag=12, type = "Ljung",fitdf = 4) # no

# Estacionariedad
plot(modelo1) # si

# Significancia
(modelo1$coef)/sqrt(modelo1$var.coef) > 1.96 # si

# Coeficientes no correlacionados: NA

# Linealidad
white.test(Cali) # si

# Bondad de ajuste
R2 = 1 - modelo1$sigma2/var(Cali) # buen ajuste
AIC(modelo1)
BIC(modelo1)

# Modelo 2
modelo2 <- auto.arima(Cali_bc, max.p = 12, max.q = 12, d=1,
                      seasonal = FALSE)

# Ruido blanco
acf(modelo2$residuals) # no
pacf(modelo2$residuals) # no

Box.test(modelo2$residuals, lag=12, type = "Ljung",fitdf = 4) # no

# Estacionariedad
plot(modelo2) # si

# Significancia
for (i in 1:4) {
  print((modelo2$coef[i])/sqrt(modelo2$var.coef[i,i]) > 1.96)
} # no todos son significativos

# Coeficientes no correlacionados
cov2cor(modelo2$var.coef) # coefs altamente correlacionados

# Linealidad
white.test(Cali_bc) # si

# Bondad de ajuste
R2 = 1 - modelo2$sigma2/var(Cali_bc) # buen ajuste
AIC(modelo2)
BIC(modelo2)

## Predicción
h <- 12

pred_modelo1 <- forecast(modelo1, h) 
pred_modelo2 <- forecast(modelo2, h)

pred_modelo2_corregido <- InvBoxCox(pred_modelo2$mean, lambda,
                                      biasadj = TRUE,
                                      fvar = var(Cali_bc))

Data_pred <- data.frame(cbind(pred_modelo1$mean,
                              pred_modelo2_corregido))
Data_pred <- Data_pred %>%
             mutate(t=seq(from = as.Date("2020/10/31"), 
                          to = as.Date("2021/09/30"), 
                          length.out = 12))

ggplot(Data_pred) +
  geom_line(aes(x=t, y = pred_modelo1.mean,
                colour = "Lineal"), size = 1) +
  geom_line(aes(x=t, y = pred_modelo2_corregido,
                colour = "Box-Cox"), size = 1) +
  scale_colour_manual("", 
                      breaks = c( "Lineal",  "Box-Cox"),
                      values = c("red", "blue")) +
  theme_minimal()