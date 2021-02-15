############################# P?gina 432 del pdf ######################################
# Ans p?g 665
#################################### 12.7 ###############################################
setwd("/Users/plazas/Dropbox/DAVID-SAMUEL/_David_/EAFIT/2019-1/Estadistica2/multivariate_analysis")
t_3_5 <- read.table("T3_5_PROBE.dat", row.names = 1)
colnames(t_3_5) <- c("y1", "y2", "y3", "y4", "y5")
cov7 <- cov(t_3_5)

             # Comp prin cov
cprincov7 <- princomp(t_3_5,cor = FALSE)        
sprcov7 <- summary(cprincov7, loadings = TRUE)
# En el 1er comp se explica un 68.4% de la varianza, mientras
# con el 2do acum se explica un 80.7%.
# Como es posible explicar mas del 80% de la varianza con los dos
# 1ros comp princ retengo esos dos

            # Comp prins correl
cprincor7 <- princomp(t_3_5, cor = TRUE)
sprcor7 <- summary(cprincor7, loadings = TRUE)
# En el 1er comp se explica un 68.3% de la varianza, mientras
# con el 2do acum se explica un 80.6%.
# Como es posible explicar mas del 80% de la varianza con los dos
# 1ros comp princ retengo esos dos

# Analizando la proporci?n que explican cada uno de los comp princ podemos observar 
# que no existe gran diferencia entre trabajar con la covarianza o trabajar con la 
# correlaci?n, adem?s las varianzas de las variables son muy parecidadpero se decide hacerlo con la cov.

lambdacov7 <- cprincov7$sdev^2          # Valores propios de los comp princ
mlambda7 <- mean(lambdacov7)            # Valor lambda promedio
plot(lambdacov7, type = "l")            # Gr?fica scree
screeplot(cprincov7, type = "lines")    # Otra forma de hacer la gr?fica scree
# Por las gr?ficas y por el valor promedio de los valores propios  se diria que se 
# retiene solamente el primer componente principal

## Facto Extra con cov
library("factoextra")
fviz_pca_ind(cprincov7)
fviz_pca_var(cprincov7)
# var nos muestra como hay una fuerte relaci?n entre las variables y el 1er comp princ
fviz_pca_biplot(cprincov7)
# Biplot nos muestra que no hay casi relaci?n entre los datos y las personas, ya que
# c/persona tiene diferente comportamiento para c/variable

## Aca vamos a interpretar el 1er comp princ como dificultad de c/persona para
#  acomodar c/u de las palabras
punt_7 <-cprincov7$scores
punt1_7 <-punt_7[,1] # Extraigo solo los scores del 1er comp prin
normp7<-(punt1_7-min(punt1_7))/(max(punt1_7)-min(punt1_7))*100  # Normalizo los scores
rankp7 <-sort(normp7) # Organizo de menor a mayor los scores
# Con el ranking hallado podemos ver que la persona que tuvo mayor dificultad fue la 1
# mientras que por otro lado la 2 fue la de menos dificultad (algo que ya se podia 
# evidencia a partir del biplot).
#######################################################################################
####################################### 12.8 #################################################
setwd("/Users/plazas/Dropbox/DAVID-SAMUEL/_David_/EAFIT/2019-1/Estadistica2/multivariate_analysis")
t_3_8 <- read.table("T3_8_GLUCOSE.dat")
colnames(t_3_8) <- c("y1","y2", "y3","x1","x2", "x3")
cov8 <- cov(t_3_8)              # Su diagonal nos da las varianzas

             # Comp prin cov
cprincov8 <- princomp(t_3_8)
sprcov8 <- summary(cprincov8, loadings = TRUE)
# En el 1er comp se explica un 55.6% de la varianza, mientras
# con el 2do acum se explica un 74.8%.

            # Comp prin cor
cprincor8 <- princomp(t_3_8,cor = TRUE)
sprcor8 <- summary(cprincor8, loadings = TRUE)
# En el 1er comp se explica un 36.3% de la varianza, mientras
# con el 2do acum se explica un 54.3%.

# Analizando la proporci?n que explican cada uno de los comp princ podemos observar 
# que existe gran diferencia entre trabajar con la cov o trabajar con la cor, como hay 
# unos componentes principales dominados por algunas variables debido a unas varianzas
# tan altas es recomendable trabajar con la cor (esto se ve ya que cl)

