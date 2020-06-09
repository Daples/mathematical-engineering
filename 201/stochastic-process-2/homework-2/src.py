import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from statsmodels.distributions.empirical_distribution import ECDF
from matplotlib import rc
from joblib import Parallel, delayed
import multiprocessing
from sim_par import brownian_motion, euler_m_ns
from tqdm import tqdm


num_cores = multiprocessing.cpu_count()
np.random.seed(123456789)
rc('text', usetex=True)

file = pd.read_csv('FB.csv')
prices = file['Close'].to_numpy()
returns = np.log(prices[1:] / prices[:-1])


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
    for _ in range(W):
        Sts = simulate_GBM(M, r, sigma, T, S0, delta_t, show=False)
        payoffs = np.vstack((Sts[:, -1] - K, np.zeros(Sts.shape[0]))).max(axis=0)
        fcall = np.exp(-r * T) * np.mean(payoffs)
        fcalls.append(fcall)
    return np.array(fcalls).mean()


def montecarlo_ou(mu, alpha, lamda, sigma, T, K, S0, M, W, delta_t):
    f = lambda x, t: alpha * (mu - x) - lamda * sigma
    g = lambda x, t: sigma
    fcalls = []
    for _ in range(W):
        Sts = euler_m_ns(f, g, delta_t, S0, M, tf=T)
        payoffs = np.vstack((Sts[:, 0, -1] - K, np.zeros(Sts.shape[0]))).max(axis=0)
        fcall = np.exp(-r * T) * np.mean(payoffs)
        fcalls.append(fcall)
    return np.array(fcalls).mean()


def finite_differences(r, sigma, T, K, S0, NS, NT=None):
    Smax = 3 * S0
    delta_S = Smax / NS
    if NT is None:
        aux = (delta_S / (sigma * Smax)) ** 2
        NT = int(np.ceil(T / aux))

    delta_t = T / NT

    # print('Condition: ', delta_t <= (delta_S / (sigma * Smax)) ** 2)

    f = np.zeros((NT + 1, NS + 1))

    js = np.array(range(NS + 1))
    f[NT, :] = js * delta_S - K
    f[NT, f[NT, :] <= 0] = 0
    f[:, NS] = max(Smax - K, 0)

    term = delta_t / (r * delta_t + 1)
    a = term * (0.5 * sigma ** 2 * js[1:-1] ** 2 - 0.5 * r * js[1:-1])
    b = term * (1 / delta_t - sigma ** 2 * js[1:-1] ** 2)
    c = term * (0.5 * sigma ** 2 * js[1:-1] ** 2 + 0.5 * r * js[1:-1])

    for i in range(NT - 1, -1, -1):
        f[i, 1:-1] = a * f[i+1, :-2] + b * f[i+1, 1:-1] + c * f[i+1, 2:]

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


def parameter_estimation(time_series, gamma):
    delta = 1

    A = 0
    for k in range(1, int(time_series.size)):
        A += time_series[k] * time_series[k - 1] / (time_series[k - 1] ** (2 * gamma))

    B = 0
    for k in range(1, int(time_series.size)):
        B += time_series[k - 1] / (time_series[k - 1] ** (2 * gamma))

    C = 0
    for k in range(1, int(time_series.size)):
        C += time_series[k] / (time_series[k - 1] ** (2 * gamma))

    D = 0
    for k in range(1, int(time_series.size)):
        D += 1 / (time_series[k - 1] ** (2 * gamma))

    E = 0
    for k in range(1, int(time_series.size)):
        E += (time_series[k - 1] / (time_series[k - 1] ** gamma)) ** 2

    alpha = (E * D - B ** 2 - A * D + B * C) / ((E * D - B **2) * delta)
    mu = (A - E * (1 - alpha * delta)) / (alpha * B * delta)
    S = 0
    for k in range(1, int(time_series.size)):
        S += ((time_series[k] - time_series[k - 1] - (alpha * (mu - time_series[k - 1]) * delta))
              / (time_series[k - 1] ** gamma)) ** 2
    sigma = ((1 / (int(time_series.size) * delta)) * S) ** 0.5

    print('alpha', alpha)
    print('mu', mu)
    print('sigma', sigma)
    return alpha, mu, sigma



