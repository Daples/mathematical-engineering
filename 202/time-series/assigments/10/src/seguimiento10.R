library(readxl)
library(dynlm)
library(strucchange)
data <- read_excel("dataUK.xlsx")

x <- ts(data$`interest rate`)
z <- ts(data$`eco sent`)

model <- dynlm(x ~ L(x, 1) + z + L(z, 1))

# 1 break point
breakpoints(x ~ 1, breaks=1)

# n break point
breakpoints(x ~ 1)
