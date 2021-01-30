function [x,y,z] = equilibriumPoints(a,b0,c,u)
    y = [(-c + sqrt(c^2 - 4*a*(15 + u)*b0))/(2*a);
        (-c - sqrt(c^2 - 4*a*(15 + u)*b0))/(2*a)];
    x = -a*y;
    z = -y;
end