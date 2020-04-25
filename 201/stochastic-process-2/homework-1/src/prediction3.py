import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc


rc('text', usetex=True)
plt.rcParams.update({'font.size': 18})
np.random.seed(123456789)

# Temperatures in Canada (from hlaniado)
file = open("temps.txt").readlines()
file = list(map(lambda x: x.replace("\n", "").split("\t"), file))

temperatures = np.array(file, dtype=float)
series = temperatures[:, list(range(3))].transpose().flatten()
plt.plot(series,'k')
plt.xlabel('$t$')
plt.ylabel('$T_t$')
plt.savefig('plts/temps.pdf', bbox_inches='tight')
plt.show()