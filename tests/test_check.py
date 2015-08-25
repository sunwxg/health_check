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
        assert check_ioexp('<ioexp;') == ['#EXCHANGE IDENTITY: BEIMSC']
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
        assert check_dpwsp('<dpwsp;') == ['#CP STATE: OK']
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
        assert check_dpwsp('<dpwsp;') == ['#CP STATE: FAIL: ARM HALT']
    except StopIteration:
        return

def test_check_allip_ok(monkeypatch):
    allip = [
    "ALARM LIST",
    "",
    "A2/APT \"BEIMSC 141/00/0\" 870 140905   0116      ",
    "MT IMEI SUPERVISION LOG FAULT",
    "",
    "LOG",
    "GREY",
    "",
    "END",
    ]

    inputs = allip
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        assert check_allip('<allip') == ['#CP ALARM: OK']
    except StopIteration:
        return

def test_check_allip_fail(monkeypatch):
    allip = [
    "ALARM LIST",
    "",
    "A2/APZ \"BEIMSC 141/00/0\" 870 140905   0116      ",
    "MT IMEI SUPERVISION LOG FAULT",
    "",
    "LOG",
    "GREY",
    "",
    "END",
    ]

    inputs = allip
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_allip('<allip')
        assert output[0] == '#CP ALARM: FAIL'
        assert output[1] == '\tA2/APZ: MT IMEI SUPERVISION LOG FAULT'
    except StopIteration:
        return

def test_check_apamp_ok(monkeypatch):
    apamp = [
    "AP MAINTENANCE DATA",
    "",
    "DIRECTORY ADDRESS DATA",
    "",
    "AP  NODE  LAN   IP               PORT  STATUS  CATEGORY",
    "1   A     1     192.168.169.1    14000 ACTIVE",
    "1   A     2     192.168.170.1    14000 PASSIVE",
    "1   B     2     192.168.170.2    14000 PASSIVE",
    "1   B     1     192.168.169.2    14000 ACTIVE",
    "",
    "AP MAINTENANCE TABLE",
    "",
    "AP  IO    ACTIVENODE  LOCALIP1          LOCALIP2",
    "1   YES   A           192.168.169.57    192.168.170.57",
    "",
    "END",
    ]

    inputs = apamp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_apamp('<apamp')
        assert output[0] == '#AP MAINTENANCE DATA: OK'
    except StopIteration:
        return

def test_check_apamp_fail(monkeypatch):
    apamp = [
    "AP MAINTENANCE DATA",
    "",
    "DIRECTORY ADDRESS DATA",
    "",
    "AP  NODE  LAN   IP               PORT  STATUS  CATEGORY",
    "1   A     1     192.168.169.1    14000 ACTIVE",
    "1   A     2     192.168.170.1    14000 PASSIVE",
    "1   B     2     192.168.170.2    14000 FAULTY",
    "1   B     1     192.168.169.2    14000 ACTIVE",
    "",
    "AP MAINTENANCE TABLE",
    "",
    "AP  IO    ACTIVENODE  LOCALIP1          LOCALIP2",
    "1   YES   A           192.168.169.57    192.168.170.57",
    "",
    "END",
    ]

    inputs = apamp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_apamp('<apamp')
        assert output[0] == '#AP MAINTENANCE DATA: FAIL'
        assert output[1] == '\t1   B     2     192.168.170.2    14000 FAULTY'
    except StopIteration:
        return
