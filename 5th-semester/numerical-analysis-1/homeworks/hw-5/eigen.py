from scipy import linalg as lin
import numpy as np

# This code is based in Gorka Eraña Robles work:
# "Implementing the QR Algorithm for efficiently computing matrix eigen values
# and eigen vectors" - 2017


eps = 2.2204e-16


def conj_t(mat1):
    return np.transpose(np.conj(mat1))


def wilkshift(a, b, c, d):
    # This function computes the wilkinson shift of a sub matrix of order 2.
    kappa = d
    s = abs(a) + abs(b) + abs(c) + abs(d)

    if s != 0:
        q = (b/s) * (c/s)

        if q != 0:
            p = 0.5*((a/s) - (d/s))
            r1 = p*p + q
            if r1 < 0:
                mult = 1j
            else:
                mult = 1

            r = np.sqrt(abs(r1))*mult
            if np.real(p)*np.real(r) + np.imag(p)*np.imag(r) < 0:
                r = -r

            kappa -= s*(q / (p + r))

    return kappa


def rot_gen(a, b):
    # This function generates a givens rotations from elements a and b
    if b == 0:
        c = 1
        s = 0
    elif a == 0:
        c = 0
        s = 1
        a = b
        b = 0
    else:
        mu = a/abs(a)
        tau = abs(np.real(a)) + abs(np.imag(a)) + abs(np.real(b)) + abs(np.imag(b))
        nu = tau*np.sqrt(abs(a/tau)**2 + abs(b/tau)**2)
        c = abs(a)/nu
        s = mu*np.conj(b)/nu
        a = nu*mu
        b = 0

    return a, b, c, s


def rot_app(c, s, x, y):
    # Returns plane rotation defined by c and s.
    t = c*x + s*y
    y = c*y - np.conj(s)*x
    x = t

    return x, y


def block_process(h, q, i2):
    n = h.shape[0]
    sigma = wilkshift(h[i2 - 1, i2 - 1], h[i2 - 1, i2],
                      h[i2, i2 - 1], h[i2, i2])

    if np.isreal(sigma) or not np.isreal(h[i2-1:i2+1, i2-1:i2+1]).all():
        h = h - sigma*np.identity(n)
        _, _, c, s = rot_gen(h[i2 - 1, i2 - 1]/lin.norm(h[i2 - 1, i2 - 1]),
                             h[i2, i2 - 1] / lin.norm(h[i2 - 1, i2 - 1]))

        h[i2 - 1, :], h[i2, :] = rot_app(c, -s, h[i2-1, :], h[i2, :])
        h[:i2 + 1, i2-1], h[:i2 + 1, i2] = rot_app(c, -np.conj(s), h[:i2 + 1, i2-1],
                                                   h[:i2 + 1, i2])
        q[:, i2-1], q[:, i2] = rot_app(c, -np.conj(s), q[:, i2-1], q[:, i2])
        h = h + sigma*np.identity(n)

    return h, q


def back_search(h, q, z):
    nh = lin.norm(h)
    i1 = z
    i2 = z
    while i1 > 0:
        if abs(h[i1, i1-1]) > eps*nh and i2 != 1:
            i1 -= 1
        else:
            if i2 != 1:
                h[i1, i1 - 1] = 0

            if i1 == i2 - 1 or i2 == 1:
                h, q = block_process(h, q, i2)

                if i2 != 2:
                    i2 = i1 - 1
                    i1 -= 1
                else:
                    i1 = 0
                    i2 = 0
            elif i1 == i2:
                i2 = i1 - 1
                i1 -= 1
            else:
                break

    return h, q, i1, i2


def house_gen(a):
    u = a.ravel()
    nu = lin.norm(a)
    if nu == 0:
        u[0] = np.sqrt(2)
        return u, nu

    if u[0] != 0:
        rho = np.conj(u[0])/abs(u[0])
    else:
        rho = 1

    u = (rho/nu) * u
    u[0] = 1 + u[0]
    u = u/np.sqrt(u[0])
    nu = - (np.conj(rho))*nu
    return u, nu


def start(*args):
    elem = np.array(args)
    s = 1/np.max(abs(elem))
    elem = s*elem

    p = elem[8] - elem[0]
    q = elem[5] - elem[0]
    r = elem[3] - elem[0]

    c = np.array([[(p*q - elem[7]*elem[6])/elem[2] + elem[1]],
                  [r - p - q],
                  [elem[4]]])

    u, _ = house_gen(c)
    return u


def qr_step(h, q, u, i1, i2):
    n = h.shape[0]
    u = np.reshape(u, (-1, 1))
    for i in range(i1, i2 - 1):
        j = max(i - 1, i1)
        v = np.transpose(u).dot(h[i:i+3, j:])
        h[i:i + 3, j:] = h[i:i+3, j:] - u.dot(v)

        iu = min(i + 3, i2)
        v = h[: iu + 1, i:i+3].dot(u)
        h[: iu + 1, i:i + 3] = h[: iu + 1, i:i+3] - v.dot(np.transpose(u))

        v = q[:, i:i+3].dot(u)
        q[:, i:i + 3] = q[:, i:i+3] - v.dot(conj_t(u))

        if i1 != i2 - 2:
            u, _ = house_gen(h[i+1:i+4, i])
            u = np.reshape(u, (-1, 1))
        if i != i1:
            h[i + 1, j] = 0
            h[i + 2, j] = 0

    if i2 > 1:
        h[i2-1, i2 - 2], h[i2, i2 - 2], c, s = rot_gen(h[i2-1, i2 - 2],
                                                       h[i2, i2 - 2])

        h[i2-1, i2-1:], h[i2, i2-1:] = rot_app(c, s, h[i2-1, i2-1:],
                                               h[i2, i2-1:])

        h[:i2 + 1, i2 - 1], h[:i2+1, i2] = rot_app(c, s, h[:i2 + 1, i2 - 1],
                                                   h[:i2+1, i2])

        q[:n, i2 - 1], q[:n, i2] = rot_app(c, s, q[:n, i2 - 1], q[:n, i2])
    return h, q


