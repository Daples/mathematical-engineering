function [a, f, g, nonlin] = decompose(system, vars)
    function [afg, var1] = classify(term, vars)
        % Standarize equation
        factors = strsplit(term, "/");
        if length(factors) == 2
            term = strcat(factors(1), "*", factors(2), "^(-1)");
        end
        
        % Split by factors of the multiplication
        factors = strsplit(term, "*");
        var1 = 0;
        n_vars = 0;
        for j=1:length(factors)
            factor = string(factors(j));
            for l=1:length(vars)
                % Count how many times a variable appears in the whole term
                var2 = vars(l);
                if contains(factor, var2)
                    n_vars = n_vars + 1;
                    var1 = l;
                    
                    % If there are variables multiplying itself, then is a
                    % non linear term.
                    if n_vars >= 2
                        afg = 2;
                        return
                    end
                    
                    % If the factor has a variable, and the number of
                    % characters is more than 1 it implies that x is 
                    % evaluated in some function, therefore is not lineal.
                    if strlength(factor) > 1
                        afg = 2;
                        return
                    end
                end
            end
        end
        
        % If the variable doesn't appear, it means it is a independent term
        if n_vars == 0
            afg = 3;
        else
            % Else, is a linear term
            afg = 1;
        end
    end
    
    lvars = length(vars);
    
    % Create matrix to create for the decomposition
    astr = repmat("0", lvars, lvars);
    fstr = repmat("0", lvars, 1);
    gstr = fstr;
    nonlin = false;
    
    for i=1:length(system)
        % Read one equation of the system, standarized to easy manipulation
        eq = string(vpa(expand(system(i)), 6));
        eq = strrep(eq, " ", "");
        eq = char(eq);
        if eq(1) == "-"
            eq = "-1*" + strrep(eq(2:length(eq)), "-", "+-1*");
        else
            eq = strrep(eq, "-", "+-1*");
        end
        eq = strsplit(eq, "+");
        
        % Classify terms of the system
        for k=1:length(eq)
            term = string(eq(k)); % Term of the equation
            % Classify if the term of the equation is independent of the
            % variables, linear or non linear.
            [afg, var] = classify(term, vars); 
            
            % Linear case
            if afg == 1
                % The variables doesn't have a factor multiplying it.
                if strlength(term) == 1
                    astr(i, var) = "1";
                else
                    % Extract factor multiplying it.
                    sub3 = char(term);
                    astr(i, var) = sub3(1:length(sub3)-2);
                end
            % Non-linear case
            elseif afg == 2
                fstr(i) = strcat(fstr(i), "+(", term, ")");
                nonlin = true;
            % Independent case.
            else
                gstr(i) = strcat(gstr(i), "+(", term, ")");
            end
        end
    end
    
    f = str2sym(fstr);
    g = str2sym(gstr);
    a = eval(str2sym(astr));
    
end

