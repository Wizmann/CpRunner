# CpRunner

Code runner for Competitive Programming

## Environment

OS: Linux, WSL on Windows, macOS(not tested)

Dependencies: Python3

## How to use

CpRunner is a python script to help compile and run code with customized tests within the code.

You can add a multiple line comments to write all the test cases so that you can run multiple tests by a simple command and boost the correctness of your code.

The syntax is simple, `^^^TEST^^^` is the beginning of one test case, and `$$$TEST$$$` is the end. Delimeter `---` is used to seperate the input and output string.

For example,

```python
a, b = map(int, raw_input().split())
print a + b

'''
^^^TEST^^^
1 2
---
3
$$$TEST$$$
'''
```

Currently, CpRunner supports C++ and Python2/3. Adding new language support could be super easy.

> Ocaml and F# will not be supported because some strange reasons. I mean it!

## Python2/3 and Pypy2/3

You can add `#!/usr/bin/python2` or `#!/usr/bin/python3` to the first line of your code file to let CpRunner to choose the version of python interpreter you want to use.

`#!/usr/bin/pypy` and `#!/usr/bin/pypy3` is for Pypy.

Actually, CpRunner only matches the first part (i.e. `#!`) and the last part(i.e. `python2` or `pypy3`). It means you can arbitrarily change the path of interpreter.
