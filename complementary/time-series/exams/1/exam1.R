#Este es el identificador para cada estudiante. 
#Modifiquelo poniendo los ultimos 5 numeros de su codigo de estudiante.
ID <- 05101

###################################################################################################
########################## Preparación ############################################################
###################################################################################################
## Corren esto sin modifcar antes de inciar a realizar el parcial.
## Cada vez que requiera correr esta seccion tiene que hacerlo desde el inicio 
## de lo contrario sus resultados cambiaran.
library(tsDyn)
library(fUnitRoots)
library(forecast)
library(tidyverse)
library(tseries)
library(MASS)
set.seed(ID)
p1 <- sample(2:5,1)
charma <- c("AR","MA")
vari <- c("w_","epsilon_")
param <- seq(-.8,0.8, by = 0.1)
param <- param[-which(param==0)]
p2 <- sample(1:2, 1)
paramch <- sample(param,1)
lags <- sort(p1)
punto1 <- paste0("Sea el siguiente modelo ",charma[p2]," w_t = ",paramch,vari[p2],"{t-",p1,"} + epsilon_t" )
x <- arima.sim(n = 10000, list(ar=c(0.95)))
adfx <- unitrootTest(x, lags=2, type=c("c"))
ppx <-pp.test(x)
kpssx <- kpss.test(x)
p3 <- sample(1:3,1)
p4 <- sample(1:3,1)
valsar <- sample(c(0,0,0,0,0.1,0.2,0.3,0.4),p3)
valsma <- sample(c(0,0,0,0,-0.1,-0.2,-0.3,-0.4),p4)
punto3 <- arima.sim(n=1000, list(ar=valsar,ma=valsma))
face <- acf(punto3)
facpe <- pacf(punto3)
punto3b1 <- arima(punto3,order = c(3,0,3), method = "CSS")
punto3b2 <- arima(punto3,order = c(3,0,3), method = "ML")
e <- punto3b2$residuals
faceres <- acf(e)
facperes <- pacf(e)

##################################################################################################
############################ Puntos Parcial ######################################################
##################################################################################################

##########################
########## Punto 1 #######
##########################
punto1


##########################
########## Punto 2 #######
##########################
adfx
ppx
kpssx

##########################
########## Punto 3 #######
##########################

###########
####a######
###########
face
facpe

###########
####b######
###########
punto3b1
punto3b2

###########
####c######
###########
faceres
facperes
