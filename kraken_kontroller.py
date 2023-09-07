from dataclasses import dataclass
from portfolio_manager import Asset, Portfolio
from constants import ACCOUNT_DETAILS, ACCOUNT_ID, KRAKEN_FIAT
from httpx_responses.ticker_info_response import TickerInfo
from httpx_responses.tradable_pairs_response import AssetPair
from market_data import MarketData
import traceback
import trio
from purchase_details import PurchaseDetails
from ui.input_output import print_error, print_info, print_warning, println
from user_data import UserData
from user_trading import OrderDirection, OrderType, UserTrading
from utils import get_usd_ticker_from_symbol

_ud = UserData()
_md = MarketData()
_ut = UserTrading()
_portfolio: Portfolio = None
_ticker_info: dict[str, TickerInfo] = None
_tradable_asset_pairs: dict[str, AssetPair] = None
_portfolio_lock = trio.Lock()
_ticker_info_lock = trio.Lock()
_tradable_asset_pairs_lock = trio.Lock()
_is_test = False

class KrakenError(Exception):
    def __init__(self, msg: str, error: list[str]):
        super().__init__(msg, error)
        print_error(msg, error)
        self.msg = msg
        self.error = error

## API Calls ----------------------------------------------
async def _get_account_balance(result: dict):
    resp = await _ud.get_account_balance()
    if resp.isError:
        raise KrakenError('Could not get account balance from Kraken. Error message(s):', resp.error)
    result['_get_account_balance'] = resp.result

async def _assign_ticker_info():
    global _ticker_info
    if _ticker_info_lock.locked():
        await _ticker_info_lock.acquire()
        _ticker_info_lock.release()
        return
    await _ticker_info_lock.acquire()
    resp = await _md.get_ticker_info()
    if resp.isError:
        raise KrakenError('Could not get ticker info from Kraken. Error message(s): ', resp.error)
    _ticker_info = resp.result
    _ticker_info_lock.release()

async def _assign_tradable_asset_pairs():
    global _tradable_asset_pairs
    if _tradable_asset_pairs:
        return
    elif _tradable_asset_pairs_lock.locked():
        await _tradable_asset_pairs_lock.acquire()
        _tradable_asset_pairs_lock.release()
    else:
        await _tradable_asset_pairs_lock.acquire()
        resp = await _md.get_tradable_asset_pairs()
        if resp.isError:
            raise KrakenError('Could not retrieve asset pairs info from Kraken. Aborting trades.', resp.error)
        _tradable_asset_pairs = resp.result
        _tradable_asset_pairs_lock.release()


async def _submit_validated_trade(ticker: str, volume: float):
    response = await _ut.add_order(OrderType.MARKET, OrderDirection.BUY, str(volume), ticker, validate=_is_test)
    if response.isError:
        print_error(f'Could not order {ticker}.', response.error)
        return
    if not response.result.transaction_ids:
        print_info('Note: This order is a test, not real.')
    println('SUCCESS! ', ticker)
    for key, msg in response.result.description.items():
        println(key, ': ', msg)
    println()

#----------------------------------------------------------
def _create_asset(symbol: str, quantity: float, price: float) -> Asset:
    asset = Asset()
    asset.symbol = symbol #get_display_symbol(symbol)
    asset.quantity = quantity
    asset.account_id = ACCOUNT_ID
    asset.last_price = price
    asset.initial_balance = asset.last_price * asset.quantity
    return asset

def _get_assets(acct_balance: dict[str, float]) -> list[Asset]:
    assets: list[Asset] = []
    for symbol, quantity in acct_balance.items():
        if symbol == 'ZUSD':
            continue
        ticker = get_usd_ticker_from_symbol(symbol)
        info = _ticker_info[ticker]
        assets.append(_create_asset(symbol, quantity, float(info.bid[0])))
    assets.append(_create_asset('ZUSD', acct_balance['ZUSD'], 1.0))
    return assets

async def _assign_portfolio():
    global _portfolio
    # if _portfolio:
    #     return
    if _portfolio_lock.locked():
        await _portfolio_lock.acquire()
        _portfolio_lock.release()
        return
    await _portfolio_lock.acquire()
    results = {}
    async with trio.open_nursery() as nursery:
        nursery.start_soon(_get_account_balance, results)
        nursery.start_soon(_assign_ticker_info)
    acct_balance = results['_get_account_balance']
    assets = _get_assets(acct_balance)
    _portfolio = Portfolio(assets, [ACCOUNT_DETAILS])
    _portfolio_lock.release()

async def _get_purchase_details(portfolio: Portfolio) -> dict[str, PurchaseDetails]:
    assets_to_buy = [a for a in portfolio.get_assets(ACCOUNT_ID) if a.symbol != 'ZUSD' and a.amount_invested > 0]
    pds: dict[str, PurchaseDetails] = {}
    async with trio.open_nursery() as nursury:
        nursury.start_soon(_assign_tradable_asset_pairs)
        nursury.start_soon(_assign_ticker_info)
    for a in assets_to_buy:
        ticker = get_usd_ticker_from_symbol(a.symbol)
        pds[ticker] = PurchaseDetails(a, ticker, _tradable_asset_pairs[ticker], float(_ticker_info[ticker].bid[0]))
    return pds

async def _validate_and_submit_trades(purchase_details: list[PurchaseDetails]):
    async with trio.open_nursery() as nursery:
        for pd in purchase_details:
            volume = pd.usd_value / pd.price
            if pd.asset_pair.status not in ['online', 'post_only']: # Validate ticker status
                print_warning(f'Could not buy {pd.symbol} because Kraken status is \"{pd.asset_pair.status}\".')
            elif pd.usd_value < pd.asset_pair.cost_min: # Validate minimum cost
                print_warning(f'Could not buy {pd.symbol} because ${pd.usd_value:,.{pd.asset_pair.pair_decimals}f} is less than required ${pd.asset_pair.cost_min:,.{pd.asset_pair.pair_decimals}f}')
            elif volume < pd.asset_pair.order_min: # Validate minimum order
                print_warning(f'Could not buy {pd.symbol} because quantity {volume:,.4f} is less than required {pd.asset_pair.order_min:,f}')
            else:
                nursery.start_soon(_submit_validated_trade, pd.ticker, volume)

###########################################################
def get_portfolio() -> Portfolio:
    global _portfolio
    # if _portfolio:
    #     return _portfolio
    try:
        trio.run(_assign_portfolio)
    except KrakenError as e:
        print(e.msg, e.error)
    except Exception as e:
        traceback.print_exc()
    finally:
        return _portfolio
    
def add_orders(portfolio: Portfolio):
    purchase_details: dict[str, PurchaseDetails] = trio.run(_get_purchase_details, portfolio)
    trio.run(_validate_and_submit_trades, purchase_details.values())
