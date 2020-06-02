from sympy.abc import x, t
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
from tqdm import tqdm

num_cores = multiprocessing.cpu_count()
np.random.seed(123456789)


# Calculate a brownian motion
def brownian_motion(n, tf, delta_t, show=False):
    def aux(delta_t1, tf1):
        arr = np.zeros(int(tf1 / delta_t1))
        for j1 in range(1, arr.size):
            arr[j1] = arr[j1 - 1] + np.sqrt(delta_t1) * np.random.normal(0, 1)
        return arr
    if show:
        print('\nSimulating Brownian Motions')
        mb = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(delta_t, tf) for i in tqdm(range(n))))
    else:
        mb = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(delta_t, tf) for i in range(n)))
    return mb


# Euler Maruyama method
def euler_m(f, g, delta_t, x0, n, bm=None, tf=-1, t0=-1, show=False):
    def aux(f1, g1, delta_t1, x01, j, bm1, tf1, arr_type=np.float):
        arr = np.zeros((x0.size, int((tf1 - t0) / delta_t)), dtype=arr_type)
        arr[:, 0] = x01
        for i in range(1, arr.shape[1]):
            t_val = t0 + i * delta_t1
            fx = f1.subs([(x, arr[:, i - 1]), (t, t_val)]).evalf()
            gx = g1.subs([(x, arr[:, i - 1]), (t, t_val)]).evalf()
            arr[:, i] = arr[:, i - 1] + fx * delta_t1 + gx * (bm1[j, i] - bm1[j, i - 1])
        return arr

    def simulation_exit_status(arr_type=np.float):
        j = 0
        try:
            if show:
                print('\nSimulating EDEs')
                xt = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(f, g, delta_t, x0, j, bm, tf,
                                                                      arr_type=arr_type) for j in tqdm(range(n))))
            else:
                xt = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(f, g, delta_t, x0, j, bm, tf, arr_type=arr_type)
                                                                      for j in range(n)))
            return (True, -1), xt
        except:
            return (False, j), []

    # Initialize optional parameters
    if tf < 0:
        tf = 1
    if t0 < 0:
        t0 = 0
    if bm is None:
        bm = brownian_motion(n, tf - t0, delta_t)

    # Simulation
    count = 0
    max_count = 20
    while True:
        exit_status, xt = simulation_exit_status()
        if exit_status[0]:
            break
        else:
            bm[exit_status[1], :] = brownian_motion(1, tf - t0, delta_t)[0, :]
            count += 1
        if count > max_count:
            _, xt = simulation_exit_status(np.complex)
            break
    return xt


def euler_m_ns(f, g, delta_t, x0, n, bm=None, tf=-1, t0=-1, show=False):
    def aux(f1, g1, delta_t1, x01, j, bm1, tf1, arr_type=np.float):
        arr = np.zeros((x0.size, int((tf1 - t0) / delta_t)), dtype=arr_type)
        arr[:, 0] = x01
        for i in range(1, arr.shape[1]):
            t_val = t0 + i * delta_t1
            fx = f1(arr[:, i - 1], t_val)
            gx = g1(arr[:, i - 1], t_val)
            arr[:, i] = arr[:, i - 1] + fx * delta_t1 + gx * (bm1[j, i] - bm1[j, i - 1])
        return arr

    def simulation_exit_status(arr_type=np.float):
        j = 0
        try:
            if show:
                print('\nSimulating EDEs')
                xt = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(f, g, delta_t, x0, j, bm, tf,
                                                                      arr_type=arr_type) for j in tqdm(range(n))))
            else:
                xt = np.array(Parallel(n_jobs=num_cores)(delayed(aux)(f, g, delta_t, x0, j, bm, tf, arr_type=arr_type)
                                                                      for j in range(n)))
            return (True, -1), xt
        except:
            return (False, j), []

    # Initialize optional parameters
    if tf < 0:
        tf = 1
    if t0 < 0:
        t0 = 0
    if bm is None:
        bm = brownian_motion(n, tf - t0, delta_t)

    # Simulation
    count = 0
    max_count = 20
    while True:
        exit_status, xt = simulation_exit_status()
        if exit_status[0]:
            break
        else:
            bm[exit_status[1], :] = brownian_motion(1, tf - t0, delta_t)[0, :]
            count += 1
        if count > max_count:
            _, xt = simulation_exit_status(np.complex)
            break
    return xt


# Milstein method
def mils(f, g, delta_t, x0, bm=None, tf=-1, t0=-1):
    # Initialize optional parameters
    if bm is None:
        bm = brownian_motion(1, tf - t0, delta_t)
    if tf < 0:
        tf = 1
    if t0 < 0:
        t0 = 0

    # Simulation
    xt = np.zeros((x0.size, int((tf - t0) / delta_t)))
    xt[:, 0] = x0
    for i in range(1, int((tf - t0) / delta_t)):
        t_val = t0 + i * delta_t
        fx = f.subs([(x, xt[:, i - 1]), (t, t_val)]).evalf()
        gx = g.subs([(x, xt[:, i - 1]), (t, t_val)]).evalf()
        gpx = g.diff(x).subs([(x, xt[:, i - 1]), (t, t_val)]).evalf()
        delta_b = bm[0, i] - bm[0, i - 1]
        xt[:, i] = xt[:, i - 1] + fx * delta_t + gx * delta_b + 0.5 * gpx * gx * (delta_b ** 2 - delta_t)
    return xt
