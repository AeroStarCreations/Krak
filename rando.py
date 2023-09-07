import httpx

from ui.format_constants import *
from ui.input_output import print_with_basic_border

#----------------------------------------------------------------
# resp = httpx.get('https://api.kraken.com/0/public/AssetPairs')

# j = resp.json()['result']

# def alt(symbol):
#     return symbol[1:] if len(symbol) > 3 and symbol[0] in ['Z', 'X'] else symbol

# for k,v in j.items():
#     base = alt(v['base'])
#     quote = alt(v['quote'])
#     print(f'{k} : {v["altname"]} : {base} : {quote}')
#     assert v['altname'] == base + quote

# LEARNINGS:
# 'altname' values have a clear pattern, unlike classic tickers (e.g. XXBTZUSD).
# Trimming one (1) 'X' and 'Z' from the front of 'base' and 'quote' values
# with length > 4 results in a valid 'altname' when combined.

#----------------------------------------------------------------

# msg = [DE, 'Portfolio value: ', G, '$', DE, f'{3022.859273:,.2f}']
# print_with_basic_border(*msg)

#----------------------------------------------------------------

bob = 3