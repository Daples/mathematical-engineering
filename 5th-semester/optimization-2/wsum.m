function [x, fsval, ideal, exitFlag] = wsum(fs, x0, weights, A, b, Aeq, beq, ...
                                  lb, ub, nonlcon, show)
% WSUM Solves a multi-objective problem by weighted sum of the objectives
% functions (normalized), with non linear functions or constraints.
%
% It solves the problem
% min (sum w_i*f_i(x)) Subject to:
% A*x <= b
% Aeq*x = beq
% c(x) <= 0
% ceq(x) = 0
%
% - fs is a cell of the nonlinear functions to minimize. {@(x)f1(x), @(x)f2(x)...}
% - weights is a matrix or vector of the weights desired to evaluate.
%
% x = WSUM(fs, x0, weights)
% x = WSUM(fs, x0, weights, A, b)
% x = WSUM(fs, x0, weights, A, b, Aeq, beq)
% x = WSUM(fs, x0, weights, A, b, Aeq, beq, lb)
% x = WSUM(fs, x0, weights, A, b, Aeq, beq, lb, ub)
% x = WSUM(fs, x0, weights, A, b, Aeq, beq, lb, ub, nonlcon)
% [x, fsval] = WSUM(_)
% [x, fsval, ideal] = WSUM(_)
% [x, fsval, ideal, exitFlag] = WSUM(_)
%
% See also FMINCON, LINWACHIEVEMENT, LINMINMAX, LINWSUM

format longg
%% Check variables that exist
    if ~exist("A", 'var') && ~exist("b", 'var')
        A = [];
        b = [];
    elseif ~exist("A", 'var') || ~exist("b", 'var')
        disp("Parameters are missing.")
        return
    end

    if ~exist("Aeq", 'var') && ~exist("beq", 'var')
        Aeq = [];
        beq = [];
    elseif ~exist("Aeq", 'var') || ~exist("beq", 'var')
        disp("Parameters are missing.");
    end

    if ~exist("lb", 'var')
        lb = [];
    end
    if ~exist("ub", 'var')
        ub = [];
    end
    if ~exist("nonlcon", 'var')
        nonlcon = [];
    end
    if ~exist("show", 'var')
        show = false;
    end
    options = optimoptions('fmincon', 'Display', 'off');

    %% Check lengths
    if isempty(fs)
        disp("There aren't any functions")
        return
    end
    if isempty(weights)
        disp("There aren't any weights")
        return
    end

    lfs = length(fs);
    lw = length(weights(:,1));
    for i = 1:lw
        if lfs ~= length(weights(i, :))
            disp("The number of weights is " +  ...
                "different to the number of functions")
            return
        end
    end

    %% Find ideal vector
    matrix = zeros(lfs, lfs);
    for i = 1:lfs
        f_op = cell2mat(fs(i));
        x_opt = fmincon(f_op, x0, A, b, Aeq, beq, lb, ub, nonlcon, options);
        for j = 1:lfs
            f = cell2mat(fs(j));
            matrix(i, j) = f(x_opt);
        end
    end
    ideal = matrix;

    %% Make objective function
    solution = zeros(length(weights(:,1)), 2*lfs + length(x0));
    for j = 1:length(weights(:,1))
        fw = @(x) 0;
        weight = weights(j, :);
        for i = 1:lfs
            fsi = matrix(:, i);
            fi = cell2mat(fs(i));
            wi = weight(i);
            fw = @(x)fw(x) + wi*fi(x)/(max(fsi) - min(fsi));
        end
        [x, ~, exitFlag] = fmincon(fw, x0, A, b, Aeq, beq, lb, ub, nonlcon, ...
                        options);

        if exitFlag == 0
            disp("Reach maxmimum iterations");
        elseif exitFlag ~= 1
            disp(['There was a problem executing fmincon, as there was an ' ...
              'exit flag of ' num2str(exitFlag) '. See linprog function' ...
              ' for more information.'])
            return
        end
        fsval = zeros(1, lfs);
        for z = 1:lfs
            f1 = cell2mat(fs(z));
            fsval(z) = f1(x);
        end

        solution(j,:) = [weight fsval x];
    end

    if length(weights(:,1)) > 1
        fprintf([repmat('%f\t', 1, size(solution, 2)) '\n'], solution')
    elseif show
        disp("Optimal solution found.");
        fprintf([repmat('%f\t', 1, size(x, 2)) '\n'], x')
    end
end
