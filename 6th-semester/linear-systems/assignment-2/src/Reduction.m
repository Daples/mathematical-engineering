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
u = 1002;
f = @(x)A*x + B*(u - u0);
delta = [0; 0; 0];
x0prima = operPoint + delta;
tout = 0:h:T - h;

xLinear = runge_kutta(f,h,T,delta);

rossler = @(x)[-x(2) - x(3); ...
               x(1) + 100/Ra*x(2); ...
               (u+Vcc0)*100/Rb + x(3)*(x(1) - 100/Rc)]/RC;

xOg = runge_kutta(rossler, h, T, x0prima);

%% Transfer function
transfer = tf(system);

%% Order reduction
rs = balred(transfer, 2);

y_aprox_mat = lsim(rs, (u - u0)*ones(1, length(tout)), tout);

plotPL(5, {tout}, {y_aprox_mat, xLinear(3,:)}, [0 T], [], "$t(s)$", "$y(V)$", ["Aprox. MATLAB" "Linear"], [], 20, {'k', 'r'});

%% Analytic reduction
syms s
[ntrans, dtrans] = tfdata(transfer);
ntrans = ntrans{1};
dtrans = dtrans{1};

zero1 = zero(transfer);
pole1 = pole(transfer);

aprox_dt = (s - pole1(2))*(s - pole1(3));
aproxD = double(fliplr(coeffs(aprox_dt)));

k = aproxD(length(aproxD))/dtrans(length(dtrans));

transfer_aux = tf(k*ntrans, aproxD);

yr_aux = lsim(transfer_aux, (u - u0)*ones(1, length(tout)), tout);
plotPL(6, {tout}, {yr_aux, xLinear(3,:)}, [0 T], [], "$t(s)$", "$y(V)$", ["Aprox." "Linear"], [], 20, {'k', 'r'});

% Bode diagram
f1 = figure(1);
bode(system,'k')
bode(transfer_aux, 'k');
set(findall(gcf,'-property','FontSize'),'FontSize',14)
grid on

%% Comparation reduced system and original system
h = 0.001;
T = 50;
tout = 0:h:T - h;

u = sin(tout);

yn = lsim(transfer, u, tout);
yr = lsim(transfer_aux, u, tout);

plotPL(1, {tout}, {yn, yr}, [0 T], [], "$t(s)$", "$y(V)$", ["Linear" "Reduced"], ...
      [], 15, {'r', 'k'});

%% Aproximation
[aprox_sys, t1] = approximation(tout, xLinear(3,:), u - u0);
y_aprox = lsim(aprox_sys, (u - u0)*ones(1, length(tout)), tout, [0 0 0]);

auxt = abs(tout - 3.096);
disp(['Growth time ' num2str(3.096 - t1)]);
plotPL(6, {tout}, {xLinear(3,:), y_aprox}, [0 T], [], "$t(s)$", "$y(V)$", ["Linear" "Order 2"], ... 
       [], 20, {'r', 'k'});
