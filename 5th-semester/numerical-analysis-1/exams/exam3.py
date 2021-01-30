import numpy as np
from sympy.abc import x
from sympy import Poly
from sympy import lambdify
from sympy import sympify
import pyperclip as pc
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt

# Variables that manage UI
e = "Error"
s = "Success"
ini = "Initial prints"
header = "Header table"
sep = "-------------------------------------------"
stages_print = True
number_decimals = 5
ns = 5
HEAD = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
WARN = '\033[93m'
FAIL = '\033[91m'
END = '\033[0m'
BOLD = '\033[1m'
UNDER = '\033[4m'


# ###### Base algorithm to read matrix and vector ######
def read_matrix(ask):
    string = input(ask)
    pc.copy(string)
    print(GREEN + "It will be saved in the clipboard!" + END)
    nums = string.replace("[", "")\
                 .replace("]", "")\
                 .replace(" ", "")\
                 .split(",")
    n = int(np.sqrt(len(nums)))
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            mat[i, j] = float(nums[i*n + j])
    return mat


def read_number(ask):
    return float(input(ask))

def read_vector(ask, cp=False):
    string = input(ask)
    if cp:
        pc.copy(string)
        print(GREEN + "It will be saved in the clipboard!" + END)
    if string == "n":
        return None
    nums = string.replace("[", "") \
                 .replace("]", "") \
                 .replace(" ", "") \
                 .split(",")
    n = int(len(nums))
    mat = np.zeros((1, n))
    for i in range(n):
        mat[0, i] = float(nums[i])
    return mat

def read_sym(ask):
    string = input(ask)
    pc.copy(string)
    print(GREEN + "It will be saved in the clipboard!" + END)
    return sympify(string)

# ###### Section for factorization of a matrix ######
def lu_gauss(matrix):
    n = matrix.shape[0]
    l1 = np.identity(n)
    stages = {0: {"": matrix.copy()}}
    for i in range(n - 1):
        # Check if row starts with different value
        if matrix[i, i] == 0:
            print("There is not a factorization LU, as position " + str((i, i)) + " has a zero.")
            return e, {}, True, [], [], []

        # Modify rows
        for j in range(i + 1, n):
            if matrix[j, i] != 0:
                mult = matrix[j, i] / matrix[i, i]
                l1[j, i] = mult
                matrix[j, i] = 0
                for z in range(i + 1, n):
                    matrix[j, z] -= mult * matrix[i, z]

        stages[i + 1] = {"": matrix.copy(), "L": l1.copy(), "U": matrix.copy()}

    return s, stages, True, l1, matrix, np.identity(n)


def lu_partial(matrix):
    n = matrix.shape[0]
    l1 = np.zeros((n, n))
    p1 = np.identity(n)
    stages = {0: {"": matrix.copy()}}
    for i in range(n - 1):
        # Modify rows
        for j in range(i + 1, n):
            if abs(matrix[i, i]) < abs(matrix[j, i]):
                aux = matrix[i, :].copy()
                matrix[i, :] = matrix[j, :]
                matrix[j, :] = aux

                aux = p1[i, :].copy()
                p1[i, :] = p1[j, :]
                p1[j, :] = aux

                aux = l1[i, :].copy()
                l1[i, :] = l1[j, :]
                l1[j, :] = aux

                # Check if row starts with different value
        if matrix[i, i] == 0:
            print("There is not a factorization LU, as there is not any value different than zero.")
            return e, {}, True, [], [], []

        for j in range(i + 1, n):
            if matrix[j, i] != 0:
                mult = matrix[j, i] / matrix[i, i]
                l1[j, i] = mult
                matrix[j, i] = 0
                for z in range(i + 1, n):
                    matrix[j, z] -= mult * matrix[i, z]
        l2 = l1.copy()
        for z in range(n):
            l2[z, z] = 1

        stages[i + 1] = {"": matrix.copy(), "L": l2.copy(), "U": matrix.copy(), "P": p1.copy()}
    for i in range(n):
        l1[i, i] = 1
    return s, stages, True, l1, matrix, p1


