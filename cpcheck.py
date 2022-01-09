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
    
    for i in xrange(1000):
        data = subprocess.check_output(["python", gen])


