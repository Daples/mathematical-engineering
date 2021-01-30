t = 100; % Final time
h = 1e-3; % Step
x0 = [0 -6.78 0.02]; % Initial Conditions

% Parametres
RC = 1;
Ra = 500;
Rb = 7500;
Rc = 17.5439;
vcc0 = 15;

n = ceil(t/h); % Number of iterations
tout1 = 0:h:t-h; % Time of simulation

x = zeros(length(x0), ceil(t/h));
x(:,1) = x0;

% Euler
for i=1:n-1
    v = [-x(2,i) - x(3,i), ...
         x(1,i) + 100/Ra*x(2,i), ...
         vcc0*100/Rb + x(3,i)*(x(1,i) - 100/Rc)];
    x(:,i+1) = x(:,i)' + h/RC*v;
end
x_euler1 = x;

% Runge kutta
x = zeros(length(x0), ceil(t/h));
x(:,1) = x0;
for i=1:n-1
    k1 = [-x(2,i) - x(3,i), ...
          x(1,i) + 100/Ra*x(2,i), ...
          vcc0*100/Rb + x(3,i)*(x(1,i) - 100/Rc)];
    k2 = [-(x(2,i) + h*k1(1)/2) - (x(3,i)+ h*k1(1)/2), ...
          (x(1,i) + h*k1(2)/2) + 100/Ra*(x(2,i)+ h*k1(2)/2), ...
          vcc0*100/Rb + (x(3,i)+ h*k1(3)/2)*(x(1,i)+ h*k1(3)/2 - 100/Rc)];
    k3 = [-(x(2,i) + h*k2(1)/2) - (x(3,i)+ h*k2(1)/2), ...
          (x(1,i) + h*k2(2)/2) + 100/Ra*(x(2,i)+ h*k2(2)/2), ...
          vcc0*100/Rb + (x(3,i) + h*k2(3)/2)*(x(1,i)+ h*k2(3)/2 - 100/Rc)];

    k4 = [-(x(2,i) + h*k3(1)) - (x(3,i)+ h*k3(1)), ...
          (x(1,i) + h*k3(2)) + 100/Ra*(x(2,i)+ h*k3(2)), ...
          vcc0*100/Rb + (x(3,i)+ h*k3(3))*(x(1,i)+ h*k3(3) - 100/Rc)];

    x(:,i+1) = x(:,i)' + h/RC*(k1/6 + k2/3 + k3/3 + k4/6);
end
x_runge1 = x;

clear t h x0 RC Ra Rb Rc vcc0 n x i k1 k2 k3 k4 v