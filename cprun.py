#!/usr/bin/python3
#coding=utf-8

import os
import sys
import re
import json
import time
import argparse
import subprocess
import resource

TIMEOUT = 10 # seconds
MAX_VIRTUAL_MEMORY = 1024 * 1024 * 1024
MEMORY_LIMIT = 256 * 1024 # KB

def limit_virtual_memory():
    # The tuple below is of the form (soft limit, hard limit). Limit only
    # the soft part so that the limit can be increased later (setting also
    # the hard limit would prevent that).
    # When the limit cannot be changed, setrlimit() raises ValueError.
    resource.setrlimit(resource.RLIMIT_AS, (MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

class ColorText(object):
    def __init__(self, text, color):
        self.text = text
        self.color = color

    def __str__(self):
        CEND      = '\033[0m'
        CBOLD     = '\033[1m'
        CRED    = '\033[91m'
        CGREEN  = '\033[32m'
        CYELLOW = '\033[33m'
        CBLUE   = '\033[34m'
        CVIOLET = '\033[35m'
        CBEIGE  = '\033[36m'
        if self.color == 'red':
            return CRED + CBOLD + self.text + CEND
        elif self.color == 'green':
            return CGREEN + CBOLD + self.text + CEND
        elif self.color == 'yellow':
            return CYELLOW + CBOLD + self.text + CEND
        elif self.color == 'blue':
            return CBLUE + CBOLD + self.text + CEND
        elif self.color == 'violet':
            return CVIOLET + CBOLD + self.text + CEND
        elif self.color == 'beige':
            return CBEIGE + CBOLD + self.text + CEND


class ExecutorResult(object):
    WRONG_ANSWER = ColorText("WA", 'red')
    TIME_LIMIT_EXCEEDED = ColorText("TLE", 'violet')
    ACCEPTED = ColorText("ACCPETED", 'green')
    MEM_LIMIT_EXCEEDED = ColorText("MLE", 'violet')
    RUNTIME_ERROR = ColorText("RE", 'red')

    def __init__(self, result, output, time, mem):
        self.result = result
        self.output = output
        self.time = time
        self.mem = mem

    def __str__(self):
        return '%s, time:%d(ms), mem:%.1f(MB)' % (self.result, int(self.time * 1000), 1.0 * self.mem / 1024)

    def get_output(self):
        return self.output

class IExecutor(object):
    def compile(self, src, **kwargs):
        pass

    def prettify_output(self, output):
        return output

    def run(self, input_data, expected_data):
        t1 = time.time()
        p = subprocess.Popen(self.exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False, preexec_fn=limit_virtual_memory)
        try:
            output = p.communicate(input=input_data.encode(), timeout=TIMEOUT)[0]
        except subprocess.TimeoutExpired:
            p.kill()
            mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
            return ExecutorResult(ExecutorResult.TIME_LIMIT_EXCEEDED, '', TIMEOUT, mem)
        t2 = time.time()
        mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        if mem > MEMORY_LIMIT:
            return ExecutorResult(ExecutorResult.MEM_LIMIT_EXCEEDED, '', t2 - t1, mem)
        elif p.returncode != 0:
            return ExecutorResult(ExecutorResult.RUNTIME_ERROR, '', t2 - t1, mem)
        elif self.check_output(expected_data, output):
            return ExecutorResult(ExecutorResult.ACCEPTED, output, t2 - t1, mem)
        else:
            return ExecutorResult(ExecutorResult.WRONG_ANSWER, self.prettify_output(output), t2 - t1, mem)

    def get_exe_path(self, src):
        for ext in self.EXTS:
            if src.endswith(ext):
                return './' + src[:-len(ext)] + ".out"
        else:
            assert False

    def check_output(self, expected, actual):
        actual = '\n'.join(map(lambda x: x.strip(), actual.decode('utf-8').strip().split('\n')))
        expected = '\n'.join(map(lambda x: x.strip(), expected.strip().split('\n')))
        return expected.strip() == actual.strip()

class CppExecutor(IExecutor):
    EXTS = [".cc", ".cpp", ".cxx"]
    def compile(self, src, **kwargs):
        self.exe = self.get_exe_path(src)
        if kwargs.get('fast', False):
            os.system("g++ -g -O2 -D__CPRUN__ --std=c++11 %s -o %s" % (src, self.exe))
        else:
            os.system("g++ -g -O0 -D__CPRUN__ --std=c++11 %s -o %s" % (src, self.exe))

class PythonExecutor(IExecutor):
    EXTS = [".py"]

    def compile(self, src, **kwargs):
        use_pypy = kwargs.get('fast', False)
        self.exe = self.get_exe_path(src, fast=use_pypy)

    def get_version(self, src, fast):
        # detect which type of python we will use to run the code: python2, python3, pypy2, pypy3
        DEFAULT = "python2" # LONG LIVE PYTHON2
        mapping = {
            "python": "python2",
            "python2": "python2",
            "python3": "python3",
            "pypy": "pypy",
            "pypy2": "pypy",
            "pypy3": "pypy3"
        }

        mapping_fast = {
            "python": "pypy",
            "python2": "pypy2",
            "python3": "pypy3",
            "pypy": "pypy",
            "pypy2": "pypy",
            "pypy3": "pypy3"
        }

        with open(src) as f:
            content = f.readlines()
            for key, value in mapping.items():
                pattern = r'^\#\!.*?\/' + key + '$'
                for line in content:
                    if re.match(pattern, line.strip(), re.IGNORECASE):
                        if fast:
                            value = mapping_fast[value]
                        return value
            else:
                return DEFAULT

    def get_exe_path(self, src, fast):
        version = self.get_version(src, fast)
        return [version, src]

class PythonExecutorForLeetcode(PythonExecutor):
    def compile(self, src, **kwargs):
        helper_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'lchelper.py')
        self.exe = self.get_exe_path(helper_path, src, fast=False)
        self.exe.append(src)

    def get_exe_path(self, helper, src, fast):
        version = self.get_version(src, fast)
        return [version, helper]

    def prettify_output(self, output):
        d = json.loads(output)
        res = ''
        if d.get('stdout', ''):
            res += '--- stdout ---\n'
            res += d['stdout'].strip()
            res += '\n--- output ---\n'
        res += d['result']
        return res

    def unify_output(self, output):
        return json.dumps(json.loads(output))

    def check_output(self, expected, actual):
        expected = self.unify_output(expected)
        actual = json.loads(actual)
        return expected.strip() == actual['result'].strip()

class A2BExecutor(IExecutor):
    EXTS = [".a2b"]
    def compile(self, src, **kwargs):
        self.exe = ['A2B', src]

class Parser(object):
    START_TAG = "^\^+test\^+$"
    END_TAG = "^\$+test\$+$"
    TEST_DELIMETER = "---+"

    STATUS_UNKNOWN = 0
    STATUS_INPUT = 1
    STATUS_OUTPUT = 2

    def __init__(self):
        self.cases = []

    def parse(self, src):
        current_input = ""
        current_output = ""
        status = self.STATUS_UNKNOWN
        with open(src) as src_file:
            for line in src_file:
                if re.match(self.START_TAG, line.strip(), re.IGNORECASE):
                    assert status == self.STATUS_UNKNOWN
                    assert not current_input
                    assert not current_output
                    status = self.STATUS_INPUT
                elif re.match(self.TEST_DELIMETER, line.strip(), re.IGNORECASE):
                    if status == self.STATUS_INPUT:
                        status = self.STATUS_OUTPUT
                elif re.match(self.END_TAG, line.strip(), re.IGNORECASE):
                    assert status == self.STATUS_OUTPUT
                    assert current_input
                    assert current_output
                    self.cases.append((current_input, current_output))
                    current_input = ''
                    current_output = ''
                    status = self.STATUS_UNKNOWN
                elif status == self.STATUS_INPUT:
                    current_input += line
                elif status == self.STATUS_OUTPUT:
                    current_output += line
        return self.cases

def get_file_ext(src):
    return '.' + src.split('.')[-1]

class ISanitizer(object):
    def check(self, path):
        pass

class TodoChecker(ISanitizer):
    def check(self, path):
        with open(path) as source:
            content = source.read()
            if "todo" in content.lower():
                print(ColorText("***WARNING***", 'red'))
                print(ColorText("There is one ore more \"TODO\"(s) in the source code.", 'red'))

            if "fixme" in content.lower():
                print(ColorText("***WARNING***", 'red'))
                print(ColorText("There is one ore more \"FIXME\"(s) in the source code.", 'red'))

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Code runner for competitive programming')
    argparser.add_argument('-f', '--fast', dest='fast', action='store_true')
    argparser.add_argument('-lc', '--leetcode', dest='leetcode', action='store_true')
    argparser.add_argument('-t', '--test', dest='test', type=int)
    argparser.add_argument('filename')

    argparser.set_defaults(fast=False)
    argparser.set_defaults(leetcode=False)
    argparser.set_defaults(test=-1) # -1 means run all tests

    args = argparser.parse_args()

    executors = [CppExecutor(), PythonExecutor(), A2BExecutor()]
    sanitizers = [TodoChecker()]

    src = args.filename
    ext = get_file_ext(src)

    idx = args.test

    cur_executor = None

    for executor in executors:
        if args.leetcode:
            if ext == '.py':
                cur_executor = PythonExecutorForLeetcode()
                break
        if ext in executor.EXTS:
            cur_executor = executor
            break
    else:
        print('No available executor for file: %s' % src)

    cur_executor.compile(src, fast=args.fast)

    cases = Parser().parse(src)
    for i, (input_data, output_data) in enumerate(cases):
        if idx != -1 and i != idx:
            continue
        status = cur_executor.run(input_data, output_data)
        print('Case %d: %s' % (i, status))
        if status.result == ExecutorResult.WRONG_ANSWER:
            print('**Excepted**')
            print(output_data)
            print('**Actual**')
            print(status.get_output())

    for sanitizer in sanitizers:
        sanitizer.check(src)
