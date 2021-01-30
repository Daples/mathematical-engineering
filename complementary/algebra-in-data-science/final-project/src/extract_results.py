#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

from matplotlib import rc, colors, cm

rc("text", usetex = True)
plt.rcParams.update({'font.size': 15})

# ============ Functions ============ #
def linear_regression(covariances, noises, distances, results):
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

def pareto_curve(covariances, noises, distances, results):
    # Pareto curve
    points_author = {}
    points_fro = {}
    points_noise = {}
    for cov in covariances:
        points_cov_author = []
        points_cov_fro = []
        points_noise_cov_a = []
        points_noise_cov_f = []
        for dist in distances:
            for noise in noises:
                key = cov + "-" + dist + "-" + noise
                if dist == distances[0]:
                    points_cov_author += results[key]
                    if noise == "impulse":
                        points_noise_cov_a += results[key]
                elif dist == distances[1]:
                    points_cov_fro += results[key]
                    if noise == "impulse":
                        points_noise_cov_f += results[key]


        points_cov_author = np.array(points_cov_author)
        points_cov_fro = np.array(points_cov_fro)
        points_author[cov] = points_cov_author
        points_fro[cov] = points_cov_fro

        points_noise_cov_a = np.array(points_noise_cov_a)
        points_noise_cov_f = np.array(points_noise_cov_f)
        points_noise[cov] = points_noise_cov_a

    # Plotting 1
    color1 = plt.get_cmap('gnuplot')
    color_norm = colors.Normalize(vmin=0, vmax=len(points_author))
    scalar_map = cm.ScalarMappable(norm=color_norm, cmap=color1)

    i = 0
    for cov in points_author:
        color = scalar_map.to_rgba(i)
        plt.scatter(points_author[cov][:, 0], points_author[cov][:, 1], color=color,
                    s=12, label=cov)
        i += 1
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("$\lambda$")
    plt.ylabel("Distance to original")
    plt.savefig("figs/author-scatter.pdf", bbox_inches='tight')

    plt.clf()

    # Plotting 2
    i = 0
    for cov in points_fro:
        color = scalar_map.to_rgba(i)
        plt.scatter(points_fro[cov][:, 0], points_fro[cov][:, 1], color=color, s=12,
                    label=cov)
        i += 1
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("$\lambda$")
    plt.ylabel("Distance to original")
    plt.savefig("figs/fro-scatter.pdf", bbox_inches='tight')

    plt.clf()

    # Plotting 3
    i = 0
    for cov in points_noise:
        color = scalar_map.to_rgba(i)
        plt.scatter(points_noise[cov][:, 0], points_noise[cov][:, 1],
                    color=color, s=12, label=cov)
        i += 1
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlabel("$\lambda$")
    plt.ylabel("Distance to original")
    plt.savefig("figs/noise-scatter.pdf", bbox_inches='tight')

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

pareto_curve(covariances, noises, distances, results)
