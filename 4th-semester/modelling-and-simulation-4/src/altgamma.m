function [resp] = altgamma(input)
    resp = zeros(1, length(input));
    for i=1:length(input)
        resp(i) = gamma(input(i));
    end
end

