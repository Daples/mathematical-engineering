function weight = find_weights(cvc)
% WEIGHTS finds the weights of a matrix comparing criterions by weighted
% achievement.
%
% weight = weights(cvc)
%
% See also ELECTRE, PROMETHEUS
    nc = length(cvc);
    %% Find weights
    % Build each function
    f = zeros(nc, nc);
    i = 1;
    j = 2;
    for rest = 1:nc
        f(rest, i) = 1;
        f(rest, j) = -cvc(i, j);
        j = j + 1;
        if j - 1 == nc
            i = i + 1;
            j = i + 1;
        end
    end

    Aeq = ones(1, nc);
    beq = 1;
    weight = linwachievement(f, ones(nc, 2), zeros(nc, 1), [], [], Aeq, beq, zeros(1, nc));
end