lambdacor8 <- cprincor8$sdev^2         # Valores propios de los comp princ
mlambda8 <- mean(lambdacor8)           # Valor lambda promedio
plot(lambdacor8,type = "l")            # Gr?fica scree
screeplot(cprincor8, type = "lines")   # Otra forma de hacer la gr?fica scree
# Por las gr?ficas uno solo retendria el primer componente principal pero al 
# analizar el valor promedio de los valores propios  se diria que se retiene 
# los dos primeros componentes principales.

## Facto Extra con cor
library("factoextra")
fviz_pca_var(cprincor8)
# Var nos muestra que existe una fuerte relaci?n entre las variables x2, y3 con el 1er
# componente principal
fviz_pca_biplot(cprincor8)

## Aca vamos a interpretar el 1er comp princ como el indice de glucosa de c/persona en
#  la sangre
punt_8 <- cprincor8$scores
punt1_8 <- punt_8[,1]   # Referente al primer comp principal
punt2_8 <- punt_8[,2]  
normp1_8 <- (punt1_8-min(punt1_8))/(max(punt1_8)-min(punt1_8))*100 #Normalizo 1
normp2_8 <- (punt2_8-min(punt2_8))/(max(punt2_8)-min(punt2_8))*100 #Normalizo 2
rankp1_7 <- order(normp1_8)    # Ordeno 1
rankp2_7 <- order(normp2_8)    # Ordeno 2
# Seg?n el comp 1er comp principal la persona 44 tiene el mayor indice de glucosa en la
# sangre mientras que la persona 29 es la que menos tiene
#######################################################################################
####################################### 12.9 ##########################################
setwd("/Users/plazas/Dropbox/DAVID-SAMUEL/_David_/EAFIT/2019-1/Estadistica2/multivariate_analysis")
t_4_3 <- read.table("T4_3_HEMATOL.dat")
cov9 <- cov(t_4_3)

         # Comp prin cov
cprincov9 <- princomp(t_4_3)
sprcov9 <- summary(cprincov9, loadings = TRUE)
# En el 1er comp se explica un 99.9% de la varianza.

         # Comp prin cor
cprincor9 <- princomp(t_4_3, cor = TRUE)
sprcor9 <- summary(cprincor9, loadings = TRUE)
# En el 1er comp se explica un 40% de la varianza, mientras
# con el 2do acum se explica un 63.7%.

# Analizando la proporci?n que explican cada uno de los comp princ podemos observar 
# que existe gran diferencia entre trabajar con la cov o trabajar con la cor, como hay 
# unos componentes principales dominados por algunas variables debido a unas varianzas
# tan altas es recomendable trabajar con la cor.

lambdacor9 <- cprincor9$sdev^2       # Valores propios de los comp princ
mlambda9 <- mean(lambdacor9)         # Valor lambda promedio
plot(lambdacor9, type = "l")         # Gr?fica scree
screeplot(cprincor9,type = "lines")  # Otra forma de hacer la gr?fica de scree
# Por las gr?ficas  y al analizar el valor promedio de los valores propios 
# se retendrian los primeros 3 componentes principales.

####################################### 12.12 ##########################################

setwd("/Users/plazas/Dropbox/DAVID-SAMUEL/_David_/EAFIT/2019-1/Estadistica2/multivariate_analysis")
t_5_6 <- read.table("T5_6_PILOT.dat")
ucov12 <- cov(t_5_6[,2:7])            # Unpooled covariance (Covarianza conjunta)

         # Unpooled covariance
cprincou12 <- princomp(t_5_6[,2:7])               # Comp princ
sprincou12 <- summary(cprincou12, loadings= TRUE) # Resumen de los comp princ

lambdau12 <- cprincou12$sdev^2          # Lambda unpooled
mlambdau12 <- mean(lambdau12)           # Lambda prom unpooled
plot(lambdau12, type = "l")             # Gr?fica de scre
screeplot(cprincou12, type = "lines")   # Otra forma de hacer la gr?fica de scree
# Por las gr?ficas  y al analizar el valor promedio de los valores propios 
# se retendrian los dos primeros componentes principales.
