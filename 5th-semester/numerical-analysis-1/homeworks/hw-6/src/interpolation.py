import numpy as np
from sympy.abc import x
from sympy import Poly
from sympy.functions import cos, sin
from sympy import lambdify
from matplotlib import pyplot as plt


def create_polynomial(coefficients):
    poly = 0
    order = len(coefficients) - 1
    for i in range(order + 1):
        poly += coefficients[i]*x**(order - i)
    return poly


def vandermonde(points):
    n = len(points)
    order = n - 1
    vand_matrix = np.zeros((n, n))
    vand_b = np.zeros((n, 1))
    j = 0
    for point in points:
        x1 = point[0]
        y = point[1]
        for i in range(n):
            vand_matrix[j, i] = x1 ** (order - i)
        vand_b[j, 0] = y
        j += 1

    cof = gauss_pivot(vand_matrix, vand_b)
    return create_polynomial(cof)


def gauss_pivot(a, b):
    def index(val, n1):
        if val < n1:
            return 0, val

        row1, col1 = index(val - n1, n1)

        return row1 + 1, col1

    pos = {}
    n = len(a)
    for i in range(n):
        pos[i] = i

    ab = np.concatenate((a.astype(float), b.astype(float)), axis=1)
    for stage in range(n - 1):
        # Change column and rows
        mat_temp = ab[:n, :n].copy()
        for j in range(stage):
            mat_temp[j, :] = np.zeros((1, n))
            mat_temp[:, j] = np.zeros((1, n))

        i_max = np.argmax(abs(mat_temp))
        i1, j1, = index(i_max, n)

        if j1 != stage or i1 != stage:
            # Change column
            temp = ab[:, j1].copy()
            ab[:, j1] = ab[:, stage].copy()
            ab[:, stage] = temp

            # Update position
            temp = pos[stage]
            pos[stage] = pos[j1]
            pos[j1] = temp

            # Change row
            temp = ab[stage, :].copy()
            ab[stage, :] = ab[i1, :].copy()
            ab[i1, :] = temp

        # Change rows
        for row in range(stage + 1, n):
            if ab[row, stage] != 0:
                mult = ab[row, stage]/ab[stage, stage]
                ab[row, stage] = 0
                for col in range(stage + 1, n + 1):
                    ab[row, col] = ab[row, col] - ab[stage, col]*mult

    # Find value of vars
    sol = np.zeros((n, 1))
    for i in range(n):
        j = n - i - 1
        solution_row = ab[j, :]
        sol[j, 0] = solution_row[-1]
        for z in range(n - 1, j, -1):
            sol[j, 0] -= solution_row[z]*sol[z]
        sol[j, 0] /= solution_row[j]

    # Organize values
    sol_real = np.zeros((n, 1))
    for j in range(n):
        sol_real[pos[j], 0] = sol[j, 0]

    return sol_real


def newton(points):
    n = len(points)

    # Make difference matrix
    dif_mat = np.zeros((n, n))
    for n_dif in range(n):
        for row in range(n_dif, n):
            if n_dif == 0:
                dif_mat[row, n_dif] = points[row][1]
            else:
                den = (dif_mat[row, n_dif - 1] - dif_mat[row - 1, n_dif - 1])
                num = points[row][0] - points[row - n_dif][0]
                dif_mat[row, n_dif] = den/num

    # Extract coefficients of polynomial
    expr = 0
    for i in range(n):
        acum = dif_mat[i, i]
        for j in range(i):
            acum *= (x - points[j][0])

        expr += acum

    cof = Poly(expr, x).all_coeffs()
    return create_polynomial(cof)


def lagrange(points):
    expr = 0
    n = len(points)
    for i in range(n):
        lk = 1
        for j in range(n):
            if i != j:
                lk *= (x - points[j][0])/(points[i][0] - points[j][0])

        expr += lk*points[i][1]

    cof = Poly(expr, x).all_coeffs()

    return create_polynomial(cof)


def graph(points, new=False, lag=False, real_f=None):
    if new:
        poly = newton(points)
    elif lag:
        poly = lagrange(points)
    else:
        poly = vandermonde(points)

    lam_p = lambdify(x, poly, modules=['numpy'])
    dist_x = points[-1][0] - points[0][0]
    x_val = np.linspace(points[0][0] - 0.05*dist_x, points[-1][0] + 0.05*dist_x, 100)
    y_val = lam_p(x_val)
    if len(y_val) != len(x_val):
        y_val = y_val[0]
    plt.plot(x_val, y_val, 'k')
    for point in points:
        plt.plot(point[0], point[1], 'bo')

    if real_f is not None:
        lam_f = lambdify(x, real_f, modules=['numpy'])
        y_val = lam_f(x_val)
        plt.plot(x_val, y_val, 'r')
    plt.show()


def extract_points(func, x_inf, x_fin, n):
    x_val = np.linspace(x_inf, x_fin, n)
    lam_f = lambdify(x, func, modules=['numpy'])
    y_val = lam_f(x_val)

    x_val = x_val.tolist()
    y_val = y_val.tolist()
    xy = list(zip(x_val, y_val))
    return xy


# my_points = [(-2, 12.13533528), (-1, 6.367879441), (2, -4.610943901), (3, 2.085536923)]
f = x*cos(x) + sin(x)
my_points = extract_points(f, -3, 3, 6)

graph(my_points, new=True, real_f=f)