##################################
def first_question():

    params = st.lognorm.fit(prices)
    _, p_val = st.kstest(prices, 'lognorm', args=params)


    plot = True
    xs = np.linspace(st.lognorm.ppf(0.01, *params), st.lognorm.ppf(0.99, *params), 1000)
    if plot:
        plt.hist(prices, density=True, color='white', ec='black', label='Data')
        plt.plot(xs, st.lognorm.pdf(xs, *params), 'r', label='Fitted')
        plt.legend()
        plt.savefig('plts/price_fitting.pdf', bbox_inches='tight')
        plt.clf()

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
        plt.clf()

    delta_t = 1
    sigma = estimate_volatility(prices, delta_t)
    r = 0.0065
    T = prices.size
    Ks = [200, 100, 50]
    S0 = prices[-1]

    # Montecarlo
    M = 10000
    W = 1000

    fs_montecarlo = []
    for K in Ks:
        fs_montecarlo.append(montecarlo(r, sigma, T, K, S0, M, W, delta_t))

    # Finite Differences
    NS = 1000
    fs_finite = []
    for K in Ks:
        fs_finite.append(finite_differences(r, sigma, T, K, S0, NS))

    # Binomial Tree
    N = 100
    fs_tree = []
    for K in Ks:
        fs_tree.append(binomial_tree(r, sigma, T, K, S0, N))

    # Exact
    fs_exact = []
    for K in Ks:
        fs_exact.append(exact(r, sigma, T, K, S0))

    print('Exact: ',fs_exact)
    print('\nMontecarlo: ', fs_montecarlo)
    print('\nFinite Differences: ',fs_finite)
    print('\nBinomial Tree: ',fs_tree)


def second_question():
    S0 = returns[-1]
    params = st.norm.fit(returns)
    plot = True
    if plot:
        ts = np.linspace(st.norm.ppf(0.01, *params), st.norm.ppf(0.99, *params), 1000)
        pdf = st.norm.pdf(ts, *params)
        plt.hist(returns, density=True, color='white', ec='black', label='Histogram')
        plt.plot(ts, pdf, 'r', label='Estimation')
        plt.legend()
        plt.savefig('plts/return_fitting.pdf', bbox_inches='tight')
        plt.clf()
    _, p_value = st.jarque_bera(returns)
    print('pval: ', p_value)

    gamma = 0
    alpha, mu, sigma = parameter_estimation(returns, gamma)
    if plot:
        f = lambda x, t: alpha * (mu - x)
        g = lambda x, t: sigma * x ** gamma
        xs = euler_m_ns(f, g, 1, returns[0], 1, tf=returns.size)
        plt.plot(returns, 'k', label='Data')
        plt.plot(xs[0, 0, :], 'r', label='Simulation')
        plt.xlabel('$t$')
        plt.ylabel('$S_t$')
        plt.legend()
        plt.savefig('plts/ou.pdf', bbox_inches='tight')
        plt.clf()

    lamda = 0.125
    Ks = [-0.1, -1, -3]
    fs_montecarlo = []

    # Montecarlo
    M = 10000
    W = 1000
    for K in Ks:
        fs_montecarlo.append(montecarlo_ou(mu, alpha, lamda, sigma, T, K, S0, M, W, delta_t))

    print(fs_montecarlo)



