from matplotlib import pyplot as plt
from numpy import linspace
from sympy import sympify as str2sym
from sympy.abc import x
from sympy.solvers import solve
from sympy import lambdify
from math import sqrt
from math import ceil
import pyperclip


SUP = str.maketrans("4567890", "⁴⁵⁶⁷⁸⁹⁰")
DECIMALS = 5


def fix_point(params, tol, n_max=100):
    g = params[0]
    x0 = params[1]
    l_fix = list()
    xd = g.subs(x, x0).evalf()
    l_fix.append([x0])
    l_fix.append([xd])
    i = 1
    diverge = False
    while abs(xd - x0) >= tol and i <= n_max:
        if abs(x0) >= 10 ** 308:
            diverge = True
            break
        else:
            x0 = xd
            xd = g.subs(x, xd).evalf()
            l_fix.append([xd])
            i += 1

    return l_fix, diverge


def bisection(params, tol, n_max=100):
    f1 = params[0]
    a = params[1]
    b = params[2]
    l_bis = list()
    x1 = (b + a) / 2
    x0 = x1 - tol - 1
    l_bis.append((a, b, x1))
    i = 1
    while abs(x1 - x0) > tol and i < n_max:
        x0 = x1
        if f1.subs(x, x0).evalf() * f1.subs(x, a).evalf() < 0:
            b = x1
        else:
            a = x1
        x1 = (b + a) / 2
        l_bis.append((a, b, x1))
        i += 1

    return l_bis, False


def secant(params, tol, n_max=100):
    f1 = params[0]
    x0 = params[1]
    x1 = params[2]
    fx0 = f1.subs(x, x0).evalf()
    fx1 = f1.subs(x, x1).evalf()
    cont = 1
    den = fx1 - fx0

    if den == 0:
        return [x0, x1], True
    # Calculate first value
    x2 = x1 - fx1 * (x1 - x0) / den
    xs = [[x0], [x1], [x2]]
    while abs(x2 - x1) > tol and cont < n_max:
        # Shift variables
        x0 = x1
        fx0 = fx1
        x1 = x2
        fx1 = f1.subs(x, x1).evalf()
        den = fx1 - fx0
        cont += 1
        if den == 0:
            return xs, True

        # Calculate next iteration
        x2 = x1 - fx1 * (x1 - x0) / den
        xs.append([x2])

    return xs, False


def read_matrix(string, vector=False):
    nums = string.replace("[", "")\
        .replace("]", "").\
        replace(" ", "").\
        split(",")
    if not vector:
        n = int(sqrt(len(nums)))
        list_a = list()
        for i in range(n):
            row = list()
            for j in range(n):
                row.append(float(nums[i*n + j]))
            list_a.append(row)
        return list_a
    else:
        vec_b = list()
        for elem in nums:
            vec_b.append(float(elem))
        return vec_b


