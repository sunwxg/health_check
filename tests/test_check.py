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
        assert output[1] == '-\tA2/APZ: MT IMEI SUPERVISION LOG FAULT'
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
        assert output[1] == '-\t1   B     2     192.168.170.2    14000 FAULTY'
    except StopIteration:
        return

def test_check_plldp(monkeypatch):
    plldp= [
    "PROCESSOR LOAD DATA",
    "INT PLOAD CALIM OFFDO OFFDI FTCHDO FTCHDI OFFMPH OFFMPL FTCHMPH FTCHMPL",
    " 1    1   75000     3     2     3      2     15      9     15       9",
    " 2    1   75000     2     3     2      3     13      9     13       9",
    " 3    1   75000     2     4     2      4     12      5     12       5",
    " 4    1   75000     3     3     3      3     14      0     14       0",
    " 5    1   75000     3     3     3      3     17      1     17       1",
    " 6    1   75000     0     2     0      2     13      0     13       0",
    " 7    1   75000     1     6     1      6     13      1     13       1",
    " 8    1   75000     0     4     0      4     10      1     10       1",
    " 9    1   75000     1     2     1      2      9      0      9       0",
    "10    1   75000     3     3     3      3     17      1     17       1",
    "11    1   75000     7     5     7      5     15      3     15       3",
    "12    1   75000     2     3     2      3     18      9     18       9",
    "",
    "INT OFFTCAP FTDTCAP",
    " 1      0       0",
    " 2      0       0",
    " 3      0       0",
    " 4      0       0",
    " 5      0       0",
    " 6      0       0",
    " 7      0       0",
    " 8      0       0",
    " 9      0       0",
    "10      0       0",
    "11      0       0",
    "12      0       0",
    "END",
    ]

    inputs = plldp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_plldp('<plldp')
        assert output[0] == '#PROCESSOR LOAD DATA: = 1% OK'
    except StopIteration:
        return

def test_check_mgsvp(monkeypatch):
    mgsvp = [
    "MT MOBILE SUBSCRIBER SURVEY",
    "",
    "HLRADDR             NSUB       NSUBA",
    "4-870772001199        10824       7859",
    "4-639879990005          221        155",
    "4-8613492233333        9179       7262",
    "",
    "TOTNSUB",
    "20224",
    "",
    "TOTNSUBA",
    "15276",
    "",
    "END",
    ]

    inputs = mgsvp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_mgsvp('<mgsvp')
        assert output[0] == '#MT MOBILE SUBSCRIBER SURVEY: OK'
    except StopIteration:
        return

def test_check_strsp(monkeypatch):
    strsp = [
    "DEVICE STATE SURVEY",
    "R        NDV         NOCC        NIDL        NBLO        RSTAT",
    "TC                0           0           0           0  NORES",
    "TCT               0           0           0           0  NORES",
    "TCONI          1024           0        1024           0  NORES",
    "TCIAL1            1           1           0           0  NORES",
    "TCIAR1            0           0           0           0  NORES",
    "BJNER1O          29           3          26          10  NORES",
    "BJNER1I          29           3          26          10  NORES",
    "END",
    ]

    inputs = strsp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_strsp('<strsp')
        assert output[0] == '#DEVICE STATE SURVEY: FAIL'
        assert output[1] == '-\tBJNER1O\t29\t3\t26\t10\tNORES'
        assert output[2] == '-\tBJNER1I\t29\t3\t26\t10\tNORES'
    except StopIteration:
        return

def test_check_exrpp(monkeypatch):
    exrpp = [
    "<exrpp:rp=all;",
    "RP DATA",
    "",
    "RP    STATE  TYPE     TWIN  STATE   DS     MAINT.STATE",
    "   0  WO     RPSCB1E                       IDLE",
    "   1  WO     RPSCB1E                       IDLE",
    "   2  WO     GARP2E                        IDLE",
    "   3  AB     GARP2E                        IDLE",
    "   4  WO     RPSCB1E                       IDLE",
    "END",
    ]

    inputs = exrpp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_exrpp('<exrpp')
        assert output[0] == '#RP DATA: FAIL'
        assert output[1] == '-\t3  AB     GARP2E                        IDLE'
    except StopIteration:
        return

