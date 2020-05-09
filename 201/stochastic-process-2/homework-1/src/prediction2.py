import matplotlib.pyplot as plt
import numpy as np
from sympy.abc import x
from scipy import stats as st
from sim_par import euler_m, brownian_motion
from matplotlib import rc
import multiprocessing
from prediction import prediction_bands

num_cores = multiprocessing.cpu_count()
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
n = 1

# Function
f = alpha * (mu - x)
g = sigma * x ** gamma
linewidth = 0.5
bm = brownian_motion(n, T, delta_t)
series2 = euler_m(f, g, delta_t, x0, n, bm=bm, tf=T, show=False)

ts = np.linspace(0, T, int(T/delta_t))
plot = False
if plot:
    for i in range(series2.shape[0]):
        plt.plot(ts, series2[i, 0, :], 'k', linewidth=linewidth)
    plt.xlabel('$t$')
    plt.ylabel('$X_t$')
    plt.savefig('plts/ornstein_serie2.pdf', bbox_inches='tight')
    plt.show()


# n = 200? 500?
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


# Extracted from https://www.quantstart.com/articles/Basics-of-Statistical-Mean-Reversion-Testing/
def hurst(ts):
    """Returns the Hurst Exponent of the time series vector ts"""
    # Create the range of lag values
    lags = [2, 4, 8, 16]

    # Calculate the array of the variances of the lagged differences
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    # Use a linear fit to estimate the Hurst Exponent
    poly = np.polyfit(np.log(lags), np.log(tau), 1)

    # Return the Hurst exponent from the polyfit output
    return poly[0] * 2.0


def statistical_analysis(time_series, alpha1=0.05, axis=0, dist='lognorm'):
    test = [alpha1]
    distribution = getattr(st, dist)
    params = [[]]
    for i in range(1, time_series.shape[axis]):
        if axis == 0:
            ts = time_series[i, 0, :]
        else:
            ts = time_series[:, 0, i]
        params.append(distribution.fit(ts))
        _, p_value = st.kstest(ts, dist, args=params[-1])
        test.append(p_value)
    max_val = max(test)
    min_val = min(test)
    test[0] = (max_val - min_val) / 2
    return test, params


# 1000 trajs
def hists(time_series, filename, axis=0, dist='chi2', plot_hist=False):
    test, params = statistical_analysis(time_series, axis=axis, dist=dist)
    test = np.array(test)
    bool_test = np.array(test >= 0.05, dtype=int)
    count = bool_test.sum()
    print(count/bool_test.size)
    if plot_hist:
        index_max = int(np.argmax(test))
        index_min = int(np.argmin(test))
        if axis == 0:
            series = time_series[index_max, 0, :]
        else:
            series = time_series[:, 0, index_max]
        _, bins, _ = plt.hist(series, label='Histogram', color='white', ec='black', density=True)
        x = np.linspace(bins[0] - 0.5, bins[-1] + 0.5, 200)
        distribution = getattr(st, dist)
        y_pdf = distribution.pdf(x, *params[index_max])
        plt.ylabel('Relative Frequency')
        plt.plot(x, y_pdf, 'r', label='Density')
        plt.legend()
        s = 'plts/maxp_' + filename
        plt.savefig(s, bbox_inches='tight')
        plt.show()
        plt.clf()

        if axis == 0:
            series = time_series[index_min, 0, :]
        else:
            series = time_series[:, 0, index_min]
        _, bins, _ = plt.hist(series, label='Histogram', color='white', ec='black', density=True)
        x = np.linspace(bins[0] - 0.5, bins[-1] + 0.5, 200)
        y_pdf = distribution.pdf(x, *params[index_min])
        plt.ylabel('Relative Frequency')
        plt.plot(x, y_pdf, 'r', label='Density')
        plt.legend()
        s = 'plts/minp_' + filename
        plt.savefig(s, bbox_inches='tight')
        plt.show()


def sensitivity(p):
    def simul(initial_param, f_param, indicator, show=False):
        lasts = []
        ls_param = np.linspace((1 - p) * initial_param, (1 + p) * initial_param, 40)
        for param in ls_param:
            funs = f_param(param)
            if show:
                print(funs)
            if indicator == 0:
                series = euler_m(funs, g, delta_t, x0, n, bm=bm, tf=T)
            else:
                series = euler_m(f, funs, delta_t, x0, n, bm=bm, tf=T)
            lower, upper = prediction_bands(series)
            lasts.append((lower[-1], upper[-1]))
        return lasts, ls_param

    def plot_sens(ls, lasts1, var):
        plt.plot(ls, list(map(lambda x: x[0], lasts1)), label='Lower bounds')
        plt.plot(ls, list(map(lambda x: x[1], lasts1)), label='Upper bounds')
        plt.xlabel(var)
        plt.ylabel('$B_{t_f}$')
        plt.legend()
        plt.savefig('plts/' + var[2:-1] + '_sens.pdf', bbox_inches='tight')
        # plt.show()
        plt.clf()

    print('Starting alpha')
    alpha_lasts, ls_alpha = simul(alpha, lambda a: a * (mu - x), 0, show=True)
    plot_sens(ls_alpha, alpha_lasts, '$\\alpha$')
    print('Starting mu')
    mu_lasts, ls_mu = simul(mu, lambda mu: alpha * (mu - x), 0, show=True)
    plot_sens(ls_mu, mu_lasts, '$\mu$')
    print('Starting sigma')
    sigma_last, ls_sigma = simul(sigma, lambda sigma: sigma * x ** gamma, 1, show=True)
    plot_sens(ls_sigma, sigma_last, '$\sigma$')
