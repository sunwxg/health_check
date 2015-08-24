#from nose.tools import *
import os
from _pytest.monkeypatch import *
from healthcheck.check import *

ioexp = [
"<ioexp;",
"EXCHANGE IDENTITY DATA",
"",
"IDENTITY",
"BEIMSC 141/00/00/1  148",
"",
"END"
]

def test_check_ioexp(monkeypatch):
    inputs = ioexp
    input_generator = (i for i in inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        start_input()
    except StopIteration:
        return

   # check_input(i)
