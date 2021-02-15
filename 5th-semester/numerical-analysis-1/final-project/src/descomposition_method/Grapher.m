syms t

% Aproximation by polinomials
x_real = (2*exp(-2*t))/3 + exp(t)/3;
y_real = exp(t)/3 - (4*exp(-2*t))/3;

xd = y_decomposed(1);
yd = y_decomposed(2);

tsim = [0 7.5];

figure(1);
fplot(x_real, tsim)
hold on
fplot(xd, tsim, 'r')

figure(2);
fplot(y_real, tsim)
hold on
fplot(yd, tsim, 'r')

% plot(y_apr(1,:), y_apr(2,:));

clear x_real y_real t tsim xd yd
