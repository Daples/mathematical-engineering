import scipy.stats as st
import matplotlib.pyplot as plt
import numpy as np

distribution0 = "alpha"
params0 = [0.1764, 0.0748, 0.2752]
distribution1 = "johnsonsu"
params1 = [-1.0438, 0.8206, 0.2698, 0.0661]
distribution2 = "johnsonsb"
params2 = [1.1338, 0.5656, 0.2592, 5.0864]


def plot(distribution, params):
    dist = getattr(st, distribution)

    loc = params[-2]
    scale = params[-1]
    arg = params[:-2]
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale)
    end1 = dist.ppf(0.99, *arg, loc=loc, scale=scale)
    x = np.linspace(start, end1, 1000)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)

    plt.clf()
    plt.plot(x, y, 'b', label=distribution)
    plt.savefig(distribution + ".pdf", bbox_inches='tight')


plot(distribution0, params0)
plot(distribution1, params1)
plot(distribution2, params2)