def gauss_interaction(params):
    def print_matrix(matrix):
        length1 = len(matrix)
        spaces = 10
        for i1 in range(length1):
            string = ""
            for j1 in range(len(matrix[i1])):
                elem1 = str(round(matrix[i1][j1], DECIMALS))
                if elem1[-2:] == ".0":
                    elem1 = elem1[:-2]
                string += elem1 + " " * (spaces - len(elem1) + DECIMALS)
            print(string)

    def det(matrix):
        def cut_matrix(index):
            aux = []
            for z1 in range(length1):
                aux1 = []
                if z1 != 0:
                    for k in range(length1):
                        if k != index:
                            aux1.append(matrix[z1][k])
                    aux.append(aux1)
            return aux

        length1 = len(matrix)
        if length1 == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        elif length1 == 1:
            return matrix[0][0]

        row = matrix[0]
        determinant = 0
        sign = 1
        for i1 in range(length1):
            if row[i1] != 0:
                determinant += row[i1] * sign * det(cut_matrix(i1))
            if sign > 0:
                sign = -1
            else:
                sign = 1

        return determinant

    def merge(a1, b1):
        for i1 in range(len(b1)):
            a1[i1].append(b1[i1])
        return a1

    def gauss(matrix):
        print("Stage 0")
        print_matrix(matrix)
        print("--------------")
        input("(press enter to start)\n")
        for i1 in range(len(matrix) - 1):
            # Check if row starts with value different than zero
            if matrix[i1][i1] == 0:
                for j1 in range(i1 + 1, len(matrix)):
                    if matrix[j1][i1] != 0:
                        aux = matrix[i1]
                        matrix[i1] = matrix[j1]
                        matrix[j1] = aux
                        break

            # Modify rows
            for j1 in range(i1 + 1, len(matrix)):
                if matrix[j1][i1] != 0:
                    multiplier = matrix[j1][i1] / matrix[i1][i1]
                    matrix[j1][i1] = 0
                    for z1 in range(i1 + 1, len(matrix[j1])):
                        matrix[j1][z1] -= multiplier * matrix[i1][z1]

            print("Stage " + str(i1 + 1))
            print_matrix(matrix)
            print("--------------")
            input("(press enter to continue)\n")

        return matrix

    matrix_a = params[0]
    vector_b = params[1]
    length = len(matrix_a)
    if length != len(vector_b):
        print("A and b do not have the same dimensions.")
        return

    for i in range(len(matrix_a)):
        if length != len(matrix_a[i]):
            print("The A matrix is not square.")
            return

    det1 = det(matrix_a)
    if det1 == 0:
        print("The determinant of A is zero, therefore the system doesn't"
              " have a unique solution.")
        return
    else:
        print("The determinant is " + str(det1) + ".")

    input("(press enter to solve)\n")

    sol = gauss(merge(matrix_a, vector_b))

    # Find solution vector
    vector = [0] * length
    for i in range(length):
        j = length - i - 1
        solution_row = sol[j]
        vector[j] = solution_row[-1]
        for z in range(j + 1, length):
            vector[j] -= solution_row[z] * vector[z]
        vector[j] = vector[j] / solution_row[j]

    i = 1
    print("Solution: ")
    for elem in vector:
        print("x" + str(i) + " = " + str(round(elem, DECIMALS)))
        i += 1


def fake_rule(params, tol, n_max=100):
    f1 = params[0]
    a = params[1]
    b = params[2]
    l_bis = list()
    fb1 = f1.subs(x, b).evalf()
    fa = f1.subs(x, a).evalf()
    x1 = (fb1 * a - fa * b)/(fb1 - fa)
    x0 = x1 - tol - 1
    l_bis.append((a, b, x1))
    i = 1
    while abs(x1 - x0) > tol and i < n_max:
        x0 = x1
        if f1.subs(x, x0).evalf() * f1.subs(x, a).evalf() < 0:
            b = x0
        else:
            a = x0
        fb1 = f1.subs(x, b).evalf()
        fa = f1.subs(x, a).evalf()
        x1 = (fb1 * a - fa * b) / (fb1 - fa)
        l_bis.append((a, b, x1))
        i += 1

    return l_bis, False


def newton(params, tol, n_max=100):
    f1 = params[0]
    x0 = params[1]
    f1d = f1.diff(x)
    xs = [[x0]]

    f1di = f1d.subs(x, x0).evalf()
    if f1di == 0:
        return xs, True

    xs.append([x0 - f1.subs(x, x0).evalf()/f1di])
    i = 1
    while abs(xs[-1][0] - xs[-2][0]) > tol and i < n_max:
        f1di = f1d.subs(x, xs[-1][0]).evalf()
        if f1di == 0:
            return xs, True
        xs.append([xs[-1][0] - f1.subs(x, xs[-1][0])/f1di])
        i += 1
    return xs, False


def newton_modified(params, tol, n_max=100):
    f1 = params[0]
    x0 = params[1]
    return newton((f1/f1.diff(x), x0), tol, n_max=n_max)


