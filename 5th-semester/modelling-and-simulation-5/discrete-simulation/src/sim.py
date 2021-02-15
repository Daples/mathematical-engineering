import numpy as np
import re
import math
import matplotlib.pyplot as plt
import random
from collections import deque
from scipy import stats as st
from read_data import DataAnalysis, DataSet


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


class Customers:
    class Customer:
        def __init__(self, type_customer, quitter, index, arrival):
            self.quit = quitter
            self.type = type_customer
            self.index = index
            self.arrival = arrival

        # Waiting time for customer
        def waiting_time(self, start_attention):
            return start_attention - self.arrival

        # Name of customer
        def __str__(self):
            return "Customer " + str(self.index)

    def __init__(self, day, hour):
        self.string = "Customer for day " + day + ", in hour " + str(hour)
        self.dist = ""
        self.params = []
        self.get_data(day, hour)

    # Get distribution for each day and hour
    def get_data(self, day, hour):
        file = open("sim-params/inter-time-distributions.sol", "r").read()
        file = file.split(header + "\n")
        file.pop(0)
        title_re = re.compile("Test for (.*) [0-9]*, hour (.*)\n")
        dist_re = re.compile("[0-9]*. (.*)[ ]*DO NOT REJECT\n")
        params_re = re.compile("\t\tParameters[ ]* \[(.*)\]\n")
        found = False
        for page in file:
            test = title_re.findall(page)[0]
            day0 = test[0]
            hour0 = int(test[1])
            if day0 == day and hour == hour0:
                dist = 0
                dist_list = dist_re.findall(page)
                params_list = params_re.findall(page)
                while True:
                    try:
                        self.dist = dist_list[dist].replace(" ", "")
                        params = params_list[dist].split(",")
                        self.params = list(map(lambda x: float(x.replace(" ", "")), params))

                        dist0 = getattr(st, self.dist)
                        if len(self.params) > 2:
                            dist0.rvs(*self.params[:-2], loc=self.params[-2], scale=self.params[-1])
                        else:
                            dist0.rvs(loc=self.params[-2], scale=self.params[-1])
                        break
                    except ValueError:
                        dist += 1
            if found and day0 != day:
                return

    # Generate an arrival for this type of customer
    def get_arrival(self):
        distribution = getattr(st, self.dist)
        loc = self.params[-2]
        scale = self.params[-1]
        if len(self.params) > 2:
            params = self.params[:-2]
            t = distribution.rvs(*params, loc=loc, scale=scale)

        else:
            t = distribution.rvs(loc=loc, scale=scale)
        return t

    # Type of customer
    def __str__(self):
        return self.string


