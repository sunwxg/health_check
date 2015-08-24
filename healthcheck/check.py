from string import strip

#<ioexp;
#EXCHANGE IDENTITY DATA

#IDENTITY
#BEIMSC 141/00/00/1  148

#END
def check_ioexp(input_str):
    print 'in fun_ioexp'
    return

check_list = {
   '<ioexp;' : check_ioexp
}

def check_input(input_str):
    input_str = strip(input_str)
    if check_list.has_key(input_str):
        check_list[input_str](input_str)

def get_input():
    try:
        while True:
            input_str = raw_input()
            check_input(input_str)

    except EOFError:
        print 'end of input'
        exit();

if __name__ == '__main__':
    get_input()
