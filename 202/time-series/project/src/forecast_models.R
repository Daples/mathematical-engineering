source("arima.R") # <- model_auto
source("arimax.R") # <- model_arimax
source("arima_lags.R") # <- model_arima9,1,9 , model_sar1_9xARMA(0,1,9)
source("tools.R")

h <- dim(xreg_new)[1]

# Forecast
pred_m1 <- forecast(model_auto, h)
pred_m2 <- forecast(model_arimax, xreg = xreg_new)
pred_m3 <- forecast(model_ar9, h)
pred_m4 <- forecast(model_sar1, h)
pred_m5 <- rep(0, N - t)
pred_m5[1] <- JNJ[length(JNJ)] + ugarchforecast(garch_model, n.ahead = 1)@forecast$seriesFor
for (i in 2:length(pred_m5)){
  pred_m5[i] <- pred_m5[i-1] + ugarchforecast(garch_model, n.ahead = 1)@forecast$seriesFor
}

# Plot forecast
pdf(file="figs/forecast.pdf", width = 10)
ggplot(data.frame(JNJ_new)) +
  geom_line(aes(x=time_new$Date, y = pred_m1$mean,
                colour = "ARIMA"), size = 1) +
  geom_line(aes(x=time_new$Date, y = pred_m2$mean,
                colour = "ARIMAX"), size = 1) +
  geom_line(aes(x=time_new$Date, y = pred_m3$mean,
                colour = "AR9"), size = 1) +
  geom_line(aes(x=time_new$Date, y = pred_m4$mean,
                colour = "SAR1"), size = 1) +
  geom_line(aes(x=time_new$Date, y = pred_m5,
                colour = "AR(1)xGARCH(1,1)"), size = 1) +
  geom_line(aes(x=time_new$Date, y = JNJ_new,
                colour = "Real"), size = 1) +
  scale_colour_manual("", 
                      breaks = c( "ARIMA",  "ARIMAX", "AR9", "SAR1", "AR(1)xGARCH(1,1)", "Real"),
                      values = c("red", "blue", "black", "pink", "green", "orange")) +
  xlab("Tiempo") +
  ylab("Predicciones") + 
  theme_minimal()
dev.off()

# Forecast with data
JNJ_complete <- as.vector(get_data(file))
# m1
pred_m1_data <- rep(0, N - t)
for (i in 1:(N - t)) {
  mod <- Arima(JNJ_complete[1:t+i], order=c(3,1,2))
  pre <- forecast(mod, 1)
  pred_m1_data[i] <- pre$mean
}

# m2
pred_m2_data <- rep(0, N - t)
for (i in 1:(N - t)) {
  mod <- Arima(JNJ_complete[1:t+i], order=c(3,1,2), xreg = xreg)
  pre <- forecast(mod, xreg=t(as.matrix(xreg_new[i,], nrow=1, ncol=4)))
  pred_m2_data[i] <- pre$mean
}

# m3
pred_m3_data <- rep(0, N - t)
for (i in 1:(N - t)) {
  mod <- Arima(JNJ_complete[1:t+i], order=c(9, 1, 9))
  pre <- forecast(mod, 1)
  pred_m3_data[i] <- pre$mean
}

# m4
pred_m4_data <- rep(0, N - t)
for (i in 1:(N - t)) {
  mod <- Arima(JNJ_complete[1:t+i], order=c(0, 1, 10), seasonal=list(order=c(1, 0, 0), period=9))
  pre <- forecast(mod, 1)
  pred_m4_data[i] <- pre$mean
}

# m5
pred_m5_data <- rep(0, N - t)
for (i in 1:(N - t)) {
  mod <- ugarchfit(spec=garch11.spec, data=JNJ_complete[1:t-1+i])
  pre <- JNJ_complete[t+i] + ugarchforecast(garch_model, n.ahead = 1)@forecast$seriesFor
  pred_m5_data[i] <- pre
}


