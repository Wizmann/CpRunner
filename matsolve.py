import numpy as np

n = int(raw_input())

A = []
B = []
for i in xrange(n):
    line = map(float, raw_input().split())
    A.append(line[:-1])
    B.append(line[-1])

A = np.mat(A)
B = np.array(B)

x = np.linalg.solve(A, B)

for i, num in enumerate(x):
    print i, num

