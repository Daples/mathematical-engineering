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


class Data:
    def __init__(self, line):
        self.turn = line[1]
        self.stage = line[3]
        self.date = line[4]

        self.start_time = line[5]
        self.waiting_time = line[6]
        self.attention_time = line[7]
        self.duration_time = line[8]
        self.final_time = line[9]

        self.attendant = no_tilde(line[11])
        self.module = line[12]
        self.service = no_tilde(line[13])
        self.state = line[14]

    def get_date(self, date_type):
        if date_type == "day":
            index = 2
        elif date_type == "month":
            index = 1
        else:
            index = 0
        return int(self.date.split("-")[index])

    def inter_arrival(self, other):
        time2 = self.start_time
        time1 = other.start_time
        if time1.hour > time2.hour:
            time1, time2 = time2, time1
        min1 = time1.minute + time1.second / 60
        min2 = time2.minute + time2.second / 60
        min2 += (time2.hour - time1.hour) * 60
        return min2 - min1

    def inter_service(self, other):
        time2 = self.attention_time
        time1 = max(other.final_time, self.start_time, key=lambda x: x.hour*60 + x.minute + x.second / 60)
        min1 = time1.minute + time1.second / 60
        min2 = time2.minute + time2.second / 60
        min2 += (time2.hour - time1.hour) * 60
        return min2 - min1

    def comp(self, other, st0=True, hour=False):
        if st0:
            time0 = self.start_time
            time1 = other.start_time
        else:
            time0 = self.attention_time
            time1 = other.attention_time
        if not hour:
            return int(time0.minute / 30) != int(time1.minute / 30)
        else:
            return time0.hour != time1.hour


