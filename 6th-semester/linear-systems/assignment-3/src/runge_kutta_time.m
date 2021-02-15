function x = runge_kutta_time(f,h,T,x0)
    N = ceil(T/h);
    x = zeros(length(x0),N);
    x(:,1) = x0;
    t = 0;
    for k=2:N
        k1 = h*f(t, x(:,k-1));
        k2 = h*f(t + h/2, x(:,k-1) + k1/2);
        k3 = h*f(t + h/2, x(:,k-1) + k2/2);
        k4 = h*f(t + h, x(:,k-1) + k3);
        x(:,k) = x(:,k-1) + (k1 + 2*k2 + 2*k3 + k4)/6;
        t = t + h;
    end
end

