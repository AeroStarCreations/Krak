from httpx import Response
from httpx_responses.kraken_response import KrakenResponse


class TickerInfoResponse(KrakenResponse):
    def __init__(self, response: Response):
        super().__init__(response)
        result = response.json()['result']
        self.result: dict[str, TickerInfo] = { ticker: TickerInfo(info) for ticker,info in result.items() }


class TickerInfo:
    base: str = None
    quote: str = None

    def __init__(self, ticker_info: object):
        self.ask = ticker_info['a']
        self.bid = ticker_info['b']
        self.last_trade_closed = ticker_info['c']
        self.volume = ticker_info['v']
        self.volume_weighted_avg_price = ticker_info['p']
        self.number_of_trades = ticker_info['t']
        self.low = ticker_info['l']
        self.high = ticker_info['h']
        self.todays_opening_price = ticker_info['o']