import time
n = int(raw_input())

for i in xrange(n):
    print i
    time.sleep(0.5)

'''
^^^TEST^^^
100000000
---
...
$$$Test$$$
^^^TEST^^^
1
---
0
$$$Test$$$
^^^TEST^^^
1
---
1234
$$$Test$$$
'''

