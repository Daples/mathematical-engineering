function [RS, dm, dn] = topsis(avc, weights, minimize, show, p, n)
%TOPSIS Uses the topsis method to outrank the alternatives of a alternative
%vs criterion matrix.
%
% - avc is the matrix comparing alternative versus criterion.
% - weights are the weights of each of the criterion
% - minimize is a boolean vector of the criterion that minimizes.
% - p the type of norm used.
% - n it is 1 if the matrix want to be normalized by (yj - best)/(worst -
% best). Another number if it is already normalized.
%
% RS = TOPSIS(avc, weights, minimize)
% RS = TOPSIS(avc, weights, minimize, show)
% RS = TOPSIS(avc, weights, minimize, show, p)
% RS = TOPSIS(avc, weights, minimize, show, p, n)
% [RS, dm] = TOPSIS(_)
% [RS, dm, dn] = TOPSIS(_)
%
% See also ELECTRE, PROMETHEUS
    %% Check exist
    if ~exist("show", 'var')
        show = false;
    end
    if ~exist("p", 'var')
        p = 2;
    end

    if ~exist("n", 'var')
        n = 1;
    end

    na = length(avc(:,1));
    nc = length(avc(1,:));
    %% Normalize matrix
    if n == 1
        for i = 1:nc
            col = avc(:, i);
            best = min(col);
            worst = max(col);
            avc(:,i) = weights(i)*(col - best)/(worst - best);
        end
    end

    %% Calculate nadir and zenith
    nadir = zeros(1, nc);
    zenith = zeros(1, nc);
    for i = 1:nc
        col = avc(:, i);
        if minimize(i)
            best = min(col);
            worst = max(col);
        else
            best = max(col);
            worst = min(col);
        end
        nadir(i) = worst;
        zenith(i) = best;
    end

    %% Calculate positive distance
    dm = zeros(1, na);
    for i = 1:na
        for j = 1:nc
            dm(i) = dm(i) + (avc(i,j) - zenith(j))^p;
        end
        dm(i) = dm(i)^(1/p);
    end

    %% Calculate negative distance
    dn = zeros(1, na);
    for i = 1:na
        for j = 1:nc
            dn(i) = dn(i) + (avc(i,j) - nadir(j))^p;
        end
        dn(i) = dn(i)^(1/p);
    end

    %% Calculate Ratio of similarity to the ideal
    RS = dn./(dm + dn);

    if show
        disp("---------------------------")
        disp("Stage 1")
        disp("Zenith")
        fprintf([repmat('%10.4f',1,size(zenith,2)) '\n'], zenith')

        disp("---------------------------")
        disp("Stage 2")
        disp("Nadir")
        fprintf([repmat('%10.4f',1,size(nadir,2)) '\n'], nadir')

        disp("---------------------------")
        disp("Stage 3")
        disp("Positive distance")
        fprintf([repmat('%10.4f',1,size(dm,2)) '\n'], dm')

        disp("---------------------------")
        disp("Stage 4")
        disp("Negative distance")
        fprintf([repmat('%10.4f',1,size(dn,2)) '\n'], dn')

        disp("---------------------------")
        disp("Stage 5")
        disp("Ratio of similarity")
        fprintf([repmat('%10.4f',1,size(RS,2)) '\n'], RS')
        disp("---------------------------")
        disp('Order')
        RS1 = RS;
        for i = 1:na
            m = find(RS1 == max(RS1));
            disp(['A' num2str(m )]);
            RS1(m) = min(RS1) - 1;
        end
    end
end
