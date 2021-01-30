function [sys2, t1] = approximation(ts, ys, us)
    %% Information from curve
    yss = ys(length(ys));
    mP = (max(ys) - yss)/yss;
    tp = ts(ys == max(ys));
    
    %% Aproximation
    zeta = 1/sqrt(1 + (pi/log(mP))^2);
    w0 = pi/(tp*sqrt(1 - zeta^2));
    k = yss/us;
    
    sys2 = tf(k*w0^2, [1, 2*zeta*w0, w0^2]);
    
    %% Time of growth
    ss1 = abs(0.1*yss - ys);
    t1 = ts(ss1 == min(ss1));
    
end