def test_check_exemp(monkeypatch):
    exemp = [
    "<exemp:rp=all,em=all;",
    "EM DATA",
    "",
    "RP    TYPE   EM  EQM                       TWIN  CNTRL  PP     STATE",
    "   2  GARP2E  0  OCITS-0                         PRIM          WO",
    "   2  GARP2E  1  JOB-0                           PRIM          WO",
    "",
    "   3  GARP2E  0  OCITS-1                         PRIM          AB",
    "   3  GARP2E  1  JOB-1                           PRIM          WO",
    "",
    "END",
    ]

    inputs = exemp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_exemp('<exemp')
        assert output[0] == '#EM DATA: FAIL'
        assert output[1] == '-\t3  GARP2E  0  OCITS-1                         PRIM          AB'
    except StopIteration:
        return

def test_check_ihcop(monkeypatch):
    ihcop = [
    "<ihcop:ipport=all;",
    "IP PORT CONNECTION DATA",
    "",
    "IPPORT  MHROLE   MHRELPORT  CURROLE",
    "IP-0-2  ACTIVE   IP-1-2     ACTIVE",
    "",
    "IPADD             SUBMASK",
    "10.128.228.50     255.255.255.248",
    "",
    "MTU",
    "1500",
    "",
    "IPMIGR          IPBK",
    "0               ",
    "",
    "SVRATE  SVTO  SVMAXTX  SVMINRX",
    "10      3     2        2",
    "",
    "SVI  SVR",
    "65   82",
    "",
    "SVGW",
    "",
    "",
    "IPPORT  MHROLE   MHRELPORT  CURROLE",
    "IP-1-2  STAND-BY IP-0-2     STAND-BY",
    "",
    "IPADD             SUBMASK",
    "10.128.228.58     255.255.255.248",
    "",
    "MTU",
    "1500",
    "",
    "IPMIGR          IPBK",
    "0               ",
    "",
    "SVRATE  SVTO  SVMAXTX  SVMINRX",
    "10      3     2        2",
    "",
    "SVI  SVR",
    "65   82",
    "",
    "SVGW",
    "",
    "END",
    ]

    inputs = ihcop
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_ihcop('<ihcop')
        assert output[0] == '#IP PORT CONNECTION DATA: OK'
        assert output[1] == '\tIP-0-2  ACTIVE   IP-1-2     ACTIVE'
    except StopIteration:
        return

def test_check_ihstp(monkeypatch):
    ihstp = [
    "<ihstp:ipport=all;",
    "IP PORT STATE",
    "",
    "IPPORT         OPSTATE  BLSTATE",
    "IP-0-2         BUSY     ",
    "IP-1-2         BUSY     ",
    "IP-2-2         BUSY     ",
    "IP-3-2         BUSY     ",
    "IP-4-2         BUSY     ",
    "IP-5-2         BUSY     ",
    "",
    "END",
    ]

    inputs = ihstp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_ihstp('<ihcop')
        assert output[0] == '#IP PORT STATE: OK'
    except StopIteration:
        return

def test_check_m3asp(monkeypatch):
    m3asp = [
    "<m3asp;",
    "M3UA ASSOCIATION STATUS",
    "",
    "SAID             STATE  BLSTATE          AUTOBLSTATE",
    "BJSAS3           ACT                     ",
    "",
    "BJSAS2           ACT                     ",
    "",
    "BJSAS1           ACT                     ",
    "",
    "END",
    ]

    inputs = m3asp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_m3asp('<ihcop')
        assert output[0] == '#M3UA ASSOCIATION STATUS: OK'
    except StopIteration:
        return

def test_check_m3rsp(monkeypatch):
    m3rsp = [
    "<m3rsp:dest=all;",
    "M3UA ROUTING DATA",
    "",
    "DEST           SPID         DST    LSHM",
    "0-9154         BJCU001      AVA    PP",
    "",
    "               SAID             PRIO  RST              CW     CWU",
    "               BJSAS3              1  EN-ACT-AVA              ",
    "",
    "0-9163         BJCTSTP      AVA    PP",
    "",
    "               SAID             PRIO  RST              CW     CWU",
    "               BJSAS3              1  EN-ACT-AVA              ",
    "",
    "END",
    ]

    inputs = m3rsp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_m3rsp('<m3rsp')
        assert output[0] == '#M3UA ROUTING DATA: OK'
    except StopIteration:
        return

