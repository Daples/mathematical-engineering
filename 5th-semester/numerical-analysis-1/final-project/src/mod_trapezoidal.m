function y = mod_trapezoidal(f,alpha,T,N)
%mod_trapezoidal Summary of this function goes here
%   Integral de Riemann-Liouville entre 0 y T
    h=T/N;
    
    y=((N-1)^(alpha+1)-(N-alpha-1)*(N^alpha))*((h^alpha)*f(0)) + ...
        (h^alpha)*f(T);
    sum = 0;
    for i=1:(N-1)
       sum = sum + ((N-i+1)^(alpha+1) -2*((N-i)^(alpha+1)) + ...
           (N-i-1)^(alpha+1))*((h^alpha)*f(i*h)); 
    end
    
    y = y + sum;
    y = y/gamma(alpha+2);
end