class Attendants:
    def __init__(self, name):
        self.name = name
        self.available0 = True
        self.priorities = {}

        self.distributions = {}
        self.get_data()

        self.inter_distribution = ""
        self.inter_params = []
        self.get_data0()

    # Get distribution for attention time
    def get_data(self):
        file = open("sim-params/attendants-distributions.sol", "r").read()
        outliers = open("sim-params/attendants-outliers.sol", "r").read().split(header)[1:]
        file = file.split(header + "\n")
        file.pop(0)
        title_re = re.compile("Test for (.*) for service (.*)\n")
        dist_re = re.compile("[0-9]*. (.*)[ ]*DO NOT REJECT\n")
        params_re = re.compile("\t\tParameters[ ]* \[(.*)\]\n")

        norm_re = re.compile("mean = (.*) desv = (.*)\n")
        for page in file:
            page_aux = page.replace(". USED RANDOM SAMPLING.", "")
            name, service = title_re.findall(page_aux)[0]
            if "Not enough data." in page_aux:
                for page_out in outliers:
                    name_out, service_out = title_re.findall(page_out)[0]
                    if name_out == self.name and service == service_out:
                        params = list(map(lambda x: float(x), norm_re.findall(page_out)[0]))
                        self.distributions[service] = ['norm', params]
                        break
            else:
                if self.name == name:
                    dist = 0
                    while True:
                        try:
                            dist0 = dist_re.findall(page_aux)[dist].replace(" ", "")
                            params = params_re.findall(page_aux)[dist].split(",")
                            params = list(map(lambda x: float(x.replace(" ", "")), params))
                            self.distributions[service] = [dist0, params]
                            self.get_time(service)
                            break
                        except ValueError:
                            dist += 1
                        except IndexError:
                            break

    # Get distribution for inter service time
    def get_data0(self):
        pages = open("sim-params/inter-services-distributions.sol", "r").read().split(header)[1:]
        title_re = re.compile("Test for (.*)\n")
        dist_re = re.compile("[0-9]*. (.*)[ ]*DO NOT REJECT\n")
        params_re = re.compile("\t\tParameters[ ]* \[(.*)\]\n")
        for page in pages:
            page = page.replace(". USED RANDOM SAMPLING.", "")
            name = title_re.findall(page)[0]
            if name == self.name:
                list_dist = dist_re.findall(page)
                dist = 0
                if len(list_dist) != 0:
                    while dist < len(list_dist):
                        try:
                            self.inter_distribution = list_dist[dist].replace(" ", "")
                            params = params_re.findall(page)[dist].split(",")
                            self.inter_params = list(map(lambda x: float(x.replace(" ", "")), params))
                            self.get_inter()
                            return
                        except ValueError:
                            dist += 1

                self.inter_distribution = "norm"
                self.inter_params = [0.05, 0]

                return

    # Generates a service time given a service
    def get_time(self, service):
        if service in self.distributions:
            distribution, params = self.distributions[service]
        else:
            distribution, params = self.distributions[list(self.distributions.keys())[0]]
        dist = getattr(st, distribution)
        loc = params[-2]
        scale = params[-1]
        if len(params) > 2:
            args = params[:-2]
            t = dist.rvs(*args, loc=loc, scale=scale)
        else:
            t = dist.rvs(loc=loc, scale=scale)
        return t

    # Generates an inter service time
    def get_inter(self):
        distribution = self.inter_distribution
        params = self.inter_params

        dist = getattr(st, distribution)
        loc = params[-2]
        scale = params[-1]
        if len(params) > 2:
            args = params[:-2]
            t = dist.rvs(*args, loc=loc, scale=scale)
        else:
            t = dist.rvs(loc=loc, scale=scale)
        return t

    # Add priority
    def add_priority(self, day, hour, priority):
        if day not in self.priorities:
            self.priorities[day] = {}

        self.priorities[day][hour] = priority

    # True if available
    def available(self):
        return self.available0

    # Change state of availability
    def change_state(self):
        self.available0 = not self.available0

    # String representation
    def __str__(self):
        return self.name