def crout(matrix):
    n = matrix.shape[0]
    u1 = np.identity(n)
    l1 = np.zeros((n, n))

    stages = {0: {"": matrix.copy()}}
    for k in range(n):
        for i in range(k, n):
            l1[i, k] = matrix[i, k] - l1[i, :k].dot(u1[:k, k])

        if l1[k, k] == 0:
            print("There is a zero in the diagonal of L, therefore the factorization failed.")
            return e, {}, True, [], [], []

        for j in range(k + 1, n):
            u1[k, j] = (matrix[k, j] - l1[k, :k].dot(u1[:k, j])) / l1[k][k]

        stages[k + 1] = {"L": l1.copy(), "U": u1.copy()}
    return s, stages, True, l1, u1, np.identity(n)


def doolittle(matrix):
    n = matrix.shape[0]
    l1 = np.identity(n)
    u1 = np.zeros((n, n))
    stages = {0: {"": matrix.copy()}}
    for k in range(n):
        for i in range(k, n):
            u1[k, i] = matrix[k, i] - l1[k, :k].dot(u1[:k, i])

        if u1[k, k] == 0:
            print("There is a zero in the diagonal of U, therefore the factorization failed.")
            return e, {}

        for j in range(k + 1, n):
            l1[j, k] = (matrix[j, k] - l1[j, :k].dot(u1[:k, k])) / u1[k, k]

        stages[k + 1] = {"L": l1.copy(), "U": u1.copy()}

    return s, stages, True, l1, u1, np.identity(n)


def cholesky(matrix):
    n = matrix.shape[0]
    l1 = np.identity(n, dtype=complex)
    u1 = np.identity(n, dtype=complex)
    stages = {0: {"": matrix.copy()}}
    for k in range(n):
        l1[k, k] = np.sqrt(matrix[k, k] - l1[k, :k].dot(u1[:k, k]))
        u1[k, k] = l1[k, k]
        if l1[k, k] == 0:
            print("Failed, there is a zero in the diagonal of L.")
            return e, {}, True, [], [], []
        for i in range(k + 1, n):
            l1[i, k] = (matrix[i, k] - l1[i, :k].dot(u1[:k, k])) / l1[k, k]

        for i in range(k + 1, n):
            u1[k, i] = (matrix[k, i] - l1[k, :k].dot(u1[:k, i])) / l1[k, k]

        stages[k + 1] = {"L": l1.copy(), "U": u1.copy()}

    return s, stages, True, l1, u1, np.identity(n)


# ###### Section for solving linear equations ######
def jacobi(d, l, u, b, x0, tol, n_max, p):
    t = np.linalg.inv(d).dot(l + u)
    c = np.linalg.inv(d).dot(b)

    te = np.linalg.eigvals(t)
    pt = max(abs(te))
    print("Spectral radius of " + str(pt))
    if pt >= 1:
        string = input("Wish to continue? [y/n]")
        if string == "n":
            return e, {}
    print("\n")
    xd = x0
    stages = {0: (None, x0), ini: {"T": t, "C": c}}
    for i in range(n_max):
        xd = t.dot(xd) + c
        stages[i + 1] = (np.linalg.norm(xd - x0, ord=p), xd)
        if np.linalg.norm(xd - x0, ord=p) < tol:
            break
        x0 = xd

    return s, stages, False


def gauss_seidel(d, l, u, b, x0, tol, n_max, p):
    t = np.linalg.inv(d - l).dot(u)
    c = np.linalg.inv(d - l).dot(b)

    te = np.linalg.eigvals(t)
    pt = max(abs(te))
    print("Spectral radius of " + str(pt))
    if pt >= 1:
        string = input("Wish to continue? [y/n]")
        if string == "n":
            return e, {}

    xd = x0
    stages = {0: (None, x0), ini: {"T": t, "C": c}}
    for i in range(n_max):
        xd = t.dot(xd) + c
        stages[i + 1] = (np.linalg.norm(xd - x0, ord=p), xd)
        if np.linalg.norm(xd - x0, ord=p) < tol:
            break
        x0 = xd

    return s, stages, False


