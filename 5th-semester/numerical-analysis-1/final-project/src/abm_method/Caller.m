% Simulation parameters
tOfSim = 1000;
N = 10000;

% Initial conditions of the mth derivative (m = ceil(q))
y0 = [2; 3; 2];

% Parameter
a = 3;
b = 0.1; 
c = 1;

% Order of derivatives
q1 = 1;
q2 = 1;
q3 = 0.8;
q = [q1; q2; q3];

f = @(x)[x(3) + (x(2) - a).*x(1); ...
         1 - b*x(2) - x(1).^2; ...
         -x(1) - c*x(3)];

%%%% Adams bashfourth
tic
yopt = adamsbashfort_opt(f, q, y0, tOfSim, N, 0.001, 10);
toc

clear q q1 q2 q3 a b c y0 N

