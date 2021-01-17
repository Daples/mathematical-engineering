function [x, fsval, diff, exitFlag] ...
         = linminmax(fs, weights, target, A, b, Aeq, beq, lb, ub, show)
% LINMINMAX Solves a multi-objective problem by minmax weighted
% achievement, with linear functions and constraints.
%
% It solves the problem
% min D Subject to:
% a_i*n_i + b_i*p_i <= D
% A*x <= b
% Aeq*x = beq
% fs(i)'*x + ni - pi = target(i).
%
% - fs is a matrix of coefficentes of each linear function. [f1; f2...]
% - target is a vector for the target for each function.
% - weights is a matrix that contains the a_i and b_i. [a1 b1; a2 b2 ...]
%
% x = LINMINMAX(fs, weights, target)
% x = LINMINMAX(fs, weights, target, A, b)
% x = LINMINMAX(fs, weights, target, A, b, Aeq, beq)
% x = LINMINMAX(fs, weights, target, A, b, Aeq, beq, lb)
% x = LINMINMAX(fs, weights, target, A, b, Aeq, beq, lb, ub)
% x = LINMINMAX(fs, weights, target, A, b, Aeq, beq, lb, ub, show)
% [x, fsval] = LINMINMAX(_)
% [x, fsval, diff] = LINMINMAX(_)
% [x, fsval, diff, exitFlag] = LINMINMAX(_)
%
% See also LINPROG, WACHIEVEMENT, MINMAX, LINWACHIEVEMENT

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
        disp("Parameters are missing.")
        return
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
    options = optimoptions('linprog', 'Display', 'off');

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
    lw = length(weights(:,1));
    for i = 1:lw
        if length(weights(i, :)) ~= 2
            disp("The number of weights is different from 2")
            return
        end
    end
    if lfs ~= length(target)
        disp("The number of targets is different from the number of functions.")
        return
    end
    num = length(fs(1,:));
    %% Make new restrictions
    if ~isempty(A)
        A = [A zeros(length(A(:,1)), 2*lfs + 1)];
    end
    if ~isempty(Aeq)
        Aeq = [Aeq zeros(length(Aeq(:,1)), 2*lfs + 1)];
    end
    if ~isempty(lb)
        lb = [lb zeros(1, 2*lfs + 1)];
    end
    if ~isempty(ub)
        ub = [ub ones(1, 2*lfs + 1)*Inf];
    end

    if isempty(Aeq)
        first = 0;
    else
        first = length(Aeq(:,1));
    end

    if isempty(A)
        first1 = 0;
    else
        first1 = length(A(:,1));
    end

    Aeq = [Aeq; zeros(lfs, num + 2*lfs + 1)];
    A = [A; zeros(lfs, num + 2*lfs + 1)];
    for j = 1:lfs
        Aeq(first + j, 1:num) = fs(j, :);
        Aeq(first + j, num + 2*j - 1) = 1;
        Aeq(first + j, num + 2*j) = -1;
        A(first1 + j, num + 2*j - 1:num + 2*j) = weights(j, :)/target(j);
        A(first1 + j, num + 2*lfs + 1) = -1;
    end
    beq = [beq; target];
    b = [b; zeros(length(target), 1)];

    %% Make objective function
    fw = [zeros(1, num + 2*lfs) 1];
    %% Solve
    [x, ~, exitFlag] = linprog(fw, A, b, Aeq, beq, lb, ub, options);
    if exitFlag == 1
        fsval = zeros(lfs, 1);
        for i = 1:lfs
            fsval(i) = fs(i, :)*x(1:num);
        end
        x = x(1:num)';
        if show
            disp("Optimal solution found.");
            disp("The value of the original variables are")
            fprintf([repmat('%f\t', 1, size(x, 2)) '\n'], x')
        end
        diff = abs(target - fsval);
    elseif exitFlag == 0
        disp("Reach maximum iterations")
    else
        disp(['There was a problem executing linprog, as there was an ' ...
              'exit flag of ' num2str(exitFlag) '. See linprog function' ...
              ' for more information.'])
    end
end
