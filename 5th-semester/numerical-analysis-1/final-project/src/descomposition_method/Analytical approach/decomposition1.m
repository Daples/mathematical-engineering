function sol = decomposition1(N, system, alpha, vars, indvar, initial)
    syms t l
    n = length(vars);
    % System decomposed
    [a, f, g, nonlin] = decompose(system, string(vars));
    
    % N aproximations of the function
    xs = sym(zeros(n, N));
    % Initial aproximation
    xs(:,1) = initial + J_apr(alpha, g, indvar, N);
    
    % Don't calculate adomian polynomials if not neccesarry.
    if nonlin
        xs_sym = reshape(sym('x', [1 N*n], 'real'), [n N]);

        syms l real
        lrow = l.^(0:N-1);
        lk = repmat(lrow, n, 1);

        Al = subs(f, vars, sum(lk.*xs_sym, 2));
    end
    for j=2:N+1
        % Adomian polynomials aproximaions
        if nonlin
            Al = 1/(j-1)*diff(Al, l);
            Aj = subs(subs(Al, l, 0), xs_sym(:, 1:j-1), xs(:, 1:j-1));
            Ja = J_apr(alpha, Aj, indvar, N);
        else
            Ja = 0;
        end
        
        % Linear terms
        ax = a*xs(:,(j-1));
        Jax = J_apr(alpha, ax, indvar, N);
        
        % Next term of the series
        xs(:,j) = Jax + Ja;      
    end
    
    sol = sum(xs,2);
end

