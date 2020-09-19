n = int(raw_input())
ns = map(int, raw_input().split())

print(reduce(lambda x, y: x ^ y, ns))

'''
^^TEST^^
9
2 2 1 3 3 3 2 3 1
---
2
$$TEST$$

^^TEST^^
1
1
---
1
$$TEST$$

^^TEST^^
3
1 1 2
---
2
$$TEST$$
'''

