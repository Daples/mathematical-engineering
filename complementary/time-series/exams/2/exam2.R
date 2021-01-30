#Este es el identificador para cada estudiante. 
#Modifiquelo poniendo su codigo de estudiante.
ID <- 201710005101

#Modifique con el lugar donde guardo el archivo de RData
setwd("D:\Dropbox\DAVID-SAMUEL\_David_\0_EAFIT\2020-2\time-series\exams\2")


###################################################################################################
########################## Preparación ############################################################
###################################################################################################
## Corren esto sin modifcar antes de inciar a realizar el parcial.

library(dynlm)
library(strucchange)
library(rugarch)
library(forecast)
library(ggplot2)
library(tidyverse)
library(tsDyn)

load("exam2.RData")


Lider <- lista$Lider[which(lista$Código==ID)]
Seguidor <- lista$Seguidor[which(lista$Código==ID)]
InfLider <- ts(Inflacion[,Lider],
               start = c(2000,1),
               end = c(2020,9),
               frequency = 12)
InfSeguidor <- ts(Inflacion[,Seguidor],
                  start = c(2000,1),
                  end = c(2020,9),
                  frequency = 12)
adl11 <- dynlm(InfSeguidor ~ L(InfSeguidor,1) + InfLider +
                 L(InfLider,1))
ADL11 <- summary(adl11)
ARMAX11 <- arima(InfSeguidor,order = c(1,0,1), xreg = InfLider)

sel <- setar(InfSeguidor,thDelay =1,ML=1,MH=1,thVar=InfLider,th=0)
THRESHOLDAR <- summary(sel)

controls <- list(gammaInt=c(1,100), nGamma=50)
lsel <- lstar(InfSeguidor,m=1, thVar=InfLider, 
              starting.control=controls)
LSTAR <- summary(lsel)

InfSeguidorcortado <- window(InfSeguidor, start=c(2000,1), end = c(2019,12))

AR1 <- arima(InfSeguidorcortado, order = c(1,0,0))
AR12 <- arima(InfSeguidorcortado, order = c(12,0,0))
AR1xSAR1 <- arima(InfSeguidorcortado, order = c(1,0,0), seasonal = c(1,0,0))

# compare information criteria
model.list = list(AR1 = AR1,
                  AR12 = AR12,
                  AR1xSAR1 = AR1xSAR1)
TablaBIC = sapply(model.list, BIC)
TablaAIC = sapply(model.list, AIC)

LjungBoxAR1 <- Box.test(AR1$residuals, lag=12, type = "Ljung",fitdf = 2)
LjungBoxAR12 <- Box.test(AR12$residuals, lag=23, type = "Ljung",fitdf = 13)
LjungBoxAR1xSAR1 <- Box.test(AR1xSAR1$residuals, lag=24, type = "Ljung",fitdf = 14)

datos_reales <- window(InfSeguidor, 
                       start = c(2020,1), 
                       end=c(2020,9))
pred_modelo_AR1 <- forecast(AR1,9)
pred_modelo_AR12 <- forecast(AR12,9)
pred_modelo_AR1xSAR1 <- forecast(AR1xSAR1,9)

Datos_validacion_pred <- data.frame(cbind(datos_reales,
                                          pred_modelo_AR1$mean,
                                          pred_modelo_AR12$mean,
                                          pred_modelo_AR1xSAR1$mean))

Datos_validacion_pred <- Datos_validacion_pred %>%
  mutate(t=seq(from = as.Date("2020/1/1"), 
               to = as.Date("2020/09/1"), 
               length.out = 9))

graficaPredicciones <- ggplot(Datos_validacion_pred) +
  geom_line(aes(x=t, y = pred_modelo_AR1.mean,
                colour = "AR1"), size = 1) +
  geom_line(aes(x=t, y = pred_modelo_AR12.mean,
                colour = "AR12"), size = 1) +
  geom_line(aes(x=t, y = pred_modelo_AR1xSAR1.mean,
                colour = "AR1xSAR1"), size = 1) +
  geom_line(aes(x=t, y = datos_reales,
                colour = "Inflacion"), size = 1) +
  scale_colour_manual("", 
                      breaks = c( "AR1",  "AR12", "AR1xSAR1","Inflacion"),
                      values = c("red", "blue","yellow", "black")) +
  theme_minimal()


graficaInflacion <- ggplot(Inflacion) + 
                    geom_line(aes(y=InfSeguidor, x=fecha))

##################################################################################################
############################ Puntos Parcial ######################################################
##################################################################################################

Lider
Seguidor

TablaBIC
TablaAIC

LjungBoxAR1
LjungBoxAR12
LjungBoxAR1xSAR1

graficaPredicciones
graficaInflacion

######################################
######### Modelos ####################
######################################

#Los modelos se presentan en orden alfabetico, 
#debe escoger el modelo correcto para resolver cada punto
ADL11
AR1
AR12
AR1xSAR1
ARMAX11
LSTAR
THRESHOLDAR


