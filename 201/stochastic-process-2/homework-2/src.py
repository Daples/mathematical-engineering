import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib import rc
from joblib import Parallel, delayed
import multiprocessing
from sim_par import brownian_motion
from tqdm import tqdm


num_cores = multiprocessing.cpu_count() - 2
np.random.seed(123456789)
rc('text', usetex=True)

def bands(ecdf):
    lower = np.zeros(len(ecdf.y))
    upper = np.zeros(len(ecdf.y))
    for i in range(len(ecdf.y)):
        lower[i] = max(ecdf.y[i] - epsilon, 0)
        upper[i] = min(ecdf.y[i] + epsilon, 1)
    return lower, upper

def calculate_returns(data):
    rs = np.zeros(data.size - 1)
    for i in range(1, data.size):
        rs[i - 1] = (data[i] - data[i - 1]) / data[i - 1]
    return rs

def estimate_volatility(data, delta_t):
    return np.sqrt(calculate_returns(data).var(ddof=1) / delta_t)


def simulate_GBM(M, r, sigma, T, S0, delta_t, bm=None, show=True):
    def aux(traj):
        arr = np.zeros(int(T / delta_t))
        arr[0] = S0
        for i in range(1, arr.size):
            arr[i] = arr[i - 1] * np.exp((r - sigma ** 2 / 2) * delta_t + sigma * (bm[traj, i] - bm[traj, i - 1]))
        return arr

    if bm is None:
        bm = brownian_motion(M, T, delta_t)
    if show:
        St = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(j) for j in tqdm(range(M))))
    else:
        St = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(j) for j in range(M)))
    return St

def exact(r, sigma, T, K, S0):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    f = S0 * st.norm.cdf(d1) - K * np.exp(-r * T) * st.norm.cdf(d2)
    return f

def montecarlo(r, sigma, T, K, S0, M, W, delta_t):
    fcalls = []
    for _ in tqdm(range(W)):
        Sts = simulate_GBM(M, r, sigma, T, S0, delta_t, show=False)
        payoffs = np.vstack((Sts[:, -1] - K, np.zeros(Sts.shape[0]))).max(axis=0)
        fcall = np.exp(-r * T) * np.mean(payoffs)
        fcalls.append(fcall)
    return np.array(fcalls).mean()

def explicit_differences(r, sigma, T, K, S0, NS, NT=None):
    Smax = 3 * S0
    delta_S = Smax / NS
    if NT is None:
        aux = (delta_S / (sigma * Smax)) ** 2
        NT = int(np.ceil(T / aux))

    delta_t = T / NT

    print('Condition: ', delta_t <= (delta_S / (sigma * Smax)) ** 2)

    f = np.zeros((NT + 1, NS + 1))

    js = np.array(range(NS + 1))
    f[NT, :] = js * delta_S - K
    f[NT, f[NT, :] <= 0] = 0
    f[:, NS] = max(Smax - K, 0)

    for i in tqdm(range(NT - 1, -1, -1)):
        for j in range(1, NS - 1):
            term = delta_t / (r * delta_t + 1)
            aj = term * (0.5 * sigma ** 2 * j ** 2 - 0.5 * r * j)
            bj = term * (1 / delta_t - sigma ** 2 * j ** 2)
            cj = term * (0.5 * sigma ** 2 * j ** 2 + 0.5 * r * j)
            f[i,j] = aj * f[i+1, j-1] + bj * f[i+1, j] + cj * f[i+1, j+1]
    return f[0, int(S0 / delta_S)]


def binomial_tree(r, sigma, T, K, S0, N):
    fs = np.zeros((N+1, N+1))
    delta_t = T / N
    u = np.exp(sigma * np.sqrt(delta_t))
    d = np.exp(-sigma * np.sqrt(delta_t))
    p = (np.exp(r * delta_t) - d) / (u - d)

    for j in range(N+1):
        fs[N, j] = max(S0 * u ** j * d ** (N - j) - K, 0)

    for i in range(N-1, -1, -1):
        for j in range(i+1):
            fs[i, j] = np.exp(-r * delta_t) * (p * fs[i+1, j+1] + (1-p) * fs[i+1, j])

    return fs[0,0]



##################################
def first_question():
    file = pd.read_csv('FB.csv')
    prices = file['Close'].to_numpy()

    params = st.lognorm.fit(prices)
    _, p_val = st.kstest(prices, 'lognorm', args=params)


    plot = False
    xs = np.linspace(st.lognorm.ppf(0.01, *params), st.lognorm.ppf(0.99, *params), 1000)
    if plot:
        plt.hist(prices, density=True, color='white', ec='black', label='Data')
        plt.plot(xs, st.lognorm.pdf(xs, *params), 'r', label='Fitted')
        plt.legend()
        plt.savefig('plts/price_fitting.pdf', bbox_inches='tight')
        plt.show()

    if plot:
        alpha = 0.05
        epsilon = np.sqrt(1 / (2 * prices.shape[0]) * np.log(2 / alpha))
        ecdf = ECDF(prices)
        lower, upper = bands(ecdf)
        plt.plot(xs, st.lognorm.cdf(xs,*params), 'r', label='CDF')
        plt.plot(ecdf.x, lower, 'k', alpha=0.3)
        plt.plot(ecdf.x, upper, 'k', alpha=0.3)
        plt.plot(ecdf.x, ecdf.y, 'k', label='ECDF')
        plt.xlabel('$t$')
        plt.ylabel('CDF($t$)')
        plt.legend()
        plt.savefig('plts/ecdf.pdf', bbox_inches='tight')
        plt.show()

    sigma = 0.3
    r = 0.05
    T = 1
    K = 100
    S0 = 100
    # M = 100
    # W = 10
    NT = 500
    NS = 150

    print(binomial_tree(r, sigma, T, K, S0, 300))

def second_question():
    file = pd.read_csv('FB.csv')
    prices = file['Close'].to_numpy()
    print(prices.shape)
    returns = np.log(prices[1:] / prices[:-1])


first_question()