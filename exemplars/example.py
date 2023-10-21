#coding=utf-8

import sys
if sys.version_info[0] == 3:
    raw_input = input
    xrange = range
    map_ = map
    def map(*args, **kwargs):
        return list(map_(*args, **kwargs))

T = int(raw_input())

for case_ in xrange(T):
    print case_