def test_check_chopp(monkeypatch):
    chopp = [
    '<chopp;',
    'COMMON CHARGING OUTPUT ADJUNCT PROCESSOR INTERFACE DATA',
    '',
    'STATUS    BSIZE    OUTP    MSNAME          DEFMSNAME       DEFBSIZE',
    'OPEN          4    00000   CHS             CHS                    4',
    'END',
    ]

    inputs = chopp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_chopp('<chopp')
        assert output[0] == '#COMMON CHARGING OUTPUT: OK'
    except StopIteration:
        return

def test_check_c7ncp(monkeypatch):
    c7ncp = [
    "<c7ncp:sp=all,ssn=all;",
    "CCITT7 SCCP NETWORK CONFIGURATION DATA",
    "",
    "SP             SPID     SPSTATE     BROADCASTSTATUS  SCCPSTATE",
    "0-9154         BJCU001  ALLOWED     CON              ALLOWED",
    "",
    "                        SSN         SUBSYSTEMSTATE   SST",
    "                        7           ALLOWED          YES",
    "                        8           ALLOWED          YES",
    "",
    "END",
    ]

    inputs = c7ncp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_c7ncp('<c7ncp')
        assert output[0] == '#CCITT7 SCCP NETWORK: OK'
    except StopIteration:
        return

def test_check_rtr_reported(monkeypatch):
    rtr_report = [
    " Directory of K:\ACS\data\RTR\CHS_CP0EX\DATAFILES\REPORTED",
    "",
    "08/19/2015  05:50 AM    <DIR>          .",
    "08/19/2015  05:50 AM    <DIR>          ..",
    "07/19/2015  05:59 AM           107,950 RTR-0719-0549.7037",
    "07/19/2015  06:09 AM           110,281 RTR-0719-0559.7038",
    "07/19/2015  06:19 AM           110,813 RTR-0719-0609.7039",
    "07/19/2015  06:29 AM            91,864 RTR-0719-0619.7040",
    "07/19/2015  06:39 AM           101,472 RTR-0719-0629.7041",
    "08/19/2015  05:00 AM           227,549 RTR-0819-0450.1495",
    "08/19/2015  05:10 AM           201,492 RTR-0819-0500.1496",
    "08/19/2015  05:20 AM           190,835 RTR-0819-0510.1497",
    "08/19/2015  05:30 AM           178,820 RTR-0819-0520.1498",
    "08/19/2015  05:40 AM           193,639 RTR-0819-0530.1499",
    "08/19/2015  05:50 AM           196,873 RTR-0819-0540.1500",
    "            4464 File(s)    614,975,232 bytes",
    "               2 Dir(s)  66,478,096,384 bytes free",
    ]

    inputs = rtr_report
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))
    
    try:
        output = check_rtr_reported('')
        assert output[0] == '#K:\\ACS\\data\\RTR\\CHS_CP0EX\\DATAFILES\\REPORTED: OK'
        assert output[1] == '\tRTR-0719-0549.7037'
        assert output[3] == '\tRTR-0819-0540.1500'
    except StopIteration:
        return

def test_check_rtr_ready(monkeypatch):
    rtr_ready = [
    " Directory of K:\ACS\data\RTR\billing\Ready",
    "",
    "08/19/2015  05:52 AM    <DIR>          .",
    "08/19/2015  05:52 AM    <DIR>          ..",
    "08/19/2015  05:52 AM    <DIR>          cdrBackup",
    "               0 File(s)              0 bytes",
    "               3 Dir(s)  66,478,096,384 bytes free",
    ]

    inputs = rtr_ready
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_rtr_ready('')
        assert output[0] == '#K:\\ACS\\data\\RTR\\billing\\Ready: 0 Files : OK'
    except StopIteration:
        return

