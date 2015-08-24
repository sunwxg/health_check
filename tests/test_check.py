#from nose.tools import *
import os
from _pytest.monkeypatch import *
from healthcheck.check import *


def test_check_ioexp(monkeypatch):
    ioexp = [
    "<ioexp;",
    "EXCHANGE IDENTITY DATA",
    "",
    "IDENTITY",
    "BEIMSC 141/00/00/1  148",
    "",
    "END"
    ]

    inputs = ioexp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        assert check_ioexp('<ioexp;') == ['EXCHANGE IDENTITY: BEIMSC']
    except StopIteration:
        return

def test_check_dpwsp_ok(monkeypatch):
    dpwsp = [
    "<dpwsp;",
    "CP STATE",
    "",
    "MAU  SB SBSTATE      RPH-A       RPH-B       BUA STATE",
    "NRM  B  WO           -           -                   1",
    "",
    "END",
    ]

    inputs = dpwsp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        assert check_dpwsp('<dpwsp;') == ['CP STATE: OK']
    except StopIteration:
        return

def test_check_dpwsp_fail(monkeypatch):
    dpwsp = [
    "<dpwsp;",
    "CP STATE",
    "",
    "MAU  SB SBSTATE      RPH-A       RPH-B       BUA STATE",
    "ARM  B  HALT           -           -                   1",
    "",
    "END",
    ]

    inputs = dpwsp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        assert check_dpwsp('<dpwsp;') == ['CP STATE: FAIL: ARMHALT']
    except StopIteration:
        return
