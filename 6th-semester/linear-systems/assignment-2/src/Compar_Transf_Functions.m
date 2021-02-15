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


%% Discrete Transfer function
tm = 1;
transfer = tf(system);
transferD = c2d(transfer, tm);

%% Comparison transfer functions with Unit step
h = 0.001;
T = 35;
tout = 0:h:T - h;
u = 1001;

f = @(x)A*x + B*(u - u0);
delta = [0; 0; 0];

xLinear = runge_kutta(f,h,T,delta);

toutz = 0:tm:T;

trans_y = lsim(transfer, ones(1, length(tout)), tout);
transD_y = lsim(transferD, ones(1, length(toutz)), toutz);

plotPL(1, {tout}, {trans_y, xLinear(3,:)}, [0 T], [], ...
       "$t(s)$", "$y(V)$", [], "", 20, {'k', 'r'});
hold on
stairs(toutz, transD_y, "b");
lgnd = legend(["Trans." "Linear" "Discrete"]);
set(lgnd, 'FontSize', 20, 'Interpreter', 'latex','Location', 'best');
hold off

%% Comparison transfer functions with Unitary impulse
h = 0.001;
T = 35;
tout = 0:h:T - h;
u = @(t) (t < tm) + 1000;

f = @(t, x)A*x + B*(u(t) - u0);
delta = [0; 0; 0];

xLinear = runge_kutta_time(f,h,T,delta);

toutz = 0:tm:T;

trans_y = lsim(transfer, u(tout) - u0, tout);
transD_y = lsim(transferD, u(toutz) - u0, toutz);

plotPL(2, {tout}, {trans_y, xLinear(3,:)}, [0 T], [], ...
       "$t(s)$", "$y(V)$", [], "", 20, {'k', 'r'});
hold on
stairs(toutz, transD_y, "b");
lgnd = legend(["Trans." "Linear" "Discrete"]);
set(lgnd, 'FontSize', 20, 'Interpreter', 'latex','Location', 'best');

%% Discrete ponderation
syms z
% Transfer symbolic
[n1, d1] = tfdata(transferD);
transferauxD = poly2sym(cell2mat(n1), z)/poly2sym(cell2mat(d1), z);

% Discrete ponderation
gt = vpa(iztrans(partfrac(transferauxD, z, 'FactorMode', 'complex')), 5);
n = 10;
gts = zeros(1,n);
for k = 0:n-1
    gts(k+1) = eval(subs(gt, k));
end

% Unit step
zu = zeros(1, n);
u = 1001;
for k = 0:n-1
  zu(k + 1) = (u - u0)*sum(gts(1:k+1));  
end

tz = tm*(0:n-1);

trans_y = lsim(transfer, ones(1, length(tout)), tout);

plotPL(4, {tout}, {trans_y}, [], [], '$t(s)$', '$y(V)$', [], [], 20, {'r'});
hold on
stairs(tz, zu, 'ko');
legend(["Linear" "Ponderation"])

% Unitary impulse
u = @(t) (t < tm) + 1000;
trans_y = lsim(transfer, u(tout) - u0, tout);

plotPL(5, {tout}, {trans_y}, [], [], '$t(s)$', '$y(V)$', [], [], 20, {'r'});
hold on
stairs(tz, gts, 'ko');
legend(["Linear" "Ponderation"])