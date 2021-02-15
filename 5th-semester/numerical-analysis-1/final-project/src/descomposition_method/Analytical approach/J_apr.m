function jf = J_apr(alpha, f, var, N)
    syms lambda
    func = (var - lambda).^(alpha-1).*subs(f,var,lambda);
    aprox = vpa(taylor(func, lambda, 'Order', N+2), 6);
   
    jf = 1./gamma(alpha).*int(aprox, lambda, 0, var);
end

