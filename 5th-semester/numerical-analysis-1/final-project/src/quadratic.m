function y = quadratic(f,alpha,T,N)
%quadratic Summary of this function goes here
%   Integral de Riemann-Liouville entre 0 y T
    h=T/(2*N);
    sum = 0;
    
    for i=0:(N-1)
        A=((2^alpha)*(h^alpha))*((((N-i-1)^(alpha+1))*(2-alpha+4*i-4*N))...
            + ((N-i)^alpha)*(2+(alpha^2)+4*(i^2)+i*(6-8*N)...
            + 3*alpha*(1+i-N)-6*N +4*(N^2)));
        B=((2^(alpha+2))*(h^alpha))*(((N-i-1)^(alpha+1))*(alpha-2*i+2*N)...
            + ((N-i)^(alpha+1))*(2+alpha+2*i-2*N));
        C=-(((2^alpha)*(h^alpha))*(((N-i)^(alpha+1))*(2+alpha+4*i-4*N)...
            + ((N-i-1)^alpha)*((alpha^2)+2*i-3*alpha*i+4*(i^2)-2*N...
            +3*alpha*N-8*i*N+4*(N^2))));
        sum = sum + A*f((2*i)*h) + B*f((2*i+1)*h) + C*f((2*i+2)*h);
    end
    y = sum;
    y = y/gamma(alpha+3);
end