def test_check_lmpfp(monkeypatch):
    lmpfp = [
    "<lmpfp;",
    "LICENSE MANAGEMENT PARAMETERS FAULT LOG",
    "NO DATA",
    "",
    "END",
    ]

    inputs = lmpfp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_lmpfp('')
        assert output[0] == '#LICENSE MANAGEMENT PARAMETERS FAULT LOG: OK'
    except StopIteration:
        return

def test_check_sybfp(monkeypatch):
    sybfp = [
    "SYSTEM BACKUP FILES",
    "",
    "FILE                           EXCHANGE",
    "RELFSW0                        BEIMSC 141/00/00/1  147",
    "",
    "SUBFILE          OUTPUTTIME    COMMANDLOG",
    "SDD              150819 0200   -",
    "LDD1             150819 0200   0000864",
    "LDD2             150818 0200   0000863",
    "PS               150529 1118   -",
    "RS               150529 1118   -",
    "",
    "",
    "FILE                           EXCHANGE",
    "RELFSW1                        BEIMSC 141/00/00/1  146",
    "",
    "SUBFILE          OUTPUTTIME    COMMANDLOG",
    "SDD              150529 0200   -",
    "LDD1             150529 0200   0000781",
    "LDD2             150528 0200   0000780",
    "PS               150408 0334   -",
    "RS               150408 0334   -",
    "END",
    ]

    inputs = sybfp
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_sybfp('')
        assert output[0] == '#SYSTEM BACKUP FILES: OK'
    except StopIteration:
        return

def test_check_caclp(monkeypatch):
    caclp = [
    "<caclp;",
    "TIME",
    "",
    "",
    "DATE     TIME     SUMMERTIME     DAY      DCAT",
    "150819   055845   NO             WED      0",
    "",
    "",
    "REFERENCE CLOCKS",
    "",
    "RC      DEV     STATE",
    "",
    "URC1    JOB-0   ACTIVE",
    "URC2    JOB-1   BLOCKED",
    "URC3            NOT CONNECTED",
    "",
    "SNTP            NOT CONNECTED",
    "",
    "END",
    ]

    inputs = caclp 
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_caclp('')
        assert output[0] == '#TIME: OK'
    except StopIteration:
        return

def test_check_alist(monkeypatch):
    alist = [
#    "K:\ACS\data\RTR\billing\Ready>alist",
    "",
    ]

    inputs = alist 
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_alist('')
        assert output[0] == '#ALIST: OK'
    except StopIteration:
        return

def test_check_cluster_node(monkeypatch):
    cluster_node = [
    "Listing status for all available nodes:",
    "",
    "Node           Node ID Status",
    "-------------- ------- ---------------------",
    "BJMSAPG1A            1 Up",
    "BJMSAPG1B            2 Up",
    "",
    ]

    inputs = cluster_node 
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_cluster_node('')
        assert output[0] == '#CLUSTER NODE: OK'
    except StopIteration:
        return

def test_check_cluster_res(monkeypatch):
    cluster_res = [
    "Listing status for all available resources:",
    "",
    "Resource             Group                Node            Status",
    "-------------------- -------------------- --------------- ------",
    "Disks K:             Disk Group           BJMSAPG1A       Online",
    "DHCP Service         Disk Group           BJMSAPG1A       Online",
    "Share K              Disk Group           BJMSAPG1A       Online",
    "Images               Disk Group           BJMSAPG1A       Online",
    "stsprov              Disk Group           BJMSAPG1A       Online",
    "stsconv              Disk Group           BJMSAPG1A       Online",
    "stsopcf              Disk Group           BJMSAPG1A       Online",
    "stsmain              Disk Group           BJMSAPG1A       Online",
    "",
    ]

    inputs = cluster_res
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_cluster_res('')
        assert output[0] == '#CLUSTER RES: OK'
    except StopIteration:
        return


