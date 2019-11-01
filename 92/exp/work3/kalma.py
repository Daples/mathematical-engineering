import numpy as np
import matplotlib.pyplot as plt


def get_zero_mean_normal_vars(cov, shape):
    n_vars, _ = cov.shape
    mean = np.zeros(n_vars)
    return np.random.multivariate_normal(mean, cov, shape)


def ideal_model(a1, x_01, t0):
    _, n_vars = a1.shape
    xs = np.zeros([t0 + 1, n_vars])
    xs[0] = x_01
    for i in range(0, t0):
        xs[i + 1] = np.matmul(a1, xs[i])
    return xs


def simulate(a1, x_01, xi1, t0):
    _, n_vars = a1.shape
    xs = np.zeros([t0 + 1, n_vars])
    xs[0] = x_01
    for i in range(0, t0):
        xs[i + 1] = np.matmul(a1, xs[i]) + xi1[i]
    return xs


def perfect_observer(h0, x0, t0):
    return np.array([np.matmul(h0, x0[i]) for i in range(0, t0 + 1)])


def noisy_observer(h0, x0, zeta, t0):
    return np.array([np.matmul(h0, x0[i]) + zeta[i] for i in range(0, t0 + 1)])


def kalman_filter(f, h, r, q, z_0, ys, ts):
    _, n_vars = f.shape
    s_0 = np.zeros([n_vars, n_vars])
    z_hat, z_pred = np.zeros([ts + 1, n_vars]), np.zeros([ts + 1, n_vars])
    s_hat, s_pred = np.zeros([ts + 1, n_vars, n_vars]), np.zeros([ts + 1, n_vars, n_vars])

    z_hat[0] = z_0
    s_hat[0] = s_0
    for i in range(0, ts):
        z_pred[i + 1] = np.matmul(f, z_hat[i])
        s_pred[i + 1] = np.matmul(np.matmul(f, s_hat[i]), f.T) + q

        m_opt = np.matmul(np.matmul(h, s_pred[i + 1]), h.T) + r
        m_opt = np.linalg.inv(m_opt)
        m_opt = np.matmul(s_pred[i + 1], np.matmul(h.T, m_opt))

        delta_y = ys[i + 1] - np.matmul(h, z_pred[i + 1])
        z_hat[i + 1] = z_pred[i + 1] + np.matmul(m_opt, delta_y)
        s_hat[i + 1] = s_pred[i + 1] - np.matmul(m_opt, np.matmul(h, s_pred[i + 1]))
    return z_hat, s_hat


def plot_simulations(ys, y_kalman0, var, t0):
    t = np.arange(t0 + 1)
    plt.scatter(t, ys[:, var])
    plt.plot(t, ys[:, var])
    plt.scatter(t, y_kalman0[:, var], color="r")
    plt.plot(t, y_kalman0[:, var], color="r")
    plt.ylabel("x1")
    plt.xlabel("Time")
    plt.legend(["Simulation", "Kalman"])
    plt.show()


def plot_chinese(x_kalman0, a_ref0, t0):
    t = np.arange(t0 + 1)
    colors = ['r', 'b', 'g', 'k']
    i = 0
    for a in a_ref0:
        as0 = np.ones(t0 + 1) * a
        plt.plot(t, as0, colors[i], label="a" + str(i + 1) + "= " + str(a))
        plt.plot(t, x_kalman0[:, 3 + i], colors[i], label="a_kal")
        i += 1
    plt.legend()
    plt.show()


T = 100

# A matrix
A = np.zeros((6, 6))
a_real = [0.8, 0.3, -0.1]
a_ref = list(map(lambda z: z + 0.5, a_real))
x_0 = np.array([0, 0, 0] + a_ref)
x_ref = 0
A[0, 0] = a_ref[0]
A[1, 0] = a_ref[1]
A[2, 0] = a_ref[2]

A[0, 3] = x_ref
A[1, 4] = x_ref
A[2, 5] = x_ref

alpha = 1
A[0, 1] = 1
A[1, 2] = 1
A[3, 3] = alpha
A[4, 4] = alpha
A[5, 5] = alpha

F = A

# Matrix of noise
Q = np.zeros((6, 6))
Q[0, 0] = 1
Q[1, 1] = 1
Q[2, 2] = 1

# Output matrix
H = np.zeros((1, 6))
H[0, 0] = 1
R = np.array([[1]])

np.random.seed(37756813)
Xi = get_zero_mean_normal_vars(Q, T + 1)
Zeta = get_zero_mean_normal_vars(R, T + 1)

x = simulate(A, np.array([0, 0, 0] + a_real), Xi, T)
y = perfect_observer(H, x, T)

x_kalman, s_kalman = kalman_filter(A, H, R, Q, x_0, y, T)
y_kalman = perfect_observer(H, x_kalman, T)
y_kalman += a_ref[0]

plot_chinese(x_kalman, a_real, T)
