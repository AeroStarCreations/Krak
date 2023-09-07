import base64
import hashlib
import hmac
import time
from urllib.parse import urlencode

import httpx

from constants import API_PRIVATE_PATH, PRIVATE_API_KEY, PRIVATE_API_URL, PUBLIC_API_KEY


class PrivateAPI:
    def _get_kraken_signature(self, urlpath, data):
        post_data = urlencode(data)
        nonce = data['nonce']
        encoded_data = (nonce + post_data).encode()
        hashed_data = hashlib.sha256(encoded_data).digest()
        message = urlpath.encode() + hashed_data
        decoded_private_key = base64.b64decode(PRIVATE_API_KEY)
        mac = hmac.new(decoded_private_key, message, hashlib.sha512).digest()
        signature_digest = base64.b64encode(mac).decode()
        return signature_digest

    def _get_nonce(self):
        return str(time.time_ns())
    
    async def _get_private_api_response(self, endpoint, data={}) -> httpx.Response:
        data.update({
            'nonce': self._get_nonce()
        })
        headers = {
            'API-Key': PUBLIC_API_KEY,
            'API-Sign': self._get_kraken_signature(f'{API_PRIVATE_PATH}{endpoint}', data)
        }
        resp = None
        async with httpx.AsyncClient() as client:
            resp = await client.post(f'{PRIVATE_API_URL}{endpoint}', headers=headers, data=data)
        return resp
    