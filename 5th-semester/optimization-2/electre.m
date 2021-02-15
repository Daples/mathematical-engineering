function [graph, conc, discor] = electre(avc, weights, minimize, show, c, d)
% ELECTRE calculates the electre graph of a multi-criterion problem.
%
% It makes the electre graph.
%
% - avc a matrix of the values of alternatives compared to criterion.
% - cvc a matric of the values of criterion compared to criterion.
% - weights is a matrix of the weight of each criterion.
% - minimize a boolean vector of which criterion are minimizing.
% - show a boolean value if you want to see the output step by step
%
% graph = ELECTRE(avc, cvc, minimize)
% graph = ELECTRE(avc, cvc, minimize, show)
% graph = ELECTRE(avc, cvc, minimize, show, c)
% graph = ELECTRE(avc, cvc, minimize, show, c, d)
% [graph, conc] = ELECTRE(_)
% [graph, conc, discor] = ELECTRE(_)
%
% See also WMINMAX, PROMETHEUS
    function val = opt(min1, a, b)
        if min1
            val = a < b;
        else
            val = b < a;
        end
    end
    %% Variables
    if ~exist('show', 'var')
        show = false;
    end

    nc = length(avc(1,:));
    na = length(avc(:,1));
    %% Concordance matrix
    conc = zeros(na, na);
    for i = 1:na
        for j = 1:na
            if j ~= i
                for z = 1:nc
                    if avc(i,z) == avc(j, z)
                        conc(i, j) = conc(i, j) + weights(z)/2;
                    elseif opt(minimize(z), avc(i, z), avc(j, z))
                        conc(i, j) = conc(i, j) + weights(z);
                    end
                end
            end
        end
    end

    %% Normalize decision matrix
    for j = 1:nc
        best = min(avc(:, j));
        worst = max(avc(:,j));
        avc(:,j) = (avc(:,j) - best)/(worst -  best);
    end
    navc = avc;

    %% Weighted normal matrix
    for j = 1:nc
        avc(:,j) = avc(:,j)*weights(j);
    end
    wnavc = avc;

    %% Discordance matrix
    discor = zeros(na, na);
    for i = 1:na
        for j = 1:na
            if j ~= i
                up = zeros(1, nc);
                down = zeros(1, nc);
                for z = 1:nc
                    down(z) = abs(avc(i, z) - avc(j, z));
                    if ~opt(minimize(z), avc(i, z), avc(j, z))
                        up(z) = down(z);
                    end
                end
                discor(i, j) = max(up)/max(down);
            end
        end
    end

    %% Calculate c, d if not given
    if ~exist("c", 'var')
        c = mean(conc(:));
    end

    if ~exist("d", 'var')
        d = mean(discor(:));
    end

    %% Calculate concordant dominance
    concd = conc;
    concd(conc > c) = 1;
    concd(conc <= c) = 0;

    %% Calculate discordant dominance
    discord = discor;
    discord(discor < d) = 1;
    discord(discor >= d) = 0;

    %% Calculate electre graph
    graph = concd.*discord;
    %% Print if neccesary
    if show
        disp("---------------------------")
        disp("Stage 1")
        disp("Concordance matrix")
        fprintf([repmat('%10.4f',1,size(conc,2)) '\n'], conc')

        disp("---------------------------")
        disp("Stage 2")
        disp("Normalize matrix")
        fprintf([repmat('%10.4f',1,size(navc,2)) '\n'], navc')

        disp("---------------------------")
        disp("Stage 3")
        disp("Weighted normalized matrix")
        fprintf([repmat('%10.4f',1,size(wnavc,2)) '\n'], wnavc')

        disp("---------------------------")
        disp("Stage 4")
        disp("Discordance matrix")
        fprintf([repmat('%10.4f',1,size(discor,2)) '\n'], discor')

        disp("---------------------------")
        disp("Stage 5")
        disp("Dominance concordance")
        fprintf([repmat('%10.4f',1,size(concd,2)) '\n'], concd')
        disp(['With c ' num2str(c)]);

        disp("---------------------------")
        disp("Stage 6")
        disp("Dominance discordance")
        fprintf([repmat('%10.4f',1,size(discord,2)) '\n'], discord')
        disp(['With d ' num2str(d)]);

        disp("---------------------------")
        disp("Stage 7")
        disp("Graph")
        fprintf([repmat('%10.4f',1,size(graph,2)) '\n'], graph')

        g = digraph(graph);
        plot(g, 'Layout', 'force');
    end
end
