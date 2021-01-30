import numpy as np

data_file = open('hw-1.txt', 'r')
data = data_file.read()
data_file.close()

data = data.split('\n')
for i in range(len(data)):
    data[i] = data[i].split(' ')

n = len(data[0])
d = len(data)

counts = {'CC-CC': [0] * n, 'CC-PS': [0] * n, 'PS-PS': [0] * n, 'PS-CC': [0] * n}

# Transition Matrix
for j in range(n):
    for i in range(2, d - 1):
        if data[i - 1][j] == '"CC"':
            if data[i][j] == '"CC"':
                counts['CC-CC'][j] += 1
            else:
                counts['CC-PS'][j] += 1
        else:
            if data[i][j] == '"PS"':
                counts['PS-PS'][j] += 1
            else:
                counts['PS-CC'][j] += 1

fCC_CC = sum(counts['CC-CC'])
fCC_PS = sum(counts['CC-PS'])
fPS_PS = sum(counts['PS-PS'])
fPS_CC = sum(counts['PS-CC'])

pCC_CC = fCC_CC / (fCC_CC + fCC_PS)
pCC_PS = fCC_PS / (fCC_CC + fCC_PS)
pPS_PS = fPS_PS / (fPS_PS + fPS_CC)
pPS_CC = fPS_CC / (fPS_PS + fPS_CC)

P = np.array([[pCC_CC, pCC_PS],
              [pPS_CC, pPS_PS]])
print('Estimated P: ' + str(P))

# Stationary distribution
A = np.array([[pCC_CC - 1, pPS_CC],
              [1, 1]])
b = np.array([[0],
              [1]])

pi = np.matmul(np.linalg.inv(A), b)
print('pi: ' + str(pi))

# Steady state?
P365 = np.linalg.matrix_power(P, n)

v1 = abs(P365[0] - np.transpose(pi))
v2 = abs(P365[1] - np.transpose(pi))
v1 = np.amax(v1)
v2 = np.amax(v2)
v = max(v1, v2)
print('Total Variation: ' + str(v))

# Last question
print('Without marketing: E[Us]=' + str(365 * (2 - 1) * 100 * (10 ** 6) * pi[1]))

new_P = np.array([[pCC_CC, pCC_PS],
                  [pPS_CC - 0.05, pPS_PS + 0.05]])
print('New P: ' + str(new_P))

A = np.array([[pCC_CC - 1, pPS_CC - 0.05],
              [1, 1]])
pi = np.matmul(np.linalg.inv(A), b)
print('New pi: ' + str(pi))


print('With marketing: ' + str((365 * (2 - 1) * 100 * (10 ** 6) * pi[1]) - (500 * (10 ** 6))))