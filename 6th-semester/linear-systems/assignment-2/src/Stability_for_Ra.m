%% Parameters and Equilibrium Points
Ra = 500;
Rb = 7500;
Rc = 17.5439;
u0 = 1000;
RC = 1;
Vcc0 = 15;
[x0,y0,z0] = equilibriumPoints(100/Ra,100/Rb,100/Rc,u0);

i = 1;
operPoint = [x0(i); y0(i); z0(i)];

%% Characteristic polynomial
syms Ras s
Asim = [0 -1/RC -1/RC;
        1/RC 100/(Ras*RC) 0;
        operPoint(3)/RC 0 1/RC*(operPoint(1)-100/Rc)];

pol = det(s*eye(3) - Asim);

[pol, ~] = numden(pol);

polc = coeffs(pol, s);

polcc = coeffs(polc(length(polc)), Ras);

polc = polc/polcc(1);

pol = poly2sym(fliplr(polc), s);

%% Transfer function for rlocus for parameter Ra
rcoeffs = coeffs(pol, Ras);

N = double(fliplr(coeffs(rcoeffs(2))));
D = double(fliplr(coeffs(rcoeffs(1))));

tfr = tf(N/D(1), D/D(1));

fg1 = figure(1);
fg1.Renderer = 'Painters';
rlocus(tfr)

%% Routh - Hurwitz
[array, first_col] = routh_hurwitz(fliplr(coeffs(pol, s)));

array(size(array, 1), 1) = array(2, size(array, 2));

first_col = vpa(first_col, 5);
expr = Ras > 0;
in_array = sym('A', [1, length(first_col) + 1]);
for i = 1:length(first_col)
    in_array(i) = first_col(i) >= 0;
end
in_array(length(first_col) + 1) = Ras > 0;
sol = solve(in_array, Ras, 'Real', true, 'ReturnConditions', true);

disp(subs(sol.conditions(1), sol.parameters, Ras));

% Print RH array
for i = 1:size(array, 1)
    for j = 1:size(array, 2)
        if i == j && i == 1
            continue
        end
        [n, d] = numden(array(i, j));
        
        nc = coeffs(n, Ras);
        dc = coeffs(d, Ras);
        
        nc = nc/dc(length(dc));
        dc = dc/dc(length(dc));
        
        array(i, j) = poly2sym(fliplr(nc), Ras)/poly2sym(fliplr(dc), Ras);
    end
end



disp(vpa(array, 5));
%% Check for non-linear
Ra_unstable = [160 170 183];
Ra_stable = [184 185 200 300];

bc = {'r', 'k', 'b', 'm', 'c', 'y'};

% Simulation outside the stability point.
h = 0.001;
T = 10;
u = 1002;
delta = [0; 0; 0];
x0prima = operPoint + delta;
tout = 0:h:T - h;

yus = cell(1, length(Ra_unstable));
lgnd = strings(1, length(Ra_unstable));
color = cell(1, length(Ra_unstable));

for i = 1:length(Ra_unstable)
    Ra = Ra_unstable(i);
    
    rossler = @(x)[-x(2) - x(3); ...
               x(1) + 100/Ra*x(2); ...
               (u+Vcc0)*100/Rb + x(3)*(x(1) - 100/Rc)]/RC;

    y = runge_kutta(rossler, h, T, x0prima);
    
    yus{i} = y(3, :);
    
    lgnd(i) = strcat("$R_a = $", num2str(Ra));
    color{i} = bc{i};
end

plotPL(1, {tout}, yus, [0 T], [], "$t(s)$", "$y(V)$", lgnd, [], 15, color);

% Stability inisde that stability point
h = 0.001;
T = 25;
u = 1002;
delta = [0; 0; 0];
x0prima = operPoint + delta;
tout = 0:h:T - h;

yus = cell(1, length(Ra_stable));
lgnd = strings(1, length(Ra_stable));
color = cell(1, length(Ra_stable));

for i = 1:length(Ra_stable)
    Ra = Ra_stable(i);
    
    rossler = @(x)[-x(2) - x(3); ...
               x(1) + 100/Ra*x(2); ...
               (u+Vcc0)*100/Rb + x(3)*(x(1) - 100/Rc)]/RC;

    y = runge_kutta(rossler, h, T, x0prima);
    
    yus{i} = y(3, :);
    
    lgnd(i) = strcat("$R_a = $", num2str(Ra));
    color{i} = bc{i};
end

plotPL(2, {tout}, yus, [0 T], [], "$t(s)$", "$y(V)$", lgnd, [], 15, color);

%% Check for linear
B = [0; 0; 100/(Rb*RC)];
C = [0 0 1];
D = 0;

Ra_unstable = [160 170 183];
Ra_stable = [184 185 200 300];

bc = {'r', 'k', 'b', 'm', 'c', 'y'};

% Simulation outside the stability point.
h = 0.001;
T = 100;
u = 1002;
delta = [0; 0; 0];
tout = 0:h:T - h;

yus = cell(1, length(Ra_unstable));
lgnd = strings(1, length(Ra_unstable));
color = cell(1, length(Ra_unstable));

for i = 1:length(Ra_unstable)
    Ra = Ra_unstable(i);
    
    A = [0 -1/RC -1/RC;
         1/RC 100/(Ra*RC) 0;
         operPoint(3)/RC 0 1/RC*(operPoint(1)-100/Rc)];
     
    f = @(x)A*x + B*(u - u0);

    y = runge_kutta(f,h,T,delta);
    
    yus{i} = y(3, :);
    
    lgnd(i) = strcat("$R_a = $", num2str(Ra));
    color{i} = bc{i};
end

plotPL(1, {tout}, yus, [0 T], [], "$t(s)$", "$y(V)$", lgnd, [], 15, color);

% Stability inisde that stability point
h = 0.001;
T = 100;
u = 1002;
delta = [0; 0; 0];
x0prima = operPoint + delta;
tout = 0:h:T - h;

yus = cell(1, length(Ra_stable));
lgnd = strings(1, length(Ra_stable));
color = cell(1, length(Ra_stable));

for i = 1:length(Ra_stable)
    Ra = Ra_stable(i);
    
    A = [0 -1/RC -1/RC;
         1/RC 100/(Ra*RC) 0;
         operPoint(3)/RC 0 1/RC*(operPoint(1)-100/Rc)];
     
    f = @(x)A*x + B*(u - u0);

    y = runge_kutta(f,h,T,delta);
    
    yus{i} = y(3, :);
    
    lgnd(i) = strcat("$R_a = $", num2str(Ra));
    color{i} = bc{i};
end

plotPL(2, {tout}, yus, [0 T], [], "$t(s)$", "$y(V)$", lgnd, [], 15, color);
