# Punto 3
data(USArrests) 
PCcor3 <- princomp(USArrests, cor=TRUE)

# Criterio 1: 80%
SPCcor3 <- summary(PCcor3, loadings=TRUE)

# Criterio 2: Mean Eigen
eigen3 <- PCcor3$sdev^2
meanEigen3 <- mean(eigen3)

# Criterio 3: Scree
screeplot(PCcor3, type = "lines")

# Ranking Indice Violencia
scoresPC3 <- SPCcor3$scores
scores1PC3 <- scoresPC3[,1]
normScores3 <- (scores1PC3-min(scores1PC3))/(max(scores1PC3)-min(scores1PC3))*100
rankScores3 <-sort(normScores3, decreasing = TRUE)

# Gráficas:
library("factoextra")
# Dos comp. ppales.
fviz_pca_ind(PCcor3)
# Circ. Correlacion
fviz_pca_var(PCcor3)
# Biplot
fviz_pca_biplot(PCcor3)

# Punto 4
# lectura de datos
setwd("/Users/plazas/Dropbox/DAVID-SAMUEL/_David_/EAFIT/2019-1/Estadistica2/")
dioxido <- read.delim("dioxido.txt")
dioxido <- dioxido[,3:8] # Omitir la primera variable
rownames(dioxido)<-c("phoenix","little Rock","San Francisco","Denver","Harford","Wilmington","Washington",
                     "Jacksonville","Miami","Atlanta","Chicago","Indianapolis","Des Moines","Wichita",
                     "Louisville","New Orleans","Baltimore","Detroit","Minneapolis","Kansas City","St Louis",
                     "Omaha","Albuquerque","Albany","Buffalo","Cincinnati","Cleveland","Columbus",
                     "Philadelphia","Pittsburgh","Providence","Memphis","Nashville","Dallas","Hosuton","Salt Lake City",
                     "Norfolk","Richmond","Seatle","Charleston","Milwaukee")
PCcor4 <- princomp(dioxido, cor=TRUE)

# Criterios
# 1. 80%
SPCcor4 <- summary(PCcor4, loadings=TRUE)

# Criterio 2: Mean Eigen
eigen4 <- PCcor4$sdev^2
meanEigen4 <- mean(eigen4)

# Criterio 3: Scree
screeplot(PCcor4, type = "lines")

# Ranking Índice Calidad Vida
scoresPC4 <- SPCcor4$scores
scores1PC4 <- scoresPC4[,1]
normScores4 <- (scores1PC4-min(scores1PC4))/(max(scores1PC4)-min(scores1PC4))*100
rankScores4 <-sort(normScores4, decreasing = TRUE)

# Ranking Índice tiempo húmedo
scores2PC4 <- scoresPC4[,2]
norm2Scores4 <- (scores2PC4-min(scores2PC4))/(max(scores2PC4)-min(scores2PC4))*100
rank2Scores4 <-sort(norm2Scores4, decreasing = TRUE)

# Ranking Índice Tipo de CLima
scores3PC4 <- scoresPC4[,3]
norm3Scores4 <- (scores3PC4-min(scores3PC4))/(max(scores3PC4)-min(scores3PC4))*100
rank3Scores4 <-sort(norm3Scores4, decreasing = TRUE)

# Gráficas:
library("factoextra")
# Dos comp. ppales.
fviz_pca_ind(PCcor4)
# Circ. Correlacion
fviz_pca_var(PCcor4)
# Biplot
fviz_pca_biplot(PCcor4)

