import matplotlib.pyplot as plt
import numpy as np
from sympy.abc import x
from sim import brownian_motion, euler_m
from matplotlib import rc


rc('text', usetex=True)
plt.rcParams.update({'font.size': 18})
np.random.seed(123456789)

# Parameters
mu = 0.003
sigma = 0.03
delta_t = 1
t_final = 365
x0 = np.array([1])
delta_mu = 0.004

# Function
f = mu * x
g = sigma * x


def simulation_1(f1, g1, mu1, linewidth=0.5):
    # Creating brownian motion
    bm = brownian_motion(1, 2*t_final, delta_t)

    # Construct the first series
    series_1 = euler_m(f1, g1, delta_t, x0, 1, bm=bm[:, :int(365 / delta_t)], tf=t_final)

    # # Construct second series
    # Constant
    series_c = euler_m(f1, g1, delta_t, series_1[:, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    # Optimistic
    mu1 += delta_mu
    f1 = mu1 * x
    series_o = euler_m(f1, g1, delta_t, series_1[:, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    # Pessimistic
    mu1 -= 2 * delta_mu
    f1 = mu1 * x
    series_p = euler_m(f1, g1, delta_t, series_1[:, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    top = max(series_1.flatten().max(), series_c.flatten().max(), series_o.flatten().max(),
              series_p.flatten().max())
    bottom = min(series_1.flatten().min(), series_c.flatten().min(), series_o.flatten().min(),
                 series_p.flatten().min())

    t_vals = np.linspace(0, 2*t_final, int(2*t_final / delta_t))
    plt.plot(t_vals[:int(t_final / delta_t)], series_1[0, :, 0], 'k', label='Series 1', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_c[0, :, 0], 'k', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_o[0, :, 0], 'b', label='Optimistic', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_p[0, :, 0], 'r', label='Pessimistic', linewidth=linewidth)
    plt.plot([t_final, t_final], [bottom, top], 'k--')
    plt.legend()
    plt.xlabel("Days")
    plt.ylabel("$X_t$")
    plt.savefig("pronostico-1-escenarios.pdf", bbox_inches='tight')


def bandwidths(f1, g1, mu1, n1, plot=False, linewidth=0.5):
    # Brownian motion
    bm = brownian_motion(n1, 2*t_final, delta_t)

    # First year simulation
    series_1 = euler_m(f1, g1, delta_t, x0, 1, bm=bm[:1, :int(365 / delta_t)], tf=t_final)
    initial_condition = series_1[:, -1, 0]

    t_val = np.linspace(0, 2*t_final, int(2*t_final / delta_t))
    t0s = t_val[:int(t_final / delta_t)]
    t1s = t_val[int(t_final / delta_t):]

    # Constant case
    series_c = euler_m(f1, g1, delta_t, initial_condition, n1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)
    if plot:
        plt.figure(1)
        top = max(series_1.flatten().max(), series_c.flatten().max())
        bottom = min(series_1.flatten().min(), series_c.flatten().min())
        plt.plot(t0s, series_1[0, :, 0].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_c[0, :, j].transpose(), linewidth=linewidth)
        plt.plot([t_final, t_final], [bottom, top], 'k--')
        plt.xlabel("Days")
        plt.ylabel("$X_t$")
        plt.savefig("pronostico-constante.pdf", bbox_inches='tight')

    # Optimistic case
    mu1 += delta_mu
    f1 = mu1 * x
    series_o = euler_m(f1, g1, delta_t, initial_condition, n1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)
    if plot:
        plt.figure(2)
        top = max(series_1.flatten().max(), series_o.flatten().max())
        bottom = min(series_1.flatten().min(), series_o.flatten().min())
        plt.plot(t0s, series_1[0, :, 0].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_o[0, :, j].transpose(), linewidth=linewidth)
        plt.plot([t_final, t_final], [bottom, top], 'k--')
        plt.xlabel("Days")
        plt.ylabel("$X_t$")
        plt.savefig("pronostico-optimista.pdf", bbox_inches='tight')

    # Pessimistic case
    mu1 -= 2 * delta_mu
    f1 = mu1 * x
    series_p = euler_m(f1, g1, delta_t, initial_condition, n1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)
    if plot:
        plt.figure(3)
        top = max(series_1.flatten().max(), series_p.flatten().max())
        bottom = min(series_1.flatten().min(), series_p.flatten().min())
        plt.plot(t0s, series_1[0, :, 0].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_p[0, :, j].transpose(), linewidth=linewidth)
        plt.plot([t_final, t_final], [bottom, top], 'k--')
        plt.xlabel("Days")
        plt.ylabel("$X_t$")
        plt.savefig("pronostico-pesimista.pdf", bbox_inches='tight')

    calculation_bandwidth(series_c)


def calculation_bandwidth(time_series):
    means = time_series[0, :, :].mean(axis=0)
    print(means.shape)


bandwidths(f, g, mu, 1000)
