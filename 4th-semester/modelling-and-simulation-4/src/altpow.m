function [resp] = altpow(base, alf)
    resp = zeros(1,length(alf));
    if length(base) == 1
        for i=1:length(alf)
            resp(i) = base^alf(i);
        end
    else
        for i=1:length(alf)
            resp(i) = base(i)^alf(i);
        end
    end
end

