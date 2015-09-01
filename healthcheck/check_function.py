# -*- coding: utf-8 -*-

import re
from string import strip, atoi

def get_input():
    try:
        return raw_input().replace('\\', '/')
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
            alarm_str = '-\t' + input_str[0] + ": "
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
            output_str.append('-\t' + input_str)

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
            output_str[0] += '= ' + input_str[1] + '%'

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

#<strsp:r=all;
#DEVICE STATE SURVEY
#R        NDV         NOCC        NIDL        NBLO        RSTAT
#TC                0           0           0           0  NORES
#TCT               0           0           0           0  NORES
#TCONI          1024           0        1024           0  NORES
#TCIAL1            1           1           0           0  NORES
#TCIAR1            0           0           0           0  NORES
#BJNER1O          29           3          26          10  NORES
#BJNER1I          29           3          26          10  NORES
#END
def check_strsp(input_str):
    output_str = ['#DEVICE STATE SURVEY: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"NBLO", input_str):
            continue

        elif input_str == 'END':
            output_str[0] += state
            return output_str
        
        input_str = input_str.split()
        if len(input_str) < 4:
            continue

        if atoi(input_str[4]) > 0:
            state = 'FAIL'
            output_str.append("-\t" + "\t".join(input_str))

#<exrpp:rp=all;
#RP DATA
#
#RP    STATE  TYPE     TWIN  STATE   DS     MAINT.STATE
#   0  WO     RPSCB1E                       IDLE
#   1  WO     RPSCB1E                       IDLE
#   2  WO     GARP2E                        IDLE
#   3  WO     GARP2E                        IDLE
#   4  WO     RPSCB1E                       IDLE
#END
def check_exrpp(input_str):
    output_str = ['#RP DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"AB", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str

#<exemp:rp=all,em=all;
#EM DATA
#
#RP    TYPE   EM  EQM                       TWIN  CNTRL  PP     STATE
#   2  GARP2E  0  OCITS-0                         PRIM          WO
#   2  GARP2E  1  JOB-0                           PRIM          WO
#
#   3  GARP2E  0  OCITS-1                         PRIM          WO
#   3  GARP2E  1  JOB-1                           PRIM          WO
#
#END
def check_exemp(input_str):
    output_str = ['#EM DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"AB", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<ihcop:ipport=all;
#IP PORT CONNECTION DATA
#
#IPPORT  MHROLE   MHRELPORT  CURROLE
#IP-0-2  ACTIVE   IP-1-2     ACTIVE
#
#IPADD             SUBMASK
#10.128.228.50     255.255.255.248
#
#MTU
#1500
#
#IPMIGR          IPBK
#0               
#
#SVRATE  SVTO  SVMAXTX  SVMINRX
#10      3     2        2
#
#SVI  SVR
#65   82
#
#SVGW
#
#
#IPPORT  MHROLE   MHRELPORT  CURROLE
#IP-1-2  STAND-BY IP-0-2     STAND-BY
#
#IPADD             SUBMASK
#10.128.228.58     255.255.255.248
#
#MTU
#1500
#
#IPMIGR          IPBK
#0               
#
#SVRATE  SVTO  SVMAXTX  SVMINRX
#10      3     2        2
#
#SVI  SVR
#65   82
#
#SVGW
#
#END
def check_ihcop(input_str):
    output_str = ['#IP PORT CONNECTION DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"IPPORT", input_str):
            input_str = strip(get_input())
            output_str.append('\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str

#<ihstp:ipport=all;
#IP PORT STATE
#
#IPPORT         OPSTATE  BLSTATE
#IP-0-2         BUSY     
#IP-1-2         BUSY     
#IP-2-2         BUSY     
#IP-3-2         BUSY     
#IP-4-2         BUSY     
#IP-5-2         BUSY     
#
#END
def check_ihstp(input_str):
    output_str = ['#IP PORT STATE: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"ABL", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif re.search(r"CBL", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<m3asp;
#M3UA ASSOCIATION STATUS
#
#SAID             STATE  BLSTATE          AUTOBLSTATE
#BJSAS3           ACT                     
#
#BJSAS2           ACT                     
#
#BJSAS1           ACT                     
#
#END
def check_m3asp(input_str):
    output_str = ['#M3UA ASSOCIATION STATUS: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"DOWN", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif re.search(r"INACT", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<m3rsp:dest=all;
#M3UA ROUTING DATA
#
#DEST           SPID         DST    LSHM
#0-9154         BJCU001      AVA    PP
#
#               SAID             PRIO  RST              CW     CWU
#               BJSAS3              1  EN-ACT-AVA              
#
#0-9163         BJCTSTP      AVA    PP
#
#               SAID             PRIO  RST              CW     CWU
#               BJSAS3              1  EN-ACT-AVA              
#
#END
def check_m3rsp(input_str):
    output_str = ['#M3UA ROUTING DATA: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"DIS", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif re.search(r"INAC", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif re.search(r"UNAVA", input_str):
            state = 'FAIL' 
            output_str.append('-\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str

#<chopp;
#COMMON CHARGING OUTPUT ADJUNCT PROCESSOR INTERFACE DATA
#
#STATUS    BSIZE    OUTP    MSNAME          DEFMSNAME       DEFBSIZE
#OPEN          4    00000   CHS             CHS                    4
#END
def check_chopp(input_str):
    output_str = ['#COMMON CHARGING OUTPUT: ']
    state = 'FAIL'

    while True:
        input_str = strip(get_input())

        if re.search(r"STATUS", input_str):
            input_str = strip(get_input()).split()
            if input_str[0] == 'OPEN' and atoi(input_str[1]) < 100:
                state = 'OK'

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<c7ncp:sp=all,ssn=all;
#CCITT7 SCCP NETWORK CONFIGURATION DATA
#
#SP             SPID     SPSTATE     BROADCASTSTATUS  SCCPSTATE
#0-9154         BJCU001  ALLOWED     CON              ALLOWED
#
#                        SSN         SUBSYSTEMSTATE   SST
#                        7           ALLOWED          YES
#                        8           ALLOWED          YES
#
#END
def check_c7ncp(input_str):
    output_str = ['#CCITT7 SCCP NETWORK: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if input_str == 'END':
            output_str[0] += state
            return output_str

 
#<lmpfp;
#LICENSE MANAGEMENT PARAMETERS FAULT LOG
#NO DATA
#
#END
def check_lmpfp(input_str):
    output_str = ['#LICENSE MANAGEMENT PARAMETERS FAULT LOG: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if not(re.search(r"'NO DATA'", input_str) == None):
            state = 'FAIL'
            output_str.append('-\t' + input_str)

        if input_str == 'END':
            output_str[0] += state
            return output_str


#SYSTEM BACKUP FILES
#
#FILE                           EXCHANGE
#RELFSW0                        BEIMSC 141/00/00/1  147
#
#SUBFILE          OUTPUTTIME    COMMANDLOG
#SDD              150819 0200   -
#LDD1             150819 0200   0000864
#LDD2             150818 0200   0000863
#PS               150529 1118   -
#RS               150529 1118   -
#END
def check_sybfp(input_str):
    output_str = ['#SYSTEM BACKUP FILES: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"RELFSW0", input_str):
            output_str.append('\tRELFSW0')
            for i in range(2):
                input_str = strip(get_input())
            for i in range(5):
                input_str = strip(get_input())
                if input_str.split()[3] != '-':
                    output_str.append('\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str


#<caclp;
#TIME
#
#
#DATE     TIME     SUMMERTIME     DAY      DCAT
#150819   055845   NO             WED      0
#
#
#REFERENCE CLOCKS
#
#RC      DEV     STATE
#
#URC1    JOB-0   ACTIVE
#URC2    JOB-1   BLOCKED
#URC3            NOT CONNECTED
#
#SNTP            NOT CONNECTED
#
#END
def check_caclp(input_str):
    output_str = ['#TIME: ']
    state = 'NO URC ACTIVE: OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"DATE", input_str):
            output_str.append('\t' + input_str)
            output_str.append('\t' + strip(get_input()))

        elif re.search(r"URC", input_str) and re.search(r"ACTIVE", input_str):
            state = 'OK'
            output_str.append('\t' + input_str)

        elif input_str == 'END':
            output_str[0] += state
            return output_str


# Directory of K:\ACS\data\RTR\CHS_CP0EX\DATAFILES\REPORTED
#
#08/19/2015  05:50 AM    <DIR>          .
#08/19/2015  05:50 AM    <DIR>          ..
#07/19/2015  05:59 AM           107,950 RTR-0719-0549.7037
#07/19/2015  06:09 AM           110,281 RTR-0719-0559.7038
#07/19/2015  06:19 AM           110,813 RTR-0719-0609.7039
#07/19/2015  06:29 AM            91,864 RTR-0719-0619.7040
#07/19/2015  06:39 AM           101,472 RTR-0719-0629.7041
#08/19/2015  05:00 AM           227,549 RTR-0819-0450.1495
#08/19/2015  05:10 AM           201,492 RTR-0819-0500.1496
#08/19/2015  05:20 AM           190,835 RTR-0819-0510.1497
#08/19/2015  05:30 AM           178,820 RTR-0819-0520.1498
#08/19/2015  05:40 AM           193,639 RTR-0819-0530.1499
#08/19/2015  05:50 AM           196,873 RTR-0819-0540.1500
#            4464 File(s)    614,975,232 bytes
#               2 Dir(s)  66,478,096,384 bytes free
def check_rtr_reported(input_str):
    output_str = ['#K:\\ACS\\data\\RTR\\CHS_CP0EX\\DATAFILES\\REPORTED: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"\.\.", input_str):
            input_str = strip(get_input()).split()
            output_str.append('\t' + input_str[4])
            output_str.append('\t...')

        elif re.search(r"bytes", input_str):
            output_str.append('\t' + last_input_str.split()[4])
            output_str[0] += state
            return output_str
        
        last_input_str = input_str


# Directory of K:\ACS\data\RTR\billing\Ready
#
#08/19/2015  05:52 AM    <DIR>          .
#08/19/2015  05:52 AM    <DIR>          ..
#08/19/2015  05:52 AM    <DIR>          cdrBackup
#               0 File(s)              0 bytes
#               3 Dir(s)  66,478,096,384 bytes free
def check_rtr_ready(input_str):
    output_str = ['#K:\\ACS\\data\\RTR\\billing\\Ready: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"bytes", input_str):
            input_str = input_str.split()
            output_str[0] += input_str[0] + " Files : " + state
            return output_str


#K:\ACS\data\RTR\billing\Ready>alist
#
def check_alist(input_str):
    output_str = ['#ALIST: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if len(input_str.split()) != 0:
            print input_str
            state = 'FAIL'

        output_str[0] += state
        return output_str

#K:\ACS\data\RTR\billing\Ready>cluster node
#Listing status for all available nodes:
#
#Node           Node ID Status
#-------------- ------- ---------------------
#BJMSAPG1A            1 Up
#BJMSAPG1B            2 Up
def check_cluster_node(input_str):
    output_str = ['#CLUSTER NODE: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"---", input_str):
            for i in range(2):
                input_str = strip(get_input()).split()
                if len(input_str) < 3:
                    state = 'FAIL'
                elif input_str[2] != 'Up':
                    state = 'FAIL'
                    output_str.append('-\t' + " ".join(input_str))
            output_str[0] += state
            return output_str


#K:\ACS\data\RTR\billing\Ready>cluster res
#Listing status for all available resources:
#
#Resource             Group                Node            Status
#-------------------- -------------------- --------------- ------
#Disks K:             Disk Group           BJMSAPG1A       Online
#DHCP Service         Disk Group           BJMSAPG1A       Online
#Share K              Disk Group           BJMSAPG1A       Online
#Images               Disk Group           BJMSAPG1A       Online
#stsprov              Disk Group           BJMSAPG1A       Online
#stsconv              Disk Group           BJMSAPG1A       Online
#stsopcf              Disk Group           BJMSAPG1A       Online
#stsmain              Disk Group           BJMSAPG1A       Online
#
def check_cluster_res(input_str):
    output_str = ['#CLUSTER RES: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search(r"---", input_str):
            while True:
                input_str = strip(get_input())
                if len(input_str) == 0:
                    break
                if not(re.search(r"Online$", input_str)):
                    state = 'FAIL'
                    output_str.append('-\t' + input_str)
            
            output_str[0] += state
            return output_str


#K:\ACS\data\RTR\billing\Ready>ssuls -l
#AP CONFIGURATION TYPE
#
#MSC
#
#
#SSU FOLDER QUOTA SUPERVISION TABLE
#
#Folder name:                  K:\ACS\DATA
#Quota limit:                  71.00GB
#Current folder size:          4.09GB (6% of quota limit)
#A2 alarm level:               8% free space
#A2 cease level:               10% free space
#A1 alarm level:               4% free space
#A1 cease level:               6% free space
#
#
#Folder name:                  K:\ACS\DATA\ACA
#Quota limit:                  4.00GB
#Current folder size:          1.64MB (0% of quota limit)
#A2 alarm level:               8% free space
#A2 cease level:               10% free space
#A1 alarm level:               4% free space
#A1 cease level:               6% free space
#
def check_ssuls(input_str):
    output_str = ['#DISK SIZE: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search('Folder name', input_str):
            folder_name = input_str.split()[2]

            for i in range(2):
                input_str = strip(get_input())
            current_size = re.search('(\d*)%', input_str).group(1)
            alarm_size = re.search('(\d*)%', strip(get_input())).group(1)

            if (atoi(current_size) > (100 - atoi(alarm_size))):
                state = 'FAIL'
                output_str.append('-\t' + folder_name + "\tcurrent size=" 
                        + current_size + '%\talarm level: ' + alarm_size
                        + '% free space')
        
        elif len(input_str.split(">")) > 1:
            output_str[0] += state
            output_str.append(input_str)
            output_str.append(True)
            return output_str


#K:\ACS\data\RTR\billing\Ready>vxdisk list
#Name             MediaName   Diskgroup      DiskStyle  Size(MB)  FreeSpace(MB)   Status       EnclosureID      P#C#T#L#
#Harddisk0                   BasicGroup        MBR      140270     70145      Uninitialized    DISKS@BJMSAPG1A  P1C0T0L0
#Harddisk1          Disk1    DataDisk          MBR      286095     0          Imported                          P1C0T3L0
#Harddisk2          Disk2    DataDisk          MBR      286095     0          Imported                          P1C0T7L0
#Harddisk3                   BasicGroup        MBR      1935       940        Uninitialized    DISKS@BJMSAPG1A  P0C0T0L0
#
def check_vxdisk(input_str):
    output_str = ['#RAID STATE: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search('Harddisk[12]', input_str):
            if input_str.split()[6] != 'Imported':
                state = 'FAIL'
                output_str.append('-\t' + " ".join(input_str.split())) 
        
        elif len(input_str.split(">")) > 1:
            output_str[0] += state
            output_str.append(input_str)
            output_str.append(True)
            return output_str


# Directory of k:\images\Nodea
#
#08/06/2015  02:11 AM    <DIR>          .
#08/06/2015  02:11 AM    <DIR>          ..
#07/07/2015  02:39 AM     2,392,627,687 Auto_BJMSAPG1A_20150707_023212.zip
#08/06/2015  02:11 AM     2,390,432,466 Auto_BJMSAPG1A_20150806_020341.zip
#               2 File(s)  4,783,060,153 bytes
#
# Directory of k:\images\Nodeb
#
#08/06/2015  02:39 AM    <DIR>          .
#08/06/2015  02:39 AM    <DIR>          ..
#07/07/2015  02:28 AM     2,466,321,530 Auto_BJMSAPG1B_20150707_021957.zip
#08/06/2015  02:39 AM     2,465,310,521 Auto_BJMSAPG1B_20150806_023024.zip
#               2 File(s)  4,931,632,051 bytes
#
#     Total Files Listed:
#               4 File(s)  9,714,692,204 bytes
#               8 Dir(s)   6,391,418,880 bytes free
def check_images(input_str):
    output_str = ['#APG BACKUP: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search('.zip', input_str):
            output_str.append('\t' + input_str.split()[4])
        
        elif re.search('bytes', input_str):
            output_str[0] += state
            return output_str

#BJMGW01> altk
#
#150819-06:02:11 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315
#
#Connecting to 10.128.163.8:56834 (CorbaSecurity=OFF, corba_class=2, java=1.6.0_26, jacoms=R80L06, jacorb=R80LX01)
#Trying file=/gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/ior16289
#Resolving the alarm service in OMS...
#Simple Alarm Client initialized...
#Starting to retrieve active alarms
#Nr of active alarms are: 1
#UNACKNOWLEDGED ALARMS: 0
#====================================================================================================================
#Date & Time (Local) S Specific Problem                    MO (Cause/AdditionalInfo)
#====================================================================================================================
#
#ACKNOWLEDGED ALARMS: 1
#====================================================================================================================
#Date & Time (Local) S Specific Problem                    MO (Cause/AdditionalInfo) Operator
#====================================================================================================================
#2015-05-28 02:39:37 w MTP3b Link Out of Service           Mtp3bSpItu=0-16173,Mtp3bSls=BJCM001_SLS,Mtp3bSlItu=BJCM001_SLC_1 (BJCM001_SLC_1 started tracking on CMA subscribe) dell
#>>> Total: 1 Alarms (0 Critical, 0 Major)
def check_mgw_altk(input_str):
    output_str = ['#MGW ALARM: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search('Total', input_str):
            if atoi(input_str.split()[2]) > 0:
                state = 'FAIL'
                output_str.append('-\t' + input_str.split(' ', 1)[1])

            output_str[0] += state
            return output_str


#BJMGW01> lgaevsrm -s 20150801
#
#150819-06:03:02 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315
#Trying password from ipdatabase file: /gsn/coreUser/moshell//sitefiles/ipdatabase...
#Startdate=20150801.000000, Enddate=20150820.060303
#.....Get /c/logfiles/alarm_event/ALARM_LOG.xml /gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/alarmLog16315.xml ... OK
#Get /c/logfiles/alarm_event/EVENT_LOG.xml /gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/eventLog16315.xml ... OK
#Get /c/logfiles/availability/CELLO_AVAILABILITY2_LOG.xml /gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/availabilityLog16315.xml ... OK
#
#Parsing alarmLog...Done.
#Parsing eventLog...Done.
#Parsing availabilityLog...Done.
#======================================================================================================
#Timestamp (UTC)     Type  Merged Log Entry
#======================================================================================================
#2015-08-01 01:00:36 OTHR  ConfigVersionCreated BJMGW01 BC4001_NDP_6.4.0.0B R10A AXM10101/11 CV=Au_CXP9018138%6_R112A03_150801_0100 UP=CXP9018138/6_R112A03 NDP6400B (BC4001_NDP_6.4.0.0B, C13.0-EP4-2)
#2015-08-01 02:49:43 AL    w MTP3b Link Out of Service           Mtp3bSpItu=2-1208,Mtp3bSls=PMMGW01_SLS,Mtp3bSlItu=PMMGW01_SLC_1 (Paumalu MGw (SLC1) |   Mtp3bSl[froId=16  rpuId=47] RAISED op= dis, av=depFl, usage=IDLE, proc=N_INIT, link=FAIL----- NB: OOS, SUERM: AERM)
#2015-08-01 02:49:53 AL    * MTP3b Link Out of Service           Mtp3bSpItu=2-1208,Mtp3bSls=PMMGW01_SLS,Mtp3bSlItu=PMMGW01_SLC_1 (Paumalu MGw (SLC1) |   Mtp3bSl[froId=16  rpuId=47] RAISED op= dis, av=depFl, usage=IDLE, proc=N_INIT, link=FAIL----- NB: OOS, SUERM: AERM)
#2015-08-01 05:46:48 AL    w MTP3b Link Out of Service           Mtp3bSpItu=2-1208,Mtp3bSls=PMMGW01_SLS,Mtp3bSlItu=PMMGW01_SLC_0 (Paumalu MGw (SLC0) |   Mtp3bSl[froId=15  rpuId=47] RAISED op= dis, av=depFl, usage=IDLE, proc=N_INIT, link=FAIL----- NB: OOS, SUERM: AERM)
#2015-08-01 05:46:59 AL    * MTP3b Link Out of Service           Mtp3bSpItu=2-1208,Mtp3bSls=PMMGW01_SLS,Mtp3bSlItu=PMMGW01_SLC_0 (Paumalu MGw (SLC0) |   Mtp3bSl[froId=15  rpuId=47] RAISED op= dis, av=depFl, usage=IDLE, proc=N_INIT, link=FAIL----- NB: OOS, SUERM: AERM)
#2015-08-01 08:33:21 AL    M MTP3b Route Set Unavailable         Mtp3bSpItu=0-16173,Mtp3bSrs=SBMSC01_SRS (SBMSC01_SRS |  Mtp3bSrs[froId=23  rpuId=47] RAISED op= dis, cong=UNCONGESTED: RofMtp3bSRSStatusChange(2353): MTP_PAUSE_IND FROs:[SR:31:ok,SLS:10:ENBL])

def isPrint(input_str):
    if input_str.split()[3] == '*':
        return False

    not_print_list = [
        'MTP3b Route Set Unavailable',
        'MTP3b Link Out of Service',
        'PDH Alarm Indication Signal',
        'ConfigVersionCreated',
        'PeriodicLogging',
        'PDH Remote Defect Indication',
        'PDH Loss of Frame',
    ]

    for i in not_print_list:
        if re.search(i, input_str):
            return False
    
    return True

def check_mgw_lgaevsrm(input_str):
    output_str = ['#MGW ALARM LOG: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search('^\d{4}-\d{2}-\d{2}', input_str):
            if isPrint(input_str):
                output_str.append('\t' + re.search('^.{66}', input_str).group(0))
                
        elif len(input_str.split(">")) > 1:
            output_str[0] += state
            output_str.append(input_str)
            output_str.append(True)
            return output_str


#BJMGW01> st plugInUnit

#150819-06:05:01 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315
#===================================================================================
#Proxy  Adm State     Op. State     MO
#===================================================================================
  #188  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=10,PlugInUnit=1
  #214  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=11,PlugInUnit=1
  #225  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=12,PlugInUnit=1
  #236  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=13,PlugInUnit=1
  #952  0 (LOCKED)    1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=22,PlugInUnit=1
 #1261  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=6,PlugInUnit=1
 #1298  0 (LOCKED)    1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=7,PlugInUnit=1
 #1307  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=8,PlugInUnit=1
 #1335  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=9,PlugInUnit=1
#===================================================================================
#Total: 23 MOs
def check_mgw_st_pluginunit(input_str):
    output_str = ['#MGW ST: ']
    state = 'OK'

    for i in range(5):
        get_input()

    while True:
        input_str = strip(get_input())

        if re.search('ENABLED', input_str):
            continue
        if re.search('===', input_str):
            continue
        if re.search('Total', input_str):
            output_str[0] += state
            return output_str
        state = 'FAIL'
        output_str.append('-\t' + input_str)


#BJMGW01> cvls

#150819-06:05:10 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315

#===================================================================================================================
#150819-06:05            CV Name                                   Upgrade Package       Release
#===================================================================================================================
#Startable:              Au_CXP9018138%6_R112A03_150819_0100       CXP9018138/6_R112A03  NDP6400B (BC4001_NDP_6.4.0.0B, C13.0-EP4-2)
#Loaded:                 BeforeDeleteMSB_AMC_7_22_20131121         CXP9018138/6_R112A03  NDP6400B (BC4001_NDP_6.4.0.0B, C13.0-EP4-2)
#Executing:              Au_CXP9018138%6_R112A03_150819_0100       CXP9018138/6_R112A03  NDP6400B (BC4001_NDP_6.4.0.0B, C13.0-EP4-2)
#Last created:           Au_CXP9018138%6_R112A03_150819_0100       CXP9018138/6_R112A03  NDP6400B (BC4001_NDP_6.4.0.0B, C13.0-EP4-2)
#-------------------------------------------------------------------------------------------------------------------
#Current UpgradePkg:     UpgradePackage=CXP9018138%6_R112A03       CXP9018138/6_R112A03  NDP6400B (BC4001_NDP_6.4.0.0B, C13.0-EP4-2)
#AutoCreatedCV:          Enabled. Daily backup at 01:00
#Ongoing CV activity:    0 (IDLE)
#Rollback status:        Rollback is on
#Rollback init timer:    30
#Rollback init counter:  5
#Rollback counter:       5
#Rollback list:          s[10] = Au_CXP9018138%6_R112A03_150818_0100 Before_Change_CsdGsmFhService_20140820 Before_ChangeBJCT_20140226 After_Subic_E1_Move_20140116 Before_Subic_E1_Move_20140114 After_AddSubic_20140107 AfterDel_NER_SL1_20140106 BeforeDeleteMSB_AMC_7_22_20131121 BeforeAddEir_20131011 UpgradeR6400B_OK_20130509 
#======================================================================================================================================
#UP name              ProductData          CVs LMs PrDate LastCV state                   Release                                     CompatIndex        
#======================================================================================================================================
#CXP9018138%6_R112A03 CXP9018138/6_R112A03  15 346 130117 150819 IDLE, UPGRADE_COMPLETED NDP6400B (BC4001_NDP_6.4.0.0B, C13.0-EP4-2) BC4001_NDP_6.4.0.0B
#======================================================================================================================================
#Id CV Name                                Creation Date    UpgradePackage       Release  Type        Operator     Comment
#======================================================================================================================================
 #1 SU_CXP9018138%6_R112A03_130509_0843    2013-05-09 08:43 CXP9018138/6_R112A03 NDP6400B upgrade_tol CPP          Temp. CV autocreated at SU
 #2 Fi_CXP9018138%6_R112A03_130509_0854    2013-05-09 08:54 CXP9018138/6_R112A03 NDP6400B other       CPP          Final CV autocreated at SU
 #3 UpgradeR6400B_OK_20130509              2013-05-09 09:31 CXP9018138/6_R112A03 NDP6400B standard    BjlesRAN     none
 #4 BeforeAddEir_20131011                  2013-10-11 01:42 CXP9018138/6_R112A03 NDP6400B standard    Administrator  none
 #5 BeforeDeleteMSB_AMC_7_22_20131121      2013-11-21 08:39 CXP9018138/6_R112A03 NDP6400B standard    Administrator  none
 #6 BeforeDel_NER_SL1_20140106             2014-01-06 03:09 CXP9018138/6_R112A03 NDP6400B standard    admin        none
 #7 AfterDel_NER_SL1_20140106              2014-01-06 03:23 CXP9018138/6_R112A03 NDP6400B standard    admin        none
 #8 Before_AddSubic_20140107               2014-01-07 06:24 CXP9018138/6_R112A03 NDP6400B standard    admin        none
 #9 After_AddSubic_20140107                2014-01-07 06:34 CXP9018138/6_R112A03 NDP6400B standard    admin        none
#10 Before_Subic_E1_Move_20140114          2014-01-14 15:42 CXP9018138/6_R112A03 NDP6400B standard    admin        none
#11 After_Subic_E1_Move_20140116           2014-01-16 03:40 CXP9018138/6_R112A03 NDP6400B standard    admin        none
#12 Before_ChangeBJCT_20140226             2014-02-26 04:28 CXP9018138/6_R112A03 NDP6400B standard    admin        none
#13 Before_Change_CsdGsmFhService_20140820 2014-08-20 06:01 CXP9018138/6_R112A03 NDP6400B standard    admin        none
#14 Au_CXP9018138%6_R112A03_150818_0100    2015-08-18 01:00 CXP9018138/6_R112A03 NDP6400B autocreate  CPP          Daily autocreated CV
#15 Au_CXP9018138%6_R112A03_150819_0100    2015-08-19 01:00 CXP9018138/6_R112A03 NDP6400B autocreate  CPP          Daily autocreated CV
#======================================================================================================================================
#>>> Total: 15 CV's, 1 UP's
def check_mgw_cvls(input_str):
    output_str = ['#MGW cvls: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())

        if re.search('Total', input_str):
            output_str[0] += state
            return output_str


#BJMGW01> pst
#
#150819-06:05:20 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315
#Connecting to 10.128.163.8:56834 (CorbaSecurity=OFF, corba_class=2, java=1.6.0_26, jacoms=R80L06, jacorb=R80LX01)
#Trying file=/gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/ior16289
#**** Bootstrapping OK
#****
#
#$pmtester_pid = 16522
#
#================================================================================
#  PROXY  SCANNER-NAME                                                  STATE
#================================================================================
#      2  USERDEF.e1ttp.STATS                                           ACTIVE
#      3  USERDEF.Vc12Ttp.STATS                                         ACTIVE
#      4  USERDEF.Vc4Ttp.STATS                                          ACTIVE
#      5  USERDEF.os155spittp.STATS                                     ACTIVE
#      6  PerformanceIndicator                                          ACTIVE
#================================================================================
#>>> Total: 5 Scanners
def check_mgw_pst(input_str):
    output_str = ['#MGW pst: ']
    state = 'OK'

    while True:
        input_str = strip(get_input())
    
        if re.search('PROXY', input_str):
            get_input()
            while True:
                input_str = strip(get_input())
                if re.search('===', input_str):
                    break
                output_str.append('\t' + input_str)

        if re.search('Total', input_str):
            output_str[0] += state
            return output_str