def sor(d, l, u, b, x0, tol, n_max, p):
    w = float(input("W: "))
    t = np.linalg.inv(d - w*l).dot((1 - w)*d + w*u)
    c = w*np.linalg.inv(d - w*l).dot(b)

    te = np.linalg.eigvals(t)
    pt = max(abs(te))
    print("Spectral radius of " + str(pt))
    if pt >= 1:
        string = input("Wish to continue? [y/n]")
        if string == "n":
            return e, {}

    xd = x0
    stages = {0: (None, x0), ini: {"T": t, "C": c}}
    for i in range(n_max):
        xd = t.dot(xd) + c
        stages[i + 1] = (np.linalg.norm(xd - x0, ord=p), xd)
        if np.linalg.norm(xd - x0, ord=p) < tol:
            break
        x0 = xd

    return s, stages, False


# ###### Section for interpolation ######
#  Create symbolic polynomial
def create_polynomial(coefficients):
    poly = 0
    poly_s = ""
    order = len(coefficients) - 1
    for i in range(order + 1):
        poly += coefficients[i]*x**(order - i)
        if coefficients[i] != 0:
            if order - i > 1:
                poly_s += format(coefficients[i], "10." + str(number_decimals) + "E") + "x^" + str(order - i)
            elif order - i == 1:
                poly_s += format(coefficients[i], "10." + str(number_decimals) + "E") + "x"
            else:
                poly_s += format(coefficients[i], "10." + str(number_decimals) + "E")
        if i != order:
            poly_s += " + "
    return poly, poly_s


def vandermonde(points):
    def gauss_pivot(a, b):
        def index(val, n2):
            if val < n2:
                return 0, val

            row1, col1 = index(val - n2, n2)

            return row1 + 1, col1

        pos = {}
        n1 = len(a)
        for i1 in range(n1):
            pos[i1] = i1

        ab = np.concatenate((a.astype(float), b.astype(float)), axis=1)
        for stage in range(n1 - 1):
            # Change column and rows
            mat_temp = ab[:n1, :n1].copy()
            for j1 in range(stage):
                mat_temp[j1, :] = np.zeros((1, n1))
                mat_temp[:, j1] = np.zeros((1, n1))

            i_max = np.argmax(abs(mat_temp))
            i1, j1, = index(i_max, n1)

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
            for row in range(stage + 1, n1):
                if ab[row, stage] != 0:
                    mult = ab[row, stage] / ab[stage, stage]
                    ab[row, stage] = 0
                    for col in range(stage + 1, n1 + 1):
                        ab[row, col] = ab[row, col] - ab[stage, col] * mult

        # Find value of vars
        sol = np.zeros((n1, 1))
        for i1 in range(n1):
            j1 = n1 - i1 - 1
            solution_row = ab[j1, :]
            sol[j1, 0] = solution_row[-1]
            for z in range(n1 - 1, j1, -1):
                sol[j1, 0] -= solution_row[z] * sol[z]
            sol[j1, 0] /= solution_row[j1]

        # Organize values
        sol_real = np.zeros((n1, 1))
        for j1 in range(n1):
            sol_real[pos[j1], 0] = sol[j1, 0]

        return sol_real
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

    cof = list(gauss_pivot(vand_matrix, vand_b).transpose().tolist())[0]
    p, ps = create_polynomial(cof)
    return s, {0: {"Vandermonde's matrix": vand_matrix, "Polynomial": ps}}, True, p


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
    s_expr = ""
    for i in range(n):
        acum = 1
        for j in range(i):
            acum *= (x - points[j][0])

        expr += acum*dif_mat[i, i]
        if i == 0:
            s_expr += format(dif_mat[i, i], "10." + str(number_decimals) + "E")
        else:
            s_expr += format(dif_mat[i, i], "10." + str(number_decimals) + "E") + "(" + str(acum) + ")"
        if i != n - 1:
            s_expr += " + "

    cof = Poly(expr, x).all_coeffs()
    p, ps = create_polynomial(cof)
    return s, {0: {"Divided differences": dif_mat, "Polynomial": s_expr,
                   "Simplified polynomial": ps}}, True, p


