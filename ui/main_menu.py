from constants import ACCOUNT_ID
from kraken_kontroller import get_portfolio
from ui.format_constants import *
from ui.input_output import (get_menu_action_choice, press_any_key_to_continue, print_header, println)
from ui.invest_menu import init_invest_menu

menu_options = {
    '1': 'Show wallet',
    '2': 'Trade cash',
    '3': 'Show open orders',
    'q': 'Quit'
}

def init_main_menu():
    print_header('The Kraken has been released!')

    while True:
        choice = get_menu_action_choice(menu_options)

        match choice:
            case '1':
                get_portfolio().print_assets_summary(ACCOUNT_ID)
                press_any_key_to_continue()
            case '2':
                init_invest_menu(get_portfolio())
            case '3':
                pass
            case _:
                println('\nA bientot!')
                break