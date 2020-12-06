#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

from matplotlib import rc

rc("text", usetex = True)
plt.rcParams.update({'font.size': 15})

# ============ Functions ============ #
def linear_regression(cov, noises, distances, results):
    time_series = []
    for cov in covariances:
        for noise in noises:
            key = cov + "-" + distances[0] + "-" + noise
            key1 = cov + "-" + distances[1] + "-" + noise

            results1 = results[key]
            results2 = results[key1]

            for i in range(len(results1)):
                time_series.append([results1[i][1], results2[i][1]])

    time_series = np.array(time_series)
    time_series = time_series / np.max(time_series, axis=0)

    model = sm.OLS(time_series[:, 1], time_series[:, :1]).fit()
    b1 = model.params
    b0 = time_series[:, 1].mean() - b1 * time_series[:, 0].mean()

    xlinear = np.linspace(0, 1, 1000)
    ylinear = b1 * xlinear + b0

    plt.scatter(time_series[:, 0], time_series[:, 1], color='k', s=8)
    plt.plot(xlinear, ylinear, 'r', label="{} $x +$ {}".format(round(b1[0], 2),
                                                            round(b0[0], 2)))
    plt.legend()
    plt.xlabel(distances[0])
    plt.ylabel(distances[1])
    plt.savefig("figs/linear.pdf", bbox_inches='tight')
    plt.show()

# ============ Main ============ #
# File CSV
file_csv = open("results/performance.csv").readlines()
lines = list(map(lambda x: x.split(","), file_csv))

# Reconstruct dictionary
results = {}
covariances = []
noises = []
distances = []

# Read csv
i = 0
while i < len(lines):
    cov = lines[i][0]
    dist = lines[i][1]
    noise = lines[i][2][:-1]

    i += 2
    res = []
    for _ in range(25):
        res.append([float(lines[i][0]), abs(complex(lines[i][1][:-1]))])
        i += 1

    if cov not in covariances:
        covariances.append(cov)
    if noise not in noises:
        noises.append(noise)
    if dist not in distances:
        distances.append(dist)

    key = cov + "-" + dist + "-" + noise
    results[key] = res

