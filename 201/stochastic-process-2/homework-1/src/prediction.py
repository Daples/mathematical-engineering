import matplotlib.pyplot as plt
import numpy as np
from sympy.abc import x
from sim_par import brownian_motion, euler_m
from scipy.stats import norm
import scipy.optimize as opt
import scipy.integrate as integrate
from matplotlib import rc


rc('text', usetex=True)
plt.rcParams.update({'font.size': 18})
np.random.seed(123456789)

# Parameters
mu = 0.003
sigma = 0.03
delta_t = 1
t_final = 365
x0 = np.array([1])
delta_mu = 0.004

# Function
f = mu * x
g = sigma * x


def simulation_1(f1, g1, mu1, linewidth=0.5):
    # Creating brownian motion
    bm = brownian_motion(1, 2*t_final, delta_t)

    # Construct the first series
    series_1 = euler_m(f1, g1, delta_t, x0, 1, bm=bm[:, :int(365 / delta_t)], tf=t_final)

    # # Construct second series
    # Constant
    series_c = euler_m(f1, g1, delta_t, series_1[0, :, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    # Optimistic
    mu1 += delta_mu
    f1 = mu1 * x
    series_o = euler_m(f1, g1, delta_t, series_1[0, :, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    # Pessimistic
    mu1 -= 2 * delta_mu
    f1 = mu1 * x
    series_p = euler_m(f1, g1, delta_t, series_1[0, :, -1], 1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)

    top = max(series_1.flatten().max(), series_c.flatten().max(), series_o.flatten().max(),
              series_p.flatten().max())
    bottom = min(series_1.flatten().min(), series_c.flatten().min(), series_o.flatten().min(),
                 series_p.flatten().min())

    t_vals = np.linspace(0, 2*t_final, int(2*t_final / delta_t))
    plt.plot(t_vals[:int(t_final / delta_t)], series_1[0, 0, :], 'k', label='Series 1', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_c[0, 0, :], 'k', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_o[0, 0, :], 'b', label='Optimistic', linewidth=linewidth)
    plt.plot(t_vals[int(t_final / delta_t):], series_p[0, 0, :], 'r', label='Pessimistic', linewidth=linewidth)
    plt.plot([t_final, t_final], [bottom, top], 'k--')
    plt.legend()
    plt.xlabel("Days")
    plt.ylabel("$X_t$")
    plt.savefig("pronostico-1-escenarios.pdf", bbox_inches='tight')
    plt.show()


def bandwidths(f1, g1, mu1, n1, plot=False, linewidth=0.5):
    # Brownian motion
    bm = brownian_motion(n1, 2*t_final, delta_t)

    # First year simulation
    series_1 = euler_m(f1, g1, delta_t, x0, 1, bm=bm[:1, :int(365 / delta_t)], tf=t_final)
    initial_condition = series_1[0, :, -1]

    t_val = np.linspace(0, 2*t_final, int(2*t_final / delta_t))
    t0s = t_val[:int(t_final / delta_t)]
    t1s = t_val[int(t_final / delta_t):]

    # Constant case
    series_c = euler_m(f1, g1, delta_t, initial_condition, n1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)
    if plot:
        plt.figure(1)
        top = max(series_1.flatten().max(), series_c.flatten().max())
        bottom = min(series_1.flatten().min(), series_c.flatten().min())
        plt.plot(t0s, series_1[0, 0, :].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_c[j, 0, :].transpose(), linewidth=linewidth)
        plt.plot([t_final, t_final], [bottom, top], 'k--')
        plt.xlabel("Days")
        plt.ylabel("$X_t$")
        plt.savefig("pronostico-constante.pdf", bbox_inches='tight')

    # Optimistic case
    mu1 += delta_mu
    f1 = mu1 * x
    #  series_o = euler_m(f1, g1, delta_t, initial_condition, n1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)
    if plot:
        plt.figure(2)
        top = max(series_1.flatten().max(), series_o.flatten().max())
        bottom = min(series_1.flatten().min(), series_o.flatten().min())
        plt.plot(t0s, series_1[0, 0, :].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_o[j, 0, :].transpose(), linewidth=linewidth)
        plt.plot([t_final, t_final], [bottom, top], 'k--')
        plt.xlabel("Days")
        plt.ylabel("$X_t$")
        plt.savefig("pronostico-optimista.pdf", bbox_inches='tight')

    # Pessimistic case
    mu1 -= 2 * delta_mu
    f1 = mu1 * x
    # series_p = euler_m(f1, g1, delta_t, initial_condition, n1, bm=bm[:, int(365 / delta_t):], t0=t_final, tf=2*t_final)
    if plot:
        plt.figure(3)
        top = max(series_1.flatten().max(), series_p.flatten().max())
        bottom = min(series_1.flatten().min(), series_p.flatten().min())
        plt.plot(t0s, series_1[0, 0, :].transpose(), 'k', linewidth=linewidth)
        for j in range(n1):
            plt.plot(t1s, series_p[j, 0, :].transpose(), linewidth=linewidth)
        plt.plot([t_final, t_final], [bottom, top], 'k--')
        plt.xlabel("Days")
        plt.ylabel("$X_t$")
        plt.savefig("pronostico-pesimista.pdf", bbox_inches='tight')



    # # Prediction Bands
    res = prediction_bands(series_c, 0.05, t1s)
    print(res.x)
    upper = res.x[0] * (t1s - t_final) + initial_condition
    lower = res.x[1] * (t1s - t_final) + initial_condition
    for j in range(n1):
        if j == n1 - 1:
            plt.plot(t1s, series_c[j, 0, :].transpose(), color='grey', alpha=0.25, linewidth=linewidth, label='Trayectories')
        plt.plot(t1s, series_c[j, 0, :].transpose(), color='grey', alpha=0.25, linewidth=linewidth)
    plt.plot(t1s, upper)
    plt.plot(t1s, lower)
    plt.show()

    # # # Mean Confidence Bands
    # lower, mean, upper = mean_band(series_c, 0.01)
    #
    # t_val = np.linspace(t_final, 2 * t_final, int(t_final / delta_t))
    #
    # plt.figure(4)
    # for j in range(n1):
    #     if j == n1 - 1:
    #         plt.plot(t1s, series_c[j, 0, :].transpose(), color='grey', alpha=0.25, linewidth=linewidth, label='Trayectories')
    #     plt.plot(t1s, series_c[j, 0, :].transpose(), color='grey', alpha=0.25, linewidth=linewidth)
    # plt.plot(t_val, lower, 'r', linewidth=linewidth)
    # plt.plot(t_val, mean, 'k', linewidth=linewidth, label='Mean')
    # plt.plot(t_val, upper, 'r', linewidth=linewidth, label='Naive Confidence Bands')
    # plt.xlabel("Days")
    # plt.ylabel("$X_t$")
    # plt.legend()
    # plt.savefig("bandas-constante.pdf", bbox_inches='tight')
    # plt.show()

def mean_band(time_series, alpha1):
    # Naive method
    n = time_series.shape[0]
    y_bar = (np.log(time_series[:, 0, :])).mean(axis=0)
    S = time_series[:, 0, :].std(axis=0, ddof=1)
    Za = norm.ppf(1 - alpha1/2)
    width = S * Za / (n ** 0.5)
    lower = np.exp(y_bar - width)
    upper = np.exp(y_bar + width)
    means = time_series[:, 0, :].mean(axis=0)
    return lower, means, upper


def prediction_bands(time_series, alpha1, t):
    x0 = time_series[0, 0, 0]
    def of(a):
        fun = (a[0] * (t - t_final) + x0) + (np.abs(a[1]) * (t - t_final) + x0 )
        return integrate.simps(fun)

    def prob(a):
        probs = np.zeros(time_series.shape[2])
        for j in range(time_series.shape[2]):
            t_val = t_final + j * delta_t
            probs_aux0 = time_series[:, 0, j]
            probs_aux1 = probs_aux0[probs_aux0 >= a[1] * (t_val - t_final) + x0]
            probs[j] = probs_aux1[probs_aux1 <= a[0] * (t_val - t_final) + x0].size / time_series.shape[0]
        return np.mean(probs)


    a0 = np.array([time_series.flatten().max(), time_series.flatten().min()]) / 365
    lb = 1 - alpha1
    bnds = ((0, 1), (-0.1, 0))

    # Constraints for SLSQP
    # cons = ({'type': 'eq', 'fun': prob}, {'type': 'ineq', 'fun': lambda a: a[0] - a[1]})

    # Constraints for trust-constr
    nlc = opt.NonlinearConstraint(prob, lb, 1)
    lc = opt.LinearConstraint([1, -1], 0, np.inf)

    res = opt.minimize(of, a0, constraints=[nlc, lc], bounds=bnds, method='trust-constr', options={'verbose': 1, 'initial_constr_penalty': 10})
    print(res)
    return res

bandwidths(f, g, mu, 200)