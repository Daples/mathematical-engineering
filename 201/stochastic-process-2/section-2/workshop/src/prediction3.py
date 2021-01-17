import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from matplotlib import rc
from arch.unitroot import VarianceRatio
from prediction2 import hurst
from scipy.optimize import least_squares
from sim_par import euler_m_ns
from sim import brownian_motion
from prediction import plot_prediction_bands

rc('text', usetex=True)
plt.rcParams.update({'font.size': 18})
np.random.seed(123456789)


# Test for mean reversion
def test_mean_reversion(times_series):
    print(VarianceRatio(times_series))
    print(VarianceRatio(times_series, lags=4))
    print(VarianceRatio(times_series, lags=8))
    print(VarianceRatio(times_series, lags=16))
    print(hurst(times_series))


def estimate_trend(time_series):
    def fun(a):
        return np.subtract(sine(ts, a), time_series)
    a0 = (1, 1, 1, 1)
    return least_squares(fun, a0)


def sine(t1, a):
    return a[0] + a[1] * t1 + a[2] * np.sin((2 * np.pi) / 365 * t1) + a[3] *np.cos((2 * np.pi) / 365 * t1)


def plot_trend(ts, time_series):
    res = estimate_trend(time_series)
    if plot:
        plt.plot(ts, time_series,'k', label='Data')
        plt.plot(ts, sine(ts, res.x), 'r', label='Estimated trend')
        plt.xlabel('$t$')
        plt.ylabel('$T_t$')
        plt.legend()
        plt.savefig('plts/sine_trend.pdf', bbox_inches='tight')
        plt.clf()


def estimate_sigma_no_a(time_series):
    Nmu = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sigma_estimated = []
    index = 0
    for month in range(n_years * len(Nmu)):
        days_month = Nmu[month % len(Nmu)]
        temp_month = time_series[index:(index + days_month)]
        sigma_estimated.append(np.sum(temp_month[1:] - temp_month[:-1]) ** 2 / days_month)
        index += days_month
    return sigma_estimated


def sigma_days(sigmas):
    Nmu = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sigmas_day = []
    for i in range(len(sigmas)):
        for j in range(Nmu[i % len(Nmu)]):
            sigmas_day.append(sigmas[i])
    return sigmas_day


def estimate_a(ts, time_series, sigmas):
    res = estimate_trend(time_series)
    sigmas_day = sigma_days(sigmas)
    Tm = sine(ts, res.x)
    sum_num = 0
    sum_denom = 0
    for day in range(1, len(time_series)):
        Y = (Tm[day - 1] - time_series[day - 1]) / sigmas_day[day - 1]
        sum_num += Y * (time_series[day] - Tm[day])
        sum_denom += Y * (time_series[day - 1] - Tm[day - 1])
    return -np.log(sum_num / sum_denom)


def differences(time_series):
    diffs = time_series[1:] - time_series[:-1]
    params = st.norm.fit(diffs)
    ts = np.linspace(st.norm.ppf(0.01), st.norm.ppf(0.99), 500)
    fitted_pdf = st.norm.pdf(ts, *params)
    plt.plot(diffs, 'k')
    plt.savefig('plts/diffs_temps.pdf', bbox_inches='tight')
    plt.xlabel('$t$')
    plt.ylabel('$T_{t+1}-T_t$')
    plt.xlabel('$t$')
    plt.clf()

    plt.plot(ts, fitted_pdf, 'r', label='Fitted density')
    plt.hist(diffs, color='w', ec='black', density=True, label='Histogram')
    plt.legend()
    plt.ylabel('$T_{t+1}-T_t$')
    plt.savefig('plts/hist_diffs_temps.pdf', bbox_inches='tight')
    plt.clf()


# File Reading
file = open("temps.txt").readlines()
file = list(map(lambda x: x.replace("\n", "").split("\t"), file))

# Number of years
n_years = 4

# Extract first n_years
temperatures = np.array(file, dtype=float)
series = temperatures[:, range(-1, -n_years - 1, -1)].transpose().flatten()

# Extract prediction period
series_pred = temperatures[:, range(-n_years - 1, -2*n_years - 1, -1)].transpose().flatten()

# Time frames
ts = np.linspace(0, len(series), len(series))
ts_pred = np.linspace(len(series), 2*len(series), len(series))

# Plotting of initial series
plot = True
if plot:
    plt.plot(series,'k')
    plt.xlabel('$t$')
    plt.ylabel('$T_t$')
    plt.savefig('plts/temps.pdf', bbox_inches='tight')

# Tests for mean reversion
test_mean_reversion(series)

# Find trend and plot
plot_trend(ts, series)

# Plotting Driving Noise
differences(series)

# Estimate trend of the series
res = estimate_trend(series)

# Estimate sigmas
sigmas = estimate_sigma_no_a(series)

# Create a simple function of sigmas in each day of the month
sigmas_day = sigma_days(sigmas)

# Estimate alpha based on the obtained sigmas
a = estimate_a(ts, series, sigmas)


# Functions to simulate the SDE
def f(x, t):
    return a * (sine(t, res.x) - x)


def g(x, t):
    return sigmas_day[int(t)]


# Supposing constant sigma for prediction
def g_pred(x, t):
    return sigmas_day[-1]


# Simulation of SDE in original time and prediction
delta_t = 1
n = 1000
bm = brownian_motion(1000, ts[-1] - ts[0], delta_t)
bm_pred = brownian_motion(n, ts_pred[-1] - ts_pred[0], delta_t)

xt = euler_m_ns(f, g, delta_t, series[0], 1000, bm=bm, tf=ts[-1], t0=ts[0], show=True)
xt_pred = euler_m_ns(f, g_pred, delta_t, series[-1], n, bm=bm_pred, tf=ts_pred[-1], t0=ts_pred[0], show=True)

# Plotting both original period and prediction
# OG
plt.plot(ts, xt[:, 0, :].mean(axis=0), 'r', label='Simulation', linewidth=0.5)
plt.plot(ts, series, 'k', label="Data", linewidth=0.5)
plt.xlabel("Days")
plt.ylabel("$T_t$")
plt.legend()
plt.savefig("plts/estimated_temps.pdf", bbox_inches='tight')
plt.clf()

# PRED
plt.plot(ts_pred, xt_pred[0, 0, :], 'r', label='Simulation', linewidth=0.5)
plt.plot(ts, series, 'k', label="Data", linewidth=0.5)
plt.plot(ts_pred, series_pred, 'k', linewidth=0.5)
plt.xlabel("Days")
plt.ylabel("$T_t$")
plt.legend()
plt.savefig("plts/pred_estimated_temps.pdf", bbox_inches='tight')
plt.clf()

# Finding prediction bands for prediction
plot_prediction_bands(ts_pred, xt_pred, "plts/bands_prediction3.pdf", alpha1=0.1, linewidth=0.5,
                      show=False, dist='norm')
