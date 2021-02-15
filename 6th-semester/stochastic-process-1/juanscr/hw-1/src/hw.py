import numpy as np

# Read data
data = open("d1.txt", "r")
data = list(map(lambda x: x.replace('"', "").replace("\n", ""),
                data.readlines()[1:]))
data = np.array(list(map(lambda x: x.split(" "), data))).transpose()

mat = np.zeros((2, 2))
dic = {"PSPS": (0, 0), "PSCC": (0, 1),
       "CCPS": (1, 0), "CCCC": (1, 1)}


def joi(val):
    return val[0] + val[1]


# Transition matrix
for i in range(data.shape[0]):
    for j in range(data.shape[1] - 1):
        pos = dic[joi(data[i, j:j+2])]
        mat[pos] += 1

for i in range(mat.shape[0]):
    mat[i, :] = mat[i, :] / sum(mat[i, :])

# Calculate pi
s_mat = np.array([[mat[0, 0] - 1, mat[1, 0]], [1, 1]])
pi = np.linalg.solve(s_mat, np.array([0, 1]))


# Calculate closeness
pn = np.linalg.matrix_power(mat, 365)

# Fourth point
vmat = np.array([[mat[0, 0] + 0.05, mat[0, 1] - 0.05], mat[1, :]])
s_mat = np.array([[vmat[0, 0] - 1, vmat[1, 0]], [1, 1]])
print(vmat)
pi2 = np.linalg.solve(s_mat, np.array([0, 1]))
print(pi2)
eu1 = pi[0] * 365 * 100 * 10 ** 6
eu2 = pi2[0] * 365 * 100 * 10 ** 6

print(eu1)
print(eu2)

if eu2 - eu1 >= 500 * 10**6:
    print(eu2 - eu1)
    print("Worth")