class Manager:
    class Turn:
        def __init__(self, time, attendant, customer):
            self.time = time
            self.attendant = attendant
            self.customer = customer

    def __init__(self, seed, inter_service=True):
        # Days of week
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        # Customers distributions
        self.customers = {}
        for key in self.days:
            self.customers[key] = []

        # Quitter probability
        self.quit = {False: 0.0, True: 0.0}

        # Services probability and correspondent ID
        self.service = {}
        self.id_service = {}

        # Modules
        self.attendants_day = {}
        for key in self.days:
            self.attendants_day[key] = []

        self.all_attendants = []

        # Create data
        self.create_customers()
        self.create_attendants_and_modules()
        self.get_prob()

        # Store queues and more
        self.queues = {}
        self.attendants = []
        self.start = []
        self.finish = []
        self.customer = Customers.Customer(0, False, 0, 0)
        self.timer = 0
        self.previous = 0
        self.index = 0
        self.inter_service = inter_service

        # Store output of simulation
        self.data = []

        self.seed = seed
        np.random.seed(self.seed)

    # Create all customers
    def create_customers(self):
        file = open("sim-params/inter-time-distributions.sol", "r").read()
        regex = re.compile("Test for (.*) [0-9]+, hour (.*)\n")
        day_hours = list(map(lambda x: (x[0], int(x[1])), regex.findall(file)))
        for day_hour in day_hours:
            self.customers[day_hour[0]].append(Customers(*day_hour))

    # Create all attendants and modules for distribution
    def create_attendants_and_modules(self):
        file = open("sim-params/priorities-names.sol", "r").read()
        services_re = re.compile("(.*) # (.*)\n")
        services = services_re.findall(file)
        for service in services:
            if ";" in service[1]:
                service1 = service[1].split(";")
                self.id_service[service1[0]] = service[0]
                self.id_service[service1[1]] = service[0]
            else:
                self.id_service[service[1]] = service[0]

        file = open("sim-params/open-modules.sol", "r").read()
        pages = file.split(header)[1:]
        title_re = re.compile("Modules for (.*) [0-9]+, hour (.*)\n")
        modules_re = re.compile("(.*): (.*) [A-Za-z]+?\n")
        names_re = re.compile("\t\t(.*)\n")
        for page in pages:
            day, hour = title_re.findall(page)[0]
            ans_regex = modules_re.findall(page)
            names = names_re.findall(page)
            index = 0
            attendants_per_hour = []
            for ans in ans_regex:
                quantity, priorities = ans
                priorities = priorities.split(",")
                aux = []
                for i in range(len(priorities)):
                    priority = priorities[i]
                    for key in self.id_service:
                        if priority == self.id_service[key]:
                            aux.append(key)
                priorities = aux
                for i in range(index, index + int(quantity)):
                    if names[i] not in map(lambda x: x.name, self.all_attendants):
                        attendant = Attendants(names[i])
                        self.all_attendants.append(attendant)
                    else:
                        attendant = list(filter(lambda x: x.name == names[i], self.all_attendants))[0]
                    attendants_per_hour.append(attendant)
                    if day == "Saturday":
                        time0 = 7
                    else:
                        time0 = 6
                    attendant.add_priority(day, int(hour) - time0, priorities)
                index += int(quantity)
            self.attendants_day[day].append(attendants_per_hour)

    def create_low_white_box(self):
        file = open("sim-params/priorities-names.sol", "r").read()
        services_re = re.compile("(.*) # (.*)\n")
        services = services_re.findall(file)
        for service in services:
            if ";" in service[1]:
                service1 = service[1].split(";")
                self.id_service[service1[0]] = service[0]
                self.id_service[service1[1]] = service[0]
            else:
                self.id_service[service[1]] = service[0]
        hours = list(range(0, 14))
        hours0 = list(range(0, 7))
        attendant = Attendants("sceballos")
        self.all_attendants.append(attendant)
        for day in self.days:
            if day == "Saturday":
                hour = hours0
            else:
                hour = hours

            for h in hour:
                attendant.add_priority(day, h, list(self.id_service.keys()))
                self.attendants_day[day].append([attendant])

    # Get service and quitters probability
    def get_prob(self):
        # Get service probability
        file = open("sim-params/service-probability.sol", "r").read()
        regex = re.compile("[A-Za-z]*[ ]*0.(.*)\n")
        values = list(map(lambda x: float("0." + x), regex.findall(file)))
        splitted = file.split("\n")
        for i in range(len(splitted) - 1):
            line = splitted[i].replace(str(values[i]), "")
            line = list(filter(lambda x: len(x) != 0, line.split(" ")))
            self.service[" ".join(line)] = values[i]

        # Get quitters probability
        file = open("sim-params/quitters-probability.sol").read()
        regex = re.compile("[A-Za-z]*[ ]*0.(.*)\n")
        values = list(map(lambda x: float("0." + x), regex.findall(file)))
        self.quit[False] = values[0]
        self.quit[True] = values[1]

    # Create clean data
    def empty_data(self, num_trials):
        data_trial = []
        for i in range(num_trials):
            data = {}
            for key in self.days:
                data[key] = {}
                for key0 in self.service:
                    data[key][key0] = []
            data_trial.append(data)
        self.data = data_trial

    # Fix empty data
    def fill_empty_data(self):
        for elem in self.data:
            for key in elem:
                for key0 in elem[key]:
                    if len(elem[key][key0]) == 0:
                        elem[key][key0] = [0]

    # Restarts queues
    def restart_queues(self):
        for key in self.id_service:
            self.queues[key] = deque()

    # Restart simulation
    def initialize_simulation(self, day):
        self.restart_queues()

        # Reset attendants occupation
        self.index = 0
        self.previous = 0
        self.timer = 0
        self.spawn_attendants(day)
        self.start = []
        self.finish = []

        # Spawn first customer
        self.spawn_customer(day, 0)
        self.timer = self.customer.arrival

    # Get string hour
    def get_str_hour(self, initial_hour):
        hour = (initial_hour[0] + int(self.timer / 60), initial_hour[1] + int(self.timer % 60))
        if hour[1] < 10:
            str_hour1 = "0" + str(hour[1])
        else:
            str_hour1 = str(hour[1])
        return str(hour[0]) + ":" + str_hour1

    # Update timer
    def update_timer(self):
        if len(self.start) != 0:
            times0 = min(self.start, key=lambda x: x.time).time
        else:
            times0 = self.customer.arrival
        if len(self.finish) != 0:
            times1 = min(self.finish, key=lambda x: x.time).time
        else:
            times1 = self.customer.arrival
        self.timer = min(times0, times1, self.customer.arrival)

    # Get next customer
    def next_customer(self, day):
        if self.customer.quit:
            non_empty_queues = list(filter(lambda x: len(self.queues[x]) > 0, self.queues))
            if len(non_empty_queues) == 0:
                self.customer.quit = False
        self.queues[self.customer.type].append(self.customer)

        # Spawn next customer
        self.spawn_customer(day, int(self.timer / 60))
        self.index += 1

    # Get next set of attendants
    def next_attendants(self, day, day_min):
        if self.timer <= day_min and int(self.timer / 60) != self.previous:
            self.spawn_attendants(day)
            self.previous = int(self.timer / 60)

    # Start services
    def start_services(self, show, str_hour, day_min):
        for start_call in self.start:
            if not start_call.customer.quit and start_call.time == self.timer:
                if show:
                    print(head + start_call.attendant.name, " started attending", str(start_call.customer),
                          "at", str_hour + "." + end)
                self.start.remove(start_call)
                next0 = self.timer + start_call.attendant.get_time(start_call.customer.type)
                if next0 <= day_min:
                    start_call.time = next0
                    self.finish.append(start_call)
                else:
                    start_call.attendant.change_state()
            elif start_call.customer.quit and start_call.time == self.timer:
                self.start.remove(start_call)
                start_call.attendant.change_state()
                if show:
                    print(red + str(start_call.customer), "abandoned at ", self.timer, end)

    # Finish services
    def finish_services(self, show, str_hour):
        for finish_call in self.finish:
            if finish_call.time == self.timer:
                if show:
                    print(green + finish_call.attendant.name, " finished attending", str(finish_call.customer),
                          "at", str_hour + "." + end)
                self.finish.remove(finish_call)
                finish_call.attendant.change_state()
                break

    # Move to attend customers based on priority
    def attend_priorities(self, day, day_min, data):
        priority = 0
        cont = True
        while cont and sum(map(lambda x: len(self.queues[x]), self.queues)) != 0:
            cont = False
            for attendant in self.attendants:
                if attendant.available():
                    if priority >= len(attendant.priorities[day][int(self.timer / 60)]):
                        continue
                    else:
                        str_service = attendant.priorities[day][int(self.timer / 60)][priority]
                        queue = self.queues[str_service]
                        cont = True
                        if len(queue) != 0:
                            customer = queue.popleft()

                            if self.inter_service:
                                next0 = self.timer + attendant.get_inter()
                                if next0 <= day_min:
                                    if next0 - customer.arrival > 0:
                                        data[str_service].append(next0 - customer.arrival)
                                    attendant.change_state()
                                    self.start.append(Manager.Turn(next0, attendant, customer))
                            else:
                                next0 = self.timer + attendant.get_time(customer.type)
                                if next0 <= day_min:
                                    if next0 - customer.arrival > 0:
                                        data[str_service].append(next0 - customer.arrival)
                                    attendant.change_state()
                                    self.finish.append(Manager.Turn(next0, attendant, customer))
                            continue
            priority += 1

    # Attend customers in queue based on attendants availability
    def attend_leftovers(self, day_min, data):
        available = list(filter(lambda x: x.available(), self.attendants))
        people_in_queue = sum(map(lambda x: len(self.queues[x]), self.queues))
        if people_in_queue != 0 and len(available) != 0:
            non_empty_queues = list(map(lambda x: self.queues[x],
                                        filter(lambda x: len(self.queues[x]) != 0, self.queues)))
            num = min(len(available), people_in_queue)
            customers = []
            for queue in non_empty_queues:
                while len(queue) > 0:
                    customers.append(queue.popleft())
                customers = list(sorted(customers, key=lambda x: x.arrival))
                for i in range(len(customers) - 1, num - 1, -1):
                    customer = customers[i]
                    self.queues[customer.type].appendleft(customer)
                customers = customers[:num]
                attendants = np.random.choice(available, size=num, replace=False)

                i = 0
                for customer in customers:
                    if self.inter_service:
                        next0 = self.timer + attendants[i].get_inter()
                        if next0 <= day_min:
                            attendants[i].change_state()
                            self.start.append(Manager.Turn(next0, attendants[i], customer))
                            if next0 - customer.arrival > 0:
                                data[customer.type].append(next0 - customer.arrival)
                    else:
                        next0 = self.timer + attendants[i].get_time(customer.type)
                        if next0 <= day_min:
                            attendants[i].change_state()
                            self.start.append(Manager.Turn(next0, attendants[i], customer))
                            if next0 - customer.arrival > 0:
                                data[customer.type].append(next0 - customer.arrival)
                    i += 1

    # Spawn customer
    def spawn_customer(self, day, hour):
        customer = self.customers[day][hour]
        time = customer.get_arrival()
        r1 = np.random.random()
        accumulator = 0
        quitter = False
        for key in self.quit:
            accumulator += self.quit[key]
            if r1 < accumulator:
                quitter = key
                break

        r2 = np.random.random()
        accumulator = 0
        type_customer = ""
        for key in self.service:
            accumulator += self.service[key]
            if r2 < accumulator:
                type_customer = key
                break

        self.customer = Customers.Customer(type_customer, quitter, self.index, self.timer + time)

    # Spawn set of attendants
    def spawn_attendants(self, day):
        self.attendants = self.attendants_day[day][int(self.timer / 60)]

    # Print attendants
    def print_attendants(self, day):
        print("Attendants available:")
        i = 1
        for attendant in self.attendants:
            print(str(i) + ".", attendant.name, attendant.priorities[day][int(self.timer/60)])
            i += 1
        print("\n")

    # Runs simulation for a several number of trials
    def run(self, num_trials=1, show=False, pause=False):
        self.empty_data(num_trials)
        # Run simulation
        for i in range(num_trials):
            if show:
                print(header)
                print(bold + "Trial " + str(i + 1) + end)

            # Run simulation for each day
            for day in self.days:
                self.simulation(day, self.data[i][day], show=show, pause=pause)
            if show:
                print()

        # Fill empty data
        self.fill_empty_data()

    # Simulation per day
    def simulation(self, day, data, show=False, pause=False):
        day_min0 = (13 * 60, 6 * 60)

        if day == "Saturday":
            day_min = day_min0[1]
            initial_hour = (7, 0)
        else:
            day_min = day_min0[0]
            initial_hour = (6, 0)

        # Reset queues for each day
        self.initialize_simulation(day)
        if show:
            print(bold + "Starting simulation for", day + end)

        # Simulation for each day
        self.index = 1
        while self.timer <= day_min:
            # Print hour
            str_hour = self.get_str_hour(initial_hour)

            # Spawn customer
            if self.customer.arrival == self.timer:
                if show:
                    print(blue + str(self.customer), "of type", self.customer.type, "arrived at", str_hour + end)
                self.next_customer(day)
            else:
                self.start_services(show, str_hour, day_min)
                self.finish_services(show, str_hour)

            # Select time to start attention for desired priorities
            self.attend_priorities(day, day_min, data)
            self.attend_leftovers(day_min, data)

            # Update timer
            self.update_timer()

            # Update attendants
            self.next_attendants(day, day_min)
            if pause:
                input()
        if show:
            print()

    def number_of_runs(self, alpha=0.05, delta=0.1, n0=5):
        ns = {}
        for key in self.service:
            ns[key] = n0
        cont = True
        while cont:
            z = st.t.ppf(1 - alpha / 2, n0 - 1)
            cont = False
            print(bold + "Starting trial for n =", n0, end)
            self.run(num_trials=n0)
            print(green + "Finished successfully!" + end)
            for i in range(len(self.data)):
                trial = self.data[i]
                aux = {}
                for key in trial:
                    for key0 in trial[key]:
                        if key0 in aux:
                            aux[key0] += trial[key][key0]
                        else:
                            aux[key0] = trial[key][key0]
                self.data[i] = aux
            means = {}
            for trial in self.data:
                for key in trial:
                    mean = np.mean(trial[key])
                    if key in means:
                        means[key].append(mean)
                    else:
                        means[key] = [mean]
            for key in means:
                n_prev = ns[key]
                ns[key] = math.ceil((np.std(means[key], ddof=1) * z / delta) ** 2)
                if ns[key] > n_prev:
                    if ns[key] > n0:
                        n0 = ns[key]
                        print(head + "Changing n0 to", n0, end)
                    cont = True
            print()
        return ns

    def print_output(self, num_trials=5, show=False, data=None, name="average-output.res"):
        if data is None:
            # Print output in file
            self.run(num_trials=num_trials)
            data = self.data.copy()
            data0 = data.pop()
            for d in data:
                for key in d:
                    for key0 in d[key]:
                        data0[key][key0] += d[key][key0]
            data = data0
        file = open("outputs/" + name, "w")
        for key in data:
            if show:
                print(header)
                print(bold + "Statistics for " + key + "." + end)
            file.write(header + "\n")
            file.write("Statistics for " + key + ".\n")
            data_day = data[key]
            for key0 in data_day:
                if show:
                    print(blue + "Type " + key0 + "." + end)
                file.write("Type " + key0 + ".\n")
                waiting = data_day[key0]
                mean = float(np.mean(waiting))
                std = float(np.std(waiting, ddof=1))

                if show:
                    print("Average waiting time: " + str(round(mean, 3)))
                    print("Standard deviation waiting time: " + str(round(std, 3)))
                file.write("Average waiting time: " + str(round(mean, 3)) + "\n")
                file.write("Standard deviation waiting time: " + str(round(std, 3)) + "\n\n")

                if show:
                    print()
            if show:
                print()
        file.close()

    def test_homogeneity(self):
        real_data = DataSet().waiting_time()

        sim_data = self.data
        data0 = sim_data.pop()
        for d in sim_data:
            for key in d:
                for key0 in d[key]:
                    data0[key][key0] += d[key][key0]
        sim_data = data0

        da = DataAnalysis()
        for key in real_data:
            for key0 in real_data[key]:
                data = [real_data[key][key0], sim_data[key][key0]]
                title = "Test for " + key + ", for type " + key0
                da.set_data(data)
                da.homogeneity_test(signal=True, plot=True, write=True,
                                    name_file="outputs/validation.res", title=title)

    def sensitivity_analysis(self):
        datas = []
        for i in range(-10, 11, 1):
            perc = 1 + i/100
            title_re = re.compile("Test for (.*) for service (.*)\n")
            norm_re = re.compile("mean = (.*) desv = (.*)\n")
            file = open("sim-params/attendants-outliers.sol", "r").read().split(header)[1:]
            for page in file:
                name, service = title_re.findall(page)[0]

                mean, desv = norm_re.findall(page)[0]
                mean = perc * float(mean)
                desv = float(desv)

                attendant = list(filter(lambda x: x.name == name, self.all_attendants))[0]
                attendant.distributions[service][1] = [mean, desv]
            self.run(num_trials=1, show=True)
            data_f = []
            for key in self.data[0]:
                data_f += self.data[0][key]["Farmacia General"]
            datas.append(np.mean(data_f))
        return datas

    def output(self, matrix):
        attendants = self.attendants_day["Monday"][0]
        i = 0
        for attendant in attendants:
            aux = []
            for elem in matrix[i]:
                for key in self.id_service:
                    if self.id_service[key] == elem:
                        aux.append(key)
            attendant.priorities["Monday"][0] = aux
            i += 1
        self.run(num_trials=1)
        data_f = []
        for key in self.data[0]:
            data_f += self.data[0][key]["Farmacia General"]

        return np.mean(data_f)

    def optimization(self):
        attendants = self.attendants_day["Monday"][0]
        matrix = []
        for attendant in attendants:
            prs = attendant.priorities["Monday"][0]
            priorities = []
            for pr in prs:
                if self.id_service[pr] not in priorities:
                    priorities.append(self.id_service[pr])
            matrix.append(priorities)

        best, zs = vnd(matrix)
        for row in best:
            print(row)

        x = np.linspace(0, len(zs) - 1, len(zs))
        plt.plot(x, zs)
        plt.savefig("opti.pdf", bbox_inches='tight')
        plt.show()


