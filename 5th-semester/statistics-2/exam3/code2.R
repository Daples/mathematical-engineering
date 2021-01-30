rm(list=ls())

crimen<- read.delim("/Users/plazas/Dropbox/DAVID-SAMUEL/_David_/EAFIT/2019-1/Estadistica2/parcial3/crimen.txt")
rownames(crimen)<-c("Atlanta","Boston "," Chicago"," Dallas","Denver","Detroit","Hartford ",
                    "Honolulu","Houston"," Kansas","Angeles","New Orleans","New York","Portland",
                    "Tucson","Washington")   

cov(crimen[,2:8])
z<-princomp(crimen[,2:8],cor = TRUE) 
summary(z,loadings = TRUE)

library("factoextra")
fviz_pca_ind(z)
fviz_pca_var(z)
fviz_pca_biplot(z)


puntuaciones<-z$scores
plot(puntuaciones[,1],puntuaciones[,2],xlab = "pc1", ylab = "pc2",type="n",lwd=2)
text(puntuaciones[,1],puntuaciones[,2],labels=abbreviate(rownames(crimen)),cex=0.7,lwd=2)
z1<-puntuaciones[,1]
iv<-(z1-min(z1))/(max(z1)-min(z1))*100
sort(iv)
