# Importar datos
data <- read.csv('/Users/plazas/Documents/statistics/apprentices.csv')
eng <- data[1:6]
pilots <- data[7:12]
n1 <- 20
n2 <- 20

# 5.18
# a)

# Vectores medias
mediaEng <- colMeans(eng)
mediaPilots <- colMeans(pilots)

# Matrices de covariazas
Seng <- cov(eng)
Spilots <- cov(pilots)

Sp <- ((n1 - 1)*Seng + (n2 - 1)*Spilots)/(n1 + n2 - 2)

# Estadístico T2 de prueba
T2 <- t(mediaEng - mediaPilots)%*%solve(((n1 + n2)/(n1*n2))*Sp)%*%(mediaEng - mediaPilots)

v <- n1 + n2 -2
p <- 6
alpha <- 0.01

Fr <- ((v - p + 1)/(v*p))*T2
Faux <- qf(alpha, p, n1+n2-p-1,lower.tail = FALSE)

# b)

for (i in c(1:p)) {
  var1 <- eng[i]
  var2 <- pilots[i]
  var1bar <- mediaEng[i]
  var2bar <- mediaPilots[i]
  
  t <- (var1bar - var2bar)/sqrt((n1+n2)/(n1*n2)*Sp[i,i])
  taux <- qt(alpha/2,n1+n2-2,lower.tail = FALSE)
  print('Estadístico t2')
  print(t)
  if (abs(t)>taux){
    print('Rechazo Ho')
  } else {
    print('No hay sufuciente evidencia para rechazar Ho')
  }
}


# Coeficiente de función discriminante: a*
a <- solve(Sp)%*%(mediaEng - mediaPilots)

#######################
# Importar datos
data2 <- read.csv('/Users/plazas/Documents/statistics/wordsverbs.csv')
d1 <- data2[6]
d2 <- data2[7]
d <- data2[6:7]
n <- 15
Sd <- cov(d)
mediad <- colMeans(d)



# Estadístico
T2r <- t(mediad)%*%solve(Sd/n)%*%mediad
vr <- n
pr <- 2
alpha <- 0.05

Frr <- ((vr - pr + 1)/(vr*pr))*T2r
Fauxr <- qf(alpha, p, n-1,lower.tail = FALSE)

# Función discriminante
ar <- solve(Sd)%*%mediad

# Test univariado
for (i in c(1:pr)) {
  var1r <- d[i]
  meand <- colMeans(var1r)
  
  tr <- sqrt(n)*meand/sqrt(Sd[i,i])
  tauxr <- qt(alpha/2,n-1,lower.tail = FALSE)
  print('Estadístico t2')
  print(tr)
  if (abs(t)>tauxr){
    print('Rechazo Ho')
  } else {
    print('No hay sufuciente evidencia para rechazar Ho')
  }
}