m = Manager(2**32 - 1, inter_service=True)


# In-Route
def swap_in_route(array, z, p=0.015):
    best_i = None
    best_j = None
    for pri in array:
        for i in range(len(pri) - 1):
            for j in range(i, len(pri)):
                if random.random() < p:
                    pri[i], pri[j] = pri[j], pri[i]
                    new_z = m.output(array)  # Objective function
                    if new_z < z:
                        z = new_z
                        best_i = i
                        best_j = j
                    pri[i], pri[j] = pri[j], pri[i]

            if best_i is not None:
                pri[best_i], pri[best_j] = pri[best_j], pri[best_i]
                best_i = None
                best_j = None
    return array, z


def move_in_route(array, z, p=0.015):
    best_i = None
    best_j = None
    for pri in array:
        for i in range(len(pri)):
            for j in range(len(pri)):
                if random.random() < p:
                    pri.insert(i, pri.pop(j))
                    new_z = m.output(array)  # Objective function
                    if new_z < z:
                        z = new_z
                        best_i = i
                        best_j = j
                    pri.insert(i, pri.pop(j))

            if best_i is not None:
                pri.insert(best_i, pri.pop(best_j))
                best_i = None
                best_j = None
    return array, z


# Inter-Route
def swap_inter_route(array, z, p=0.01):
    best_pri = None
    best_i = None
    best_j = None
    for s in range(len(array)):
        source_pri = array[s]
        for i in range(len(source_pri)):
            for o in range(s, len(array)):
                obj_pri = array[o]
                for j in range(len(obj_pri)):
                    if random.random() < p:
                        source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]

                        from_obj_in_source = [y for y, x in enumerate(source_pri) if x == obj_pri[j]]
                        from_source_in_obj = [y for y, x in enumerate(obj_pri) if x == source_pri[i]]

                        if len(from_obj_in_source) > 1:
                            rnd = random.randint(0, 2)
                            index_pop_source = from_obj_in_source[rnd]
                            elem_pop_source = source_pri[index_pop_source]
                            source_pri.pop(index_pop_source)

                        if len(from_source_in_obj) > 1:
                            rnd = random.randint(0, 2)
                            index_pop_obj = from_source_in_obj[rnd]
                            elem_pop_obj = source_pri[index_pop_obj]
                            obj_pri.pop(index_pop_obj)

                        new_z = m.output(array)  # Objective function
                        if new_z < z:
                            z = new_z
                            best_i = i
                            best_j = j
                            best_pri = o
                        else:
                            if not len(from_source_in_obj) == 2 and not len(from_source_in_obj) == 2:
                                source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]
                            else:
                                if len(from_source_in_obj) == 2:
                                    obj_pri.insert(index_pop_obj, elem_pop_obj)
                                if len(from_obj_in_source) == 2:
                                    source_pri.insert(index_pop_source, elem_pop_source)
                                source_pri[i], obj_pri[j] = obj_pri[j], source_pri[i]

            if best_i is not None:
                obj_pri = array[best_pri]
                source_pri[best_i], obj_pri[best_j] = obj_pri[best_j], source_pri[best_i]

    return array, z


def vnd(array, max_it=5):
    i = 0
    z = m.output(array)
    zs = [z]
    while i <= max_it:
        print("Starting iteration", i)
        array, z = swap_in_route(array, z)
        r = random.randint(0, 2)
        if r == 1:
            print("Making swap and move.")
            array, z = swap_in_route(array, z)
            array, z = move_in_route(array, z)
        else:
            print("Making move and swap")
            array, z = move_in_route(array, z)
            array, z = swap_in_route(array, z)
        print("Finish iteration!")
        i += 1
        zs.append(z)
    return array, zs


m.run(num_trials=1, show=True)