def test(params):
    f1 = params[0]
    a = params[1]
    b = params[2]
    fa = f1.subs(x, a).evalf()
    fb1 = f1.subs(x, b).evalf()

    print("\nChecking values of function...")
    print("f(" + str(a) + ") = " + str(fa))
    print("f(" + str(b) + ") = " + str(fb1))

    if not fa.is_real or not fb1.is_real \
            or not a <= fa <= b or not a <= fb1 <= b:
        print("The theorem fails, as the function evaluated in one of the interval"
              " is not in the interval.")
        return

    try:
        print("\n")
        critics = list(solve(f1, x))
        for i in range(len(critics)):
            critics[i] = critics[i].evalf()

        if len(critics) > 0:
            print("The critic points are: " + str(critics))
            for cr in critics:
                if cr and a <= cr <= b:
                    fc = f1.subs(x, cr).evalf()
                    print("f(" + str(cr) + ") = " + str(fc))
                    if not fc.is_real or not a <= fc <= b:
                        print("The theorem fails, as this function has a critic point "
                              "outside the interval.")
                        return
                else:
                    print("Critic point outside the interval.")
        else:
            print("There aren't any critic points.")

        print("It is true that g([a,b]) is in [a, b].")
        ans = input("Want to continue? [y/n]")
        if ans == "n":
            return
    except NotImplementedError:
        ans = input("Couldn't find critic points analytically. Want to see the "
                    "graph of the function? [y/n] ")
        if ans == "y":
            lam_f = lambdify(x, f1, modules=['numpy'])
            x_val = linspace(a, b, ceil((b - a)/0.1))
            y_val = lam_f(x_val)
            plt.plot(x_val, y_val)
            plt.axis([a, b, a, b])
            plt.show()
            ans = input("Want to continue? [y/n]")
            if ans == "n":
                return

    print("\nChecking values of derivative...")
    f1d = f1.diff(x)
    fa = abs(f1d.subs(x, a).evalf())
    fb1 = abs(f1d.subs(x, b).evalf())
    print("|f'(" + str(a) + ")| = " + str(fa))
    print("|f'(" + str(b) + ")| = " + str(fb1))
    nums = [fa, fb1]

    if not fa.is_real or not fb1.is_real \
            or not 0 < fa < 1 or not 0 < fb1 < 1:
        print("The theorem fails, as the derivative evaluated in one of "
              "the interval is not less than 1.")
        return

    try:
        print("\n")
        critics = list(solve(f1d, x))
        for i in range(len(critics)):
            critics[i] = critics[i].evalf()
        if len(critics) > 0:
            print("The critic points are: " + str(critics))
            for cr in critics:
                if cr.is_real and a <= cr <= b:
                    fc = f1.subs(x, cr).evalf()
                    nums.append(fc)
                    print("|f'(" + str(cr) + ")| = " + str(fc))
                    if not fc.is_real or not 0 < fc < 1:
                        print("The theorem fails, as this function has a critic point "
                              "outside the interval.")
                        return
                else:
                    print("The critic point is outside the interval.")
        else:
            print("There aren't any critic points.")

        print("It is true that g'((a,b)) is in (0, 1).")
        print("With k = " + str(max(nums)))
    except NotImplementedError:
        ans = input("Couldn't find critic points analytically. Want to see the "
                    "graph of the derivative of the function? [y/n] ")
        if ans == "y":
            lam_f = lambdify(x, f1d, modules=['numpy'])
            x_val = linspace(a, b, ceil((b - a) / 0.1))
            y_val = lam_f(x_val)
            plt.plot(x_val, y_val)
            plt.axis([a, b, 0, 1])
            ans = input("Want to continue? [y/n]")
            if ans == "n":
                return


def test_multiplicity(params):
    f1 = params[0]
    x0 = params[1]
    m = 0
    f0 = f1.subs(x, x0).evalf()
    while f0 == 0:
        if m < 4:
            derivative_num = "'"*m
        else:
            derivative_num = str(m).translate(SUP)
        print("f" + derivative_num + "(" + str(x0) + ") = " + str(f0))
        m += 1
        f1 = f1.diff(x)
        f0 = f1.subs(x, x0).evalf()

    if m < 4:
        derivative_num = "'" * m
    else:
        derivative_num = str(m).translate(SUP)
    print("f" + derivative_num + "(" + str(x0) + ") = " + str(f0))
    print("It's multiplicity is " + str(m))


def identity(f, x0):
    return f.subs(x, x0).evalf()


def f_point(f, x0):
    return f.subs(x, x0).evalf() - x0


# Name, Parameters, Names_table, start, Failed message, If it prints, method
fp = ("Fix point", ["X0"], ["x"], 0, "The iterations are not decreasing.", f_point,
      True, fix_point)
