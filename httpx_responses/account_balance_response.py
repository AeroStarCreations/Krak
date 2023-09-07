from httpx import Response
from httpx_responses.kraken_response import KrakenResponse


class AccountBalanceResponse(KrakenResponse):
    def __init__(self, response: Response):
        super().__init__(response)
        json = response.json()
        self.result: dict[str, float] = { asset: float(quantity) for asset, quantity in json['result'].items() }