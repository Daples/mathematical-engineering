%% Parameters and Equilibrium Points
Ra = 500;
Rb = 7500;
Rc = 17.5439;
Vcc0 = 15;
u0 = 1000;
RC = 1;
[x0,y0,z0] = equilibriumPoints(100/Ra,100/Rb,100/Rc,u0);

i = 1;
operPoint = [x0(i); y0(i); z0(i)];

%% Linearization
A = [0 -1/RC -1/RC;
     1/RC 100/(Ra*RC) 0;
     operPoint(3)/RC 0 1/RC*(operPoint(1)-100/Rc)];
B = [0; 0; 100/(Rb*RC)];
C = [0 0 1];
D = 0;

system = ss(A, B, C, D);

%% Simulation
h = 0.001;
T = 35;
tout = 0:h:T - h;
u = @(t) 1001*(t == 0) + 1000*(t ~= 0);

f = @(t, x)A*x + B*(u(t/h) - u0);
delta = [0; 0; 0];
x0prima = operPoint + delta;

xLinear = runge_kutta_time(f,h,T,delta);

%% Transfer functions
tm = 1;
transfer = tf(system);
transferD = c2d(transfer, tm);

%% Analytic transfer function
syms s t k z
n = length(A);
transferaux = ((C*((s*eye(n) - A)\B) + D));
[N,D] = numden(transferaux);
Nc = coeffs(N);
Dc = coeffs(D);
Nc = Nc/Dc(length(Dc));
Dc = Dc/Dc(length(Dc));

transferaux = vpa(poly2sym(fliplr(Nc),s)/poly2sym(fliplr(Dc),s),5);

%% Analytic Discrete transfer function
time_response = ilaplace(transferaux/s);
discrete_time_response = subs(time_response, t, tm*k);
zetat = ztrans(discrete_time_response);

transferauxD = (1 - z^-1)*zetat;

[N,D] = numden(transferauxD);
Nc = coeffs(N);
Dc = coeffs(D);

Nc = Nc/Dc(length(Dc));
Dc = Dc/Dc(length(Dc));

Nc = Nc(abs(Nc) > 1e-10);
Dc = Dc(abs(Dc) > 1e-10);

transferauxD = vpa(poly2sym(fliplr(Nc),z)/poly2sym(fliplr(Dc),z),5);