def sensitivity(p, og_param, f1, f2, f3, fig_name, param_name, n_param=20, monte=True, finit=True, tree=True,
                isint=False, lb=0.0):
    if p < 0:
        aux = max(lb, (1 + p) * og_param)
        params = np.linspace(aux, (1 - p) * og_param, n_param)
    else:
        params = np.linspace((1 - p) * og_param, (1 + p) * og_param, n_param)

    fs_montecarlo = []
    fs_finite = []
    fs_tree = []

    for param in params:
        if isint:
            param = int(param)
        if monte:
            fs_montecarlo.append(montecarlo(*f1(param)))
        if finit:
            fs_finite.append(finite_differences(*f2(param)))
        if tree:
            fs_tree.append(binomial_tree(*f3(param)))

    ymax = max(fs_montecarlo + fs_finite + fs_tree)
    ymin = min(fs_montecarlo + fs_finite + fs_tree)

    if monte:
        plt.plot(params, fs_montecarlo, 'k', label='Montecarlo')
    if finit:
        plt.plot(params, fs_finite, 'r', label='Finite Diff.')
    if tree:
        plt.plot(params, fs_tree, 'b', label='Binom. Tree')
    plt.plot([og_param, og_param], [ymin, ymax], 'k--', alpha=0.7)
    plt.xlabel(param_name)
    plt.ylabel('$f_{\mathrm{call}}$')
    plt.legend()
    plt.savefig(fig_name, bbox_inches='tight')
    plt.clf()


def sensitivity_ou(p, og_param, f1, fig_name, param_name, n_param=20, isint=False, lb=0.0):
    if p < 0:
        aux = max(lb, (1 + p) * og_param)
        params = np.linspace(aux, (1 - p) * og_param, n_param)
    else:
        params = np.linspace((1 - p) * og_param, (1 + p) * og_param, n_param)

    fs_montecarlo = []

    for param in params:
        if isint:
            param = int(param)
        fs_montecarlo.append(montecarlo_ou(*f1(param)))


    ymax = max(fs_montecarlo)
    ymin = min(fs_montecarlo)

    plt.plot(params, fs_montecarlo, 'k')
    plt.plot([og_param, og_param], [ymin, ymax], 'k--', alpha=0.7)
    plt.xlabel(param_name)
    plt.ylabel('$f_{\mathrm{call}}$')
    plt.savefig(fig_name, bbox_inches='tight')
    plt.clf()

# Option 1
delta_t = 1
sigma = estimate_volatility(prices, delta_t)
r = 0.0065
K = 200
S0 = prices[-1]
T = prices.size

# Option 2
alpha, mu, sigma_ou = parameter_estimation(returns, 0)
lamda = 0.125
K_ou = -1
S0_ou = returns[-1]
T_ou = returns.size

# Montecarlo
M = 5000
W = 500

# Finite Differences
NS = 1000

# Binomial Tree
N = 100

def first_sens():
    def f1(T):
        return [r, sigma, T, K, S0, M, W, delta_t]

    def f2(T):
        return [r, sigma, T, K, S0, NS]

    def f3(T):
        return [r, sigma, T, K, S0, N]

    def f_1(T):
        return [mu, alpha, lamda, sigma_ou, T, K_ou, S0_ou, M, W, delta_t]

    sensitivity(0.5, T, f1, f2, f3, 'plts/first_sens_opt1.pdf', '$T$')
    sensitivity_ou(0.5, T_ou, f_1, 'plts/first_sens_opt2.pdf', '$T$', n_param=20)


def second_sens():
    def f1(r):
        return [r, sigma, T, K, S0, M, W, delta_t]

    def f2(r):
        return [r, sigma, T, K, S0, NS]

    def f3(r):
        return [r, sigma, T, K, S0, N]

    sensitivity(0.5, r, f1, f2, f3, 'plts/second_sens_opt1.pdf', '$r$')


def third_sens():
    def f1(sigma):
        return [r, sigma, T, K, S0, M, W, delta_t]

    def f2(sigma):
        return [r, sigma, T, K, S0, NS]

    def f3(sigma):
        return [r, sigma, T, K, S0, N]

    def f_1(sigma):
        return [mu, alpha, lamda, sigma, T_ou, K_ou, S0_ou, M, W, delta_t]

    sensitivity(0.5, sigma, f1, f2, f3, 'plts/third_sens_opt1.pdf', '$\sigma$')
    sensitivity_ou(0.5, sigma_ou, f_1, 'plts/third_sens_opt2.pdf', '$\sigma$', n_param=20)


