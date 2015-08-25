import re
from string import strip

def get_input():
    try:
        return raw_input()
    except EOFError:
        exit()


#<ioexp;
#EXCHANGE IDENTITY DATA

#IDENTITY
#BEIMSC 141/00/00/1  148

#END
def check_ioexp(input_str):
    output_str = ['#EXCHANGE IDENTITY: ']
    while True:
        input_str = strip(get_input())

        if input_str == 'IDENTITY':
            input_str = strip(get_input()).split(" ")[0]
            output_str[0] += input_str

        elif input_str == 'END':
            return output_str


#<dpwsp; 
#CP STATE
#
#MAU  SB SBSTATE      RPH-A       RPH-B       BUA STATE
#NRM  B  WO           -           -                   1
#
#END
def check_dpwsp(input_str):
    output_str = ['#CP STATE: ']
    while True:
        input_str = strip(get_input()).split()
        if len(input_str) == 0:
            continue

        if input_str[0] == 'MAU':
            input_str = strip(get_input()).split()
            if (input_str[0] == 'NRM') and (input_str[2] == 'WO'):
                output_str[0] += 'OK' 
            else:
                output_str[0] += 'FAIL: '+ input_str[0] + ' ' + input_str[2]

        elif input_str[0] == 'END':
            return output_str


#<allip:acl=a2;
#ALARM LIST
#
#A2/APT "BEIMSC 141/00/0" 870 140905   0116      
#MT IMEI SUPERVISION LOG FAULT
#
#LOG
#GREY
#
#END
def check_allip(input_str):
    output_str = ['#CP ALARM: ']
    state = 'OK'

    while True:
        input_str = strip(get_input()).split()
        if len(input_str) == 0:
            continue

        if re.search(r"APZ", input_str[0]):
            state = 'FAIL' 
            alarm_str = '\t' + input_str[0] + ": "
            input_str = strip(get_input())
            output_str.append(alarm_str + input_str)

        elif input_str[0] == 'END':
            output_str[0] += state
            return output_str

#<apamp;
#AP MAINTENANCE DATA
#
#DIRECTORY ADDRESS DATA
#
#AP  NODE  LAN   IP               PORT  STATUS  CATEGORY
#1   A     1     192.168.169.1    14000 ACTIVE
#1   A     2     192.168.170.1    14000 PASSIVE
#1   B     2     192.168.170.2    14000 PASSIVE
#1   B     1     192.168.169.2    14000 ACTIVE
#
#AP MAINTENANCE TABLE
#
#AP  IO    ACTIVENODE  LOCALIP1          LOCALIP2
#1   YES   A           192.168.169.57    192.168.170.57
#
#END
def check_apamp(input_str):
    output_str = ['#AP MAINTENANCE DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"FAULTY", input_str):
            state = 'FAIL' 
            output_str.append('\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str
