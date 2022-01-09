#coding=utf-8

import six
import sys
import inspect
import json

old_stdout = sys.stdout
my_stdout = six.StringIO()
sys.stdout = my_stdout

filename = sys.argv[1]

if six.PY3:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
            'Solution', filename)

    solution = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solution)
elif six.PY2:
    import imp
    solution = imp.load_source('Solution', filename)
else:
    raise Exception("unexpected python version")

S = solution.Solution()
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
