from scipy.stats import kstest
from numpy import mean


def read_data():
    file = open('hw-2.csv', 'r')
    file_data = file.read()
    file_data = file_data.split('\n')
    n = len(file_data)
    for i in range(n):
        file_data[i] = file_data[i][2:]

    inter_times = [0]*n
    i = 0
    for time in file_data:
        aux = time.split(':')
        inter_times[i] = int(aux[0]) + int(aux[1])/60
        i += 1
    l = 1/mean(inter_times)
    _, pvalue = kstest(inter_times, 'expon', args=(0, 1/l))
    print(inter_times)
    print('p-value ' + str(pvalue))
    print('lambda: ' + str(l))


read_data()
