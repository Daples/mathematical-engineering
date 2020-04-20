import matplotlib.pyplot as plt
import numpy as np
from sympy.abc import x
from sim_par import euler_m, brownian_motion
from matplotlib import rc
import multiprocessing

num_cores = multiprocessing.cpu_count() - 1
rc('text', usetex=True)
plt.rcParams.update({'font.size': 18})
np.random.seed(123456789)

# # Parameters
alpha = 0.5
mu = 1.25
sigma = 0.4
gamma = 0.5

delta_t = 0.1
x0 = np.array([1])
T = 30
n = 200

# Function
f = alpha * (mu - x)
g = sigma * x ** gamma
linewidth = 0.5
bm = brownian_motion(n, T, delta_t)
series2 = euler_m(f, g, delta_t, x0, n, bm=bm, tf=T, show=True)
ts = np.linspace(0, T, int(T/delta_t))
plot = False
if plot:
    plt.plot(ts, series2[0, 0, :], 'k', linewidth=linewidth)
    plt.xlabel('$t$')
    plt.ylabel('$X_t$')
    plt.savefig('plts/ornstein_serie2.pdf', bbox_inches='tight')
    plt.show()

def parameter_estimation(time_series, plot=False):
    mults = [(i+1)/10  for i in range(10)]
    delta = delta_t
    alphas = np.zeros((len(mults), n))
    mus = np.zeros((len(mults), n))
    sigmas = np.zeros((len(mults), n))

    for i in range(len(mults)):
        mult = mults[i]
        for j in range(n):
            A = 0
            for k in range(1, int(time_series.shape[2] * mult)):
                A += time_series[j, 0, k] * time_series[j, 0, k - 1] / (time_series[j, 0, k - 1] ** (2 * gamma))

            B = 0
            for k in range(1, int(time_series.shape[2] * mult)):
                B += time_series[j, 0, k - 1] / (time_series[j, 0, k - 1] ** (2 * gamma))

            C = 0
            for k in range(1, int(time_series.shape[2] * mult)):
                C += time_series[j, 0, k] / (time_series[j, 0, k - 1] ** (2 * gamma))

            D = 0
            for k in range(1, int(time_series.shape[2] * mult)):
                D += 1 / (time_series[j, 0, k - 1] ** (2 * gamma))

            E = 0
            for k in range(1, int(time_series.shape[2] * mult)):
                E += (time_series[j, 0, k - 1] / (time_series[j, 0, k - 1] ** gamma)) ** 2

            alphas[i, j] = (E * D - B ** 2 - A * D + B * C) / ((E * D - B **2) * delta)
            mus[i, j] = (A - E * (1 - alphas[i, j] * delta)) / (alphas[i, j] * B * delta)
            S = 0
            for k in range(1, int(time_series.shape[2] * mult)):
                S += ((time_series[j, 0, k] - time_series[j, 0, k - 1] - (alphas[i, j]
                      * (mus[i, j] - time_series[j, 0, k - 1]) * delta)) / (time_series[j, 0, k - 1] ** gamma)) ** 2
            sigmas[i, j] = ((1 / (int(mult * time_series.shape[2]) * delta)) * S) ** 0.5

    print('alpha', np.mean(alphas[-1, :]))
    print('mu', np.mean(mus[-1, :]))
    print('sigma', np.mean(sigmas[-1, :]))

    if plot:
        ts = np.array(mults) * T
        # alpha
        alpha_means = alphas.mean(axis=1)
        plt.plot(ts, alpha_means, 'ko-', label='Estimation')
        plt.plot(ts, np.ones(len(ts)) * alpha, 'k--', alpha=0.5, label='Real value')
        plt.xlabel('$\\tilde{t}$')
        plt.ylabel('$\hat{\\alpha}$')
        plt.savefig('plts/alphas.pdf', bbox_inches='tight')
        plt.clf()

        # mu
        mu_means = mus.mean(axis=1)
        plt.plot(ts, mu_means, 'ko-', label='Estimation')
        plt.plot(ts, np.ones(len(ts)) * mu, 'k--', alpha=0.5, label='Real value')
        plt.xlabel('$\\tilde{t}$')
        plt.ylabel('$\hat{\mu}$')
        plt.savefig('plts/mus.pdf', bbox_inches='tight')
        plt.clf()

        # sigma
        sigma_means = sigmas.mean(axis=1)
        plt.plot(ts, sigma_means, 'ko-', label='Estimation')
        plt.plot(ts, np.ones(len(ts)) * sigma, 'k--', alpha=0.5, label='Real value')
        plt.xlabel('$\\tilde{t}$')
        plt.ylabel('$\hat{\sigma}$')
        plt.savefig('plts/sigmas.pdf', bbox_inches='tight')
        plt.clf()

