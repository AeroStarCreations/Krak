from enum import Enum

from constants import KRAKEN_SYMBOL_MAP


def transform_data_enum(val: Enum) -> str:
    return val.name.replace('_', '-').lower()

def transform_data_bool(val: bool):
    """
    There's an issue where passing a boolean value in a `data` object
    causes an API error response of `EAPI:Invalid key`. To avoid this,
    we can transform the booleans to strings as httpx would. I'm not
    100% sure why this works.
    httpx implementation: https://github.com/encode/httpx/blob/5b156dca7f3ec637b575708198f60a062109f141/httpx/_utils.py#L56C17-L56C17
    """
    return 'true' if val else 'false'

def get_display_symbol(symbol: str) -> str:
    return KRAKEN_SYMBOL_MAP[symbol] if symbol in KRAKEN_SYMBOL_MAP else symbol

def get_alt_symbol(symbol: str) -> str:
    return symbol[1:] if len(symbol) > 3 and symbol[0] in ['Z', 'X'] else symbol

def is_supernational(symbol) -> bool:
    return len(symbol) > 3 and symbol[0] == 'X'

def get_usd_quote_for_base(base: str) -> str:
    return 'ZUSD' if is_supernational(base) else 'USD'

def get_usd_ticker_from_symbol(symbol: str) -> str:
    return symbol + get_usd_quote_for_base(symbol)
