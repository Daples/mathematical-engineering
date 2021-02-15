function fig1 = plotPL(i,x, y, xlims, ylims, xlabels, ylabels, legends, titles, fontSize, params)
    warning('off', 'all');
    if ~exist('fontSize', 'var')  || fontSize <= 15 
        fontSize = 15;
    end
    
    if ~exist('titles', 'var') 
        titles = "";
    end
    if ~exist('legends', 'var')
        legends = [];
    end
    
    if ~exist('ylabels', 'var')
        ylabels = "";
    end
    
    if ~exist('xlabels', 'var')
        xlabels = "";
    end
    
    if ~exist('xlims', 'var')
        xlims = [];
    end
    
    if ~exist('ylims', 'var')
        ylims = [];
    end
    
    if ~exist('params', 'var')
        params = repmat({'k'}, length(y(:,1)), 1);
    end
    % Strings with parameters for plot. E.g. 'ro' is red and circles.
    % legends
    fig1 = figure(i);
    fig1.Renderer='Painters';

    hold on
    for i = 1:length(y)
        if i > length(x)
            xs = cell2mat(x(1));
            ys = cell2mat(y(i));
            if length(xs) ~= length(ys)
                disp(["X1 and Y" num2str(i) "are not the same size"])
                close
                continue 
            end
            plot(xs, ys, cell2mat(params(i)));
        else
            xs = cell2mat(x(i));
            ys = cell2mat(y(i));
            if length(xs) ~= length(ys)
                disp(["X" num2str(i) " and Y" num2str(i) " are not the same size"])
                close
                continue
            end
            plot(xs, ys, cell2mat(params(i)));
        end
    end
    hold off
    if ~isempty(legends)
        lgnd = legend(legends);
        set(lgnd, 'FontSize', fontSize, 'Interpreter', 'latex','Location', 'best');
    end
    if ~isempty(xlims)
        xlim(xlims);
    end
    xl = xlabel(xlabels, 'Interpreter','latex');
    set(xl, 'FontSize', fontSize, 'Interpreter', 'latex');
    if ~isempty(ylims)
        ylim(ylims);
    end
    yl = ylabel(ylabels);
    set(yl, 'FontSize', fontSize, 'Interpreter', 'latex');
    tl = title(titles);
    set(tl, 'FontSize', fontSize, 'Interpreter', 'latex');
    
    aux = gca;
    aux.FontSize = fontSize;
end