def test_check_ssuls(monkeypatch):
    ssuls = [
    "AP CONFIGURATION TYPE",
    "",
    "MSC",
    "",
    "",
    "SSU FOLDER QUOTA SUPERVISION TABLE",
    "",
    "Folder name:                  K:\ACS\DATA",
    "Quota limit:                  71.00GB",
    "Current folder size:          4.09GB (99% of quota limit)",
    "A2 alarm level:               8% free space",
    "A2 cease level:               10% free space",
    "A1 alarm level:               4% free space",
    "A1 cease level:               6% free space",
    "",
    "",
    "Folder name:                  K:\ACS\DATA\ACA",
    "Quota limit:                  4.00GB",
    "Current folder size:          1.64MB (0% of quota limit)",
    "A2 alarm level:               8% free space",
    "A2 cease level:               10% free space",
    "A1 alarm level:               4% free space",
    "A1 cease level:               6% free space",
    "",
    "c:>alist",
    ]

    inputs = ssuls
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_ssuls('')
        assert output[0] == '#DISK SIZE: FAIL'
    except StopIteration:
        return

def test_check_vxdisk(monkeypatch):
    vxdisk = [
    "Name             MediaName   Diskgroup      DiskStyle  Size(MB)  FreeSpace(MB)   Status       EnclosureID      P#C#T#L#",
    "Harddisk0                   BasicGroup        MBR      140270     70145      Uninitialized    DISKS@BJMSAPG1A  P1C0T0L0",
    "Harddisk1          Disk1    DataDisk          MBR      286095     0          Imported                          P1C0T3L0",
    "Harddisk2          Disk2    DataDisk          MBR      286095     0          Imported                          P1C0T7L0",
    "Harddisk3                   BasicGroup        MBR      1935       940        Uninitialized    DISKS@BJMSAPG1A  P0C0T0L0",
    "",
    "c:>alist",
    ] 

    inputs = vxdisk 
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_vxdisk('')
        assert output[0] == '#RAID STATE: OK'
    except StopIteration:
        return

def test_check_images(monkeypatch):
    images = [
    " Directory of k:\images\Nodea",
    "",
    "08/06/2015  02:11 AM    <DIR>          .",
    "08/06/2015  02:11 AM    <DIR>          ..",
    "07/07/2015  02:39 AM     2,392,627,687 Auto_BJMSAPG1A_20150707_023212.zip",
    "08/06/2015  02:11 AM     2,390,432,466 Auto_BJMSAPG1A_20150806_020341.zip",
    "               2 File(s)  4,783,060,153 bytes",
    "",
    " Directory of k:\images\Nodeb",
    "",
    "08/06/2015  02:39 AM    <DIR>          .",
    "08/06/2015  02:39 AM    <DIR>          ..",
    "07/07/2015  02:28 AM     2,466,321,530 Auto_BJMSAPG1B_20150707_021957.zip",
    "08/06/2015  02:39 AM     2,465,310,521 Auto_BJMSAPG1B_20150806_023024.zip",
    "               2 File(s)  4,931,632,051 bytes",
    "",
    "     Total Files Listed:",
    "               4 File(s)  9,714,692,204 bytes",
    "               8 Dir(s)   6,391,418,880 bytes free",
    "",
    "c:>alist",
    ]

    inputs = images
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_images('')
        assert output[0] == '#APG BACKUP: OK'
    except StopIteration:
        return

def test_check_mgw_altk(monkeypatch):
    altk = [
    "BJMGW01> altk",
    "",
    "150819-06:02:11 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315",
    "",
    "Connecting to 10.128.163.8:56834 (CorbaSecurity=OFF, corba_class=2, java=1.6.0_26, jacoms=R80L06, jacorb=R80LX01)",
    "Trying file=/gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/ior16289",
    "Resolving the alarm service in OMS...",
    "Simple Alarm Client initialized...",
    "Starting to retrieve active alarms",
    "Nr of active alarms are: 1",
    "UNACKNOWLEDGED ALARMS: 0",
    "====================================================================================================================",
    "Date & Time (Local) S Specific Problem                    MO (Cause/AdditionalInfo)",
    "====================================================================================================================",
    "",
    "ACKNOWLEDGED ALARMS: 1",
    "====================================================================================================================",
    "Date & Time (Local) S Specific Problem                    MO (Cause/AdditionalInfo) Operator",
    "====================================================================================================================",
    "2015-05-28 02:39:37 w MTP3b Link Out of Service           Mtp3bSpItu=0-16173,Mtp3bSls=BJCM001_SLS,Mtp3bSlItu=BJCM001_SLC_1 (BJCM001_SLC_1 started tracking on CMA subscribe) dell",
    ">>> Total: 1 Alarms (0 Critical, 0 Major)",
    ]

    inputs = altk 
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_mgw_altk('')
        assert output[0] == '#MGW ALARM: FAIL'
    except StopIteration:
        return

