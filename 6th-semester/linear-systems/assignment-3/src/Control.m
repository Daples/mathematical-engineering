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
C = [0 0 1];
D = 0;
A = [0 -1/RC -1/RC;
        1/RC 100/(Ra*RC) 0;
        operPoint(3)/RC 0 1/RC*(operPoint(1)-100/Rc)];
    
B = [0; 0; 100/(Rb*RC)];
system = ss(A, B, C, D);

T = 1;

systemD = c2d(system,1);
%% Simulation
h = 0.001;
Tf = 100;
u = 1002;
f = @(x)A*x + B*(u - u0);
delta = [0;0;0];
x0prima = operPoint + delta;
tout1 = 0:h:Tf - h;

xLinear = runge_kutta(f,h,Tf,delta);

% rossler = @(x)[-x(2) - x(3); ...
%                x(1) + 100/Ra*x(2); ...
%                (u+Vcc0)*100/Rb + x(3)*(x(1) - 100/Rc)]/RC;

xLinearComparar = xLinear + operPoint;
%xOg = runge_kutta(rossler,h,T,x0prima);


plotPL(3, {tout1}, {xLinear(3,:)}, [],[],'$t$','$y$', ...
       ["Rossler System"; "Linear Approximation"],[], 20, {'k';'r'});
%% Reaction Curve 1
x1 = 3.162;
x2 = 3.124;
y1 = 0.0052804;
y2 = 0.0052097;
m = (y2-y1)/(x2-x1);
b = (y1-m*x1);
hold on
y = @(x)m*x+b;
t = 0:0.1:5;
plot(t,y(t))

% PID Control
R = m;
L = -b/m + T/2;
RL = R*L;
Kp = 1.2/RL;
Ti = 2*L;
Td = 0.5*L;

q0 = Kp*(1+T/(2*Ti)+Td/T);
q1 = -Kp*(1-T/(2*Ti)+2*Td/T);
q2 = Kp*Td/T;

disp(q0);
disp(q1);
disp(q2);
%% Chien-Hrones-Reswick
Kp = 0.95/RL;
Ti = 2.4*L;
Td = 0.42*L;

q0 = Kp*(1+T/(2*Ti)+Td/T);
q1 = -Kp*(1-T/(2*Ti)+2*Td/T);
q2 = Kp*Td/T;

disp(q0);
disp(q1);
disp(q2);

%% Sens
margin1 = allmargin(systemD);
Ku = margin1.GainMargin(2);
Tu = margin1.GMFrequency(2);
Tu = 2*pi/Tu;

Kp = 0.6*Ku;
Ti = Tu/2;
Td = Tu/8;

q0 = Kp*(1+T/(2*Ti)+Td/T);
q1 = -Kp*(1-T/(2*Ti)+2*Td/T);
q2 = Kp*Td/T;

disp(q0);
disp(q1);
disp(q2);

%% PID analítico
tfD = tf(systemD);
tf1 = approximation(tout1, xLinear(3,:), u - u0);
tf_aprox = c2d(tf1, T);

[N, D] = tfdata(tf_aprox);

syms z q0s q1s q2s r1s
P = (z - r1s)*(z - 1);
Q = q0s*z^2 + q1s*z + q2s;

Az = poly2sym(D, z);
Bz = poly2sym(N, z);

sol = Az*P + Bz*Q;

csol = fliplr(coeffs(sol, z, 'All'));

despol = (z - 0.5)^4;
desired = fliplr(coeffs(despol, z, 'All'));
solutions = solve(csol == desired);

q0 = double(solutions.q0s);
q1 = double(solutions.q1s);
q2 = double(solutions.q2s);
r1 = double(solutions.r1s);

%% Controllability Matrix
% Continuous
Mc = [B A*B A^2*B];
rankC = rank(Mc);
nCondC = cond(Mc);

% Discrete
McD = [systemD.B systemD.A*systemD.B systemD.A^2*systemD.B];
rankD = rank(McD);
nCondD = cond(McD);

%% state feedback control
K = acker(systemD.A,systemD.B,[0,0,0]);
poles = eig(A); % Original
newPoles = eig(systemD.A-systemD.B*K); % With control

%% state feedback control with ref != 0
An = [systemD.A zeros(3,1);
    -systemD.C 1];
Bn = [systemD.B; 0];

Kaux = acker(An,Bn, [0.5,0.5,0.5,0.5]);
K = Kaux(1:3);
L = Kaux(4);
prop = eig(An-Bn*Kaux); % New poles
