import numpy as np


# d1 - Average temp: 28.5
# d7 - Precipitation Amount
# d8 - Insolation duration
# d9 - humidity

def runge_kutta(f1, y0, t1):
    h = 0.01
    n = int(t1 / h)
    y1 = np.zeros((len(y0), n))
    y1[:, 0] = y0
    for i1 in range(1, n):
        yf = y1[:, i1 - 1]
        k1 = f1(yf)
        k2 = f1(yf + k1*h/2)
        k3 = f1(yf + k2*h/2)
        k4 = f1(yf + k3*h)
        m = h*(k1 + 2*k2 + 2*k3 + k4)/6
        y1[:, i1] = y1[:, i1 - 1] + m

    y = np.zeros((t1, 1))
    for j in range(0, n, int(1/h)):
        y[int(j*h), 0] = y1[2, j]

    return y*3


def extract_data(str1):
    df = open("data_paper.txt", "r")
    found = False
    l1 = []
    for line in df.readlines():
        line = line.replace("\n", "")
        if found and line != "":
            l1.append(float(line))
        elif found:
            break

        if line == str1:
            found = True

    df.close()

    return [np.mean(l1), np.std(l1)]


def gen_norm(mv):
    return np.random.normal(mv[0], mv[1], (T, 1))


data_file = open('data.txt','w')


T = 182
strings = ["d1", "d8", "d9"]
data = []
for str2 in strings:
    data.append(extract_data(str2))

data = list(map(gen_norm, data))

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
data.insert(1, d7)
for i in data:
    np.ndarray.tolist(i)

s = ''
for i in data:
    for j in i:
        s = s + str(j[0]) + ','
    s = s[0:len(s)-1]
    data_file.write(s + '\n')
    s = ''

data_file.close()
