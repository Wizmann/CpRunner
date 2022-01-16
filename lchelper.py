#coding=utf-8

import six
import sys
import inspect
import json

if six.PY3:
    from typing import *

old_stdout = sys.stdout
my_stdout = six.StringIO()
sys.stdout = my_stdout

filename = sys.argv[1]

with open(filename) as solution_file:
    solution_code = solution_file.read()
    exec(solution_code)

S = Solution()
entry = sorted(
    inspect.getmembers(S, predicate=inspect.ismethod),
    key=lambda p: p[1].__code__.co_firstlineno)[0][0]

def parse_input(lines):
    args = []
    for line in lines:
        arg = json.loads(line)
        args.append(arg)
    return args

lines = [line for line in sys.stdin]

res = getattr(S, entry)(*parse_input(lines))
sys.stdout.flush()

stdout = my_stdout.getvalue()
sys.stdout = old_stdout

print(json.dumps(
    {
        'result' : json.dumps(res),
        'stdout' : stdout
    }))
