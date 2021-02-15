syms x y z t
% Variables of the system
vars = [x; y; z];

% Independent variable
ind_var = t;

% Parameters of simulation
tsim = 0:1/100:1;

% Initial conditions
y0 = [2; 3; 2];

% Parameters
a = 3;
b = 0.1;
c = 1;

% Order of derivative
q1 = 1;
q2 = 1;
q3 = 0.8;
alpha = [q1; q2; q3];

% System
f = [z + (y-a)*x;
     1 - b*y - x^2;
     -x - c*z];

% Number of polynomials used
N = 10;

tic
y_apr = decomposition1(N, f, alpha, vars, ind_var, y0, tsim);
toc

clear q1 q2 q3 alpha f y0 indvar vars x y z t

