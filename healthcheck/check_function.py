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
    output_str = ['EXCHANGE IDENTITY: ']
    while True:
        input_str = strip(get_input())

        if input_str == 'END':
            return output_str

        elif input_str == 'IDENTITY':
            input_str = strip(get_input()).split(" ")[0]
            output_str[0] += input_str

#<dpwsp; 
#CP STATE
#
#MAU  SB SBSTATE      RPH-A       RPH-B       BUA STATE
#NRM  B  WO           -           -                   1
#
#END
def check_dpwsp(input_str):
    output_str = ['CP STATE: ']
    while True:
        input_str = strip(get_input()).split()
        if len(input_str) == 0:
            continue

        if input_str[0] == 'END':
            return output_str

        elif input_str[0]== 'MAU':
            input_str = strip(get_input()).split()
            if (input_str[0] == 'NRM') and (input_str[2] == 'WO'):
                output_str[0] += 'OK' 
            else:
                output_str[0] += 'FAIL: '+ input_str[0] + ' ' + input_str[2]