def lagrange(points):
    expr = 0
    n = len(points)
    lks = np.zeros((n, n))
    for i in range(n):
        lk = 1
        for j in range(n):
            if i != j:
                lk *= (x - points[j][0])/(points[i][0] - points[j][0])

        expr += lk*points[i][1]
        lks[i, :] = Poly(lk, x).all_coeffs()

    cof = Poly(expr, x).all_coeffs()
    p, ps = create_polynomial(cof)
    return s, {0: {"Polynomials of Lagrange": lks, "Polynomial": ps}}, True, p


# ###### Section for splines ######
def lineal_spline(points):
    n = len(points)
    a = np.zeros((2*(n - 1), 2*(n - 1)))
    b = np.zeros((2*(n - 1), 1))
    # Condition of interpolation
    a[0, 0] = points[0][0]
    a[0, 1] = 1
    b[0, 0] = points[0][1]
    for i in range(1, n):
        a[i, 2*(i - 1)] = points[i][0]
        a[i, 2*i - 1] = 1

        b[i, 0] = points[i][1]

    # Condition of continuity
    for j in range(1, n - 1):
        a[j + n - 1, 2*(j - 1)] = points[j][0]
        a[j + n - 1, 2*j - 1] = 1
        a[j + n - 1, 2*j] = -points[j][0]
        a[j + n - 1, 2*j + 1] = -1

        b[j + n - 1, 0] = 0

    ab = np.linalg.solve(a, b)

    def lineal(val):
        for i1 in range(n - 1):
            if points[i1][0] <= val <= points[i1+1][0]:
                return ab[2*i1]*val + ab[2*i1 + 1]

    ab_aux = np.zeros((n - 1, 2))
    for i in range(n - 1):
        ab_aux[i, 0] = ab[2*i]
        ab_aux[i, 1] = ab[2*i + 1]

    return s, {0: {"Coefficients": ab_aux}}, True, lineal


def quad_spline(points):
    front = float(input("f''(X0): "))
    n = len(points)
    a = np.zeros((3*(n - 1), 3*(n - 1)))
    b = np.zeros((3*(n - 1), 1))

    # Condition of interpolation
    a[0, 0] = points[0][0]**2
    a[0, 1] = points[0][0]
    a[0, 2] = 1
    b[0, 0] = points[0][1]
    for i in range(1, n):
        a[i, 3*(i - 1)] = points[i][0]**2
        a[i, 3*i - 2] = points[i][0]
        a[i, 3*i - 1] = 1

        b[i, 0] = points[i][1]

    # Condition of continuity
    for j in range(1, n - 1):
        a[j + n - 1, 3*(j - 1)] = points[j][0]**2
        a[j + n - 1, 3*j - 2] = points[j][0]
        a[j + n - 1, 3*j - 1] = 1
        a[j + n - 1, 3*j] = -points[j][0]**2
        a[j + n - 1, 3*j + 1] = -points[j][0]
        a[j + n - 1, 3*j + 2] = -1

        b[j + n - 1, 0] = 0

    # Softness condition
    for j in range(1, n - 1):
        a[j + 2*n - 3, 3*(j - 1)] = 2*points[j][0]
        a[j + 2*n - 3, 3*j - 2] = 1
        a[j + 2*n - 3, 3*j] = -2*points[j][0]
        a[j + 2*n - 3, 3*j + 1] = -1
        b[j + 2*n - 3, 0] = 0

    b[-1, 0] = front
    a[-1, 0] = 2

    ab = np.linalg.solve(a, b)

    def quad(val):
        for i1 in range(n - 1):
            if points[i1][0] <= val <= points[i1+1][0]:
                return ab[3*i1]*val**2 + ab[3*i1 + 1]*val + ab[3*i1 + 2]

    ab_aux = np.zeros((n - 1, 3))
    for i in range(n - 1):
        ab_aux[i, 0] = ab[3*i]
        ab_aux[i, 1] = ab[3*i + 1]
        ab_aux[i, 2] = ab[3*i + 2]

    return s, {0: {"Coefficients": ab_aux}}, True, quad


