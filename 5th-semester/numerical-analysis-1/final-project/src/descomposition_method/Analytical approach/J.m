function jf = J(alpha, f, var)
    syms lambda
    jf = vpa(1./gamma(alpha).* ...
         int((var - lambda).^(alpha-1) ... 
         .*subs(f,var,lambda), lambda, 0, var), 6);
end

