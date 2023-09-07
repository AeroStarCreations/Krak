from httpx import Response
from httpx_responses.kraken_response import KrakenResponse


class TradablePairsResponse(KrakenResponse):
    def __init__(self, response: Response):
        super().__init__(response)
        result = response.json()['result']
        self.result: dict[str, AssetPair] = { ticker: AssetPair(info) for ticker, info in result.items() }

class AssetPair:
    def __init__(self, info: object):
        self.altname: str = info['altname']
        self.websocket_name: str = info['wsname']
        self.asset_class_base: str = info['aclass_base']
        self.base: str = info['base']
        self.asset_class_quote: str = info['aclass_quote']
        self.quote: str = info['quote']
        self.pair_decimals: int = info['pair_decimals']
        self.cost_decimals: int = info['cost_decimals']
        self.lot_decimals: int = info['lot_decimals']
        self.lot_multiplier: int = info['lot_multiplier']
        self.leverage_buy: list[int] = info['leverage_buy']
        self.leverage_sell: list[int] = info['leverage_sell']
        self.fees_taker: list[PairFee] = [PairFee(fee) for fee in info['fees']]
        self.fees_maker: list[PairFee] = [PairFee(fee) for fee in info['fees_maker']]
        self.fee_volume_currency: str = info['fee_volume_currency']
        self.margin_call: int = info['margin_call']
        self.margin_stop: int = info['margin_stop']
        self.order_min: float = float(info['ordermin'])
        self.cost_min: float = float(info['costmin'])
        self.tick_size: str = info['tick_size']
        self.status: str = info['status']   # online, cancel_only, post_only, limit_only, reduce_only
        self.long_position_limit: int = info['long_position_limit'] if 'long_position_limit' in info else None
        self.short_position_limit: int = info['short_position_limit'] if 'short_position_limit' in info else None

class PairFee:
    def __init__(self, info: list):
        self.trade_volume: int = info[0]
        self.fee: float = info[1] / 100