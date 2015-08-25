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

#PROCESSOR LOAD DATA
#INT PLOAD CALIM OFFDO OFFDI FTCHDO FTCHDI OFFMPH OFFMPL FTCHMPH FTCHMPL
# 1    1   75000     3     2     3      2     15      9     15       9
# 2    1   75000     2     3     2      3     13      9     13       9
# 3    1   75000     2     4     2      4     12      5     12       5
# 4    1   75000     3     3     3      3     14      0     14       0
# 5    1   75000     3     3     3      3     17      1     17       1
# 6    1   75000     0     2     0      2     13      0     13       0
# 7    1   75000     1     6     1      6     13      1     13       1
# 8    1   75000     0     4     0      4     10      1     10       1
# 9    1   75000     1     2     1      2      9      0      9       0
#10    1   75000     3     3     3      3     17      1     17       1
#11    1   75000     7     5     7      5     15      3     15       3
#12    1   75000     2     3     2      3     18      9     18       9
#
#INT OFFTCAP FTDTCAP
# 1      0       0
# 2      0       0
# 3      0       0
# 4      0       0
# 5      0       0
# 6      0       0
# 7      0       0
# 8      0       0
# 9      0       0
#10      0       0
#11      0       0
#12      0       0
#END
def check_plldp(input_str):
    output_str = ['#PROCESSOR LOAD DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"PLOAD", input_str):
            input_str = strip(get_input()).split()
            output_str[0] += '= ' + input_str[1]

        elif input_str == 'END':
            output_str[0] += ' ' + state
            return output_str

#<mgsvp;
#MT MOBILE SUBSCRIBER SURVEY
#
#HLRADDR             NSUB       NSUBA
#4-870772001199        10824       7859
#4-639879990005          221        155
#4-8613492233333        9179       7262
#
#TOTNSUB
#20224
#
#TOTNSUBA
#15276
#
#END
def check_mgsvp(input_str):
    output_str = ['#MT MOBILE SUBSCRIBER SURVEY: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"HLRADDR", input_str):
            output_str.append("\t" + input_str)
            while True:
                input_str = (strip(get_input()).split())
                if len(input_str) == 0:
                    break
                output_str.append("\t" + "\t".join(input_str))

        elif input_str == 'END':
            output_str[0] += state
            return output_str
