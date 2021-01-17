import matplotlib.pyplot as plt
import os


def read_csv(dir1, dir2, name, y_label, plot=True, save=True):
    if len(dir2) != 0:
        dirs = "../" + str(dir1) + "/" + str(dir2) + "/" + str(name)
    else:
        dirs = "../" + str(dir1) + "/" + str(name)
    file = open(dirs + ".csv", "r")
    file = file.readlines()
    i = 0
    while i < len(file):
        if file[i] == '"x","y","color","pen down?"\n':
            break
        i += 1

    x = []
    y = []
    for j in range(i+1, len(file)):
        line = file[j].split(",")
        x.append(float(line[0][1:-1]))
        y.append(float(line[1][1:-1]))
    if plot:
        plt.clf()
        plt.plot(x, y)
        plt.xlabel("Ticks")
        plt.ylabel(y_label)
        if save:
            plt.savefig(dirs + ".pdf", bbox_inches='tight')
        else:
            plt.show()
    return x, y


def format_pdf(dir1):
    dir0 = "../" + dir1
    files = os.listdir(dir0)
    for file in files:
        if os.path.isdir(dir0 + "/" + file):
            format_pdf(dir1 + "/" + file)
        else:
            if ".pdf" in file:
                dir1_test = dir1.split("/")[-1]
                os.rename(dir0 + "/" + file,
                          dir0 + "/" + dir1_test + "-" + file[:-4] + ".pdf")


def plot_sens():
    ys = []
    for num in range(90, 111):
        name = str(num) + "-diabetes"
        _,  y = read_csv("sensitivity", "", name, "", plot=False)
        ys.append(y)

    means = list(map(lambda x: sum(x[-300:]) / 300, ys))
    interval = list(map(lambda x: x / 100, range(90, 111)))
    plt.plot(interval, means)
    plt.ylim([80, 100])
    plt.xlabel("Ticks")
    plt.ylabel("Average Individuals")
    plt.savefig("../sensitivity/sensitivity-diabetes.pdf", bbox_inches='tight')


def plot_results_validation():
    to_do = [("validation", "diabetes-1", "diabetes", "Individuals"),
             ("validation", "diabetes-1", "healthy", "Individuals"),
             ("validation", "healthy-1", "healthy", "Individuals"),
             ("validation", "healthy-1", "diabetes", "Individuals"),
             ("validation", "healthy-1", "married", "Individuals"),
             ("validation", "radius-0", "bmi", "Average BMI"),
             ("validation", "radius-0", "married", "Individuals"),
             ("validation", "radius-1e6", "bmi", "Average BMI"),
             ("validation", "radius-1e6", "married", "Individuals"),
             ("validation", "population-0", "diabetes", "Individuals"),
             ("validation", "population-0", "healthy", "Individuals"),
             ("validation", "population-0", "risk", "Individuals"),
             ("results", "", "bmi", "Average BMI"),
             ("results", "", "diabetes", "Individuals"),
             ("results", "", "married", "Individuals"),
             ("results", "", "risk", "Individuals"),
             ("results", "", "healthy", "Individuals")]
    for elem in to_do:
        read_csv(*elem)
    format_pdf("")

