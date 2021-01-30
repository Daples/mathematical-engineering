function jf = J_nabla(alpha, f, var, value_var)
    function res = Nabla(alpha, f, var, n, h)
        is = 1:n;
        vect1 = alpha - is + n;
        vect2 = - is + 1 + n;
        fih = subs(f, var, is*h);
        
        sumatoria = sum(gamma(vect1)./gamma(vect2).*fih, 2);
        
        res = h.^alpha./gamma(alpha).*sumatoria;
    end
    
    n = 10;
    h = value_var/n;
    jf = eval(1/h*((n*h - value_var)*Nabla(alpha, f, var, n-1, h) + ...
              (value_var - (n-1)*h)*Nabla(alpha, f, var, n, h)));
end

