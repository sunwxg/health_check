from string import strip

def get_input():
    try:
        return raw_input()
    except EOFError:
        exit()

def print_preline():
    print '-' * 60

#<ioexp;
#EXCHANGE IDENTITY DATA

#IDENTITY
#BEIMSC 141/00/00/1  148

#END
def check_ioexp(input_str):
    while True:
        input_str = strip(get_input())
        if input_str == 'END':
            return
        elif input_str == 'IDENTITY':
            input_str = strip(get_input()).split(" ")[0]
            
            print_preline()
            print 'EXCHANGE IDENTITY:', input_str
        
    return

check_list = {
   '<ioexp;' : check_ioexp
}

def check_input(input_str):
    input_str = strip(input_str)
    if check_list.has_key(input_str):
        check_list[input_str](input_str)

def start_input():
    try:
        while True:
            input_str = raw_input()
            check_input(input_str)

    except EOFError:
        print_preline()
        print 'end of input'
        exit()

if __name__ == '__main__':
    start_input()
