import base64
import hashlib
import hmac
import httpx
import json
import os
import time
from urllib.parse import urlencode
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

PUBLIC_API_KEY = os.getenv('PUBLIC_KEY')
PRIVATE_API_KEY = os.getenv('PRIVATE_KEY')

API_URL = 'https://api.kraken.com'
API_PUBLIC_PATH = '/0/public/'
API_PRIVATE_PATH = '/0/private/'
PUBLIC_API_URL = f'{API_URL}{API_PUBLIC_PATH}'
PRIVATE_API_URL = f'{API_URL}{API_PRIVATE_PATH}'

def _get_kraken_signature(urlpath, data):
    post_data = urlencode(data)
    nonce = data['nonce']
    encoded_data = (nonce + post_data).encode()
    hashed_data = hashlib.sha256(encoded_data).digest()
    message = urlpath.encode() + hashed_data
    decoded_private_key = base64.b64decode(PRIVATE_API_KEY)
    mac = hmac.new(decoded_private_key, message, hashlib.sha512).digest()
    signature_digest = base64.b64encode(mac).decode()
    return signature_digest

def _get_nonce():
    return str(time.time_ns())
    
def _get_user_api_response(endpoint, data):
    data.update({
        'nonce': _get_nonce()
    })
    headers = {
        'API-Key': PUBLIC_API_KEY,
        'API-Sign': _get_kraken_signature(f'{API_PRIVATE_PATH}{endpoint}', data)
    }
    return httpx.post(f'{PRIVATE_API_URL}{endpoint}', headers=headers, data=data)

def _get_market_api_response(endpoint, params):
    return httpx.get(f'{PUBLIC_API_URL}{endpoint}', params=params)

def get_account_balance():
    return _get_user_api_response('Balance', {})

def get_trade_balance(asset=None):
    data = { 'asset': asset } if asset else {}
    return _get_user_api_response('TradeBalance', data)

def get_asset_info(assets: list, asset_class='currency'):
    params = {
        'asset': ','.join(assets),
        'aclass': asset_class
    }
    return _get_market_api_response('Assets', params)

def get_ticker_info(pair=None):
    # Response details: https://docs.kraken.com/websockets/#message-ticker
    params = { 'pair': pair } if pair else None
    return _get_market_api_response('Ticker', params)

AssetPairInfo = Enum('AssetPairInfo', ['INFO', 'LEVERAGE', 'FEES', 'MARGIN'])

def get_asset_pair_info(pairs=['BTC/USD'], info: AssetPairInfo=AssetPairInfo.INFO):
    params = {
        'pair': ','.join(pairs),
        'info': info.name.lower()
    }
    return _get_market_api_response('AssetPairs', params)


resp = get_account_balance()
resp = get_asset_pair_info(['eth/usd'])

print(resp)
print('------------')
print(resp.text)
print('------------')
print(resp.content)
print('------------')
print(resp.url)
print('------------')
print(resp.headers)
print('------------')
print(resp.encoding)
print('------------')
print(json.dumps(resp.json(), indent=2))