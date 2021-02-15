function x = runge_kutta(f,h,T,x0)
    N = ceil(T/h);
    x = zeros(length(x0),N);
    x(:,1) = x0;
    for k=2:N
        k1 = f(x(:,k-1));
        k2 = f(x(:,k-1) + k1*h/2);
        k3 = f(x(:,k-1) + k2*h/2);
        k4 = f(x(:,k-1) + k3*h);
        
        x(:,k) = x(:,k-1) + h*(k1/6 + k2/3 + k3/3 + k4/6);
    end
end

