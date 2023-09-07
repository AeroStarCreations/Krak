from portfolio_manager import Portfolio
from constants import ACCOUNT_ID
from kraken_kontroller import add_orders
from ui.format_constants import *

from ui.input_output import get_float_from_user, get_yes_no_from_user, press_any_key_to_continue, print_header, print_with_basic_border, println

def _print_available_cash(available_cash: float):
    print_with_basic_border(f'Tradable cash: ${available_cash:,.2f}')

def _invest_portfolio(portfolio: Portfolio):
    total_cash = portfolio.get_cash_balance(ACCOUNT_ID)
    fees = 0.0026
    investable_cash = total_cash * (1.0 - fees)
    _print_available_cash(investable_cash)
    println('How much cash (USD) do you want to invest?')
    invest_amount = get_float_from_user(0.01, float(f'{investable_cash:.2f}'))
    portfolio.invest_balanced(ACCOUNT_ID, invest_amount - total_cash)

def _show_planned_trades(portfolio: Portfolio):
    println(B, 'Planned trades:\n')
    for a in portfolio.get_assets(ACCOUNT_ID):
        if a.amount_invested > 0:
            println(B, a.symbol, DE, f': \t${a.amount_invested:,.4f}')
    println()

def init_invest_menu(portfolio: Portfolio):
    print_header('Release the Kash!')
    _invest_portfolio(portfolio)
    _show_planned_trades(portfolio)
    ans = get_yes_no_from_user('Ready to submit trades?')
    if ans:
        ans = get_yes_no_from_user('Are you sure? These trades will be submitted immediately.')
        if ans:
            add_orders(portfolio)
    press_any_key_to_continue()