def cubic_spline(points):
    front = float(input("f''(X0): "))
    front_f = float(input("f''(Xn): "))
    n = len(points)
    a = np.zeros((4*(n - 1), 4*(n - 1)))
    b = np.zeros((4*(n - 1), 1))

    # Condition of interpolation
    a[0, 0] = points[0][0]**3
    a[0, 1] = points[0][0]**2
    a[0, 2] = points[0][0]
    a[0, 3] = 1
    b[0, 0] = points[0][1]
    for i in range(1, n):
        a[i, 4*(i - 1)] = points[i][0]**3
        a[i, 4*i - 3] = points[i][0]**2
        a[i, 4*i - 2] = points[i][0]
        a[i, 4*i - 1] = 1

        b[i, 0] = points[i][1]

    # Condition of continuity
    for j in range(1, n - 1):
        a[j + n - 1, 4*(j - 1)] = points[j][0]**3
        a[j + n - 1, 4*j - 3] = points[j][0]**2
        a[j + n - 1, 4*j - 2] = points[j][0]
        a[j + n - 1, 4*j - 1] = 1
        a[j + n - 1, 4*j] = -points[j][0]**3
        a[j + n - 1, 4*j + 1] = -points[j][0]**2
        a[j + n - 1, 4*j + 2] = -points[j][0]
        a[j + n - 1, 4*j + 3] = -1

        b[j + n - 1, 0] = 0

    # Softness condition
    for j in range(1, n - 1):
        a[j + 2*n - 3, 4*(j - 1)] = 3*points[j][0]**2
        a[j + 2*n - 3, 4*j - 3] = 2*points[j][0]
        a[j + 2*n - 3, 4*j - 2] = 1

        a[j + 2*n - 3, 4*j] = -3*points[j][0]**2
        a[j + 2*n - 3, 4*j + 1] = -2*points[j][0]
        a[j + 2*n - 3, 4*j + 2] = -1

        b[j + 2*n - 3, 0] = 0

    # Second derivative softness conditions
    for j in range(1, n - 1):
        a[j + 3*n - 5, 4*(j - 1)] = 6*points[j][0]
        a[j + 3*n - 5, 4*j - 3] = 2

        a[j + 3*n - 5, 4*j] = -6*points[j][0]
        a[j + 3*n - 5, 4*j + 1] = -2

        b[j + 3*n - 5, 0] = 0

    b[-2, 0] = front
    a[-2, 0] = 6*points[0][0]
    a[-2, 1] = 2

    b[-1, 0] = front_f
    a[-1, -4] = 6*points[-1][0]
    a[-1, -3] = 2

    ab = np.linalg.solve(a, b)

    def cubic(val):
        for i1 in range(n - 1):
            if points[i1][0] <= val <= points[i1+1][0]:
                return ab[4*i1]*val**3 + ab[4*i1 + 1]*val**2 + ab[4*i1 + 2]*val + ab[4*i1 + 3]

    ab_aux = np.zeros((n - 1, 4))
    for i in range(n - 1):
        ab_aux[i, 0] = ab[4*i]
        ab_aux[i, 1] = ab[4*i + 1]
        ab_aux[i, 2] = ab[4*i + 2]
        ab_aux[i, 3] = ab[4*i + 3]

    return s, {0: {"Coefficients": ab_aux}}, True, cubic


def trapeze(f, a, b, n):
    h = (b - a)/n
    integral = f.subs(x, a) + f.subs(x, b)
    i = 1
    while i < n:
        x1 = a + i*h
        integral += 2*f.subs(x, x1)
        i += 1

    integral *= h/2
    integral = integral.evalf()
    return s, {0: {"Integral value": float(integral)}}, True


def simpson13(f, a, b, n):
    h = (b - a)/n
    integral = f.subs(x, a) + f.subs(x, b)
    i = 1
    while i < n:
        x1 = a + i*h
        if i%2 == 0:
            integral += 2*f.subs(x, x1)
        else:
            integral += 4*f.subs(x, x1)
        i += 1
    integral *= h/3
    integral = integral.evalf()
    return s, {0: {"Integral value": float(integral)}}, True


