from enum import Enum
from constants import PUBLIC_API_URL
import httpx

from httpx_responses.ticker_info_response import TickerInfoResponse
from httpx_responses.tradable_pairs_response import TradablePairsResponse

### ENUMS #################################################################
AssetPairInfo = Enum('AssetPairInfo', ['INFO', 'LEVERAGE', 'FEES', 'MARGIN'])

class MarketData:

    async def _get_market_api_response(self, endpoint, params=None):
        async with httpx.AsyncClient() as client:
            return await client.get(f'{PUBLIC_API_URL}{endpoint}', params=params)
    
    ### KRAKEN APIS ###########################################################

    # https://docs.kraken.com/rest/#tag/Market-Data/operation/getServerTime
    def get_server_time(self) -> httpx.Response:
        pass

    # https://docs.kraken.com/rest/#tag/Market-Data/operation/getSystemStatus
    def get_system_status(self) -> httpx.Response:
        """
        Get the current system status or trading mode. For a more detailed description, visit https://status.kraken.com/.

        Returns
        -------
        httpx.Response
            The `result` property will have one of four values: "online", "maintenance", "cancel_only", or "post_only"

        [Documentation](https://docs.kraken.com/rest/#tag/Market-Data/operation/getSystemStatus)
        """
        return self._get_market_api_response('SystemStatus')

    def get_asset_info(self, assets: list[str]=None, asset_class: str="currency") -> httpx.Response:
        """
        Get information about the assets that are available for deposit, withdrawal, trading and staking.
        If no assets are provided, information is returned for all assets on Kraken.

        Parameters
        ----------
        assets : list[str]
            List of asset symbols to get info on, by default None
                Example: `['XBT', 'ETH']`
        asset_class : str, optional
            Asset class, by default None

        Returns
        -------
        httpx.Response
            Information about the assets specified in request.
        
        [Documentation](https://docs.kraken.com/rest/#tag/Market-Data/operation/getAssetInfo)
        """        
        params = { 'aclass': asset_class }
        if assets:
            params['asset'] = ','.join(assets)
        return self._get_market_api_response('Assets', params)

    async def get_tradable_asset_pairs(self, pairs: list[str]=None, info: AssetPairInfo=AssetPairInfo.INFO) -> TradablePairsResponse:
        """
        Get data for tradable asset pairs. If no pairs are provided, information will be returned for
        all tradable asset pairs.

        Parameters
        ----------
        pairs : list[str]
            Asset pairs to get data for, by default []
                Example: `['BTC/USD', 'ETH/BTC']`
        info : AssetPairInfo, optional
            Info to retrieve, by default AssetPairInfo.INFO

        Returns
        -------
        TradablePairsResponse
            Information about the tradable asset pairs

        [Documentation](https://docs.kraken.com/rest/#tag/Market-Data/operation/getTradableAssetPairs)
        """
        params = { 'info': info.name.lower() }
        if pairs:
            params['pair'] = ','.join(pairs)
        response = await self._get_market_api_response('AssetPairs', params)
        return TradablePairsResponse(response)

    async def get_ticker_info(self, pairs: list[str]=None) -> TickerInfoResponse:
        """
        Gets detailed ticker information about an asset pair. 

        Note: Today's prices start at midnight UTC. Leaving the pair parameter blank will
        return tickers for all tradeable assets on Kraken.

        Parameters
        ----------
        pairs : list[str], optional
            Asset pairs to get data for, by default None

        Returns
        -------
        TickerInfoResponse
            Response with tickers' information.
        
        [Documentation](https://docs.kraken.com/rest/#tag/Market-Data/operation/getTickerInformation)
        """        
        params = { 'pair': ','.join(pairs) } if pairs else None
        response = await self._get_market_api_response('Ticker', params)
        return TickerInfoResponse(response)

    # https://docs.kraken.com/rest/#tag/Market-Data/operation/getOHLCData
    def get_ohlc_data():
        pass

    # https://docs.kraken.com/rest/#tag/Market-Data/operation/getOrderBook
    def get_order_book():
        pass

    # https://docs.kraken.com/rest/#tag/Market-Data/operation/getRecentTrades
    def get_recent_trades():
        pass

    # https://docs.kraken.com/rest/#tag/Market-Data/operation/getRecentSpreads
    def get_recent_spreads():
        pass