def test_check_mgw_lgaevsrm(monkeypatch):
    lga = [
    "BJMGW01> lgaevsrm -s 20150801",
    "",
    "150819-06:03:02 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315",
    "Trying password from ipdatabase file: /gsn/coreUser/moshell//sitefiles/ipdatabase...",
    "Startdate=20150801.000000, Enddate=20150820.060303",
    ".....Get /c/logfiles/alarm_event/ALARM_LOG.xml /gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/alarmLog16315.xml ... OK",
    "Get /c/logfiles/alarm_event/EVENT_LOG.xml /gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/eventLog16315.xml ... OK",
    "Get /c/logfiles/availability/CELLO_AVAILABILITY2_LOG.xml /gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/availabilityLog16315.xml ... OK",
    "",
    "Parsing alarmLog...Done.",
    "Parsing eventLog...Done.",
    "Parsing availabilityLog...Done.",
    "======================================================================================================",
    "Timestamp (UTC)     Type  Merged Log Entry",
    "======================================================================================================",
    "2015-08-01 01:00:36 OTHR  ConfigVersionCreated BJMGW01 BC4001_NDP_6.4.0.0B R10A AXM10101/11 CV=Au_CXP9018138%6_R112A03_150801_0100 UP=CXP9018138/6_R112A03 NDP6400B (BC4001_NDP_6.4.0.0B, C13.0-EP4-2)",
    "2015-08-01 02:49:43 AL    w MTP3b Link Out of Service           Mtp3bSpItu=2-1208,Mtp3bSls=PMMGW01_SLS,Mtp3bSlItu=PMMGW01_SLC_1 (Paumalu MGw (SLC1) |   Mtp3bSl[froId=16  rpuId=47] RAISED op= dis, av=depFl, usage=IDLE, proc=N_INIT, link=FAIL----- NB: OOS, SUERM: AERM)",
    "2015-08-01 02:49:53 AL    * MTP3b Link Out of Service           Mtp3bSpItu=2-1208,Mtp3bSls=PMMGW01_SLS,Mtp3bSlItu=PMMGW01_SLC_1 (Paumalu MGw (SLC1) |   Mtp3bSl[froId=16  rpuId=47] RAISED op= dis, av=depFl, usage=IDLE, proc=N_INIT, link=FAIL----- NB: OOS, SUERM: AERM)",
    "2015-08-01 05:46:48 AL    w MTP3b Link Out of Service           Mtp3bSpItu=2-1208,Mtp3bSls=PMMGW01_SLS,Mtp3bSlItu=PMMGW01_SLC_0 (Paumalu MGw (SLC0) |   Mtp3bSl[froId=15  rpuId=47] RAISED op= dis, av=depFl, usage=IDLE, proc=N_INIT, link=FAIL----- NB: OOS, SUERM: AERM)",
    "2015-08-01 05:46:59 AL    * MTP3b Link Out of Service           Mtp3bSpItu=2-1208,Mtp3bSls=PMMGW01_SLS,Mtp3bSlItu=PMMGW01_SLC_0 (Paumalu MGw (SLC0) |   Mtp3bSl[froId=15  rpuId=47] RAISED op= dis, av=depFl, usage=IDLE, proc=N_INIT, link=FAIL----- NB: OOS, SUERM: AERM)",
    "2015-08-01 08:33:21 AL    M MTP3b Route Set Unavailable         Mtp3bSpItu=0-16173,Mtp3bSrs=SBMSC01_SRS (SBMSC01_SRS |  Mtp3bSrs[froId=23  rpuId=47] RAISED op= dis, cong=UNCONGESTED: RofMtp3bSRSStatusChange(2353): MTP_PAUSE_IND FROs:[SR:31:ok,SLS:10:ENBL])",
    ]

    inputs = lga 
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_mgw_lgaevsrm('')
        assert output[0] == '#MGW ALARM LOG: OK'
    except StopIteration:
        return

