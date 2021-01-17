function [phim, phin, final] = prometheus(np, avc, weights, minimize, lps, pparams, show)
% PROMETHEUS Applies the prometheus method for a given alternatives vs
% criterion matrix.
%
% - np is the version of the prometheus wanted.
% - avc is a matrix of alternatives vs criterion
% - weights is matrix of the weight of each criterion.
% - minimize is a boolean vector of the functions you want to minimize.
%
% - lps is the number of preference function you want to use for each
% criterion.
%   1: USUAL CRITERION
%       0 if x <= 0
%       1 if x > 0
%   2: CUASI CRITERION (param ls)
%       0 if x <= ls
%       1 if x > ls
%   3: LINEAL PREFERENCE (x/m if x <= m) (param m)
%       x/m if x <= m
%       1 if x > m
%   4: LEVELS (1/2 if q <= x <= q + p) (param q, p)
%       0 if x <= q
%       1/2 if q < x <= q + p
%       1 if x > q + p
%   5: LINEAL PREFERENCE AND AREA OF INDIFERENCE (param s, r)
%       0 if x <= q
%       (x - s)/r if s < x <= s + r
%       1 if x > s + r
%   6: GAUSSIAN (param sigma)
%       0 if x < 0
%       1 - exp(-x^2/2sigma^2) if x >= 0
%
% - pparams is a cell for the parameter of each function. For example, if
% there are two criterion that have the usual criterion and levels
% criterion respectively, pparms = {[], [q p]}
%
% phim = PROMETHEUS(np, avc, weights, minimize, lps, pparams)
% phim = PROMETHEUS(np, avc, weights, minimize, lps, pparams, show)
% [phim, phin] = PROMETHEUS(_)
% [phim, phin, final] = PROMETHEUS(_)
%
% See also ELECTRE, WMINMAX
    function op = opt(min, a, b)
        if min && a < b
            op = b - a;
        elseif min
            op = 0;
        elseif a > b
            op = a - b;
        else
            op = 0;
        end
    end
    function P = usual(fa, fb, min)
        if opt(min, fa, fb) <= 0
            P = 0;
        else
            P = 1;
        end
    end
    function P = cuasi(min, fa, fb, l)
        if opt(min, fa, fb) <= l
            P = 0;
        else
            P = 1;
        end
    end
    function P = lineal(min, fa, fb, m)
        x = opt(min, fa, fb);
        if x <= m
            P = x/m;
        else
            P = 1;
        end
    end
    function P = levels(min, fa, fb, qp)
        q = qp(1);
        p = qp(2);
        x = opt(min, fa, fb);
        if x <= q
            P = 0;
        elseif q < x <= q + p
            P = 1/2;
        else
            P = 1;
        end
    end
    function P = lineal_indiference(min, fa, fb, sr)
        x = opt(min, fa, fb);
        s = sr(1);
        r = sr(2);
        if x <= s
            P = 0;
        elseif s <= x && x <= s + r
            P = (x - s)/r;
        else
            P = 1;
        end
    end
    function P = gaussian(min, fa, fb, sigma)
        x = opt(min, fa, fb);
        if x <= 0
            P = 0;
        else
            P = 1 - exp(-x^2/(2*sigma^2));
        end
    end

    if ~exist("show", "var")
        show = false;
    end

    funcs = {@usual, @cuasi,@lineal,@levels, @lineal_indiference, ...
             @gaussian};


    na = length(avc(:,1));
    nc = length(weights);

    %% Calculate pi
    pi = zeros(na, na);
    for i = 1:na
        for j = 1:na
            if i ~= j
                for z = 1:nc
                    func = cell2mat(funcs(lps(z)));
                    param = cell2mat(pparams(z));
                    val = weights(z)*func(minimize(z), avc(i, z), avc(j, z), param);
                    pi(i, j) = pi(i, j) + val;
                end
            end
        end
    end

    %% Make phi+
    phim = sum(pi, 2)/(na - 1);

    %% Make phi-
    phin = sum(pi, 1)'/(na - 1);

    %% Compare
    if np == 1
        compared = zeros(na, na);
        for i = 1:na
            for j = i:na
                if phim(i) == phin(j) && phin(i) == phin(j)
                    compared(i, j) = 0;
                elseif phim(i) > phim(j) && phin(i) < phin(j)
                    compared(i,j) = 1;
                elseif phim(j) > phim(i) && phin(j) < phin(i)
                    compared(i,j) = -2;
                else
                    compared(i,j) = -1;
                end
            end
        end
        final = compared;
    else
        phi = phim - phin;
        final = phi;
    end
    %% Print if neccessary
    if show
        disp("---------------------------")
        disp("Stage 1")
        disp("Pi")
        fprintf([repmat('%10.4f',1,size(pi,2)) '\n'], pi')

        disp("---------------------------")
        disp("Stage 2")
        disp("Positive phi")
        fprintf([repmat('%10.4f',1,size(phim,2)) '\n'], phim')

        disp("---------------------------")
        disp("Stage 3")
        disp("Negative phi")
        fprintf([repmat('%10.4f',1,size(phin,2)) '\n'], phin')

        disp("---------------------------")
        disp("Stage 4")
        if np == 1
            for i = 1:na
                for j = i:na
                    if i ~= j
                        if compared(i,j) == -1
                            disp(['A' num2str(i) ', A' num2str(j) ' are ' ...
                                  'not comparable.']);
                        elseif compared(i,j) == 1
                            disp(['A' num2str(i) ' is better than A' num2str(j)]);
                        elseif compared(i,j) == 0
                            disp(['A' num2str(i) ' is indiferent to ' num2str(j)]);
                        else
                            disp(['A' num2str(j) ' is better than A' num2str(i)]);
                        end
                    end
                end
                disp(" ");
            end
        else
            disp("Phi")
            fprintf([repmat('%10.4f',1,size(phi,2)) '\n'], phi')
            disp("---------------------------")
            disp('Order')
            for i = 1:na
                m = find(phi == max(phi));
                disp(['A' num2str(m )]);
                phi(m) = min(phi) - 1;
            end
        end
    end
end
