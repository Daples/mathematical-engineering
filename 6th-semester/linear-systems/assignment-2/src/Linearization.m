%% Equilibrium Points
% Parameters
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
[A,B] = linmod('rosslerSystemLinear', operPoint, 0,'v5');
C = [0 0 1];
D = 0;
system = ss(A, B, C, D);

%% Analytic Linearization
Aaux = [0 -1/RC -1/RC;
        1/RC 100/(Ra*RC) 0;
        operPoint(3)/RC 0 1/RC*(operPoint(1)-100/Rc)];
    
Baux = [0; 0; 100/(Rb*RC)];

%% Simulation
h = 0.001;
T = 100;
u = 1002;
f = @(x)Aaux*x + Baux*(u - u0);
delta = [0;0;0];
x0prima = operPoint + delta;
tout = 0:h:T - h;

xLinear = runge_kutta(f,h,T,delta);

rossler = @(x)[-x(2) - x(3); ...
               x(1) + 100/Ra*x(2); ...
               (u+Vcc0)*100/Rb + x(3)*(x(1) - 100/Rc)]/RC;

xLinearComparar = xLinear + operPoint;
xOg = runge_kutta(rossler,h,T,x0prima);

%% Linear VS nonLinear
plotPL(3, {tout}, {xOg(3,:); xLinearComparar(3,:)}, [],[],'$t$','$y$', ...
       ["Rossler System"; "Linear Approximation"],[], 20, {'k';'r'});
