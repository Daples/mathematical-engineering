from arch.unitroot import PhillipsPerron
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm


plt.rc('text', usetex=True)
plt.rcParams.update({'font.size': 16})

# Read data
file = open('seguimiento5.csv', 'r')
file = file.read().split('\n')[1:-1]
data = np.array([line.split(',')[1] for line in file], dtype=float)

plot = True
# Plot data
if plot:
    plt.plot(data, 'k')
    plt.xlabel('$t$')
    plt.ylabel('$x_t$')
    plt.savefig('figs/ts.pdf', bbox_inches='tight')

# Model Analysis
if plot:
    sm.graphics.tsa.plot_acf(data, lags=100, title='')
    plt.savefig('figs/acf.pdf', bbox_inches='tight')
    plt.clf()
    sm.graphics.tsa.plot_pacf(data, lags=25, title='')
    plt.savefig('figs/pacf.pdf', bbox_inches='tight')

## Test for stationarity
# Dickey-Fuller
outDF = sm.tsa.stattools.adfuller(data, 12, regression='nc')
print('p_val DF:', outDF[1])

# KPSS
outKPSS = sm.tsa.stattools.kpss(data, nlags=12)
print('p_val KPSS:', outKPSS[1])

# Phillips - Perron
print('p_val PP:', PhillipsPerron(data).pvalue)

# Estimate model
mod = sm.tsa.arima.ARIMA(data, order=(12, 0, 0))
res = mod.fit()
print(res.summary())

if plot:
    plt.clf()
    plt.rcParams.update({'font.size': 11})
    fig = res.plot_diagnostics()
    fig.tight_layout(pad=1.25)
    plt.savefig("figs/res.pdf")
