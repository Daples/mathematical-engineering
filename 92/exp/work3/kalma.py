import numpy as np
import math
import matplotlib.pyplot as plt

def get_zero_mean_normal_vars(cov, shape):
    n_vars, _ = cov.shape
    mean = np.zeros(n_vars)
    return np.random.multivariate_normal(mean, cov, shape)


def simulate(A, x_0, xi, t):
    _, n_vars = A.shape
    x = np.zeros([t + 1, n_vars])
    x[0] = x_0
    for i in range(t):
        x[i + 1] = np.matmul(A, x[i]) + xi[i]
    return x

def perfect_observer(H, x_0, t):
    return np.array([np.matmul(H, x_0[i]) for i in range(0, t + 1)])

def kalman_filter(F, H, R, Q, z_0, y, t):
    _, n_vars = F.shape
    s_0 = np.zeros([n_vars, n_vars])
    z_hat, z_pred = np.zeros([t + 1, n_vars]), np.zeros([t + 1, n_vars])
    s_hat, s_pred = np.zeros([t + 1, n_vars, n_vars]), np.zeros([t + 1, n_vars, n_vars])

    z_hat[0] = z_0
    s_hat[0] = s_0
    for i in range(0, t):
        F = A(F[:3,0], z_hat[i][0:3])

        z_pred[i + 1] = np.matmul(F, z_hat[i])
        s_pred[i + 1] = np.matmul(np.matmul(F, s_hat[i]), F.T) + Q

        m_opt = np.matmul(np.matmul(H, s_pred[i + 1]), H.T) + R
        m_opt = np.linalg.inv(m_opt)
        m_opt = np.matmul(s_pred[i + 1], np.matmul(H.T, m_opt))

        delta_y = y[i + 1] - np.matmul(H, z_pred[i + 1])
        z_hat[i + 1] = z_pred[i + 1] + np.matmul(m_opt, delta_y)
        s_hat[i + 1] = s_pred[i + 1] - np.matmul(m_opt, np.matmul(H, s_pred[i + 1]))

    return z_hat, s_hat

def A(a_ref, x_ref):
    A = np.zeros((6, 6))
    A[0:3, 0] = a_ref
    # A[0:2, 1:3] = np.eye(2) # Comment for group 3
    A[0:3, 3:6] = np.eye(3) * x_ref[0]
    A[3:6, 3:6] = np.eye(3)
    return A

def plot_simulations(y, y_kalman, var, t):
    t = np.arange(t + 1)
    plt.scatter(t, y[:, var])
    plt.plot(t, y[:, var])
    plt.scatter(t, y_kalman[:, var], color="r")
    plt.plot(t, y_kalman[:, var], color="r")
    plt.ylabel("variable %d" % var)
    plt.xlabel("Time")
    plt.legend(["Simulation", "Kalman"])
    plt.show()

def plot_estimation(a_est, a_real, t):
    colors = ["r", "g", "b"]
    for i, a in enumerate(a_real):
        plt.hlines(a, 0, t+1, color=colors[i], linestyles='dashed')
        plt.plot(a_est[:, i], color= colors[i])
    plt.legend(["a1", "a2", "a3"])
    plt.savefig('chinese_original.pdf', bbox_inches='tight')
    plt.show()

def plot_variance(sigma, T):
    t = np.arange(T+1)
    y = [np.trace(sigma[i]) for i in range(T+1)]
    plt.scatter(t, y)
    plt.plot(t, y)
    plt.ylabel("Value")
    plt.xlabel("Time")
    plt.show()

T = 400

a_real = np.array([0.1, -0.2, 0.2])
a_ref = a_real - 0.2
x_ref = np.zeros(3)

x_0 = np.concatenate( (x_ref, a_ref) )

# Matrix of noise
Q = np.eye(6) * 1
# Q = np.zeros((6,6))
# Q[0:3, 0:3] = np.eye(3) * 0.1** 2
# Q[3:6, 3:6] = np.eye(3) * 0.1** 2

# Output matrixz
H = np.zeros((1, 6))
H[0, 0] = 1
H[0, 1] = 1
H[0, 2] = 1


R = np.eye(1) * 5

seed = 1063421940 #np.random.randint(0,2**30-1)
np.random.seed(seed)
print(seed)

Xi = get_zero_mean_normal_vars(Q, T + 1)
Zeta = get_zero_mean_normal_vars(R, T + 1)

x = simulate(A(a_ref, x_ref), x_0, Xi, T)
y = perfect_observer(H, x, T)

x_kalman, s_kalman = kalman_filter(A(a_ref, x_ref), H, R, Q, x_0, y, T)
y_kalman = perfect_observer(H, x_kalman, T)

print(x_kalman[-1, 3:])
plot_estimation(x_kalman[:,3:], a_real, T)
#plot_simulations(y, y_kalman, 0, T)
#plot_variance(s_kalman, T)