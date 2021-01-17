import numpy as np
import os
import re
import warnings
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from scipy import stats as st
warnings.filterwarnings('ignore')

import pandas

# Aesthetic
blue = '\033[94m'
green = '\033[92m'
red = '\033[91m'
end = '\033[0m'
bold = '\033[1m'
head = '\033[95m'

header = "===================================="
n_spaces = 8
n_round = 5
np.random.seed(2 ** 32 - 1)


def no_tilde(string):
    string = string.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o")
    return string.replace("ú", "u").replace("ñ", "n")


class DataAnalysis:
    def __init__(self):
        self.to_analyze = []
        self.solutions = []
        self.possible_distributions = ["alpha", "anglit", "arcsine", "beta", "betaprime", "bradford", "burr",
                                       "cauchy", "chi", "chi2", "cosine", "dgamma", "dweibull", "erlang", "expon",
                                       "exponnorm", "exponweib", "exponpow", "f", "fatiguelife", "fisk", "foldcauchy",
                                       "foldnorm", "frechet_r", "frechet_l", "genlogistic", "genpareto", "gennorm",
                                       "genexpon", "genextreme", "gausshyper", "gamma", "gengamma", "genhalflogistic",
                                       "gilbrat", "gompertz", "gumbel_r", "gumbel_l", "halfcauchy", "halflogistic",
                                       "halfnorm", "halfgennorm", "hypsecant", "invgamma", "invgauss", "invweibull",
                                       "johnsonsb", "johnsonsu", "ksone", "kstwobign", "laplace", "levy", "levy_l",
                                       "logistic", "loggamma", "loglaplace", "lognorm", "lomax", "maxwell", "mielke",
                                       "nakagami", "ncx2", "ncf", "nct", "norm", "pareto", "pearson3", "powerlaw",
                                       "powerlognorm", "powernorm", "rdist", "reciprocal", "rayleigh", "rice",
                                       "recipinvgauss", "semicircular", "t", "triang", "truncexpon", "truncnorm",
                                       "tukeylambda", "uniform", "vonmises", "vonmises_line", "wald", "weibull_min",
                                       "weibull_max", "wrapcauchy"]

    # Set data to analyze
    def set_data(self, data):
        self.to_analyze = data

    # Kolmogorov test for every distribution
    def fitting_test(self, rank=10, level=0.05, title="", show=False, plot=False,
                     signal=False, write=False, name_file=""):
        results = []
        if signal:
            if title != "":
                print(bold + "Starting test", title + "." + end)
            else:
                print(bold + "Starting test." + end)
        for distribution in self.possible_distributions:
            dist = getattr(st, distribution)
            try:
                params = list(dist.fit(self.to_analyze))
            except ValueError:
                print(red + "Failed fitting with", distribution, end)
                continue
            _, p_value = st.kstest(self.to_analyze, distribution, args=params)
            if len(results) < rank:
                results.append((p_value, distribution, params, dist))
            else:
                results = list(sorted(results, reverse=True))
                if results[-1][0] < p_value:
                    results.pop()
                    results.append((p_value, distribution, params, dist))
                results = list(sorted(results, reverse=True))
        if len(results) > 0 and signal:
            print(green + "Finished!\n" + end)
        elif len(results) == 0:
            if signal:
                print(head  + "Test failed!" + end)
            return
        self.solutions = results
        if show:
            self.print_results_fitting(level=level, title=title)
        if plot:
            self.plot_fitting()
        if write:
            if name_file != "":
                self.write_results_fitting(level=level, title=title, file=name_file)
            else:
                self.write_results_fitting(level=level, title=title)

    # Print results of fitting
    def print_results_fitting(self, level=0.05, title=""):
        # Print results
        i = 1
        print(header)
        if title != "":
            print(bold + title + end)
        for result in self.solutions:
            if result[0] < level:
                acc = red + "REJECT" + end
            else:
                acc = green + "DO NOT REJECT" + end
            n = n_spaces
            if len(result[1]) < 5:
                n += (5 - len(result[1]))
            elif len(result[1]) > 5:
                n -= (len(result[1]) - 5)
            spaces = " " * n
            print(str(i) + ". " + result[1] + spaces + acc)
            print("\t\tP-value for test", result[0])
            print("\t\tParameters      ", result[2])
            i += 1

    # Write in a file the results
    def write_results_fitting(self, level=0.05, title="", file="output.sol"):
        writer = open(file, "a")
        # Print results
        i = 1
        writer.write(header + "\n")
        if title != "":
            writer.write(title + "\n")
        for result in self.solutions:
            if result[0] < level:
                acc = "REJECT"
            else:
                acc = "DO NOT REJECT"
            n = n_spaces
            if len(result[1]) < 5:
                n += (5 - len(result[1]))
            elif len(result[1]) > 5:
                n -= (len(result[1]) - 5)
            spaces = " " * n
            writer.write(str(i) + ". " + result[1] + spaces + acc + "\n")
            writer.write("\t\tP-value for test " + str(round(result[0], n_round)) + "\n")
            rounded_params = list(map(lambda x: round(x, n_round), result[2]))
            writer.write("\t\tParameters      " + str(rounded_params) + "\n")
            i += 1
        writer.close()

    # Plot all the histograms
    def plot_fitting(self):
        color1 = plt.get_cmap('gist_rainbow')
        color_norm = colors.Normalize(vmin=0, vmax=len(self.solutions))
        scalar_map = cm.ScalarMappable(norm=color_norm, cmap=color1)
        # Histogram
        plt.hist(self.to_analyze, color=scalar_map.to_rgba(0), label="Data", normed=True)
        i = 1
        for solution in self.solutions:
            arg = solution[2][:-2]
            loc = solution[2][-2]
            scale = solution[2][-1]

            dist = solution[-1]

            start = dist.ppf(0.01, *arg, loc=loc, scale=scale)
            end1 = dist.ppf(0.99, *arg, loc=loc, scale=scale)
            x = np.linspace(start, end1, 1000)
            y = dist.pdf(x, loc=loc, scale=scale, *arg)

            plt.plot(x, y, color=scalar_map.to_rgba(i), label=solution[1])
            i += 1
        plt.legend()
        plt.show()

    # Kruskal Wallis test for a number of samples
    def homogeneity_test(self, title="", name_file="output.sol", level=0.05,
                         signal=False, show=False, write=False, plot=False):
        samples = self.to_analyze
        og = len(samples)
        samples = list(filter(lambda x: len(x) > 5, samples))
        if signal:
            print(bold + "Making test", title + end)
            if og != len(samples):
                print(blue + "Removed samples with less than 5 measurements" + end)
                if len(samples) < 2:
                    print(red + "Not enough data for test\n" + end)
                    return
        p_value = 0
        if len(samples) >= 2:
            _, p_value = st.kruskal(*samples)
        means = list(map(lambda x: sum(x) / len(x), samples))
        self.solutions = (p_value, means, samples)
        if write:
            self.write_results_homo(level=level, title=title, name_file=name_file)
        if show:
            print(head)
            print(bold + title + end)
            if p_value < level:
                print(green + "The data is homogeneous" + end)
            else:
                print(red + "The data is NOT homogeneous" + end)
        if signal:
            print(green + "Finished test!\n" + end)
        if plot:
            self.plot_homo(title=title)

    # Write results for homogeneity test
    def write_results_homo(self, level=0.05, title="", name_file=""):
        file = open(name_file, "a+")
        file.write(header + "\n")
        if title != "":
            file.write(title + "\n")
        n = n_spaces
        if len(self.solutions[1]) < 2:
            file.write("NOT ENOUGH DATA FOR TEST.\n")
        else:
            str1 = "The data is homogeneous."
            p_value = self.solutions[0]
            if p_value < level:
                str1 = "The data is NOT homogeneous."
            if len(str1) < 24:
                n += (24 - len(str1))
            else:
                n -= (len(str1) - 24)
            spaces = " " * n
            file.write(str1 + spaces + str(p_value) + "\n")
            spaces = " "*n_spaces
            for i in range(len(self.solutions[1])):
                mean = self.solutions[1][i]
                file.write("Mean " + str(i + 1) + spaces + str(round(mean, n_round)) + "\n")
        file.close()

    # Plot box plots
    def plot_homo(self, title=""):
        samples = np.array(self.solutions[-1]).transpose()
        plt.clf()
        plt.boxplot(samples)

        title_file = title.replace(" ", "-").lower().replace(",", "") + ".pdf"
        plt.savefig(title_file, bbox_inches='tight')
