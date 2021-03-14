#!/usr/bin/python3
#coding=utf-8

import os
import sys
import shutil

exemplars_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'exemplars')

exts = [
    (['cc', 'cpp', 'cxx'], 'cpp'),
    (['py'], 'py'),
]

d = {}

for keys, value in exts:
    for key in keys:
        d[key] = value

filename = sys.argv[1]
ext = filename.split('.')[-1]

if ext in d:
    ext = d[ext]
else:
    assert False

example_file = os.path.join(exemplars_path, 'example.' + ext)
if not os.path.exists(filename):
    shutil.copy(example_file, filename)