ft = ("Test theorem fix point", [], [], True, test)
fm = ("Test multiplicity", [], [], True, test_multiplicity)
fb = ("Bisection", ["a", "b"], ("a", "b", "xm"), 0, "", identity, True, bisection)
fs = ("Secant", ["x0", "x1"], ["x"], 1, "There's a division by 0.", identity, True, secant)
fg = ("Gauss", ["A", "b"], (False, True), False, gauss_interaction)
fn = ("Newton", ["X0"], ["x"], 0, "The derivative became 0.", identity, True, newton)
fnm = ("Newton modified", ["X0"], ["x"], 0, "There's a division by 0.", identity,
       True, newton_modified)
ffp = ("False position", ["a", "b"], ("a", "b", "xm"), 0, "", identity, True, fake_rule)

methods = {1: fp, 2: fb, 3: fs, 4: fg, 5: fn, 6: fnm, 7: ffp, 8: ft, 9: fm}


def ui():
    def round_str(er1, decimals1):
        er_str = list(str(er1).split("e"))

        er_str[0] = str(round(float(er_str[0]), decimals1))
        if len(er_str) > 1:
            return er_str[0] + "e" + er_str[1]
        else:
            return er_str[0]

    global DECIMALS
    while True:
        lm = len(methods)
        print("\n-----------------------------")
        print("0. Quit")
        for i in range(1, lm + 1):
            print(str(i) + ". " + methods[i][0])
        print(str(lm + 1) + ". Change preset decimals")

        ans = int(input("What method do you want to use? "))
        if not 0 <= ans <= lm+1:
            print("Invalid option.")
            continue
        elif ans == 0:
            return
        elif ans == lm + 1:
            DECIMALS = int(input("How many decimals you want? "))
            continue

        tuple_method = methods[ans]
        name_func = tuple_method[0]
        func = tuple_method[-1]
        integers = tuple_method[-2]
        names_params = tuple_method[1]
        if ans != lm:
            print("--------\n\nMethod " + name_func)
        else:
            print("\n\n")
        print("------Parameters------ ")
        params = []
        if integers:
            f_string = input("Function to use: ")
            pyperclip.copy(f_string)
            print("The function will be in your clipboard for further use!")
            params.append(str2sym(f_string))

            if ans == lm - 1:
                params.append(float(input("a: ")))
                params.append(float(input("b: ")))
                func(params)
                input("(press enter to continue)")
                continue
            elif ans == lm:
                params.append(float(input("x0: ")))
                func(params)
                input("(press enter to continue)")

        i = 0
        for name in names_params:
            if integers:
                params.append(float(input(name + ": ")))
            else:
                vector = bool(tuple_method[2][i])
                params.append(read_matrix(input(name + ": "), vector=vector))
                i += 1

        if integers:
            tolerance = float(input("Tolerance: "))
            n_max = int(input("Maximum number of iterations: "))
            list_solution, diverge = func(params, tolerance, n_max=n_max)
            titles = tuple_method[2]
            print("\nMethod:\n--------------")
            spaces = 10
            string = "i" + " "*(spaces + DECIMALS - 1)
            for title in titles:
                string += title + " "*(spaces - len(title) + DECIMALS)
            print(string + "F(x)" + " "*(spaces - 4 + DECIMALS) + "Error")

            i = 0
            ant = 0
            start = tuple_method[3]
            for sol in list_solution:
                if i > start:
                    er = round_str(str(abs(sol[-1] - ant)), DECIMALS)
                else:
                    er = ""

                string = str(i) + " "*(spaces - len(str(i)) + DECIMALS)
                for elem in sol:
                    elem1 = round_str(str(elem), DECIMALS)
                    string += elem1 + " "*(spaces - len(elem1) + DECIMALS)
                    ant = elem
                fx = round_str(tuple_method[5](params[0], sol[-1]), DECIMALS)
                string += fx + " "*(spaces - len(fx) + DECIMALS)
                string += er
                print(string)
                i += 1

            if diverge:
                print("\nThe method failed because: " + tuple_method[4])

            print("\nFunction passed " + str(params[0]))
            input("(press enter to continue)")
        else:
            func(params)
            input("(press enter to continue)")


ui()
