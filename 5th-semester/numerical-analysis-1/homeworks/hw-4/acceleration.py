import math as m


def bisection(function_intervals, tol, n_max=100):
    f1 = function_intervals[0]
    a = function_intervals[1]
    b = function_intervals[2]
    l_bis = list()
    l0 = abs(b - a)
    i = 0
    while abs(b - a) >= l0*tol and i < n_max:
        x1 = (b + a)/2
        l_bis.append(x1)
        if f1(x1)*f1(a) < 0:
            b = x1
        else:
            a = x1

        i += 1

    return l_bis, [f1, a, b]


def aitken(method, tol, *args, first=True):
    p1 = list()
    q1 = list()
    f1 = args[0]
    calculate_q = True
    if first:
        nums, args = method(args, tol, n_max=4)
    else:
        nums, args = method(args[1:], tol, n_max=4)
    p1 += nums
    q1.append(p1[0] - ((p1[1] - p1[0])**2/((p1[2] - p1[1]) - (p1[1] - p1[0]))))
    if abs(f1(q1[-1])) <= tol:
        return q1
    q1.append(p1[1] - ((p1[2] - p1[1]) ** 2 / ((p1[3] - p1[2]) - (p1[2] - p1[1]))))

    i = 1
    while True:
        if calculate_q:
            if abs(f1(q1[-1])) <= tol:
                calculate_q = False
            else:
                i += 1
                nums, args = method(args, tol, n_max=1)
                if nums[0] == p1[-1]:
                    nums.pop(0)
                p1 += nums
                try:
                    q1.append(p1[i] - (p1[i+1] - p1[i])**2/((p1[i+2] - p1[i+1]) - (p1[i+1] - p1[i])))
                except IndexError:
                    break
                except ZeroDivisionError:
                    break
        else:
            nums, args = method(args, tol)
            if nums[0] == p1[-1]:
                nums.pop(0)
            p1 += nums
            break

    return p1, q1


def print_lists(list1, list2, str_list1="List1", str_list2="List2",
                name_file="List.txt", title1="Comparison", decimals=5, initials1=1,
                initials2=1):

    def round_str(er, decimals1):
        er_str = list(str(er).split("e"))

        er_str[0] = str(round(float(er_str[0]), decimals1))
        if len(er_str) > 1:
            return er_str[0] + "e" + er_str[1]
        else:
            return er_str[0]

    # Create file
    file = open(name_file, "w+")
    max_len = max([len(list1), len(list2)])

    # Printing initial table
    spaces = " "*(decimals + 9)
    l_sp = len(spaces)
    file.write(title1 + "\n")
    file.write("i" + spaces + str_list1 + spaces + str_list2
               + spaces + "Error1" + spaces + "Error2")

    for i in range(max_len):
        # Make sure same spaces to i.
        spaces_i = " "*(l_sp + 1 - len(str(i)))
        file.write("\n")

        # Calculating number of list1
        if i < len(list1):
            num1 = round_str(list1[i], decimals)
            if i > initials1 - 1:
                er1 = round_str(abs(list1[i] - list1[i-1]), 4)
            else:
                er1 = ""
        else:
            num1 = " "*(decimals + 2)
            er1 = ""

        # Calculating number of list 2
        if i < len(list2):
            num2 = round_str(list2[i], decimals)
            if i > initials2 - 1:
                er2 = round_str(abs(list2[i] - list2[i-1]), 4)
            else:
                er2 = ""
        else:
            num2 = " "*(decimals + 2)
            er2 = ""

        spaces12 = " "*(l_sp + 5 - len(str(num1)))
        spaces1er = " "*(l_sp + 5 - len(str(num2)))
        spaces_er1er2 = " "*(l_sp + 6 - len(str(er1)))
        file.write(str(i) + spaces_i + num1 + spaces12 + num2
                   + spaces1er + str(er1) + spaces_er1er2 + str(er2))
    file.close()


