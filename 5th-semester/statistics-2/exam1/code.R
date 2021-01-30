# 4.
cafe <- read.delim("/Users/plazas/Downloads/cafe.txt")
valores <- cafe[1:10,2:7] # Seleccionar los números sin títulos

# a)
vectMedias <- colMeans(valores) # Vector medias
S <- cov(valores) # Matriz de covarianza muestral
R <- cor(valores) # Matriz de correlaciones muestral

# b)
eigS <- eigen(S,only.values = TRUE) # Valores propios de S
detS <- det(S) # Determinante S
trS <- sum(eigS[["values"]]) # Traza S

# c) 
a <- rbind(0.5827, 0.6409, 0.2746, 0.3107, 0.2210, 0.1693)
b <- rbind(0.5335, 0.6936, 0.1116, 0.4469, 0.0020, 0.1478)

z1 <- 0.5827*cafe["Intar"]+0.6409*cafe["Aroma"]+0.2746*cafe["Cuerpo"]+0.3107*cafe["AcidezTasa"]+0.2210*cafe["Amargo"]+0.1693*cafe["Astr"]
z2 <- 0.5335*cafe["Intar"]-0.6936*cafe["Aroma"]-0.1116*cafe["Cuerpo"]+0.4469*cafe["AcidezTasa"]-0.0020*cafe["Amargo"]+0.1478*cafe["Astr"]


z1Media <- colMeans(z1) # Media z1
z2Media <- colMeans(z2) # Media z2

zMedia <- rbind(z1Media,z2Media) # Media de las combinaciones lineales
zCov <- t(a)%*%S%*%b # Matriz covarianzas


# e)
n = 10;
Sa <- diag(6)*0
for (i in 1:10) {
  yi = as.matrix(valores[i,1:6])
  Sa <- Sa + t(yi)%*%yi
}
Sa <- (1/(n-1))*Sa - n*t(vectMedias)%*%vectMedias


