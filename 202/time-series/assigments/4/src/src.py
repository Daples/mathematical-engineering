import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import statsmodels.api as sm

plt.rc('text', usetex=True)
plt.rcParams.update({'font.size': 15})

def autocov(x, j):
    s = 0
    mean = np.mean(x)
    n = np.size(x)
    for t in range(j, n):
        s += (x[t] - mean)*(x[t-j] - mean)
    return s/(n - 1)


def autocorr(x, j):
    return autocov(x, j)/autocov(x, 0)


x = [2, 3, 1, -1, -4, -2, 0, 2, 1, -2]
rs = []
for j in range(1, 4):
    rs.append(autocorr(x, j))
    print("rho_"+str(j), ":", autocorr(x, j))
rs = np.reshape(rs, (len(rs), 1))


# returns vector of AR coefficients
def yule_walker(rs):
    j = rs.shape[0]
    A = np.ones((j, j))
    for k in range(j-1):
        A[(k+1):, k] = rs[:-(k+1), 0]
        A[k, (k+1):] = rs[:-(k+1), 0]
    return np.matmul(np.linalg.inv(A), rs)


# returns \hat{p}_j^j
def pacf(x, j, rs=None):
    if j == 1:
        return autocorr(x, j)
    else:
        if rs is None:
            rs = []
            for i in range(1, j+1):
                rs.append(autocorr(x, i))
            rs = np.reshape(rs, (len(rs), 1))

        return yule_walker(rs)[-1, 0]


for j in range(1, 4):
    print('rho_' + str(j) + str(j) + ':', pacf(x, j))


def process(x0, T, theta, sigma2=1):
    e = st.norm.rvs(size=(T), loc=0, scale=sigma2**0.5)
    xs = np.zeros(T)
    xs[0] = x0
    for t in range(1, T):
        xs[t] = xs[t-1] + e[t] - theta*e[t-1]
    return xs


def diff(x):
    xs = np.zeros(x.size - 1)
    for t in range(xs.size):
        xs[t] = x[t+1] - x[t]
    return xs


xs = process(0, 10000, 0.6)
ws = diff(xs)

lags = 40
fig1 = sm.graphics.tsa.plot_acf(ws, lags=lags)
plt.xlabel("lag")
plt.ylabel("$\hat{\\rho}_j$")
plt.title("")
plt.savefig("acf.pdf", bbox_inches='tight')

fig2 = sm.graphics.tsa.plot_pacf(ws, lags=lags)
plt.xlabel("lag")
plt.ylabel("$\hat{\\rho}_j^j$")
plt.title("")
plt.savefig("pacf.pdf", bbox_inches='tight')