def shift_method(h, q, n_max=100):
    n = h.shape[0]
    i2 = n - 1
    it = 0
    while i2 > 0:
        if it > n_max:
            print("Maximum number of iterations reached.")

        old_i2 = i2
        h, q, i1, i2 = back_search(h, q, i2)

        if i2 == old_i2:
            it += 1
        else:
            it = 0

        if i2 > 0:
            u = start(h[i1, i1], h[i1, i1+1], h[i1+1, i1], h[i1+1, i1+1],
                      h[i1 + 2, i1+1], h[i2-1, i2-1], h[i2-1, i2], h[i2, i2 - 1],
                      h[i2, i2])

            h, q = qr_step(h, q, u, i1, i2)
    return h, q


def hess(a):
    n = a.shape[0]
    h = a.astype(float)
    q = np.identity(n)
    for k in range(n - 2):
        u, h[k + 1, k] = house_gen(h[k + 1:, k])
        q[k + 1:, k] = u

        u = np.reshape(u, (-1, 1))
        v = conj_t(u).dot(h[k + 1:, k + 1:])
        h[k + 1:, k + 1:] = h[k + 1:, k + 1:] - u.dot(v)
        h[k + 2:, k] = 0

        v = h[:, k+1:].dot(u)
        h[:, k + 1:] = h[:, k+1:] - v.dot(conj_t(u))

    ind = np.identity(n)
    for k in range(n - 3, -1, -1):
        u = q[k+1:, k]
        u = np.reshape(u, (-1, 1))
        v = conj_t(u).dot(q[k+1:, k+1:])
        q[k + 1:, k + 1:] = q[k+1:, k+1:] - u.dot(v)
        q[:, k] = ind[:, k]
    return h, q


def clean(mat1):
    n = mat1.shape[0]
    m = mat1.shape[1]
    for i in range(n):
        for j in range(m):
            if abs(mat1[i, j]) < 1e-9:
                mat1[i, j] = 0


def real_schur(matrix, n_max=100):
    h, q = hess(matrix)
    t, q = shift_method(h, q, n_max=n_max)
    clean(t)
    clean(q)
    return t, q


def eig_val(t):
    def eig2(a, b, c, d):
        trace = a + d
        det = a*d - b*c

        disc = trace**2/4 - det
        if disc < 0:
            mult = 1j
        else:
            mult = 1

        l11 = trace/2 + np.sqrt(abs(disc))*mult
        l21 = trace/2 - np.sqrt(abs(disc))*mult
        return l11, l21
    n = t.shape[0]
    i = n - 1
    val = []
    while i >= 0:
        if i - 1 >= 0 and t[i, i - 1] != 0:
            l1, l2 = eig2(t[i - 1, i - 1], t[i - 1, i], t[i, i - 1], t[i, i])
            val.append(l1)
            val.append(l2)
            i -= 2
        else:
            val.append(t[i, i])
            i -= 1

    j = 0
    for num in val:
        if abs(np.real(num)) < 1e-10:
            val[j] = np.imag(num)*1j

        if abs(np.imag(num)) < 1e-10:
            val[j] = np.real(num)
        j += 1
    return val


def solve_homo(a):
    n = a.shape[0]

    _, u = lin.lu(a, permute_l=True)
    clean(u)
    print(u)

    # Make it a solvable problem
    b = np.zeros((n - 1, 1), dtype=complex)
    for j in range(n - 1):
        b[j, 0] = -u[j, n - 1]

    aeq = u[:n - 1, :n - 1].astype(complex)

    sol = lin.solve(aeq, b)
    vec = np.zeros((n, 1), dtype=complex)
    vec[n - 1, 0] = 1
    for j in range(n - 1):
        vec[j, 0] = sol[j, 0]

    vec = vec/lin.norm(vec)
    return vec


def eig_vec(a, eigs):
    n = a.shape[0]
    vecs = np.zeros((n, n), dtype=complex)
    i = 0
    for eig1 in eigs:
        a1 = a - eig1*np.identity(n)
        vec = solve_homo(a1)
        vecs[:, i] = np.reshape(vec, (1, -1))
        i += 1

    return vecs


def eig(matrix):
    t, _ = real_schur(matrix)
    eig_vals = np.diag(eig_val(t))
    vecs = eig_vec(matrix, eig_vals)

    return eig_vals, vecs


def roots(coeffs):
    n = len(coeffs) - 1
    if n == -1:
        print("There are not any coefficients")
        return []
    elif coeffs[-1] == 0:
        print("The last coefficient cannot be zero.")
    elif n == 0:
        if coeffs[0] == 0:
            return 0
        else:
            print("There aren't any roots")
            return []
    elif n == 1:
        return -coeffs[0]/coeffs[1]

    a = np.zeros((n, n))
    # Fill with ones
    for i in range(n - 1):
        a[i, i + 1] = 1

    # Fill with coefficients
    for j in range(n):
        a[n - 1, j] = -coeffs[j]/coeffs[-1]

    t, _ = real_schur(a)

    return eig_val(t)


matrix1 = np.array([[0.2133, 0.0522, 0.2197],
                    [0.5878, 0.6833, 0.4063],
                    [0.1428, 0.6086, 0.6299]])

# matrix1 = np.array([[2,-3,1],[0,4,2],[1,-8,7]])
val1, vec1 = eig(matrix1)

print("Eigen values:")
print(val1)
print("\nEigen vectors:")
print(vec1)
