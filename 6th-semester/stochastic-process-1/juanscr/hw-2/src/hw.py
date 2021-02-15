import warnings
import datetime
from scipy import stats
warnings.filterwarnings('ignore')

import pandas


def duration(time1, time2):
    if time1.hour > time2.hour:
        time1, time2 = time2, time1
    min1 = time1.minute + time1.second/60
    min2 = time2.minute + time2.second/60
    min2 += (time2.hour - time1.hour)*60
    return min2 - min1


df = pandas.read_excel(io="hw.xlsx").to_numpy().flatten()
times0 = []
times = []
time_before = 0
for i in range(df.shape[0]):
    value = df[i]
    if i == df.shape[0] - 1:
        times0.append(value)
    if i == 0:
        initial_time = datetime.time(0, 0, 0)
        times.append(duration(initial_time, value))
        times0.append(initial_time)
        time_before = value
        continue
    times.append(duration(time_before, value))
    time_before = value

lambda1 = 106 / duration(*times0)
_, p_value = stats.kstest(times, 'expon', args=(0, 1 / lambda1))
print(p_value)
print(lambda1)
print(0.075 * 60)