class DataSet:
    def __init__(self):
        # Reading data
        cwd = os.getcwd()
        os.chdir("..")
        path = os.path.join(os.getcwd(), "data/data.xlsx")
        file = pandas.read_excel(path).to_numpy()
        os.chdir(cwd)
        self.data = []
        start = False
        for i in range(file.shape[0]):
            d = Data(file[i, :])
            if not start and d.get_date("day") == 26:
                start = True
            if start:
                self.data.append(d)

        # Starting day of the week
        self.initial_day = 0
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"]

        # Analyzer of data
        self.analyzer = DataAnalysis()

    # Get inter times for an hour, given it's initial index
    def inter_times(self, initial_index=0):
        inter_time = []
        index = initial_index
        for i in range(initial_index + 1, len(self.data)):
            index = i
            data0 = self.data[i - 1]
            data = self.data[i]
            if data0.stage == 2 or data.stage == 2:
                continue
            if data0.comp(data, hour=True):
                break
            dur = data.inter_arrival(data0)
            inter_time.append(dur)
        return inter_time, index

    # Finds distributions for each day and hour
    def all_inter_times(self):
        da = self.analyzer
        # Initial test
        day_prev = self.data[0].get_date("day")
        index_day = self.initial_day

        j = 0
        while j < len(self.data) - 1:
            day = self.data[j].get_date("day")
            index_day = (index_day + (day - day_prev)) % len(self.days)
            title = "Test for " + self.days[index_day] + " " + str(day) + \
                    ", hour " + str(self.data[j].start_time.hour)
            day_prev = day
            inter_times, j = self.inter_times(j)
            if len(inter_times) != 0:
                da.set_data(inter_times)
                da.fitting_test(title=title, signal=True, write=True,
                                name_file="sim-params/inter-time-distributions.sol")
                
    # Gets length of service for each attendant
    def service_times(self, attendant, service):
        aux = filter(lambda x: x.attendant == attendant and x.service == service, self.data)
        times = filter(lambda x: x != "empty", map(lambda x: x.duration_time, aux))
        return list(map(lambda x: x.hour*60 + x.minute + x.second/60, times))
    
    # Finds distributions for each type of service for each attendant
    def all_service_times(self):
        names = list(set(map(lambda x: x.attendant, self.data)))
        names = list(filter(lambda x: x != "empty", names))
        for name in names:
            attendant_name = list(filter(lambda x: x.attendant == name, self.data))
            services = list(set(map(lambda x: x.service, attendant_name)))
            for service in services:
                title = "Test for " + name + " for service " + service
                service_times = self.service_times(name, service)
                if len(service_times) in range(2, 16):
                    file = open("sim-params/attendants-distributions.sol", "a+")
                    file.write(header + "\n")
                    file.write(title + "\n")
                    file.write("Not enough data.\n")
                    file.close()
                    continue
                elif len(service_times) == 1:
                    continue
                else:
                    services2 = service_times
                self.analyzer.set_data(services2)
                self.analyzer.fitting_test(write=True, title=title, signal=True, 
                                           name_file="sim-params/attendants-distributions.sol")
    
    # Supposes normal distributions in case of not enough data for test
    def service_times_outliers(self):
        # Make data for outliers without test
        file = open("sim-params/attendants-distributions.sol", "r").read()
        file0 = open("sim-params/attendants-outliers.sol", "w")
        pages = file.split(header)[1:]
        title = re.compile("Test for (.*) for service (.*)\n")
        for page in pages:
            page = page.replace(". USED RANDOM SAMPLING.", "")
            if "Not enough data." in page:
                name, service = title.findall(page)[0]
                data_name = self.service_times(name, service)
                std = float(np.std(data_name, ddof=1))
                file0.write(header + "\n")
                file0.write("Test for " + str(name) + " for service " + str(service) + "\n")
                string = "mean = " + str(round(float(np.mean(data_name)), n_round)) + \
                         " desv = " + str(round(std, n_round)) + "\n"
                file0.write(string)
        file0.close()

    # Gets inter services times for each attendant
    def inter_service_times(self, aux, attendant):
        if aux is None:
            aux = self.data
        inter = {}
        i = 0
        data = list(filter(lambda x: x.attendant == attendant, aux))
        while i < len(data) - 1:
            data0 = data[i]
            data1 = data[i + 1]
            i += 1
            if data0.comp(data1):
                continue
            t = data1.inter_service(data0)
            if t > 0:
                if data0.attention_time.hour in inter:
                    inter[data0.attention_time.hour].append(t)
                else:
                    inter[data0.attention_time.hour] = [t]
        return inter

    # Finds distributions for all inter service times
    def all_inter_service_times(self):
        names = list(set(map(lambda x: x.attendant, self.data)))
        names = list(filter(lambda x: x != "empty", names))
        aux = list(sorted(filter(lambda x: x.attention_time != "empty", self.data),
                          key=lambda x: (x.get_date("day"),
                                         x.attention_time.hour * 60 +
                                         x.attention_time.minute +
                                         x.attention_time.second / 60)))
        for name in names:
            inter_service = self.inter_service_times(aux, name)
            for hour in inter_service:
                title = "Test for " + name + ", hour " + str(hour)
                self.analyzer.set_data(inter_service[hour])
                self.analyzer.fitting_test(write=True, title=title, signal=True, show=False,
                                           name_file="sim-params/inter-services-distributions.sol")
    
    # Gets open modules for hour in a day
    def open_modules(self, aux, initial_index=0):
        modules = []
        names = {}
        index = initial_index
        if aux is None:
            aux = self.data
        for i in range(initial_index, len(aux)):
            index = i
            data = aux[i]
            if i + 1 < len(aux) and data.comp(aux[i + 1], st0=False):
                index = i + 1
                break
            if data.module != "empty":
                modules.append(data.module)
                if data.module in names:
                    names[data.module].append(data.attendant)
                else:
                    names[data.module] = [data.attendant]
        return modules, names, index
    
    # Writes file with all open modules per hour a day
    def all_open_modules(self):
        names = {"Admisiones 1": 1, "Admisiones 2": 2, "Farmacia 1": 5,
                 "Farmacia 2": 1, "Farmacia 3": 10, "Farmacia 4": 11,
                 "FARMACIA 5": 6, "FARMACIA 6": 2, "FARMACIA 7": 3,
                 "FARMACIA 9": 4, "FARMACIA 10": 7, "FARMACIA 11": 8,
                 "FARMACIA 12": 9, "FARMACIA ENTREGAS": 12}
        file = open("sim-params/priorities-names.sol", "r").read().split(header)[1:]
        module_re = re.compile("Module (.*) Capacity [0-9]*\n")
        priorities_re = re.compile("(.*): (.*)\n")
        for page in file:
            priorities = priorities_re.findall(page)
            title = module_re.findall(page)[0].lower()
            for key in names:
                if title in key.lower():
                    for priority in priorities:
                        if int(priority[0]) == names[key]:
                            names[key] = priority[1]
        file = open("sim-params/open-modules.sol", "w")
        day_prev = self.data[0].get_date("day")
        index_day = self.initial_day
        aux = list(sorted(filter(lambda x: x.attention_time != "empty", self.data),
                          key=lambda x: (x.get_date("day"),
                                         x.attention_time.hour * 60 +
                                         x.attention_time.minute +
                                         x.attention_time.second / 60)))
        i = 0
        index = 0
        while i < len(aux) - 1:
            day = aux[i].get_date("day")
            index_day = (index_day + (day - day_prev)) % len(self.days)
            title = "Modules for " + self.days[index_day] + " " + str(day) + \
                    ", hour " + str(aux[i].attention_time.hour) + "-" + str(index)
            index = (index + 1) % 2
            print(title + "\n")
            day_prev = day
            modules, attendants, i = self.open_modules(aux, initial_index=i)
            priorities = list(map(lambda x: names[x], set(modules)))
            aux0 = {}
            for module in attendants:
                if names[module] not in aux0:
                    aux0[names[module]] = list(set(attendants[module]))
                else:
                    aux0[names[module]] += list(set(attendants[module]))
            for name in aux0:
                aux0[name] = list(set(aux0[name]))
            attendants = aux0

            file.write(header + "\n")
            file.write(title + "\n")
            for elem in set(priorities):
                if '4' in elem:
                    module = "Admisiones"
                else:
                    module = "Farmacia"
                file.write(str(priorities.count(elem)) + ": " + elem + " " + module + "\n")
                for name in attendants[elem]:
                    file.write("\t\t" + name + "\n")
        file.close()

    # Gets service probability
    def service_probability(self):
        services = list(filter(lambda x: x != "empty", map(lambda x: x.service, self.data)))
        unique_services = list(set(services))
        file = open("sim-params/service-probability.sol", "w")
        ns = n_spaces*4
        for service in unique_services:
            n = ns
            if len(service) < 8:
                n += (8 - len(service))
            else:
                n -= (len(service) - 8)
            spaces = " "*n
            file.write(service + spaces + str(services.count(service)/len(services)) + "\n")
        file.close()

    # Gets quitters probability
    def quitters_probability(self):
        states = list(filter(lambda x: x != "empty", map(lambda x: x.state, self.data)))
        unique_states = set(states)
        file = open("sim-params/quitters-probability.sol", "a+")
        for state in unique_states:
            n = n_spaces
            if len(state) < 8:
                n += (8 - len(state))
            else:
                n -= (len(state) - 8)
            spaces = " " * n
            file.write(state + spaces + str(states.count(state) / len(states)) + "\n")
        file.close()

    # Gets second stage probability
    def stage_probability(self):
        stages = list(filter(lambda x: x != "empty", map(lambda x: x.stage, self.data)))
        unique_stages = set(stages)
        file = open("output.sol", "a+")
        for stage_number in unique_stages:
            stage = str(stage_number)
            n = n_spaces
            if len(stage) < 8:
                n += (8 - len(stage))
            else:
                n -= (len(stage) - 8)
            spaces = " " * n
            file.write(stage + spaces + str(stages.count(stage_number) / len(stages)) + "\n")
        file.close()

    # Get waiting time per day per type of customer
    def waiting_time(self):
        data = {}

        day_prev = self.data[0].get_date("day")
        index_day = self.initial_day
        for data0 in self.data:
            if data0.waiting_time == "empty" or data0.stage == 2 or data0.service == "empty":
                continue
            day = data0.get_date("day")
            index_day = (index_day + (day - day_prev)) % len(self.days)

            if self.days[index_day] not in data:
                data[self.days[index_day]] = {}

            if data0.service not in data[self.days[index_day]]:
                data[self.days[index_day]][data0.service] = []

            time = data0.waiting_time
            data[self.days[index_day]][data0.service].append(time.hour * 60 + time.minute + time.second / 60)

            day_prev = day
        return data

    # Gets all parameters needed for simulating
    def get_all_params(self):
        self.all_inter_times()
        self.all_service_times()
        self.service_times_outliers()
        self.all_inter_service_times()
        self.all_open_modules()
        self.service_probability()
        self.quitters_probability()


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


DataSet().all_inter_times()
