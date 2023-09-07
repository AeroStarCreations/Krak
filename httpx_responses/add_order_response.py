from httpx import Response
from httpx_responses.kraken_response import KrakenResponse


class AddOrderResponse(KrakenResponse):
    def __init__(self, response: Response):
        super().__init__(response)
        if not self.isError:
            result = response.json()['result']
            self.result = AddOrderResult(result)

class AddOrderResult:
    def __init__(self, result: object):
        self.description: dict[str, str] = result['descr']
        self.transaction_ids: list[str] = result['txid'] if 'txid' in result else None