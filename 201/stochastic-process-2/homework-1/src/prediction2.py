import matplotlib.pyplot as plt
import numpy as np
from sympy.abc import x
from sim_par import euler_m
from sim import brownian_motion
from scipy.stats import norm, lognorm
from matplotlib import rc
from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()
rc('text', usetex=True)
plt.rcParams.update({'font.size': 18})
np.random.seed(123456789)

# # Parameters
alpha = 0.5
mu = 0.5
sigma = 0.5
gamma = 0

delta_t = 1/500
x0 = np.array([1])

# Function
f = alpha * (mu - x)
g = sigma * x ** gamma
linewidth = 0.5
bm = brownian_motion(1, 1, delta_t)
series2 = euler_m(f, g, delta_t, x0, 1, bm=bm)
ts = np.linspace(0, 1, 500)
plot = False
if plot:
    plt.plot(ts, series2[0, 0, :], 'k', linewidth=linewidth)
    plt.xlabel('$t$')
    plt.ylabel('$X_t$')
    plt.savefig('plts/ornstein_serie2.pdf', bbox_inches='tight')
    plt.show()

print(np.mean(series2, axis=2))