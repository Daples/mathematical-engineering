import math

err = "e"
success_point = "sp"
success = "st"


def sum_vectors(v1, v2):
    v3 = [0] * len(v1)
    for i in range(len(v1)):
        v3[i] = v1[i] + v2[i]
    return v3


def multiply_vector(k, v1):
    vn = [0] * len(v1)
    for i in range(len(v1)):
        vn[i] = k * v1[i]
    return vn


def search_by_triangles(func, x0, dim, tol, mat):
    def check(fa):
        pos = min(fa)
        if pos <= tol:
            return vertices[fa.index(pos)], success_point

        return 0, err

    def make(ver1):
        sv = str(ver1)[1:-1]
        sv1 = sv.split("],")
        resp = ""
        for st in sv1:
            if st != sv1[-1]:
                resp += st + "];"
            else:
                resp += st + ";"

        return resp

    # Generate initial figure
    vertices = [x0]
    s = 0.5
    for j in range(dim):
        aux = [0]*dim
        aux[j] = 1
        vertices.append(sum_vectors(x0, multiply_vector(s, aux)))

    # Create function vectors
    fxs = list(map(func, vertices))
    cont = 0

    # print("Initial vertices " + str(ver))
    print(make(vertices))

    while max(fxs)*min(fxs) >= 0:
        cont = cont + 1
        fx_abs = list(map(abs, fxs))

        # One of the vertices is in the curve
        sol, er = check(fx_abs)
        if er == success_point:
            return sol, [], er

        if not mat:
            print("--------")
            print("Iteration " + str(cont))

        ##############################################
        # Calculate the best
        fl = min(fx_abs)
        best_index = fx_abs.index(fl)
        best = vertices[best_index]

        # Calculate the worst
        fh = max(fx_abs)
        worst_index = fx_abs.index(fh)
        worst = vertices[worst_index]

        # Calculate the second worst
        f_copy = fx_abs.copy()
        f_copy[worst_index] = fl

        fs = max(f_copy)

        # Centroid
        ver_copy = vertices.copy()
        ver_copy.pop(worst_index)
        c = [0]*dim
        for v in ver_copy:
            c = sum_vectors(c, v)

        c = multiply_vector(1 / dim, c)
        #########################################
        # Control parameters
        alf = 1
        bet = 0.5
        gamma = 2
        delta = 0.5

        ###########################################
        # Reflection
        xr = sum_vectors(c, multiply_vector(alf, sum_vectors(c, multiply_vector(-1, worst))))
        fr = abs(func(xr))
        if fl <= fr < fs:
            vertices[worst_index] = xr
            fxs[worst_index] = func(xr)
            if not mat:
                print("Reflecting... " + str(vertices))
            else:
                print(make(vertices))
            continue

        #######################################
        # Expansion
        if fr < fl:
            xe = sum_vectors(c, multiply_vector(gamma, sum_vectors(xr, multiply_vector(-1, c))))
            fe = abs(func(xe))

            if fe < fr:
                vertices[worst_index] = xe
                fxs[worst_index] = func(xe)
                if not mat:
                    print("Expanding... " + str(vertices))
                else:
                    print(make(vertices))
                continue
            else:
                vertices[worst_index] = xr
                fxs[worst_index] = func(xr)
                if not mat:
                    print("Expanding... " + str(vertices))
                else:
                    print(make(vertices))
                continue

        #########################################
        # Contraction
        if fs <= fr < fh:
            xc = sum_vectors(c, multiply_vector(bet, sum_vectors(xr, multiply_vector(-1, c))))
            fc = abs(func(xc))
            if fc <= fr:
                vertices[worst_index] = xc
                fxs[worst_index] = func(xc)
                if not mat:
                    print("Contracting... " + str(vertices))
                else:
                    print(make(vertices))
                continue
            elif fr >= fh:
                xc = sum_vectors(c, multiply_vector(bet, sum_vectors(worst, multiply_vector(-1, c))))
                fc = abs(func(xc))
                if fc < fh:
                    vertices[worst_index] = xc
                    fxs[worst_index] = func(xc)
                    if not mat:
                        print("Contracting... " + str(vertices))
                    else:
                        print(make(vertices))
                    continue

        #########################
        # Shrink
        for j in range(len(vertices)):
            aux = sum_vectors(vertices[j], multiply_vector(-1, best))
            vertices[j] = sum_vectors(best, multiply_vector(delta, aux))
        fxs = list(map(func, vertices))

        if not mat:
            print("Shrinking... " + str(vertices))
        else:
            print(make(vertices))

    return vertices, fxs, success


def norm(v1, v2):
    nv = sum_vectors(v1, multiply_vector(-1, v2))
    for j in range(len(nv)):
        nv[j] = nv[j]**2

    return math.sqrt(sum(nv))


def bisect(f2, a, b, tol):
    x = sum_vectors(a, multiply_vector(0.5, sum_vectors(b, multiply_vector(-1, a))))
    l0 = norm(a, b)
    if f2(x) <= tol:
        return x

    while norm(b, a) > l0*tol:
        if f2(a)*f2(x) < 0:
            b = x
        else:
            a = x
        x = sum_vectors(a, multiply_vector(0.5, sum_vectors(b, multiply_vector(-1, a))))

    return x


def find_points_curve(f3, x0, tol=1e-15, dim=2, mat=False):
    if len(x0) != dim:
        print("The initial point is not valid.")

    for x in x0:
        try:
            x = float(x)
        except ValueError:
            print(str(x) + " is not a number.")

    if abs(f3(x0)) <= tol:
        print(str(x0) + " is a point in the curve.")

    vertices1, fv, er = search_by_triangles(f3, x0, dim, tol, mat)

    if er != success_point:
        a = vertices1[fv.index(min(fv))]
        b = vertices1[fv.index(max(fv))]
        xb = bisect(f3, a, b, tol)
        print("------------")
        print("Value in the curve is " + str(xb))
        print("With a difference of " + str(f(xb)))
    else:
        print("------------")
        print("Value in the curve is " + str(vertices1))
        print("With a difference of " + str(f(vertices1)))


def f(x):
    return 100*(x[1] - x[0]**2)**2 + (1 - x[0])**2


find_points_curve(f, [100, 100])
