library(simmer)
library(simmer.plot)
set.seed(1234)

lambda <- 2
mu <- 4
c <- 7
T <- 600

m.queue <- trajectory() %>%
  seize('server', amount=1) %>%
  timeout(function() rexp(1, mu)) %>%
  release('server', amount=1)

mm77.env <- simmer() %>%
  add_resource('server', capacity=c, queue_size=0) %>%
  add_generator('arrival', m.queue, function() rexp(1, lambda)) %>%
  run(until=T)

get_mon_arrivals(mm77.env) %>%
  with(sum(!finished) / length(finished))

rho <- lambda/mu
pi_0 <- 1/( sum( rho^(0:c)/factorial(0:c) ) )
pi_c <- ((rho^c)/factorial(c))*pi_0
Ls <- rho*(1 - pi_c)
Ts <- Ls/lambda
mm77.N <- Ls

plot(get_mon_resources(mm77.env), 'usage', 'server', items=c('system','queue')) + ylim(-0.05, 0.6) +
  geom_hline(yintercept=mm77.N)
