#!/usr/bin/python3
#coding=utf-8

import os
import sys
import re
import time
import subprocess
import resource
import tempfile

if __name__ == '__main__':
    gen = sys.argv[1]
    ours = sys.argv[2]
    theirs = sys.argv[3]
    
    for i in range(1000):
        data = subprocess.check_output(["python2", gen])

        try:
            v1 = subprocess.check_output([ours], input=data)
            v2 = subprocess.check_output([theirs], input=data)

            v1 = list(map(float, v1.split()))
            v2 = list(map(float, v2.split()))
            n = len(v1)
            assert(len(v1) == len(v2))
            for j in range(n):
                diff = abs(v1[j] - v2[j])
                if diff > 1e9 or diff / v1[j] > 1e9 or diff / v2[j] > 1e9:
                    raise Exception()
        except:
            with open('check.err', 'wb+') as f:
                f.write(data)
            print('ERROR')
            print(data.decode('utf-8'))
            raise
        if i % 100 == 0:
            print('%d cases ... passed' % i)
    else:
        print('OK')

