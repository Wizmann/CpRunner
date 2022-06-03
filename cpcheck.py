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

            if v1.strip() != v2.strip():
                raise Exception()
        except:
            with open('check.err', 'wb+') as f:
                f.write(data)
            print('ERROR')
            raise
    else:
        print('OK')

