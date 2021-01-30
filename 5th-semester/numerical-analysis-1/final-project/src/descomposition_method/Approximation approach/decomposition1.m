function y = decomposition1(N, system, alpha, vars, indvar, initial, tsim)
    n = length(vars);
    % System decomposed
    [a, f, g, nonlin] = decompose(system, string(vars));
    
    % Don't calculate adomian polynomials if not neccesarry.
    if nonlin
        xs_sym = reshape(sym('x', [1 N*n], 'real'), [n N]);

        syms l real
        lrow = l.^(0:N-1);
        lk = repmat(lrow, n, 1);
        
        % Calculate the adomian polinomials
        As = sym(zeros(length(system), N+1));
        As(:,1) = subs(f, vars, sum(lk.*xs_sym, 2));
        for j=2:N+1
            As(:,j) = 1/j*diff(As(:,j-1), l);
        end
    end
    y = zeros(length(system), length(tsim));
    y(:,1) = initial;
    
    % Simulate for each t
    for i=2:length(tsim)
        ti = tsim(i);
        
        % N aproximations of the function
        xs = zeros(n, N);
        % Initial aproximation
        xs(:,1) = initial + J_nabla(alpha, g, indvar, ti);
        
        for j=2:N+1
            % Adomian polynomials aproximaions
            if nonlin
                Aj = subs(subs(As(:,j-1), l, 0), xs_sym(:, 1:j-1), xs(:, 1:j-1));
                Ja = J_nabla(alpha, Aj, indvar, ti);
            else
                Ja = 0;
            end

            % Linear terms
            ax = a*xs(:,(j-1));
            Jax = J_nabla(alpha, ax, indvar, ti);

            % Next term of the series
            xs(:,j) = Jax + Ja;
            
            % The aproximation of the function in that time
            y(:,i) = y(:,i) + xs(:,j);
        end
    end
end



