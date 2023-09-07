from collections import defaultdict
import json
import os
import re

from dotenv import load_dotenv
from constants import ACCOUNT_DETAILS, KRAKEN_SYMBOL_MAP

from market_data import MarketData
from portfolio_manager import Portfolio, Asset
from user_data import UserData
from user_trading import OrderDirection, OrderType, UserTrading

load_dotenv()

PUBLIC_API_KEY = os.getenv('PUBLIC_KEY')
PRIVATE_API_KEY = os.getenv('PRIVATE_KEY')

API_URL = 'https://api.kraken.com'
API_PUBLIC_PATH = '/0/public/'
API_PRIVATE_PATH = '/0/private/'
PUBLIC_API_URL = f'{API_URL}{API_PUBLIC_PATH}'
PRIVATE_API_URL = f'{API_URL}{API_PRIVATE_PATH}'


md = MarketData()

resp = md.get_system_status()
if resp.json()['result']['status'] != 'online':
    print(f'System unavailable: {resp.json()["result"]["status"]}')
    exit

def transform_symbol(symbol):
    if symbol in KRAKEN_SYMBOL_MAP:
        return KRAKEN_SYMBOL_MAP[symbol]
    return symbol

ud = UserData()
assets = defaultdict(Asset)

## Get Kraken account balances
resp = ud.get_account_balance()
for symbol, balance in resp.json()['result'].items():
    # Quantity
    symbol = transform_symbol(symbol)
    print(f'{symbol} :\t{balance.rstrip("0")}')
    assets[symbol].symbol = symbol
    assets[symbol].quantity = float(balance)
    assets[symbol].account_id = ACCOUNT_DETAILS.id

print('~~~~~~~~~~~~~~~~~~~~~~~~~~')

def get_ticker_pair(symbol):
    # if symbol[0] in ['X', 'Z']:
    #     return f'{symbol}ZUSD'
    return f'{symbol}/USD'

def get_asset_symbol_from_pair(pair):
    symbol = re.sub(r'Z?USD$', '', pair)
    return transform_symbol(symbol)

# def parse_ticker_info(pairs):
#     return {f'{get_asset_symbol_from_pair(pair)}USD': info for pair, info in pairs.items()}

## Get current prices and update Asset objects
ticker_pairs = [get_ticker_pair(symbol) for symbol in assets.keys() if symbol != 'USD']
resp = md.get_ticker_info(ticker_pairs)
pairs_info = resp.json()['result']
total_bal = 0
for pair, buy_info in pairs_info.items():
    # Current price
    symbol = pair.split('/')[0]
    price = float(buy_info['a'][0])
    assets[symbol].last_price = price
    assets[symbol].initial_balance = assets[symbol].quantity * price
    total_bal += assets[symbol].initial_balance
    print(f'{symbol} :\t${assets[symbol].initial_balance:.2f}')

# Gotta populate info for USD
assets['USD'].last_price = 1.0
assets['USD'].initial_balance = assets['USD'].quantity / 1.003 # Consider fees (0.26% for me). If we spend our total balance, we'll overdraft when fees are applied. (SPEND * 1.0026 = Initial_Balance)
total_bal += assets['USD'].initial_balance
print(f'USD :\t${assets["USD"].initial_balance:.2f}')

print(f'Total: \t${total_bal:.2f}')
print('~~~~~~~~~~~~~~~~~~~~~~~~~')

portfolio = Portfolio(list(assets.values()), [ACCOUNT_DETAILS])
portfolio.invest_balanced(ACCOUNT_DETAILS.id)
# portfolio.print_categories(ACCOUNT_DETAILS.id)
portfolio.print_assets(ACCOUNT_DETAILS.id)

## Get info about tradable asset pairs (e.g. XXX/USD)
assets_to_buy = [a for a in portfolio.get_assets(ACCOUNT_DETAILS.id) if a.symbol != 'USD' and a.amount_invested != 0]
resp = md.get_tradable_asset_pairs([f'{a.symbol}/USD' for a in assets_to_buy])
pair_trade_info = resp.json()['result']

ut = UserTrading()

for asset in assets_to_buy:
    pair = f'{asset.symbol}/USD'
    buy_info = pair_trade_info[pair]

    ordermin = float(buy_info['ordermin']) # (in terms of base currency)
    costmin = float(buy_info['costmin']) # price * volume (in terms of quote currency)
    # precision = buy_info['pair_decimals']
    asset_price = float(pairs_info[pair]['a'][0])
    spend_amount = asset.amount_invested
    volume = spend_amount / asset_price

    if volume < ordermin:
        print(f'Could not order {asset} because volume is too small. ({volume} < {ordermin})')
        continue
    if spend_amount < costmin:
        print(f'Could not order {asset} because cost is too small. ({spend_amount} < {costmin}')
        continue
    ## place order
    print(f'Buy {volume:,.4f} {asset.symbol} @ ${asset_price:,.4f} for ${spend_amount:,.4f}')
    # resp = ut.add_order(OrderType.MARKET, OrderDirection.BUY, str(volume), pair, validate=True)
    print(json.dumps(resp.json(), indent=2))

# Welcome message

# What do you want to do?
## Show balance
## Invest cash
## Show open orders
## Other
