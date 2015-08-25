#!/usr/bin/python

from check_function import *
from string import strip

check_list = {
    'EXCHANGE IDENTITY DATA' : check_ioexp,
    'CP STATE' : check_dpwsp,
    'ALARM LIST' : check_allip,
    'AP MAINTENANCE DATA' : check_apamp,
    'PROCESSOR LOAD DATA' : check_plldp,
    'MT MOBILE SUBSCRIBER SURVEY' : check_mgsvp,
    'DEVICE STATE SURVEY' : check_strsp,
    'RP DATA' : check_exrpp,
    'EM DATA' : check_exemp,
    'IP PORT CONNECTION DATA' : check_ihcop,
}

def print_preline():
    print '-' * 60

def print_out(output_str):
    for i in output_str:
        print i

def check_input(input_str):
    input_str = input_str.strip()
    if check_list.has_key(input_str):
        output_str = check_list[input_str](input_str)
        print_out(output_str)

def start_input():
    print_preline()
    try:
        while True:
            input_str = raw_input()
            check_input(input_str)

    except EOFError:
        print_preline()
        exit()

if __name__ == '__main__':
    start_input()
