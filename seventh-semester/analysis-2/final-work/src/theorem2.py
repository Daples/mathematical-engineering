import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors

plt.rc('text', usetex=True)
plt.rcParams.update({'font.size': 16})

def rk4(f, y0, tf, h=0.01):
    n = int(tf / h)
    y = np.zeros((len(y0), n))
    y[:, 0] = y0
    t = 0
    for i in range(1, n):
        yf = y[:, i - 1]
        k1 = f(t, yf)
        k2 = f(t + h / 2, yf + k1 * h / 2)
        k3 = f(t + h / 2, yf + k2 * h / 2)
        t += h
        k4 = f(t, yf + k3 * h)
        m = h*(k1 + 2*k2 + 2*k3 + k4)/6
        y[:, i] = y[:, i - 1] + m

    return y


# Generate initial condition and equation for each k
def x_k(k):
    return lambda t, x: alpha * x * np.exp(-gamma * t) * u_k(t, k), [1 + 1/k]


# Exact system
def x(t, x):
    return alpha * x * np.exp(-gamma * t) * u(t)


# Exact Control
def u(t):
    if t < 25:
        return 0.5
    else:
        return -1


# Sequence of Controls
def u_k(t, k):
    if t < 25:
        return 0.5 + (-1 / k) ** 2
    else:
        return -1 - (1 / k)

# Simulation parameters and ks
alpha = 0.3
gamma = 0.05
ks = [3, 6, 9, 27, 81, 243]
h = 0.01
tf = 100
ys = []
for k in ks:
    x_kt, x0k = x_k(k)
    ys.append(rk4(x_kt, x0k, tf, h=h))

y = rk4(x, [0], tf, h=h)

# Cividis color map
color1 = plt.get_cmap('viridis')
color_norm = colors.Normalize(vmin=0, vmax=len(ks)-1)
scalar_map = cm.ScalarMappable(norm=color_norm, cmap=color1)

# Plotting each trajectory with selective labels
ts = np.linspace(0, tf, int(tf / h))
index = 0
for y in ys:
    color = scalar_map.to_rgba(index)
    k = str(ks[index])
    if len(ks) < 7 or index == 0:
        plt.plot(ts, y[0,:], color=color, label="$x^{(" + k + ")}(t)$", linewidth=0.6)
    else:
        plt.plot(ts, y[0,:], color=color, linewidth=0.6)
    index += 1

plt.plot(ts, y[0, :], 'r', label="$x(t)$", linewidth=1)
plt.legend()
plt.grid()

# Saving and show figure
plt.savefig("theorem2.pdf", bbox_inches='tight')
plt.show()