def find_better_w(args):
    a = args[0]
    many = args[1]
    d = np.diag(np.diag(a))

    n = a.shape[0]
    l1 = np.zeros((n, n))
    u1 = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i < j:
                u1[i, j] = -a[i, j]
            if i > j:
                l1[i, j] = -a[i, j]
    first = True
    radiusmin = 0
    wmin = 0
    stages = {}
    w = 0
    h = 2/many
    while w <= 2:
        t = np.linalg.inv(d - w*l1).dot((1 - w)*d + w*u1)
        radius = max(abs(np.linalg.eigvals(t)))
        plt.plot(w, radius, 'ro')
        if first:
            radiusmin = radius
            wmin = w
            first = False
        if radius < radiusmin:
            radiusmin = radius
            wmin = w
        w += h

    print(BLUE + "Optimal w found " + str(wmin) + END)
    plt.show(block=False)
    return {}, False


def find_optimal_value(args):
    f = args[0]
    a = args[1]
    b = args[2]
    tol = args[3]
    method = args[4]
    if method == 1:
        f_used = f.diff().diff()
        print("f''(x) = " + str(f_used))
    else:
        f_used = f.diff().diff().diff().diff()
        print("f4(x) = " + str(f_used))

    fl = lambdify(x, f_used, modules=['numpy'])
    xs = np.linspace(a, b, 100)
    ys = fl(xs)
    
    im = np.argmax(abs(ys))
    ym = ys[im]
    xm = a + (b - a)/100*im
    plt.plot(xm, ym, 'ro')
    plt.plot(xs, ys, 'k')
    plt.show(block=False)

    if method == 1:
        bound = np.sqrt((b - a)**3*abs(ym)/(12*tol))
    else:
        bound = ((b - a)**5*abs(ym)/(180*tol))**(0.25)

    print(format(bound, "10." + str(number_decimals) + "E") + "<= n")
    return {}, True

# ###### Handlers of every section ######
lum = {1: ("LU with simple gauss.",  lu_gauss),
       2: ("LU with partial gauss.", lu_partial),
       3: ("LU with Crout.", crout),
       4: ("LU with doolittle.", doolittle),
       5: ("LU with cholesky", cholesky)}


def lu(num):
    m1 = lum[num][1]
    a = read_matrix("Matrix to decompose: ")
    b = read_vector("Right side vector (if not needed, write n): ")
    if b is not None:
        b = b.transpose()
    ex, stages, type1, l1, u1, p1 = m1(a)
    if ex == s:
        if b is not None:
            b = p1.dot(b)
            n = a.shape[0]

            z = np.zeros((n, 1), dtype=l1.dtype)
            for i in range(n):
                z[i, 0] = b[i]
                for j in range(i):
                    z[i, 0] -= l1[i, j]*z[j, 0]
                z[i, 0] /= l1[i, i]

            x1 = np.zeros((n, 1), dtype=l1.dtype)
            for i in range(n - 1, -1, -1):
                x1[i, 0] = z[i]
                for j in range(n - 1, i, -1):
                    x1[i, 0] -= u1[i, j]*x1[j, 0]
                x1[i, 0] /= u1[i, i]

            stages[max(stages)]["Solution"] = x1

        return stages, type1
    else:
        return e


eqs = {1: ("Find solution with Jacobi.", jacobi),
       2: ("Find solution with Gauss-seidel.", gauss_seidel),
       3: ("Find solution with SOR.", sor)}


def solve(num):
    x0 = read_vector("X0: ").transpose()
    b = read_vector("b: ").transpose()
    a = read_matrix("A: ")
    d = np.diag(np.diag(a))

    n = a.shape[0]
    l1 = np.zeros((n, n))
    u1 = np.zeros((n, n))

    tol = float(input("Tolerance: "))
    n_max = int(input("Maximum iterations: "))
    p = int(input("Norm: "))
    for i in range(n):
        for j in range(n):
            if i < j:
                u1[i, j] = -a[i, j]
            if i > j:
                l1[i, j] = -a[i, j]
    ex, stages, type1 = eqs[num][1](d, l1, u1, b, x0, tol, n_max, p)
    if ex == s:
        stages[header] = ["E", "X"]
        return stages, type1
    else:
        return ex


