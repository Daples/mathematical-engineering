function y = adamsbashfort(f, alpha, y0, T, N)

    function p = calc_p(j, h, y0, alpha, f, b, y, m)
        sum = 0;
        for k=0:m-1
            sum = sum + ((j*h)^k/factorial(k))*y0(k+1,:);
        end
        sum2 = 0;
        for k=0:j-1
            [fx, fy, fz] = f(k*h, y(:,k+1), alpha);
            sum2 = sum2 + b(:,j-k)'.*[fx, fy, fz];
        end
        
        term1 = altpow(h, alpha)./altgamma(alpha + 1);
        
        p = sum + term1.*sum2;
    end
    
    function yj = calc_y(j, h, y0, alpha, f, a, y, m, p)
        sum = 0;
        for k=0:m-1
            sum = sum + ((j*h)^k/factorial(k))*y0(k+1,:);
        end
        
        sum2 = 0;
        for k=0:j-1
            [fx, fy, fz] = f(k*h, y(:,k+1), alpha);
            sum2 = sum2 + a(:,j-k)'.*[fx, fy, fz];
        end
        [fp, fpy, fpz] = f(j*h, p, alpha);
        [f0, f0y, f0z] = f(0,y(:,1), alpha);
        term = [fp, fpy, fpz] + (altpow(j-1, alpha+1) - (j-1-alpha).*altpow(j,alpha)).*[f0, f0y, f0z];
        yj = sum + altpow(h, alpha)./altgamma(alpha + 2).*(term + sum2);
        
    end

    h = T/ N;
    m = ceil(alpha);
    b = zeros(length(y0),N);
    a = zeros(length(y0),N);
    for k=1:N
        b(:,k) = altpow(k, alpha) - altpow(k-1, alpha);
        a(:,k) = altpow(k+1,alpha + 1) - 2*altpow(k, alpha+1) + altpow(k-1, alpha+1);
    end
    y = zeros(length(y0),N+1);
    y(:,1) = y0(1,:);
    for j=1:N
       p = calc_p(j, h, y0, alpha, f, b, y, m);
       y(:,j+1) = calc_y(j, h, y0, alpha, f, a, y, m, p);           
    end
    
end

