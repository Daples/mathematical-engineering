import simpy
import random
import math

# Variables for distributions
mean_arrival = 15

mu_fitting = 40
sigma_fitting = 10
sigma_ln = math.sqrt(math.log(sigma_fitting/mu_fitting**2 + 1))
mu_ln = math.log(mu_fitting) - sigma_ln**2/2

mu_inspection = 5
sigma_inspection = 1.5

less_re_inspection = 1
top_re_inspection = 3

mean_pay_time = 3

# Parameters for simulation
max_fitters = 2
max_ramps = 3
max_queue = 4

time_simulation = 400
seed = 4000

# Monitoring variables
nc = 0
nc_left_queue = 0
nc_decided_leave = 0
nc_re_done = 0

times_inspection = []
time_system = []

# Aesthetic
blue = '\033[94m'
green = '\033[92m'
red = '\033[91m'
end = '\033[0m'
bold = '\033[1m'
head = '\033[95m'

round_time = 4


# Manage arrivals
def str1(time):
    return str(round(time, round_time))


def source(e):
    global nc
    index = 0
    print(bold + "------------------------------" + end)
    print(head + "Joe's workshop simulation\n" + end)
    while True:
        # Arrival
        c = car(e, index)
        nc += 1
        e.process(c)

        # Next arrival
        t = random.expovariate(1.0 / mean_arrival)
        index += 1
        yield e.timeout(t)


# Car inspection
def re_inspection(e):
    # Re-inspection from Joe
    with joe.request() as reqj:
        yield reqj

        ti = random.uniform(less_re_inspection, top_re_inspection)
        yield e.timeout(ti)
        joe.release(reqj)


# Process while occupying ramp
def ramp_process(e, name, arrive):
    global nc_decided_leave
    global nc_re_done
    # Inspect car
    with joe.request() as reqj:
        yield reqj

        times_inspection.append(e.now - arrive)
        tl = random.normalvariate(mu_inspection, sigma_inspection)
        yield e.timeout(tl)
        string1 = "Joe inspected " + str(name) + " at " + str1(e.now)
        joe.release(reqj)

        decision = random.uniform(0, 1)
        if decision < 0.7:
            print(string1 + " and decided to stay.")
        else:
            print(blue + string1 + " and decided to leave." + end)
            time_system.append(e.now - arrive)
            nc_decided_leave += 1
            return

    while True:
        # Ask for Fitter
        with fitters.request() as reqf:
            # Fitting work
            yield reqf
            tf = random.lognormvariate(mu_ln, sigma_ln)

            yield e.timeout(tf)
            print(name, "finished fitting job at", str1(e.now))
            fitters.release(reqf)

        # Re inspection
        yield e.process(re_inspection(e))

        string = "Joe re-inspected " + str(name) + " at " + str1(e.now)

        # Work done
        done = random.uniform(0, 1)

        if done >= 0.1:
            print(green + string + " and is ready to leave." + end)
            break
        print(string + " and has to be re done.")
        nc_re_done += 1

    # Pay to Joe
    with joe.request() as reqj:
        yield reqj

        tp = random.expovariate(1.0 / mean_pay_time)
        yield e.timeout(tp)
        print(name, "paid Joe and left at", str1(e.now))
        time_system.append(e.now - arrive)
        joe.release(reqj)


def car(e, index):
    global nc_left_queue
    name = "Car " + str(index)

    # Arriving
    string = name + " arrived at " + str1(e.now)
    arrive = e.now

    # For queue to ramp
    with queue.request() as reqq:
        if queue.count == max_queue:
            print(red + string, "and left. Too many cars at line." + end)
            nc_left_queue += 1
            return
        print(string)
        yield reqq

        # Ramp behavior
        with ramps.request() as reqr:
            yield reqr
            queue.release(reqq)

            wait = env.now - arrive
            string = name + " is using ramp"

            if wait != 0:
                string += ", it waited " + str1(wait)
            else:
                string += "."

            print(string)

            # Process while using ramp
            yield e.process(ramp_process(e, name, arrive))

            # Released ramp and go out of system
            ramps.release(reqr)


# Simpy Environment
env = simpy.Environment()

# Random seed
random.seed(seed)

# Resources
joe = simpy.Resource(env, capacity=1)
fitters = simpy.Resource(env, capacity=max_fitters)
ramps = simpy.Resource(env, capacity=max_ramps)
queue = simpy.Resource(env, capacity=max_queue)

# Run Simulation
env.process(source(env))
env.run(until=time_simulation)

# Print statistics
print(bold + "------------------------------" + end)
print(head + "Important statistics\n" + end)

print(bold + "1. Total Number of:" + end)
print("Cars who arrived", nc)
print("Cars that left because queue", nc_left_queue)
print("Cars that left after inspection", nc_decided_leave)
print("Cars that where re done", nc_re_done)
print("")

print(bold + "2. Averages: " + end)
print("Time before inspection", sum(times_inspection)/len(times_inspection))
print("Time of costumer in system", sum(time_system)/len(time_system))