inter = {1: ("Vandermonde interpolation.", vandermonde),
         2: ("Newton interpolation.", newton),
         3: ("Lagrange interpolation.", lagrange)}

def plot_piece(func, xf):
    xs = np.linspace(xf[0][0], xf[-1][0], 100)
    if not callable(func):
        func = lambdify(x, func, modules=['numpy'])
        ys = func(xs)
    else:
        xs = list(xs)
        ys = []
        for i in range(len(xs)):
            ys.append(func(xs[i]))
        

    plt.plot(xs, ys, 'k')

    for x1 in xf:
        plt.plot(x1[0], x1[1], 'bo')

    plt.show(block=False)


def interpolation(num):
    xs = list(read_vector("X: "))[0]
    fxs = list(read_vector("F(X): ", cp=True))[0]

    ex, stages, type1, func = inter[num][1](list(zip(xs, fxs)))
    ans = input("Want to plot the function? [y/n]")
    if ans == "y":
        plot_piece(func, list(zip(xs, fxs)))
    if ex == s:
        return stages, type1
    return ex


spl = {1: ("Lineal spline.", lineal_spline),
       2: ("Quadratic spline.", quad_spline),
       3: ("Cubic spline.", cubic_spline)}


def splines(num):
    xs = list(read_vector("X: "))[0]
    fxs = list(read_vector("F(X): ", cp=True))[0]

    ex, stages, type1, func = spl[num][1](list(zip(xs, fxs)))
    ans = input("Want to plot the function? [y/n]")
    if ans == "y":
        plot_piece(func, list(zip(xs, fxs)))
    if ex == s:
        return stages, type1
    return ex


integ = {1: ("Trapeze rule.", trapeze),
         2: ("Simpson 1/3", simpson13)}


def integral(num):
    f = read_sym("Function to integrate: ")
    a = read_number("a: ")
    b = read_number("b: ")
    n = int(read_number("n: "))
    _, stages, typ = integ[num][1](f, a, b, n)
    return stages, typ


def modify_decimal():
    global number_decimals
    number_decimals = int(input("Number of decimals wanted: "))
    return e, True


def modify_spaces():
    global ns
    ns = int(input("Number of spaces between elements: "))
    return e, True


settings = {1: ("Change decimal numbers", modify_decimal),
            2: ("Change number of spaces", modify_spaces)}


def setting_handler(num):
    er, typ = settings[num][1]()
    return er, typ


add = {1: ("Find optimal w for SOR", find_better_w, {"Matrix: ":read_matrix, "How many Ws in that interval: ": read_number}),
       2: ("Find optimal n for integral", find_optimal_value, {"f: ": read_sym, "a: ": read_number, "b: ": read_number, "tol: ": read_number, "Method (1 for Trapeze and 2 for Simpson): ": read_number})}

def additional(num):
    option = add[num]
    args = []
    for key in option[2]:
        args.append(option[2][key](key))
    stages, typ = option[1](args)
    return stages, typ

