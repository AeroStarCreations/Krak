from dataclasses import dataclass, field
from httpx_responses.tradable_pairs_response import AssetPair
from portfolio_manager import Asset

@dataclass
class PurchaseDetails:
    _asset: Asset
    ticker: str
    asset_pair: AssetPair
    price: float
    symbol: str = field(init=False)
    usd_value: float = field(init=False)

    def __post_init__(self):
        if self._asset:
            self.symbol = self._asset.symbol
            self.usd_value = self._asset.amount_invested