def fix_point(function_initial, tol, n_max=100):
    g1 = function_initial[0]
    p0 = function_initial[1]
    xs = [p0, g1(p0)]
    i = 2
    while i < n_max and abs(xs[-1] - xs[-2]) >= tol:
        xs.append(g1(xs[-1]))
        i += 1
    return xs, [g1, xs[-1]]


def steffensen(tol, *args):
    return aitken(fix_point, tol, *args, first=False)


def secant(f1, x0=0.0, x1=1.0, tol=1e-15, n_max=1e5):
    fx0 = f1(x0)
    if abs(fx0) <= tol:
        return [x0]
    fx1 = f1(x1)
    cont = 1
    den = fx1 - fx0

    # Calculate first value
    x2 = x1 - fx1 * (x1 - x0) / den
    xs = [x0, x1, x2]
    while abs(x2 - x1) > tol and abs(fx1) > tol and den != 0 and cont < n_max:
        # Shift variables
        x0 = x1
        fx0 = fx1
        x1 = x2
        fx1 = f1(x2)
        den = fx1 - fx0
        cont += 1

        # Calculate next iteration
        x2 = x1 - fx1*(x1 - x0)/den
        xs.append(x2)

    return xs


def muller(f1, x0=0.0, x1=1.0, x2=2.0, tol=1e-15, n_max=1e5):
    fx0 = f1(x0)
    if abs(fx0) <= tol:
        return [x0]
    fx1 = f1(x1)
    if abs(fx1) <= tol:
        return [x1]
    fx2 = f1(x2)
    if abs(fx2) <= tol:
        return [x2]

    # Calculating x3
    cont = 1
    xs = [x0, x1, x2]
    h1 = x1 - x0
    h2 = x2 - x1
    d1 = (fx1 - fx0) / h1
    d2 = (fx2 - fx1) / h2
    a = (d2 - d1) / (h2 + h1)
    b = d2 + (h2 * a)
    d = m.sqrt(abs(b ** 2 - 4 * (fx2 * a)))
    if abs(b - d) < abs(b + d):
        e = b + d
    else:
        e = b - d
    x3 = x2 - (2 * fx2) / e
    xs.append(x3)

    while abs(x3 - x2) > tol and abs(fx2) >= tol and cont < n_max:
        # Shifting variables for next iteration
        x0 = x1
        fx0 = fx1
        x1 = x2
        fx1 = fx2
        x2 = x3
        fx2 = f1(x3)
        cont += 1

        # Calculating next value
        h1 = x1 - x0
        h2 = x2 - x1

        d1 = (fx1 - fx0) / h1
        d2 = (fx2 - fx1) / h2

        a = (d2 - d1) / (h2 + h1)
        b = d2 + (h2 * a)
        if b**2 > 4*fx2*a:
            d = m.sqrt(b ** 2 - 4 * (fx2 * a))
        else:
            d = 0
        if abs(b - d) < abs(b + d):
            e = b + d
        else:
            e = b - d

        x3 = x2 - (2 * fx2) / e
        xs.append(x3)

    return xs


# Bisection functions
# Example 1
def f(x):
    return m.exp(3*x - 12) + x*m.cos(3*x) - x**2 + 4


# Example 2
def f2(x):
    return (x-3)**3


# Secant and Muller function
# Example 1
def g(x):
    return x**3 - 3*x + 2


# Example 2
def g2(x):
    return 16*x**4 - 40*x**3 + 5*x**2 + 20*x + 6


# Steffensen
# Example 1
def h_og(x):
    return x**3 + 4*x**2 - 10


def h(x):
    return m.sqrt(10/(x + 4))


# Example 2
def h2_og(x):
    return m.exp(x) - x - 2


def h2e(x):
    return m.log(x + 2)