# UI interaction
def print_stages(stage, type1):
    def print_element(elem, i):
        if type(elem) is np.ndarray:
            comp = np.iscomplexobj(elem)
            for row in elem:
                i = 0
                string1 = ""
                for elem1 in row:
                    if comp:
                        ns1 = ns
                        if i < len(row) - 1 and np.real(row[i + 1]) < 0 and np.imag(row[i + 1]) != 0:
                            ns1 -= 1
                        if i == 0 and np.real(row[i]) < 0:
                            ns1 -= 1
                        re = np.real(elem1)
                        ie = np.imag(elem1)
                        if re != 0 and ie != 0:
                            string1 += format(re, "10." + str(number_decimals) + "E") + " + "
                            string1 += "j" + format(ie, "10." + str(number_decimals) + "E") + BOLD + END + " "*ns1
                        if ie == 0:
                            if re < 0:
                                ns1 -= 1
                            ns1 += 9 + number_decimals
                            string1 += format(re, "10." + str(number_decimals) + "E") + " "*ns1
                        else:
                            ns1 += 8 + number_decimals
                            string1 += "j" +  format(ie, "10." + str(number_decimals) + "E") + BOLD + END + " "*ns1

                    else:
                        ns1 = ns
                        if i < len(row) - 1 and row[i + 1] < 0:
                            ns1 -= 1

                        if i == 0 and row[i] < 0:
                            ns1 -= 1
                        string1 += format(elem1, "10." + str(number_decimals) + "E") + " "*ns1
                        i += 1
                print(string1)
        elif type(elem) is str:
            print(elem)
        elif type(elem) is float or type(elem) is int:
            print(format(elem, "10." + str(number_decimals) + "E"))
        else:
            is1 = str(i)
            string1 = is1 + " " * (6 + number_decimals + ns - len(is1))
            for elem1 in elem:
                if elem1 is not None:
                    if type(elem1) is np.ndarray:
                        z = 0
                        for elem2 in elem1:
                            ns1 = ns
                            if z < len(elem1) - 1 and elem1[z + 1] < 0:
                                ns1 -= 1
                            string1 += format(elem2[0], "10." + str(number_decimals) + "E") + " " * ns1
                            z += 1
                    else:
                        string1 += format(elem1, "10." + str(number_decimals) + "E") + " " * ns
                else:
                    string1 += " "*(ns + 6 + number_decimals)
            print(string1)

    def print_header(head2):
        string1 = "i" + " "*(5 + ns + number_decimals)
        for elem in head2:
            se = str(elem)
            string1 += se + " "*(6 + ns + number_decimals - len(se))
        print(BOLD + string1 + END)

    print(sep)
    if type1 == stages_print:
        stage0 = stage[0]
        for key in stage0:
            if key != "":
                print(BOLD + str(key) + END)
            print_element(stage0[key], key)
            print("\n")

        for key in sorted(stage):
            if key == 0:
                continue
            print(BOLD + "Stage " + str(key) + END)
            for key1 in stage[key]:
                if key1 != "":
                    print(BOLD + str(key1) + END)
                print_element(stage[key][key1], key)
                print("\n")
    else:
        stage0 = stage[ini]
        stage.pop(ini)
        for key in stage0:
            if key != "":
                print(str(key))
            print_element(stage0[key], key)
            print("\n")

        print_header(stage[header])
        stage.pop(header)
        for key in sorted(stage):
            print_element(stage[key], key)
    input("(press any key to continue)")


options = {1: ("LU Factorization", lu, lum),
           2: ("Solve linear equations", solve, eqs),
           3: ("Interpolation", interpolation, inter),
           4: ("Splines", splines, spl),
           5: ("Integration", integral, integ),
           6: ("Additional", additional, add),
           7: ("Settings", setting_handler, settings)}


escape = {1: ("Quit", -1),
          2: ("Back", -2)}


def print_options(opt, final_msg):
    final = max(opt)
    for i in range(1, final + 1):
        print(BOLD + str(i) + END + ". " + opt[i][0])
    print(BOLD + str(final + 1) + END + ". " + escape[final_msg][0])
    while True:
        selection = input(BLUE + "Write selection: " + END)
        try:
            selection = int(selection)
            if selection in range(1, final + 1):
                return selection
            elif selection == final + 1:
                return escape[final_msg][1]
            print(FAIL + "Wrong input." + END + "\n")
        except ValueError:
            print(FAIL + "Integer needed" + END + "\n")


def ui():
    while True:
        print(sep)
        select = print_options(options, 1)
        if select == escape[1][1]:
            break

        new_options = options[select]
        method = new_options[1]
        new_dic = new_options[2]

        print("\n")
        select2 = print_options(new_dic, 2)
        if select2 == escape[2][1]:
            print("\n\n")
            continue

        stages, typ = method(select2)
        if stages != e and len(stages) != 0:
            print_stages(stages, typ)

        print("\n\n")


ui()
