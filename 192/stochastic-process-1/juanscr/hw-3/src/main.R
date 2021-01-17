## Homework for Stochastic Process subject.
##
## Tested with R 3.6.1


# Parameters of simulation
c = 7
N = 7
max_time = 1000
rate_0 = 2
rate_1 = 4
show = FALSE

# Data structures
set.seed(5)
ts = list()
ls = list()
attendants = rep(0, c)
arrival_time = rexp(1, rate = rate_0)
t = arrival_time
n = 0

# Simulation
while (t < max_time) {
  if (t == arrival_time) {
    # Arrival of customer
    for (i in 1:length(attendants)) {
      if (attendants[i] == 0) {
        if (show) {
          print(paste("Arriving customer at", t), quote=FALSE)
        }
        tf = rexp(1, rate = rate_1)
        ts = append(ts, tf)
        attendants[i] = t + tf
        n = n + 1
        break
      }
    }
    arrival_time = t + rexp(1, rate = rate_0)
  }
  else {
    # Finish attending
    for (i in 1:length(attendants)) {
      if (t == attendants[i]) {
        if (show){
          print(paste("Finish attending customer at", t), quote=FALSE)
        }
        attendants[i] = 0
        n = n - 1
        break
      }
    }
  }
  
  # Update timer
  min0 = arrival_time
  for (attendant in attendants) {
    if (attendant != 0 && attendant < min0) {
      min0 = attendant
    }
  }
  
  # Update ls
  if (as.integer(t) != as.integer(min0)) {
    delta = as.integer(min0) - as.integer(t)
    for (i in 1:delta) {
      ls = append(ls, n)
    }
  }
  
  t = min0
  
}

### Analyzing data
# Theoretical values
p = rate_0 / rate_1
pi0 = 0
for (i in 0:c) {
  pi0 = pi0 + p^i/factorial(i)
}
pi0 = pi0 ^ -1
pic = p^c / factorial(c) * pi0

ls_t = p * (1 - pic) # Theoretical ls
ts_t = 1 / rate_1 # Theoretical ts

# Estimated values
ts_s = mean(unlist(ts, use.names = FALSE)) # Simulated ts
ls_s = mean(unlist(ls, use.names = FALSE)) # Simulated ls

### Obtaining plots
plotter <- function(xs, real) {
  y = list()
  for (i in 1:length(xs)) {
    aux = unlist(xs[1:i], use.names = FALSE)
    y = append(y, mean(aux))
  }
  x = (1:length(xs))
  y = unlist(y, use.names = FALSE)
  y_real = unlist(rep(real, length(xs)), use.names = FALSE)
  plot(x, y, type="l", col="red")
  lines(x, y_real, col="blue")
  legend("bottomright", c("real", "simualted"), fill = c("blue", "red"))
}