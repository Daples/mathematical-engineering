import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 16})
plt.rc('text', usetex=True)


def rk4(f, y0, tf, h=0.01):
    n = int(tf / h)
    y = np.zeros((len(y0), n), dtype=complex)
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


def f(t, y):
    return 0.5 + np.exp(-t) * u(t)


y0 = [0]
tf = 1
h = 0.001
ts = np.linspace(0, tf, int(tf/h))

u = lambda t: 0.5
ys1 = rk4(f, y0, tf, h)

u = lambda t: -0.25
ys2 = rk4(f, y0, tf, h)

u = lambda t: 0.5 * np.sin(4*np.pi*t)
ys3 = rk4(f, y0, tf, h)


plt.plot(ts, ys1[0, :], 'b', label='$u_1(t)$')
plt.plot(ts, ys2[0, :], 'r', label='$u_2(t)$')
plt.plot(ts, ys3[0, :], color='orange', label='$u_3(t)$')
plt.plot(ts, ts * (2*np.exp(-2)), 'k--', label='Estimation')
plt.plot(ts, ts * 2, 'k--')
plt.grid()
plt.xlabel('$t$')
plt.ylabel('$x^u(t)$')
plt.legend()
plt.savefig('theorem3.pdf', bbox_inches='tight')
plt.show()
