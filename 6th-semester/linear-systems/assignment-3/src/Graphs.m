%% Plot comparisong non linear and linear control (sensibility)
% Run Heuristic2 with sensibility parameters, with a repeating stair
% sequence between 0 and 2. Put in the output blocks a sample time of 100.
% This graph compares where the controller stabilizes the linear system and
% the non linear.
n = length(y) - 1;
us = us(1:n);
ynl = y(2:n+1);

f1 = plotPL(1, {us}, {ynl, us}, [0 2], [], "$u(V)$", "$y_{ss}(V)$", ["Nonlinear", ...
       "Linear"], "", -1, {'r', 'b'});

saveTightFigure(f1, "Graphics/sens_lin_vs_nonlin.pdf");

f2 = plotPL(2, {us}, {cont(2:n+1)}, [0 2], [], "$u(V)$", "$u_{ss}(V)$", "Nonlinear", "", ...
            -1, {'r'});
saveTightFigure(f2, "Graphics/control_sens_lin_vs_nonlin.pdf");

%% Finding lower bound for reference, PID sensitivity heuristic
% Lower bound of the reference, for the controller. r(t) = -0.25,
% critically stable behaviour (tFinal = 1000)
f3 = plotPL(1, {tout}, {y, us}, [0 tout(length(tout))], [], "$t(s)$", "$y(V)$", ...
            ["Nonlinear" "Input"], "", -1, {'r', 'b'});
saveTightFigure(f3, "Graphics/sens_u_-0_25.pdf");

f4 = plotPL(2, {tout}, {cont}, [0 tout(length(tout))], [], "$t(s)$", "$u(V)$", ...
            "Control", "", -1, {'k'});
saveTightFigure(f4, "Graphics/control_sens_low_bound_ref.pdf");

%% Plotting for a ramp input
% Plotting different outputs with a ramp input, varying the slope for
% different values.
f1 = plotPL(1, {tout}, {y, us}, [0 tout(length(tout))], [], "$t(s)$", "$y(V)$", ...
            ["Nonlinear" "Input"], "", -1, {'r', 'b'});
saveTightFigure(f1, "Graphics/sens_ramp_ref_-0_05.pdf");

f2 = plotPL(2, {tout}, {cont}, [0 tout(length(tout))], [], "$t(s)$", "$u(V)$", ...
            "Control", "", -1, {'k'});
saveTightFigure(f2, "Graphics/control_sens_ramp_ref_-0_05.pdf");

%% Plotting for approximated PID analytic
% Plotting different outputs with a constant input, varying the value.
f1 = plotPL(1, {tout}, {y, us}, [0 tout(length(tout))], [], "$t(s)$", ...
            "$y(V)$", ["Nonlinear" "Input"], "", -1, {'r', 'b'});
saveTightFigure(f1, "Graphics/analytic_u_0_5_poles_0_4.pdf");

f2 = plotPL(2, {tout}, {cont}, [0 tout(length(tout))], [], "$t(s)$", "$u(V)$", ...
            "Control", "", -1, {'k'});
saveTightFigure(f2, "Graphics/control_analytic_u_0_5_poles_0_4.pdf");

%% Plotting sensitivity analisis for analytic PID
f1 = plotPL(1, {tout}, {y, us}, [0 tout(length(tout))], [], "$t(s)$", ...
            "$y(V)$", ["Nonlinear" "Input"], "", -1, {'r', 'b'});
saveTightFigure(f1, "Graphics/analytic_sensitivity_a_300.pdf");

f2 = plotPL(2, {tout}, {cont}, [0 tout(length(tout))], [], "$t(s)$", "$u(V)$", ...
            "Control", "", -1, {'k'});
saveTightFigure(f2, "Graphics/control_analytic_a_300.pdf");

%% Plotting state feedback control ref 0
% Plotting varying initial conditions
f1 = plotPL(1, {tout}, {y}, [0 tout(length(tout))], [], "$t(s)$", ...
            "$\lambda y(V)$", "Nonlinear", "", -1, {'r'});
saveTightFigure(f1, "Graphics/sfc_x30_50_ref_0.pdf");

f2 = plotPL(2, {tout}, {cont}, [0 tout(length(tout))], [], "$t(s)$", "$u(V)$", ...
            "Control", "", -1, {'k'});
saveTightFigure(f2, "Graphics/control_sfc_x30_50_ref_0.pdf");

%% Plotting state feedback control ref 0
% Plotting varying initial conditions
f1 = plotPL(1, {tout}, {y}, [0 tout(length(tout))], [], "$t(s)$", ...
            "$y(V)$", "Nonlinear", "", -1, {'r'});
saveTightFigure(f1, "Graphics/sfc_x30_50_ref_0.pdf");

f2 = plotPL(2, {tout}, {cont}, [0 tout(length(tout))], [], "$t(s)$", "$u(V)$", ...
            "Control", "", -1, {'k'});
saveTightFigure(f2, "Graphics/control_sfc_x30_50_ref_0.pdf");
%% Plotting state feedback control ref 0 analysis sensitivity
f1 = plotPL(1, {tout}, {y}, [0 tout(length(tout))], [], "$t(s)$", ...
            "$y(V)$", "Nonlinear", "", -1, {'r'});
saveTightFigure(f1, "Graphics/analysis_sfc_a_450.pdf");

f2 = plotPL(2, {tout}, {cont}, [0 tout(length(tout))], [], "$t(s)$", "$u(V)$", ...
            "Control", "", -1, {'k'});
saveTightFigure(f2, "Graphics/control_analysis_sfc_a_450.pdf");

%% Plotting state feedback control ref != 0 analysis sensitivity
% Plotting varying initial conditions
f1 = plotPL(1, {tout}, {y us}, [0 tout(length(tout))], [], "$t(s)$", ...
            "$y(V)$", ["Nonlinear" "Input"], "", -1, {'r', 'b'});
saveTightFigure(f1, "Graphics/analysis_sfc_a_250_ref_dif_0.pdf");

f2 = plotPL(2, {tout}, {cont}, [0 tout(length(tout))], [], "$t(s)$", "$u(V)$", ...
            "Control", "", -1, {'k'});
saveTightFigure(f2, "Graphics/control_analysis_sfc_a_250_ref_dif_0.pdf");