function [x, fsval, diff, exitFlag] = ...
         minmax(fs, x0, weights, target, linfs, lintarget, A, b, Aeq, ...
                beq, lb, ub, nonlcon, show)
% MINMAX Solves a multi-objective problem by minmax weigheted achievement,
% with non linear functions or non linear constraints.
%
% It solves the problem
% min D Subject to:
% a_i*n_i + b_i*p_i <= D
% A*x <= b
% Aeq*x = beq
% c(x) <= 0
% ceq(x) = 0
% fs_i(x) + ni - pi = target(i).
% linfs(i)'*x + ni - pi = lintarget(i).
%
% - fs is a cell of the nonlinear functions. {@(x)f1(x), @(x)f2(x)...}
% - target is a vector for the target for each function.
% - weights is a matrix that contains the a_i and b_i. [a1 b1; a2 b2 ...]
% - linfs is a matrix of coefficentes of each linear function. [f1; f2...]
% - lintarget are the targets for every linear function.
% - nonlcon is a cell with the nonlinear constraints. {@(x)c(x), @(x)ceq(x)}
%
% x = MINMAX(fs, x0, weights, target)
% x = MINMAX(fs, x0, weights, target, linfs, lintarget)
% x = MINMAX(fs, x0, weights, target, linfs, lintarget, A, b)
% x = MINMAX(fs, x0, weights, target, linfs, lintarget, A, b, Aeq, beq)
% x = MINMAX(fs, x0, weights, target, linfs, lintarget, A, b, Aeq, beq, lb)
% x = MINMAX(fs, x0, weights, target, linfs, lintarget, A, b, Aeq, beq, lb, ub)
% x = MINMAX(fs, x0, weights, target, linfs, lintarget, A, b, Aeq, beq, lb, ub, nonlcon)
% x = MINMAX(fs, x0, weights, target, linfs, lintarget, A, b, Aeq, beq, lb, ub, nonlcon, show)
% [x, fsval] = MINMAX(_)
% [x, fsval, diff] = MINMAX(_)
% [x, fsval, diff, exitFlag] = MINMAX(_)
%
% See also LINMINMAX, WACHIEVEMENT, LINWACHIEVEMENT, FMINCON

format longg
%% Check variables that exist
    if ~exist("linfs", 'var') && ~exist("lintarget", 'var')
        linfs = [];
        lintarget = [];
    elseif ~exist("linfs", 'var') || ~exist("lintarget", 'var')
        disp("Parameters are missing")
        return
    end
    if ~exist("A", 'var') && ~exist("b", 'var')
        A = [];
        b = [];
    elseif ~exist("A", 'var') || ~exist("b", 'var')
        disp("Parameters are missing.");
        return
    end

    if ~exist("Aeq", 'var') && ~exist("beq", 'var')
        Aeq = [];
        beq = [];
    elseif ~exist("Aeq", 'var') || ~exist("beq", 'var')
        disp("Parameters are missing.")
    end

    if ~exist("lb", 'var')
        lb = [];
    end
    if ~exist("ub", 'var')
        ub = [];
    end
    if ~exist("nonlcon", 'var')
        nonlcon = {@(x)[], @(x)[]};
        empt = true;
    else
        empt = false;
    end

    if ~exist("show", 'var')
        show = false;
    end
    options = optimoptions('fmincon', 'Display', 'off');

    %% Check lengths
    if isempty(fs) && isempty(linfs)
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
        if length(weights(i, :)) ~= 2
            disp("The number of weights is different from 2")
            return
        end
    end
    if lfs ~= length(target)
        disp("The number of targets is different from the number of func")
        return
    end

    if ~isempty(linfs)
        llinfs = length(linfs(:,1));
        if llinfs ~= length(lintarget)
            disp("The number of targets is different from the number of linear functions.")
            return
        end
    else
        llinfs = 0;
    end
    num = length(x0);
    nlfs = lfs;
    lfs = lfs + llinfs;

    if lfs ~= lw
        disp("There aren't the same number of weights as functions")
    end

    %% Warning
    if nlfs == 0 && empt
        disp(['Warning: There are not any nonlinear objective functions' ...
             ' or constraints. Use instead linminmax for better ' ...
             'accuracy.'])
    end

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

    x0 = [x0 zeros(1, 2*lfs + 1)];
    Aeq = [Aeq; zeros(llinfs, num + 2*lfs + 1)];
    A = [A; zeros(lfs, num + 2*lfs + 1)];

    for j = 1:lfs
        % Non linear constraints
        if j <= nlfs
            rest = cell2mat(nonlcon(2));
            f = cell2mat(fs(j));
            rest1 = @(x) f(x) + x(num + 2*j - 1) - x(num + 2*j) - target(j);
            nonlcon(2) = {@(x) [rest(x) rest1(x)]};
            t = target(j);
        else
            j1 = j - nlfs;
            Aeq(first + j1, 1:num) = linfs(j1, :);
            Aeq(first + j1, num + 2*j - 1) = 1;
            Aeq(first + j1, num + 2*j) = -1;
            t = lintarget(j1);
        end
        A(first1 + j, num + 2*j - 1:num + 2*j) = weights(j, :)/t;
        A(first1 + j, num + 2*lfs + 1) = -1;
    end

    c = cell2mat(nonlcon(1));
    ceq = cell2mat(nonlcon(2));
    nonlcon = @(x) deal(c(x), ceq(x));

    if llinfs ~= 0
        beq = [beq; lintarget];
        b = [b; zeros(lfs, 1)];
    end

    %% Make objective function
    fw = @(x) x(num + 2*lfs + 1);
    %% Solve
    [x, ~, exitFlag] = fmincon(fw, x0, A, b, Aeq, beq, lb, ub, nonlcon, options);
    x = x(1:num);
    if exitFlag == 1
        fsval = zeros(lfs, 1);
        for i = 1:lfs
            if i <= nlfs
                f1 = cell2mat(fs(i));
                fsval(i) = f1(x);
            end

            if i <= llinfs
                fsval(i + nlfs) = linfs(i, :)*x';
            end
        end
        if show
            disp("Optimal solution found.");
            disp("The value of the original variables are")
            fprintf([repmat('%f\t', 1, size(x, 2)) '\n'], x')
        end
        diff = abs([target; lintarget] - fsval);
    elseif exitFlag == 0
        disp("Reach maximum iterations")
    else
        disp(['There was a problem executing linprog, as there was an ' ...
              'exit flag of ' num2str(exitFlag) '. See linprog function' ...
              ' for more information.'])
    end

end
