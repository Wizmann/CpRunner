#!/usr/bin/python3
#coding=utf-8

import os
import sys
import re
import time
import subprocess
import resource

class IExecutor(object):
    def compile(self, src):
        pass

    def run(self, input_data, output_data):
        t1 = time.time()
        p = subprocess.Popen(self.exe, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        output = p.communicate(input=input_data.decode())[0]
        t2 = time.time()
        p.wait()
        mem = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        if output.strip() == output_data.strip().encode():
            return True, output, t2 - t1, mem
        else:
            return False, output, t2 - t1, mem

    def get_exe_path(self, src):
        for ext in self.EXTS:
            if src.endswith(ext):
                return './' + src[:-len(ext)] + ".out"
        else:
            assert False

class CppExecutor(IExecutor):
    EXTS = [".cc", ".cpp", ".cxx"]
    def compile(self, src):
        self.exe = self.get_exe_path(src)
        os.system("g++ -g --std=c++11 %s -o %s" % (src, self.exe))

class PythonExecutor(IExecutor):
    EXTS = [".py", ".py2"]

    def compile(self, src):
        self.exe = self.get_exe_path(src)

    def get_exe_path(self, src):
        return ["python2", src]

class Python3Executor(IExecutor):
    EXTS = [".py3"]

    def compile(self, src):
        self.exe = self.get_exe_path(src)

    def get_exe_path(self, src):
        return ["python3", src]

class Parser(object):
    START_TAG = "^\^+test\^+$"
    END_TAG = "^\$+test\$+$"
    TEST_DELIMETER = "-+"

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
        elif self.color == 'voilet':
            return CVIOLET + CBOLD + self.text + CEND
        elif self.color == 'beige':
            return CBEIGE + CBOLD + self.text + CEND

if __name__ == '__main__':
    executors = [CppExecutor(), PythonExecutor(), Python3Executor()]

    src = sys.argv[1]
    ext = get_file_ext(src)

    cur_executor = None

    for executor in executors:
        if ext in executor.EXTS:
            cur_executor = executor
            break
    else:
        print('No available executor for file: %s' % src)

    cur_executor.compile(src)

    cases = Parser().parse(src)
    for i, (input_data, output_data) in enumerate(cases):
        result, actual, t, mem = cur_executor.run(input_data, output_data)
        if result:
            print('Case %d: %s, time:%d(ms), mem:%.1f(MB)' % (i, ColorText("passed", 'green'), int(t * 1000), 1.0 * mem / 1024))
        else:
            print('Case %d: %s, time:%d(ms), mem:%.1f(MB)' % (i, ColorText("failed", 'red'), int(t * 1000), 1.0 * mem / 1024))
            print('**Excepted**')
            print(output_data)
            print('**Actual**')
            print(actual.decode())