# Plot with previous data
# ARIMA
pdf(file="figs/forecast_arima.pdf", width = 10)
ggplot(data.frame(JNJ_new)) +
  geom_line(aes(x=time_new$Date, y = pred_m1_data,
                colour = "ARIMA(3,1,2)"), size = 1) +
  geom_line(aes(x=time_new$Date, y = JNJ_new,
                colour = "Real"), size = 1) +
  scale_colour_manual("", 
                     breaks = c("ARIMA", "Real"),
                     values = c("black", "orange")) +
  xlab("Tiempo") +
  ylab("Predicciones") + 
  theme_minimal()
dev.off()

# ARIMAX
pdf(file="figs/forecast_arimax.pdf", width = 10)
ggplot(data.frame(JNJ_new)) +
  geom_line(aes(x=time_new$Date, y = pred_m2_data,
                colour = "ARIMAX(3,1,2)"), size = 1) +
  geom_line(aes(x=time_new$Date, y = JNJ_new,
                colour = "Real"), size = 1) +
  scale_colour_manual("", 
                      breaks = c("ARIMA", "Real"),
                      values = c("black", "orange")) +
  xlab("Tiempo") +
  ylab("Predicciones") + 
  theme_minimal()
dev.off()

# AR9
pdf(file="figs/forecast_ar9.pdf", width = 10)
ggplot(data.frame(JNJ_new)) +
  geom_line(aes(x=time_new$Date, y = pred_m3_data,
                colour = "AR(9)"), size = 1) +
  geom_line(aes(x=time_new$Date, y = JNJ_new,
                colour = "Real"), size = 1) +
  scale_colour_manual("", 
                      breaks = c("ARIMA", "Real"),
                      values = c("black", "orange")) +
  xlab("Tiempo") +
  ylab("Predicciones") + 
  theme_minimal()
dev.off()

# SAR1
pdf(file="figs/forecast_sar1.pdf", width = 10)
ggplot(data.frame(JNJ_new)) +
  geom_line(aes(x=time_new$Date, y = pred_m4_data,
                colour = "SAR(1)_9"), size = 1) +
  geom_line(aes(x=time_new$Date, y = JNJ_new,
                colour = "Real"), size = 1) +
  scale_colour_manual("", 
                      breaks = c("ARIMA", "Real"),
                      values = c("black", "orange")) +
  xlab("Tiempo") +
  ylab("Predicciones") + 
  theme_minimal()
dev.off()

#AR(1)xGARCH(1,1)
pdf(file="figs/forecast_garch.pdf", width = 10)
ggplot(data.frame(JNJ_new)) +
  geom_line(aes(x=time_new$Date, y = pred_m5_data,
                colour = "AR(1)xGARCH(1,1)"), size = 1) +
  geom_line(aes(x=time_new$Date, y = JNJ_new,
                colour = "Real"), size = 1) +
  scale_colour_manual("", 
                      breaks = c("ARIMA", "Real"),
                      values = c("black", "orange")) +
  xlab("Tiempo") +
  ylab("Predicciones") + 
  theme_minimal()
dev.off()

# All
pdf(file="figs/all.pdf", width = 10)
ggplot(data.frame(JNJ_new)) +
  geom_line(aes(x=time_new$Date, y = pred_m1_data,
                colour = "ARIMA"), size = 1) +
  geom_line(aes(x=time_new$Date, y = pred_m2_data,
                colour = "ARIMAX"), size = 1) +
  geom_line(aes(x=time_new$Date, y = pred_m3_data,
                colour = "AR9"), size = 1) +
  geom_line(aes(x=time_new$Date, y = pred_m4_data,
                colour = "SAR1"), size = 1) +
  geom_line(aes(x=time_new$Date, y = pred_m5_data,
                colour = "AR(1)xGARCH(1,1)"), size = 1) +
  geom_line(aes(x=time_new$Date, y = JNJ_new,
                colour = "Real"), size = 1) +
  scale_colour_manual("", 
                      breaks = c( "ARIMA",  "ARIMAX", "AR9", "SAR1", "AR(1)xGARCH(1,1)", "Real"),
                      values = c("red", "blue", "black", "pink", "green", "orange")) +
  xlab("Tiempo") +
  ylab("Predicciones") + 
  theme_minimal()
dev.off()