def test_check_mgw_st_pluginunit(monkeypatch):
    st = [
    "",
    "150819-06:05:01 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315",
    "===================================================================================",
    "Proxy  Adm State     Op. State     MO",
    "===================================================================================",
    " #188  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=10,PlugInUnit=1",
    " #214  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=11,PlugInUnit=1",
    " #225  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=12,PlugInUnit=1",
    " #236  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=13,PlugInUnit=1",
    " #952  0 (LOCKED)    1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=22,PlugInUnit=1",
    "#1261  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=6,PlugInUnit=1",
    "#1298  0 (LOCKED)    1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=7,PlugInUnit=1",
    "#1307  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=8,PlugInUnit=1",
    "#1335  1 (UNLOCKED)  1 (ENABLED)   Equipment=1,Subrack=MAIN,Slot=9,PlugInUnit=1",
    "===================================================================================",
    "Total: 23 MOs",
    ]

    inputs = st
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_mgw_st_pluginunit('')
        assert output[0] == '#MGW ST: OK'
    except StopIteration:
        return

def test_check_cvls(monkeypatch):
    cvls = [
    "BJMGW01> cvls",
    "",
    "150819-06:05:10 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315",
    "",
    "11 After_Subic_E1_Move_20140116           2014-01-16 03:40 CXP9018138/6_R112A03 NDP6400B standard    admin        none",
    "12 Before_ChangeBJCT_20140226             2014-02-26 04:28 CXP9018138/6_R112A03 NDP6400B standard    admin        none",
    "13 Before_Change_CsdGsmFhService_20140820 2014-08-20 06:01 CXP9018138/6_R112A03 NDP6400B standard    admin        none",
    "14 Au_CXP9018138%6_R112A03_150818_0100    2015-08-18 01:00 CXP9018138/6_R112A03 NDP6400B autocreate  CPP          Daily autocreated CV",
    "15 Au_CXP9018138%6_R112A03_150819_0100    2015-08-19 01:00 CXP9018138/6_R112A03 NDP6400B autocreate  CPP          Daily autocreated CV",
    "======================================================================================================================================",
    ">>> Total: 15 CV's, 1 UP's",
    ]

    inputs = cvls
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_mgw_cvls('')
        assert output[0] == '#MGW cvls: OK'
    except StopIteration:
        return

def test_check_mgw_pst(monkeypatch):
    pst = [
    "BJMGW01> pst",
    "",
    "150819-06:05:20 10.128.163.8 10.0r MGW_NODE_MODEL_C_1_12 stopfile=/tmp/16315",
    "Connecting to 10.128.163.8:56834 (CorbaSecurity=OFF, corba_class=2, java=1.6.0_26, jacoms=R80L06, jacorb=R80LX01)",
    "Trying file=/gsn/coreUser/moshell_logfiles/logs_moshell/tempfiles/20150819-060119_16289/ior16289",
    "**** Bootstrapping OK",
    "****",
    "",
    "$pmtester_pid = 16522",
    "",
    "================================================================================",
    "  PROXY  SCANNER-NAME                                                  STATE",
    "================================================================================",
    "      2  USERDEF.e1ttp.STATS                                           ACTIVE",
    "      3  USERDEF.Vc12Ttp.STATS                                         ACTIVE",
    "      4  USERDEF.Vc4Ttp.STATS                                          ACTIVE",
    "      5  USERDEF.os155spittp.STATS                                     ACTIVE",
    "      6  PerformanceIndicator                                          ACTIVE",
    "================================================================================",
    ">>> Total: 5 Scanners",
    ]

    inputs = pst
    input_generator = iter(inputs)
    monkeypatch.setattr('__builtin__.raw_input', lambda : next(input_generator))

    try:
        output = check_mgw_pst('')
        assert output[0] == '#MGW pst: OK'
    except StopIteration:
        return
