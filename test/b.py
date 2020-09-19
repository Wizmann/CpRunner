INF = 10 ** 10

def numToChar(x):
    if 0 <= x <= 9:
        return str(x)
    else:
        return 'ABCDEF'[x - 10]

def getNum(res, n):
    first = True
    digits = ''
    for i in xrange(n - 1, -1, -1):
        if res[i]:
            first = False
        if not first:
            digits += numToChar(res[i])
    return digits

assert numToChar(10) == 'A'
assert numToChar(15) == 'F'

n = int(raw_input())
ns = []
for i in xrange(n):
    ns.append(int(raw_input()))
ns = ns[::-1]
ns.append(INF)

res = [0 for i in xrange(n + 1)]

while res[n] == 0:
    res[0] += 1
    g = 0
    for i in xrange(n + 1):
        res[i] += g
        g = 0
        if res[i] >= ns[i]:
            g = res[i] / ns[i]
            res[i] %= ns[i]
        if g == 0:
            break
    if res[n] == 0:
        print getNum(res, n)

'''
^^TEST^^
1
10
---
1
2
3
4
5
6
7
8
9
$$TEST$$
^^TEST^^
1
2
---
1
$$$$TEST$$$$
^^^TEST^^
2
5
3
---
1
2
10
11
12
20
21
22
30
31
32
40
41
42
$$$TEST$$
'''
