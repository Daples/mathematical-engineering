import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import scipy.stats as st
from matplotlib import rc
from arch.unitroot import VarianceRatio
from prediction2 import hurst
from scipy.optimize import least_squares
from sim_par import euler_m_ns
from prediction2 import hists
from prediction import plot_prediction_bands


rc('text', usetex=True)
plt.rcParams.update({'font.size': 18})
np.random.seed(123456789)

# Temperatures in Canada (from hlaniado)
file = open("temps.txt").readlines()
file = list(map(lambda x: x.replace("\n", "").split("\t"), file))
n_years = 4
temperatures = np.array(file, dtype=float)
series = temperatures[:, range(n_years)].transpose().flatten()
series_pred = temperatures[:, range(n_years, 2*n_years)].transpose().flatten()
ts = np.linspace(1, len(series) + 1, len(series))
plot = False

if plot:
    plt.plot(series,'k')
    plt.xlabel('$t$')
    plt.ylabel('$T_t$')
    plt.savefig('plts/temps.pdf', bbox_inches='tight')
    plt.show()

# Test for mean reversion
def test_mean_reversion(times_series):
    print(VarianceRatio(series))
    print(VarianceRatio(series, lags=4))
    print(VarianceRatio(series, lags=8))
    print(VarianceRatio(series, lags=16))
    print(hurst(series))


def estimate_trend(time_series):
    def fun(a):
        return np.subtract(sine(ts, a), time_series)
    a0 = (1, 1, 1, 1)
    return least_squares(fun, a0)


def sine(t1, a):
    return a[0] + a[1] * t1 + a[2] * np.sin((2 * np.pi) / 365 * t1) + a[3] *np.cos((2 * np.pi) / 365 * t1)

def plot_trend(time_series):
    res = estimate_trend(time_series)
    if plot:
        plt.plot(ts, time_series,'k', label='Data')
        plt.plot(ts, sine(ts, res.x), 'r', label='Estimated trend')
        plt.xlabel('$t$')
        plt.ylabel('$T_t$')
        plt.ylim((-10, 30))
        plt.legend()
        plt.savefig('plts/sine_trend.pdf', bbox_inches='tight')
        plt.show()

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

def estimate_sigma(time_series, a_param, a_sine, sigmas):
    Nmu = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    sigma_estimated = []
    index = 0
    for month in range(n_years * len(Nmu)):
        days_month = Nmu[month % len(Nmu)]
        temp_month = time_series[(index + 1):(index + days_month)]
        j1 = ts[(index + 1):(index + days_month - 1)]
        Tj1 = temp_month[:-1]
        ej1 = np.random.normal()
        Tj1m = sine(j1, a_sine)
        Tv = a_param * Tj1m + (1 - a_param) * Tj1 + sigmas[month] * ej1
        aux = (Tv - a_param * Tj1m - (1 - a_param) * Tj1) ** 2
        sigma_estimated.append(np.sum(aux) / (days_month - 2))
        index += days_month
    return sigma_estimated


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

res = estimate_trend(series)
sigmas = estimate_sigma_no_a(series)
sigmas_day = sigma_days(sigmas)
m = 5
for i in range(m):
    a = estimate_a(ts, series, sigmas)
    sigmas = estimate_sigma(series, a, res.x, sigmas)

def f(x, t):
    return a * (sine(t, res.x) - x)
def g(x, t):
    return sigmas_day[int(t - 1)]
def g_pred(x, t):
    return sigmas_day[-1]

delta_t = 1
x0 = series[0]
t0 = 1
n = 1

n = 1000
xt_pred = euler_m_ns(f, g_pred, delta_t, series[-1], n, bm=None, tf=2 * len(series), t0=len(series), show=True)
ts_pred = np.linspace(len(series), 2 * len(series) - 1, len(series))

plot_prediction_bands(ts_pred, xt_pred, 'plts/bands_prediction3.pdf', dist='norm')

# for j in range(xt_pred.shape[0]):
#     if j == 0:
#         plt.plot(ts_pred, xt_pred[j, 0, :], 'r', alpha=0.5, label='Prediction')
#     else:
#         plt.plot(ts_pred, xt_pred[j, 0, :], 'r', alpha=0.01)
# plt.plot(ts_pred, series_pred, 'k')
# plt.plot(ts, series, 'k', label='Data')
# plt.plot([len(series), len(series)], (-30,30), 'k--', alpha=0.5)
# plt.xlabel('$t$')
# plt.ylabel('$T_t$')
# plt.legend()
# plt.savefig('plts/pred_estimated_temps.pdf')
# plt.show()