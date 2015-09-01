#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
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
    'IP PORT STATE' : check_ihstp,
    'M3UA ASSOCIATION STATUS' : check_m3asp,
    'M3UA ROUTING DATA' : check_m3rsp,
    'COMMON CHARGING OUTPUT ADJUNCT PROCESSOR INTERFACE DATA' : check_chopp,
    'CCITT7 SCCP NETWORK CONFIGURATION DATA' : check_c7ncp,
    'Directory of K:/ACS/data/RTR/CHS_CP0EX/DATAFILES/REPORTED' : check_rtr_reported,
    'Directory of K:/ACS/data/RTR/billing/Ready' : check_rtr_ready,
    'LICENSE MANAGEMENT PARAMETERS FAULT LOG' : check_lmpfp,
    'SYSTEM BACKUP FILES' : check_sybfp,
    'TIME' : check_caclp,
    'alist' : check_alist,
    'cluster node' : check_cluster_node,
    'cluster res' : check_cluster_res,
    'ssuls -l' : check_ssuls,
    'vxdisk list' : check_vxdisk,
    'Directory of k:/images/Nodea' : check_images,
    'Directory of k:/images/Nodeb' : check_images,
    'altk' : check_mgw_altk,
    'lgaevsrm' : check_mgw_lgaevsrm,
    'st' : check_mgw_st_pluginunit,
    'cvls' : check_mgw_cvls,
    'pst' : check_mgw_pst,
    'vols' : check_mgw_vols,
}


def print_preline():
    print '-' * 60

def print_out(output_str):
    print_preline()
    for i in output_str:
        print i

def check_AXE_input(input_str):
    input_str = input_str.strip().split('>')
    if len(input_str) == 1:
        # CP command
        if check_list.has_key(input_str[0]):
            output_str = check_list[input_str[0]](input_str)
            print_out(output_str)
    else:
        # APG command
        if check_list.has_key(input_str[1]):
            output_str = check_list[input_str[1]](input_str)
            if (output_str[len(output_str) - 1] == True):
                # get last input from return value
                output_str.pop()
                input_str = output_str.pop()
                print_out(output_str)
                check_AXE_input(input_str)
            else:
                print_out(output_str)
    return

def check_MGW_input(input_str):
    input_str = input_str.strip().split('>')
    if len(input_str) == 2:
        input_str = input_str[1].split()
        if len(input_str) == 0:
            return

        input_str = input_str[0].strip()
        if check_list.has_key(input_str):
            output_str = check_list[input_str](input_str)
            if (output_str[len(output_str) - 1] == True):
                # get last input from return value
                output_str.pop()
                input_str = output_str.pop()
                print_out(output_str)
                check_MGW_input(input_str)
            else:
                print_out(output_str)

node = {
    'axe' : check_AXE_input,
    'mgw' : check_MGW_input,
}

def start_input():
    if len(sys.argv) == 1:
        sys.argv.append('axe')

    try:
        while True:
            input_str = raw_input().replace('\\', '/')
            node[sys.argv[1]](input_str)

    except EOFError:
        print_preline()
        exit()

if __name__ == '__main__':
    start_input()
