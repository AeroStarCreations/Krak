from dataclasses import dataclass, field
from constants import KRAKEN_FIAT
from data_display.header import DataType
from data_display.table import Table
from data_display.table_printer import print_table
from market_data import MarketData
from ui.format_constants import *
from ui.input_output import get_user_input, print_header, print_with_basic_border, println
from user_data import UserData
from utils import get_display_symbol
from portfolio_manager import Portfolio

# Inspo: https://www.dataquest.io/blog/how-to-use-python-data-classes/
@dataclass(order=True)
class _Balance:
    usd_value: float = field(init=False, repr=False) # also used first when sorting
    symbol: str
    quantity: str
    bid: str = '1.0'
    usd_value_str: str = field(init=False, repr=False)

    def __post_init__(self):
        self.usd_value = float(self.quantity) * float(self.bid)
        self.usd_value_str = f'{self.usd_value:,.4f}'
            

def _get_longest_len(items: list[str]) -> int:
    return len(max(items, key=len))

def _print_total_usd_value(total: float):
    msg = [DE, 'Portfolio value: ', G, '$', DE, f'{total:,.2f}']
    print_with_basic_border(*msg)

def _print_asset_table(balances: list[_Balance], total: float):
    asset_h = 'Asset'
    quantity_h = 'Quantity'
    usd_h = 'USD Value'
    percent_h = 'Allocation'
    longest_symbol = max(_get_longest_len([b.symbol for b in balances]), len(asset_h))
    longest_quantity = max(_get_longest_len([b.quantity for b in balances]), len(quantity_h))
    longest_usd = max(_get_longest_len([b.usd_value_str for b in balances]), len(usd_h))
    row_length = 12 + longest_symbol + longest_quantity + longest_usd + len(percent_h)
    divider = [BU, ' | ', DE]
    println(B, f' {asset_h:^{longest_symbol}}', *divider, f'{quantity_h:^{longest_quantity}}', *divider, f'{usd_h:>{longest_usd+1}}', *divider, f'{percent_h}')
    println(BU, '=' * row_length)
    for b in balances:
        percent = f'{b.usd_value/total*100:5.2f} %'
        println(f' {b.symbol:^{longest_symbol}}', *divider, f'{b.quantity:^{longest_quantity}}', *divider, f'${b.usd_value_str:>{longest_usd}}', *divider, f'{percent:^{len(percent_h)}}')
        println(BU, '-' * row_length)

def _print_portfolio(balances: list[_Balance]):
    total = sum([b.usd_value for b in balances])
    _print_total_usd_value(total)
    _print_asset_table(balances, total)

def _is_supernational(symbol) -> bool:
    return len(symbol) > 3 and symbol[0] == 'X'

def _get_quote_for_base(base: str) -> str:
    return 'ZUSD' if _is_supernational(base) else 'USD'

def _get_tickers(symbols: list[str]) -> dict:
    ticks = dict()
    for base in symbols:
        if base in KRAKEN_FIAT:
            continue
        quote = _get_quote_for_base(base)
        ticker = base + quote
        ticks[ticker] = {
            'base': base,
            'quote': quote
        }
    return ticks

def init_balance():
    print_header('Kraken Portfolio')

    ud = UserData()
    resp = ud.get_account_balance().json()
    # test_data = {
    #     'XXBT': '0.0176815100',
    #     'XETH': '0.3671252900',
    #     'ZUSD': '250.0578',
    #     'DOT': '14.7500000000',
    #     'LINK': '44.7910000000',
    #     'UNI': '46.1140000000',
    #     'MATIC': '552.2000000000',
    #     'SOL': '3.9545751000',
    #     'ADA': '632.70000000',
    # }

    if resp['error']:
        println(R, 'There was an error: ', resp['error'])
        return

    account_balance = resp['result']
    symbols = list(account_balance.keys())
    tickers = _get_tickers(symbols)

    balances: list[_Balance] = list()

    md = MarketData()
    resp = md.get_ticker_info(tickers.keys())
    if resp.json()['error']:
        println(R, 'There was an error getting ticker info: ', resp.json()['error'])
        return
    
    for ticker,info in resp.json()['result'].items():
        base = tickers[ticker]['base']
        display_symbol = get_display_symbol(base)
        quantity = account_balance[base].rstrip('0')
        bid = info['b'][0]
        balances.append(_Balance(display_symbol, quantity, bid))

    for base, quantity in account_balance.items():
        if base in KRAKEN_FIAT:
            balances.append(_Balance(base[1:], quantity.rstrip('0')))

    balances.sort(reverse=True)

    _print_portfolio(balances)

    get_user_input(f'\n{I}Press any key to continue')

# table = (Table()
#              .with_header('Asset')
#              .with_header('Quantity', DataType.NUMBER)
#              .with_header('USD Value', DataType.DOLLAR)
#              .with_header('Allocation', DataType.PERCENT))
#     for b in balances:
#         table.add_row([b.symbol, b.quantity, b.usd_value, b.usd_value/total])
#     print_table(table)