def fourth_sens():
    def f1(K):
        return [r, sigma, T, K, S0, M, W, delta_t]

    def f2(K):
        return [r, sigma, T, K, S0, NS]

    def f3(K):
        return [r, sigma, T, K, S0, N]

    def f_1(K):
        return [mu, alpha, lamda, sigma_ou, T_ou, K, S0_ou, M, W, delta_t]

    sensitivity(0.5, K, f1, f2, f3, 'plts/fourth_sens_opt1.pdf', '$K$')
    sensitivity_ou(0.5, K_ou, f_1, 'plts/fourth_sens_opt2.pdf', '$K$', n_param=20)


def fifth_a_sens():
    def f1(M):
        return [r, sigma, T, K, S0, M, W, delta_t]

    def f2(M):
        return []

    def f3(M):
        return []

    def f_1(M):
        return [mu, alpha, lamda, sigma_ou, T_ou, K_ou, S0_ou, M, W, delta_t]

    sensitivity((M - 10) / M, M, f1, f2, f3, 'plts/fifth_a_sens_opt1.pdf', '$M$', finit=False, tree=False, isint=True)
    sensitivity_ou((M - 10) / M, M, f_1, 'plts/fifth_a_sens_opt2.pdf', '$M$', n_param=20, isint=True)


# TODO: Increment W > 100
def fifth_b_sens():
    def f1(W):
        return [r, sigma, T, K, S0, M, W, delta_t]

    def f2(W):
        return []

    def f3(W):
        return []

    def f_1(W):
        return [mu, alpha, lamda, sigma_ou, T_ou, K_ou, S0_ou, M, W, delta_t]

    sensitivity((W - 100) / W, W, f1, f2, f3, 'plts/fifth_b_sens_opt1.pdf', '$W$', finit=False, tree=False, isint=True)
    sensitivity_ou((W - 100) / W, W, f_1, 'plts/fifth_b_sens_opt2.pdf', '$W$', n_param=20, isint=True)


def fifth_c_sens():
    def f1(delta_t):
        return [r, sigma, T, K, S0, M, W, delta_t]

    def f2(delta_t):
        return []

    def f3(delta_t):
        return []

    def f_1(delta_t):
        return [mu, alpha, lamda, sigma_ou, T_ou, K_ou, S0_ou, M, W, delta_t]

    sensitivity(1-T/(100*delta_t), delta_t, f1, f2, f3, 'plts/fifth_c_sens_opt1.pdf', '$\Delta t$', finit=False,
                tree=False, lb=0.1)
    sensitivity_ou(1-T/(100*delta_t), delta_t, f_1, 'plts/fifth_c_sens_opt2.pdf', '$\Delta t$', n_param=20, lb=0.1)


def sixth_sens():
    def f1(NS):
        return []

    def f2(NS):
        return [r, sigma, T, K, S0, NS]

    def f3(NS):
        return []

    sensitivity(0.5, NS, f1, f2, f3, 'plts/sixth_sens_opt1.pdf', '$N_s$', monte=False, tree=False, isint=True)


def seventh_sens():
    def f1(N):
        return []

    def f2(N):
        return []

    def f3(N):
        return [r, sigma, T, K, S0, N]

    sensitivity(0.5, N, f1, f2, f3, 'plts/seventh_sens_opt1.pdf', '$N$', monte=False, finit=False, isint=True)


def eight_sens():
    def f_1(lamda):
        return [mu, alpha, lamda, sigma_ou, T_ou, K_ou, S0_ou, M, W, delta_t]

    sensitivity_ou(0.5, lamda, f_1, 'plts/eight_sens_opt2.pdf', '$\lambda$', n_param=20)


def run_sens():
    print('Starting 1')
    first_sens()
    print('\nStarting 2')
    second_sens()
    print('\nStarting 3')
    third_sens()
    print('\nStarting 4')
    fourth_sens()
    print('\nStarting 5a')
    fifth_a_sens()
    print('\nStarting 5b')
    fifth_b_sens()
    print('\nStarting 5c')
    fifth_c_sens()
    print('\nStarting 6')
    sixth_sens()
    print('\nStarting 7')
    seventh_sens()
    print('\nStarting 8')
    eight_sens()

print('First Question:')
first_question()

print('Second Question:')
second_question()

print('Starting Senstivity:')
run_sens()