# Print Muller vs Secant
# Example 1
x0_s = 2.2
x1_s = 2.1
x2_m = 2.0
tol_s = 1e-5
title = "Secant vs Muller with f(x) = x^3 - 3x + 2, with: \nFor the Secant method x0 = " + str(x0_s) + ", x1 = " + \
        str(x1_s) + "\nFor the muller method x0 = " + str(x0_s) + ", x1 = " + str(x1_s) + ", x2 = " + str(x2_m) + "\n" \
        + "With a tolerance of " + str(tol_s) + "\n"
p = secant(g, x0=x0_s, x1=x1_s, tol=tol_s)
q = muller(g, x0=x0_s, x1=x1_s, x2=x2_m, tol=tol_s)
print_lists(p, q, str_list1="Seca.", str_list2="Mull.", name_file="Muller Example 1.txt", title1=title,
            decimals=8, initials1=2, initials2=3)

# Example 2
x0_s = 2.5
x1_s = 2.0
x2_m = 2.3
tol_s = 1e-5
title = "Secant vs Muller with f(x) = 16x^4 - 40x^3 + 5x^2 + 20x + 6, with: \nFor the Secant method x0 = " + str(x0_s) \
        + ", x1 = " + str(x1_s) + "\nFor the muller method x0 = " + str(x0_s) + ", x1 = " + str(x1_s) + ", x2 = " + \
        str(x2_m) + "\n" + "With a tolerance of " + str(tol_s) + "\n"
p = secant(g2, x0=x0_s, x1=x1_s, tol=tol_s)
q = muller(g2, x0=x0_s, x1=x1_s, x2=x2_m, tol=tol_s)
print_lists(p, q, str_list1="Seca.", str_list2="Mull.", name_file="Muller Example 2.txt", title1=title,
            decimals=8, initials1=2, initials2=3)

############################################
# Print Fix point vs Steffensen
# Example 1
x0_f = 1.5
tol_st = 1e-5
p, q = steffensen(tol_st, h_og, h, x0_f)
title = "Fix point vs Steffensen, to approximate the root of f(x) = x^3 + 4*x^2 - 10 with the function \n" \
        "g(x) = (10/(x + 4))^(1/2) with x0 = 1.5.\n"
print_lists(p, q, str_list1="FixP.", str_list2="Stef.", name_file="Steffensen Example 1.txt", title1=title,
            decimals=8)

# Example 2
x0_f = 1.5
tol_st = 1e-5
p, q = steffensen(tol_st, h2_og, h2e, x0_f)
title = "Fix point vs Steffensen, to approximate the root of f(x) = e^x - x - 2 with the function \n" \
        "g(x) = ln(x + 2) with x0 = 1.5.\n"
print_lists(p, q, str_list1="FixP.", str_list2="Stef.", name_file="Steffensen Example 2.txt", title1=title,
            decimals=8)

############################################
# Print Bisection vs Aitken
# Example 1
a_bisection = 2
b_bisection = 3
tol_bisection = 1e-5
p, q = aitken(bisection, tol_bisection, f, a_bisection, b_bisection)
f_str = "e^(3x - 12) + x cos(3x) - x^2 + 4"
title = "Bisection vs Aitken with " + f_str + ", with an interval [" + str(a_bisection) + ", " + \
        str(b_bisection) + "] with tolerance " + str(tol_bisection) + "\n"
print_lists(p, q, str_list1="Bise.", str_list2="Aitk.", name_file="Aitken Example 1.txt", title1=title,
            decimals=8)

# Example 2
a_bisection = 2.5
b_bisection = 5
tol_bisection = 1e-5
p, q = aitken(bisection, tol_bisection, f2, a_bisection, b_bisection)
f_str = "(x - 3)**3"
title = "Bisection vs Aitken with " + f_str + ", with an interval [" + str(a_bisection) + ", " + \
        str(b_bisection) + "] with tolerance " + str(tol_bisection) + "\n"
print_lists(p, q, str_list1="Bise.", str_list2="Aitk.", name_file="Aitken Example 2.txt", title1=title,
            decimals=8)
