from nose.tools import *
from healthcheck.check import *

ioexp = [
"<ioexp;",
"EXCHANGE IDENTITY DATA",
"",
"IDENTITY",
"BEIMSC 141/00/00/1  148",
"",
"END",
]

def test_check_ioexp():
    for i in ioexp:
        check_input(i)
