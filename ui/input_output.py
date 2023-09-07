from builtins import print as _print
import os
from ui.format_constants import *
import re


def CFG(id: int):    # Custom foreground color
    assert id >= 0 and id <= 255
    return f'\033[38;5;{id}m'

def CBG(id: int):    # Custom background color
    assert id >= 0 and id <= 255
    return f'\033[48;5;{id}m'

def RGBFG(r: int, g: int, b: int): # RGB foreground
    for x in [r, g, b]:
        assert x >= 0 and x <= 255
    return f'\033[38;2;{r};{g};{b}m'

def RGBBG(r: int, g: int, b: int): # RGB background
    for x in [r, g, b]:
        assert x >= 0 and x <= 255
    return f'\033[48;2;{r};{g};{b}m'

def to_string(*args):
    return ''.join(map(str, args))

def print(*args, line_end=''):
    _print(f'{RE}{to_string(*args)}{RE}', end=line_end)

def println(*args):
    print(*args, line_end='\n')

def true_len(string):
    # Credit: https://stackoverflow.com/a/68635860
    return len(re.sub(r'[\u001B\u009B][\[\]()#;?]*((([a-zA-Z\d]*(;[-a-zA-Z\d\/#&.:=?%@~_]*)*)?\u0007)|((\d{1,4}(?:;\d{0,4})*)?[\dA-PR-TZcf-ntqry=><~]))', '', string))

# _____________________________________
# \`»«´/-------------------------\`»«´/
#  \`´/–––––––––--––––––––––––––––\`´/ 
#   ||  Salut! Je m'appele Nazza!  ||  
#    \\---------------------------//  
#     ``-------------------------´´  
def print_header(msg):
    os.system('clear')
    msg_len = true_len(msg)
    println(CFG(32), B, '_' * (msg_len + 12))
    println(CFG(68), B, '\`»«´/' + '-' * msg_len + '\`»«´/')
    println(CFG(104), B, ' \`´/-' + '-' * msg_len + '-\`´/')
    println(CFG(140), B, '  ||  ', CFG(39), msg, CFG(140), '  ||  ')
    println(CFG(176), B, '   \\\\-' + '-' * msg_len + '-//')
    println(CFG(212), B, '    ``' + '-' * msg_len + '´´')
    println()

def print_with_basic_border(*args: str):
    length = true_len(to_string(*args))
    border = [BU, '»', '-' * (2 + length), '«']
    println(*border)
    println(BU, B, '| ', *args, DE, BU, ' |')
    println(*border, '\n')

def get_user_input(msg=''):
    if msg and not re.match(r'.*\s+$', msg):
        msg += ' '
    i = input(f'{CFG(140)}{B}{F}{msg}❯ {RE}')
    println()
    return i

def press_any_key_to_continue():
    get_user_input(f'\n{I}Press any key to continue')

def print_error(msg: str, errors: list[str]):
    println(R, B, msg, errors)

def print_warning(msg: str):
    println(Y, B, msg)

def print_info(msg):
    println(BU, B, msg)

def get_menu_action_choice(menu: dict):
    while True:
        println(G, 'Select an action:')
        for k,v in menu.items():
            println(BU, f' {k}', RE, ') ', v)
        println()

        while True:
            user_input = get_user_input()

            if user_input not in menu.keys():
                println(Y, f'Uh-oh! \"{user_input}\" is invalid. Please enter a valid option. (e.g. \"{list(menu.keys())[0]}\")\n')
            else:
                println(f'You selected \"{menu[user_input]}\"')
                return user_input
            
def get_float_from_user(min: float=None, max: float=None) -> float:
    while True:
        user_input = None
        try:
            user_input = float(get_user_input())
            if user_input < min:
                print_warning(f'Value must be greater than or equal to {min}, was \"{user_input}\"')
            elif user_input > max:
                print_warning(f'Value must be less than or equal to {max}, was \"{user_input}\"')
            else:
                return user_input
        except ValueError:
            user_input = '' if not user_input else user_input
            print_warning(f'Value must be a number, was \"{user_input}\"')

def get_yes_no_from_user(msg: str) -> bool:
    while True:
        println(msg)
        user_input = get_user_input('(y/n)')
        if user_input.lower() in ['y', 'yes']:
            return True
        elif user_input.lower() in ['n', 'no']:
            return False
        else:
            print_warning('Could not interpret user input. Enter \"y\", \"n\", \"yes\", or \"no\"')