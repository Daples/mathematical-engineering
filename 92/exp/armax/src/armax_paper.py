import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt


def sim(a, t1):
    y = np.zeros(t1, dtype=float)
    y[0] = 480
    for t1 in range(1, t1):
        y[t1] = 237.565 + 0.426 * y[t1 - 1] + c.dot(a[t1 - 1:t1 + 1]) + b.dot(d[:, t1])
    return y


data_file = open('data.txt', 'r')


data = data_file.read()
data = data.split('\n')

d = np.array([data[0].split(','),
              data[1].split(','),
              data[2].split(','),
              data[3].split(',')], dtype=float)

b = np.array([8.9087, -1.557, 31.919, -2.045])
c = np.array([1, 0.153])

t = 182

# Noise
a1 = np.random.normal(0, 1, t)
a2 = sp.t.rvs(0.7, size=t)

y1 = sim(a1, t)
y2 = sim(a2, t)

plt.figure(1)
plt.plot(y1, "r", label="Normal")
plt.plot(y2, label="T-Student")
plt.legend()
plt.show()
