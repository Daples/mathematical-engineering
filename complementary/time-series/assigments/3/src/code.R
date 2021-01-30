
grad_p1 = function(theta){
  theta1 = theta[1]
  theta2 = theta[2]
  term = (1 + theta1^2 + theta2^2)
  p1 = ((-1 + theta2)*term - 2*theta1*(-theta1 + theta1*theta2))/(term^2)
  p2 = (theta1*term - 2*theta2*(-theta1 + theta1*theta2))/(term^2)
  return(c(p1,p2))
}

grad_p2 = function(theta){
  theta1 = theta[1]
  theta2 = theta[2]
  term = (1 + theta1^2 + theta2^2)
  p1 = (2*theta1*theta2)/(term^2)
  p2 = (2*theta2^2 - term)/(term^2)
  return(c(p1,p2))
}
 

p1 = function(theta){
  theta1 = theta[1]
  theta2 = theta[2]
  return (abs((-theta1 + theta1*theta2)/(1 + theta1^2 + theta2^2)))
}
  

p2 = function(theta){
  theta1 = theta[1]
  theta2 = theta[2]
  return (abs((-theta2)/(1 + theta1^2 + theta2^2)))
}


optimize = function(f, grad, p0, h, tol){
  thetas = list(p0)
  i = 2
  while (TRUE){
    prev_theta = thetas[[i-1]]
    new_theta = prev_theta + h*grad(prev_theta)
    thetas[[i]] = new_theta
    if (abs(f(new_theta)-f(prev_theta)) < tol){
      break
    }
    i = i+ 1
  }
  return(thetas[[length(thetas)]])  
}
 

h = 0.01
tol = 1e-10
p0 = c(0, 0)
thetas_rho1 = optimize(p1, grad_p1, p0, h, tol)
thetas_rho2 = optimize(p2, grad_p2, p0, h, tol)
