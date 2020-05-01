import matplotlib.pyplot as plt
import numpy as np
from sympy.abc import x
from sim_par import brownian_motion, euler_m
import scipy.stats as st
from matplotlib import rc
from joblib import Parallel, delayed
import multiprocessing
import time

num_cores = multiprocessing.cpu_count()
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
    series_c = euler_m(f1, g1, delta_t, series_1[0, :, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    # Optimistic
    mu1 += delta_mu
    f1 = mu1 * x
    series_o = euler_m(f1, g1, delta_t, series_1[0, :, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    # Pessimistic
    mu1 -= 2 * delta_mu
    f1 = mu1 * x
    series_p = euler_m(f1, g1, delta_t, series_1[0, :, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    top = max(series_1.flatten().max(), series_c.flatten().max(), series_o.flatten().max(),
              series_p.flatten().max())
    bottom = min(series_1.flatten().min(), series_c.flatten().min(), series_o.flatten().min(),
                 series_p.flatten().min())

    t_vals = np.linspace(0, 2*t_final, int(2*t_final / delta_t))
    plt.plot(t_vals[:int(t_final / delta_t)], series_1[0, 0, :], 'k', label='Series 1', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_c[0, 0, :], 'k', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_o[0, 0, :], 'b', label='Optimistic', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_p[0, 0, :], 'r', label='Pessimistic', linewidth=linewidth)
    plt.plot([t_final, t_final], [bottom, top], 'k--')
    plt.legend()
    plt.xlabel("Days")
    plt.ylabel("$X_t$")
    plt.savefig("pronostico-1-escenarios.pdf", bbox_inches='tight')
    plt.show()


def bandwidths(f1, g1, mu1, n1, plot=False, linewidth=0.5):
    # Brownian motion
    bm = brownian_motion(n1, 2*t_final, delta_t)

    # First year simulation
    series_1 = euler_m(f1, g1, delta_t, x0, 1, bm=bm[:1, :int(365 / delta_t)], tf=t_final)
    initial_condition = series_1[0, :, -1]

    t_val = np.linspace(0, 2*t_final, int(2*t_final / delta_t))
    t0s = t_val[:int(t_final / delta_t)]
    t1s = t_val[int(t_final / delta_t):]

    # Constant case
    series_c = euler_m(f1, g1, delta_t, initial_condition, n1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)
    if plot:
        plt.figure(1)
        top = max(series_1.flatten().max(), series_c.flatten().max())
        bottom = min(series_1.flatten().min(), series_c.flatten().min())
        plt.plot(t0s, series_1[0, 0, :].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_c[j, 0, :].transpose(), linewidth=linewidth)
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
        plt.plot(t0s, series_1[0, 0, :].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_o[j, 0, :].transpose(), linewidth=linewidth)
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
        plt.plot(t0s, series_1[0, 0, :].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_p[j, 0, :].transpose(), linewidth=linewidth)
        plt.plot([t_final, t_final], [bottom, top], 'k--')
        plt.xlabel("Days")
        plt.ylabel("$X_t$")
        plt.savefig("pronostico-pesimista.pdf", bbox_inches='tight')

    plot_prediction_bands(t1s, series_c, 'plts/bands_constant.pdf', 0.1)
    plot_prediction_bands(t1s, series_o, 'plts/bands_optimistic.pdf', 0.1)
    plot_prediction_bands(t1s, series_p, 'plts/bands_pessimistic.pdf', 0.1)


def plot_prediction_bands(ts, times_series, filename, alpha1=0.1, linewidth=0.5, show=False, dist='lognorm'):
    lower, upper = prediction_bands(times_series, alpha1, dist=dist)
    n1 = times_series.shape[0]
    for j in range(n1):
        if j == n1 - 1:
            plt.plot(ts, times_series[j, 0, :].transpose(), color='grey', alpha=0.25, linewidth=linewidth,
                     label='Trajectories')
        plt.plot(ts, times_series[j, 0, :].transpose(), color='grey', alpha=0.05, linewidth=linewidth)
    plt.plot(ts, upper, 'r', linewidth=linewidth, label='Prediction Bands')
    plt.plot(ts, lower, 'r', linewidth=linewidth)
    plt.xlabel("Days")
    plt.ylabel("$X_t$")
    plt.legend()
    plt.savefig(filename, bbox_inches='tight')
    if show:
        plt.show()
    plt.clf()


def prediction_bands(time_series, alpha1=0.1, dist='lognorm'):
    distribution = getattr(st, dist)
    tf = time_series.shape[2]
    x0 = time_series[0, 0, 0]

    def aux(i):
        return distribution.fit(time_series[:, 0, i])

    params = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(i) for i in range(1, tf)))
    lower = np.zeros(tf)
    upper = np.zeros(tf)
    lower[0] = x0
    upper[0] = x0
    for p in range(tf - 1):
        lower[p + 1] = distribution.ppf(alpha1/2, *params[p, :])
        upper[p + 1] = distribution.ppf(1 - (alpha1/2), *params[p, :])
    return lower, upper


def sensitivity(f1, g1, mu1, sigma1, alpha1, p, n1, linewidth=0.5):
    # Brownian motion
    bm = brownian_motion(n1, 2 * t_final, delta_t)

    # First year simulation
    series_1 = euler_m(f1, g1, delta_t, x0, 1, bm=bm[:, :int(365 / delta_t)], tf=t_final)
    initial_condition = series_1[0, :, -1]

    t_val = np.linspace(0, 2 * t_final, int(2 * t_final / delta_t))
    t1s = t_val[int(t_final / delta_t):]
    sigmas = np.linspace(sigma1 - sigma1 * p, sigma1 + sigma1 * p, 40)
    symbols = {-1: 'pessimistic', 0: 'constant', 1: 'optimistic'}

    for key in symbols:
        simulations = {}
        f1 = (mu1 + key*delta_mu) * x
        for sigma in sigmas:
            g1 = sigma*x
            simulation = euler_m(f1, g1, delta_t, initial_condition, n1, bm=bm[:, int(365 / delta_t):],
                                 tf=2*t_final, t0=t_final)
            simulations[sigma] = prediction_bands(simulation, alpha1)

        lower = np.array(list(map(lambda x: x[0][-1], simulations.values())))
        upper = np.array(list(map(lambda x: x[1][-1], simulations.values())))

        plt.plot(sigmas, lower, linewidth=linewidth, label='Lower bounds')
        plt.plot(sigmas, upper, linewidth=linewidth, label='Upper bounds')
        plt.xlabel('$\sigma$')
        plt.ylabel('$B_{t_f}$')
        plt.legend()
        name = 'plts/sens_' + symbols[key] + '.pdf'
        plt.savefig(name, bbox_inches='tight')
        plt.clf()
