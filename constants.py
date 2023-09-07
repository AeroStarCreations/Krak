from dotenv import load_dotenv
import os
from portfolio_manager import AccountDetails, Allocation, AllocationCategory

load_dotenv()

PUBLIC_API_KEY = os.getenv('PUBLIC_KEY')
PRIVATE_API_KEY = os.getenv('PRIVATE_KEY')

API_URL = 'https://api.kraken.com'
API_PUBLIC_PATH = '/0/public/'
API_PRIVATE_PATH = '/0/private/'
PUBLIC_API_URL = f'{API_URL}{API_PUBLIC_PATH}'
PRIVATE_API_URL = f'{API_URL}{API_PRIVATE_PATH}'

_ALLOCATION = (Allocation()
              .with_category(
                  AllocationCategory('Large Cap (1-10)')
                    .with_asset('XETH', 35)
                    .with_asset('XXBT', 35)
                    .with_asset('ADA', 5)
                    .with_asset('SOL', 5)
              ).with_category(
                  AllocationCategory('Mid Cap (11-50)')
                    .with_asset('MATIC', 5)
                    .with_asset('DOT', 5)
                    .with_asset('LINK', 5)
                    .with_asset('UNI', 5)
              ).with_category(
                  AllocationCategory('Other')
                    .with_asset('ZUSD', 0)
              )).verify()

ACCOUNT_ID = 'kraken'

ACCOUNT_DETAILS = AccountDetails(ACCOUNT_ID, 'Kraken', _ALLOCATION)

KRAKEN_SYMBOL_MAP = {
    'XBT': 'BTC',
    'XXBT': 'BTC',
    'XETH': 'ETH',
    'ZUSD': 'USD'
}

# https://support.kraken.com/hc/en-us/articles/360000381846-Cash-deposit-options-fees-minimums-and-processing-times-
KRAKEN_FIAT = [
    'ZUSD',
    'ZEUR',
    'ZCAD',
    'ZAUD',
    'ZGBP',
    'ZCHF',
    'ZJPY',
    'USD',
    'EUR',
    'CAD',
    'AUD',
    'GBP',
    'CHF',
    'JPY'
]