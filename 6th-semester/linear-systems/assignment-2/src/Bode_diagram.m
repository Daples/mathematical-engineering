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
A = [0 -1/RC -1/RC;
     1/RC 100/(Ra*RC) 0;
     operPoint(3)/RC 0 1/RC*(operPoint(1)-100/Rc)];
B = [0; 0; 100/(Rb*RC)];
C = [0 0 1];
D = 0;

system = ss(A, B, C, D);
systemD = c2d(system, 1);

%% Bode
f1 = figure(1);
bode(system,'k')
[mag, phase, wout] = bode(system,'k');
set(findall(gcf,'-property','FontSize'),'FontSize',14) % -55.5xdB, w=1, 165deg
grid on

f2 = figure(2);
bode(systemD,'k')
[magD, phaseD] = bode(systemD,'k');
set(findall(gcf,'-property','FontSize'),'FontSize',14)
grid on

% Margins
margin = allmargin(system);

%% Information from Bode_diagram
% Resonance Peak
Mr = max(mag);
MrD = max(magD);

% Resonance Frequency
Wr = wout(mag == Mr);
WrD = wout(magD == MrD);

% Bandwidth
Wb = bandwidth(system);
WbD = bandwidth(systemD);

%% Simulation with sine wave comparation linear and non-linear
h = 0.001;
T = 35;
u = @(t) sin(t);
f = @(t, x)A*x + B*u(t);
delta = [0; 0; 0];
x0prima = operPoint + delta;
tout = 0:h:T - h;

xLinear = runge_kutta_time(f,h,T,delta);

rossler = @(t, x)[-x(2) - x(3); ...
                  x(1) + 100/Ra*x(2); ...
                  (u(t)+Vcc0 + u0)*100/Rb + x(3)*(x(1) - 100/Rc)]/RC;

xLinearComparar = xLinear + operPoint;
xOg = runge_kutta_time(rossler,h,T,x0prima);

plotPL(1, {tout}, {xLinearComparar(3,:), xOg(3,:)}, [0 T], [], "$t(s)$", ...
       "$y(V)$", ["Linear aproximation" "Rossler system"], [], 15, {'r', 'k'});
   
%% Sine wave compared to information
h = 0.001;
T = 50;
u = @(t) sin(t);
f = @(t, x)A*x + B*u(t);
delta = [0; 0; 0];
x0prima = operPoint + delta;
tout = 0:h:T - h;

xLinear = runge_kutta_time(f,h,T,delta);

rossler = @(t, x)[-x(2) - x(3); ...
                  x(1) + 100/Ra*x(2); ...
                  (u(t)+Vcc0 + u0)*100/Rb + x(3)*(x(1) - 100/Rc)]/RC;

xLinearComparar = xLinear + operPoint;
sin_bode = @(t) 0.0017*sin(t + 165*pi/180);

plotPL(1, {tout}, {xLinear(3,:), sin_bode(tout)}, [0 T], [], "$t(s)$", ...
       "$y(V)$", ["Linear" "Sine wave"], [], 15, {'r', 'k'});