%% It needs the package https://bit.ly/3py0pu1
%% Finding the epsilon of the computer
a = 0;
b = 0.1;

for n=1:10000
    l0 = (a + b)/2;
    l1 = (a + l0)/2;

    sum1 = 1 + l1;
    if sum1 == 1
        a = l1;
    else
        b = l1;
    end
end

pr = ['The epsilon of the computer is ' num2str(double(l1))];
disp(pr);

%% Finding the max of the computer

l = 1;
while (10^l) < inf
    l = l + 1;
end

c = vpi(10)^(l-1);
d = vpi(10)^l;
for i=1:1000
    m0 = c/2 + d/2;
    m1 = c/2 + m0/2;
    m2 = d/2 + m0/2;

    if double(m1) == inf
        d = m1;
    elseif double(m2) == inf
        d = m2;
        c = m1;
    else
        c = m2;
    end
end

m0 = (c + d)/2;

pra = ['The max of the computer is ' num2str(double(m0))];
disp(pra);
