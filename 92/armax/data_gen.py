import numpy as np


# d1 - Average temp: 28.5
# d7 - Precipitation Amount
# d8 - Insolation duration
# d9 - humidity


data_file = open('data.txt','w')

T = 182
d1 = np.random.normal(28.5, 1.5, (T,1))
d8 = np.random.normal(9, 1.5, (T,1))
d9 = np.random.normal(75, 2, (T,1))


def runge_kutta(f1, y0, T1):
    h = 0.01
    n = int(T1/h)
    y1 = np.zeros((len(y0), n))
    y1[:, 0] = y0
    for i in range(1, n):
        yf = y1[:, i - 1]
        k1 = f1(yf)
        k2 = f1(yf + k1*h/2)
        k3 = f1(yf + k2*h/2)
        k4 = f1(yf + k3*h)
        m = h*(k1 + 2*k2 + 2*k3 + k4)/6
        y1[:, i] = y1[:, i - 1] + m

    y = np.zeros((T1, 1))
    for j in range(0, n, int(1/h)):
        y[int(j*h), 0] = y1[2, j]

    return y


a = 0.29
b = 0.14
c = 4.52
f = lambda x: np.array([-x[1] - x[2],
                        x[0] + a*x[1],
                        b + x[2]*(x[0] - c)])

d7 = runge_kutta(f, np.array([0.72, 1.28, 0.21]), T)
# precipitation weird
# d7 = np.random.normal(-1, 2, (T,1)) #????????????????????????/
# for i in range(T):
#    d7[i][0] = max(d7[i][0],0)

# matrix
data = [d1, d7, d8, d9]
for i in data:
    np.ndarray.tolist(i)

s = ''
for i in data:
    for j in i:
        s = s + str(j[0]) + ','
    s = s[0:len(s)-1]
    data_file.write(s + '\n')
    s = ''
