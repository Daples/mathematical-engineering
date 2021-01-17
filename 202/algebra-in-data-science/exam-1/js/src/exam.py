# Packages and global behavior
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.linalg as la

from matplotlib import rc
from sklearn.covariance import ledoit_wolf, oas

rc('text', usetex=True)

########### Third Point ###########
# Order of matrix
n = 5

# Hilbert Matrix
h5 = la.hilbert(n)

# Create the xn
ns = range(1, 101)
xs = list(map(lambda n_aux: n_aux * np.ones((n, 1)), ns))

# Create all the bn
bs = list(map(lambda x: h5.dot(x), xs))

# Create the pseudo solutions
x_apr = list(map(lambda b: np.linalg.inv(h5).dot(b), bs))

# Create graph for distances
distances = []
for i in range(len(xs)):
    norm = np.linalg.norm(xs[i] - x_apr[i], ord='fro')
    distances.append(np.sqrt(norm))

plt.plot(ns, distances, 'k')
plt.xlabel("$n$")
plt.ylabel("$d_2(x, \hat{x})$")
plt.savefig("hilbert_distance.pdf", bbox_inches='tight')
plt.clf()

# Solution
x_apr_pseudo = list(map(lambda b: np.linalg.pinv(h5).dot(b), bs))

# Create graph for distances
distances_p = []
for i in range(len(xs)):
    norm = np.linalg.norm(xs[i] - x_apr_pseudo[i], ord='fro')
    distances_p.append(np.sqrt(norm))

plt.plot(ns, distances_p, 'k')
plt.xlabel("$n$")
plt.ylabel("$d_2(x, \hat{x})$")
plt.savefig("hilbert_distance_pseudo.pdf", bbox_inches='tight')
plt.clf()

########### Fourth Point ###########
# Succession
def a_n(n):
    aux = np.array([[1, 2, 3],
                    [2 + 1 / n ** 2, 4 + 1 / n ** 2, 6 + 1 / (2 * n ** 2)],
                    [3 + 1 / (n + 1), 6 + 1 / (2*n + 1), 9 + 1 / (3*n + 2)]])

    return aux

# Succession B
def b(n):
    an = a_n(n)
    return an.T.dot(an)

# Plotting condition number
n_mat = range(1, 100)
conds = list(map(lambda n: np.linalg.cond(b(n)), n_mat))
plt.plot(n_mat, conds, 'k')
plt.xlabel("$n$")
plt.ylabel("$\mathrm{cond}(B_n)$")
plt.savefig("cond_b.pdf", bbox_inches='tight')
plt.clf()

# Ledoit wolf
def generate_dataset(n):
    means = [1, 1, 1]
    data = np.random.multivariate_normal(means, b(n), size=500)
    return data

conds_lw = list(map(lambda n: np.linalg.cond(ledoit_wolf(generate_dataset(n))[0]), n_mat[2:]))
plt.plot(n_mat[2:], conds_lw, 'k')
plt.xlabel("$n$")
plt.ylabel("$\mathrm{cond}(\mathrm{LW}(D_n))$")
plt.savefig("cond_b_lw.pdf", bbox_inches='tight')
plt.clf()

# Plotting determinant of LW
dets = list(map(lambda n: np.linalg.det(ledoit_wolf(generate_dataset(n))[0]), n_mat))
plt.plot(n_mat, dets, 'k')
plt.xlabel("$n$")
plt.ylabel("$\mathrm{det}(\mathrm{LW}(D_n))$")
plt.savefig("det_lw.pdf", bbox_inches='tight')
plt.clf()

########### Fifth Point ###########
# Read portafolio (Generic code from workshop)
file = open("portfolio100.txt").readlines()
data = []
for line in file:
    row = []
    acum = ""
    for char in line:
        if char != " ":
            acum += char
        if char == " " and len(acum) != 0:
            row.append(float(acum))
            acum = ""
    if acum != "":
        row.append(float(acum))
    data.append(row)

data = np.array(data, dtype=np.float)

# Function for binary distances with Pearson method
def binary_distances(matrix, means):
    dists = np.zeros(matrix.shape[1])
    for j in range(matrix.shape[1]):
        a, b, c, d = 0, 0, 0, 0
        for i in range(matrix.shape[0]):
            if matrix[i, j] == means[i]:
                cond = int(matrix[i, j] == 1)
                a += cond
                d += 1 - cond
            else:
                cond = int(matrix[i, j] == 1)
                b += cond
                c += 1 - cond
        dists[j] = (a*d - b*c) / (np.sqrt((a+c) * (b+d) * (a+b) * (c+d)))
    return dists

# Last column
lc = np.zeros(data.shape[0])
lc[data[:, -1] > 0] = 1

# Binary matrix
binary_data = np.zeros(data.shape)
binary_data[data > 0] = 1

# Distance vector
dists = binary_distances(binary_data, lc)
indexes = dists.argsort()[:2]
best_columns = data[:, indexes]

# Plotting of data
plt.scatter(best_columns[:, 0], best_columns[:, 1], s=4, c='k')
plt.xlabel("$x_{" + str(indexes[0]) + "}$")
plt.ylabel("$x_{" + str(indexes[1]) + "}$")
plt.savefig("data.pdf", bbox_inches='tight')
plt.clf()

# Mahalanobis distance
def mahalanobis(data, mu, icov):
    diff = data - mu
    return np.sqrt((diff.dot(icov) * diff).sum(-1))

# Removal of outliers
def remove_outliers(dataset, cov):
    mean = np.mean(dataset, axis = 0)
    distances = mahalanobis(dataset, mean, np.linalg.inv(cov))
    perc_90 = np.percentile(distances, 90)

    # Data separation
    data_small = dataset[distances <= perc_90, :]
    data_big = dataset[distances > perc_90, :]

    return data_small, data_big

# Correlation to covariance
def corr_to_cov(data, correlation):
        stds = data.std(axis=0, ddof=1)
        cov = np.zeros(correlation.shape)
        for i in range(correlation.shape[0]):
            for j in range(correlation.shape[1]):
                cov[i, j] = correlation[i, j] * stds[i] * stds[j]
        return cov

# Different covariances
cov1 = np.cov(best_columns.T) # Standard
cov2, _ = ledoit_wolf(best_columns) # LW
cov3 = corr_to_cov(best_columns, pd.DataFrame(best_columns).corr(
       method="kendall").to_numpy()) # Kendall
cov4, _ = oas(best_columns)

# Plotting method
def plotting(data, cov, figname):
    icov = np.linalg.inv(cov)
    data_small1, data_big1 = remove_outliers(data, icov)
    plt.scatter(data_small1[:, 0], data_small1[:, 1], color='k', s=4)
    plt.scatter(data_big1[:, 0], data_big1[:, 1], color='r', s=4)
    plt.savefig(figname, bbox_inches='tight')

# Plotting for each covariance
plotting(best_columns, cov1, "cov-standard.pdf")
plotting(best_columns, cov2, "cov-lw.pdf")
plotting(best_columns, cov3, "cov-kendall.pdf")
plotting(best_columns, cov4, "cov-oas.pdf")
