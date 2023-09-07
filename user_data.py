from enum import Enum

from httpx import Response

from constants import API_PRIVATE_PATH, PRIVATE_API_KEY, PRIVATE_API_URL, PUBLIC_API_KEY
from httpx_responses.account_balance_response import AccountBalanceResponse
from private_api import PrivateAPI
from utils import transform_data_bool

### ENUMS #################################################################
CloseTime = Enum('CloseTime', ['BOTH', 'OPEN', 'CLOSE'])

class UserData(PrivateAPI):

    ### KRAKEN APIS ###########################################################

    async def get_account_balance(self) -> AccountBalanceResponse:
        """
        Retrieve all cash balances, net of pending withdrawals

        Returns
        -------
        AccountBalanceResponse
            The response will contains balances for all account assets ('result') and/or an array of errors ('error')

        [Documentation](https://docs.kraken.com/rest/#tag/User-Data/operation/getAccountBalance)
        """
        response = await self._get_private_api_response('Balance')
        return AccountBalanceResponse(response)

    def get_trade_balance(self, asset: str='ZUSD') -> Response:
        """
        Retrieve a summary of collateral balances, margin position valuations, equity, and margin level.

        Parameters
        ----------
        asset : str, optional
            Base asset used to determine balance, by default 'ZUSD'

        Returns
        -------
        httpx.Response
            Result containing the summary

        [Documentation](https://docs.kraken.com/rest/#tag/User-Data/operation/getTradeBalance)
        """        
        data = { 'asset': asset }
        return self._get_private_api_response('TradeBalance', data)

    def get_open_orders(self, include_trades: bool=False, userref: int=None) -> Response:
        """
        Retreive information about current open orders.

        Parameters
        ----------
        include_trades : bool, optional
            Whether or not to include trades related to position in output, by default False
        userref : int, optional
            Restrict results to given user reference ID, by default None

        Returns
        -------
        httpx.Response
            Response containing 'result' and 'error'

        [Documentation](https://docs.kraken.com/rest/#tag/User-Data/operation/getOpenOrders)
        """        
        data = {
            'trades': transform_data_bool(include_trades)
        }
        if userref:
            data['userref'] = userref
        return self._get_private_api_response('OpenOrders', data)
    
    def get_closed_orders(self, include_trades: bool=False, userref: int=None, start: int=None, end: int=None, ofs: int=None, closetime: CloseTime=CloseTime.BOTH) -> Response:
        data = {
            'trades': transform_data_bool(include_trades),
            'closetime': closetime.name.lower()
        }
        if userref:
            data['userref'] = userref
        if start:
            data['start'] = start
        if end:
            data['end'] = end
        if ofs:
            data['ofs'] = ofs
        return self._get_private_api_response('ClosedOrders', data)
    
    def query_orders_info(self):
        pass
    
    def get_trades_history(self):
        pass
    
    def query_trades_info(self):
        pass
    
    def get_open_positions(self):
        pass
    
    def get_ledgers_info(self):
        pass
    
    def query_ledgers(self):
        pass
    
    def get_trade_volume(self):
        pass
    
    def request_export_report(self):
        pass
    
    def get_expoert_report_status(self):
        pass
    
    def retrieve_data_export(self):
        pass
    
    def delete_export_report(self):
        pass
    