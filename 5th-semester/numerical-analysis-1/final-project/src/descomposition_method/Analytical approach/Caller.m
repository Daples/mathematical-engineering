%%%% Decomposition
syms x y z t

% Initial conditions
y01 = [1; -1];

% Parameters
% a = 3;
% b = 0.1;
% c = 1;

% System
f1 = [y;
      2*x - y];
  
% Order of system
alpha1 = [1; 1];

% Variables
vars = [x; y];

% Independent variables
ind_var = t;

% Number of polynomials
N = 30;

tic
y_decomposed = decomposition1(N, f1, alpha1, vars, ind_var, y01);
toc

clear x y z t y01 f1 alpha1 vars ind_var N