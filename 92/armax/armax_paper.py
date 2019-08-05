import numpy as np
import matplotlib.pyplot as plt


data_file = open('data.txt','r')

data = data_file.read()
data = data.split('\n')

d = np.array([data[0].split(','),
              data[1].split(','),
              data[2].split(','),
              data[3].split(',')], dtype=float)

# Sim Time
T = 182

b = np.array([8.9087, -1.557, 31.919, -2.045])
c = np.array([1, 0.153])

# Noise
a = np.random.normal(0, 1, T)

Y = np.zeros(T, dtype=float)
Y[0] = 480
for t in range(1, T):
    print(str(t))
    Y[t] = 237.565 + 0.426*Y[t-1] + c.dot(a[t-1:t+1]) + b.dot(d[:, t])

plt.figure(1)
plt.plot(Y)
plt.figure(2)
plt.plot(d[1,0:31])
plt.show()
