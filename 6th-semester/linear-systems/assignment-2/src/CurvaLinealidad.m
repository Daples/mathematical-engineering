
X = sim('rosslerSystemLinearCurve');

u = u(1:length(u) - 1);
n_yss = length(u);
T = 100;
h = 1e-3;
yss = zeros(n_yss,1);

for i = 1:n_yss
    yss(i) = y((T*i/h + 1));
end

yss_linear = zeros(n_yss,1);

for i = 1:n_yss
    yss_linear(i) = yLinApprox((T*i/h + 1));
end

%% Plot Curve

plotPL(1, {u;u}, {yss;yss_linear},[],[],'$u(V)$','$y_{ss}(V)$',["Rossler System" "Linear Model"],[],20,{'k';'b'});
