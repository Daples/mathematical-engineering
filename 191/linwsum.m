function [x, fsval, ideal, exitFlag] = ...
         linwsum(fs, weights, A, b, Aeq, beq, lb, ub, show)
% LINWSUM Solves a multi-objective problem by weighted sum of the objectives
% linear functions (normalized).
%
% It solves the problem
% min (sum w_i*f_i(x)) Subject to:
% A*x <= b
% Aeq*x = beq
%
% - weights is a matrix or vector of the weights desired to evaluate.
%
% x = LINWSUM(fs, weights)
% x = LINWSUM(fs, weights, A, b)
% x = LINWSUM(fs, weights, A, b, Aeq, beq)
% x = LINWSUM(fs, weights, A, b, Aeq, beq, lb)
% x = LINWSUM(fs, weights, A, b, Aeq, beq, lb, ub)
% x = LINWSUM(fs, weights, A, b, Aeq, beq, lb, ub, show)
% [x, fsval] = LINWSUM(_)
% [x, fsval, ideal] = LINWSUM(_)
% [x, fsval, ideal, exitFlag] = LINWSUM(_)
%
% See also FMINCON, LINWACHIEVEMENT, LINMINMAX, WSUM

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
    if ~exist("show", 'var')
        show = false;
    end
    options2 = optimoptions('linprog', 'Display', 'off');

    %% Check lengths
    if isempty(fs)
        disp("There aren't any functions")
        return
    end
    if isempty(weights)
        disp("There aren't any weights")
        return
    end
    lfs = length(fs(:,1));
    lw = length(weights(:, 1));
    for i = 1:length(lw)
        if lfs ~= length(weights(i, :))
            disp("The number of weights is " +  ...
                "different to the number of functions")
            return
        end
    end
    %% Find ideal vector
    matrix = zeros(lfs, lfs);
    for i = 1:lfs
        f_op = fs(i,:);
        x_opt = linprog(f_op, A, b, Aeq, beq, lb, ub, options2);
        for j = 1:lfs
            matrix(i, j) = fs(j,:)*x_opt;
        end
    end
    ideal = matrix;

    %% Make objective function
    solution = zeros(length(weights(:,1)), 2*lfs + length(fs(1,:)));
    for j = 1:lw
        weight = weights(j, :);
        fw = zeros(1, length(fs(1,:)));
        for i = 1:lfs
            fsi = matrix(:, i);
            fi = fs(i, :);
            wi = weight(i);
            fw = fw + wi*fi/(max(fsi) - min(fsi));
        end
        [x, ~, exitFlag] = linprog(fw, A, b, Aeq, beq, lb, ub, options2);

        if exitFlag == 0
            disp("Reach maxmimum iterations");
        elseif exitFlag ~= 1
            disp(['There was a problem executing linprog, as there was an ' ...
              'exit flag of ' num2str(exitFlag) '. See linprog function' ...
              ' for more information.'])
            return
        end

        fsval = zeros(1, lfs);
        for z = 1:lfs
            fsval(z) = fs(z, :)*x;
        end
        solution(j, :) = [weight fsval x'];
    end

    if length(weights(:,1)) > 1
        fprintf([repmat('%f\t', 1, size(solution, 2)) '\n'], solution')
    elseif show
        disp("Optimal solution found.");
        x = x';
        fprintf([repmat('%f\t', 1, size(x, 2)) '\n'], x')
    end

end
