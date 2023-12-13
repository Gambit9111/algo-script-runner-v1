from pybit.unified_trading import HTTP
import pandas as pd
from binance.spot import Spot
from datetime import datetime, timedelta

def ask_bid(session: HTTP, symbol: str) -> tuple:
    """
    _description_
    generate latest ask and bid prices for a given symbol

    Args:
        session (HTTP): bybit http session
        symbol (str): trading pair

    Returns:
        tuple: returns a tuple of ask and bid prices
    """
    
    
    ob = session.get_orderbook(category="spot", symbol=symbol)
    
    ask = float(ob['result']['a'][0][0])
    bid = float(ob['result']['b'][0][0])
    
    # print(f"Ask: {ask}")
    # print(f"Bid: {bid}")
    
    return ask, bid

def get_wallet_balance(session: HTTP) -> tuple:
    """
    _description_
    get wallet balance

    Args:
        session (HTTP): bybit http session

    Returns:
        float: returns wallet balance and unrealized pnl
    """
    
    wallet = session.get_wallet_balance(accountType="UNIFIED")
    
    total_wallet_balance = round(float(wallet['result']['list'][0]['totalWalletBalance']), 2)
    unrealized_pnl = round(float(wallet['result']['list'][0]['coin'][0]['unrealisedPnl']), 2)
    
    

    # print(f"Wallet Balance: {total_wallet_balance} $")
    # print(f"Unrealized PnL: {unrealized_pnl} $")

    
    return total_wallet_balance, unrealized_pnl

def buy_spot_limit(session: HTTP, symbol: str, qty: float, price: float, price_decimals: int) -> None:
    spot_limit = session.place_order(
        category="spot",
        symbol=symbol,
        side="Buy",
        orderType="Limit",
        qty=qty,
        price=round(price, price_decimals),
        timeInForce="PostOnly",
    )
    print(f"buy spot limit @ {price}, qty: {qty}")

def open_long_position(session: HTTP, symbol: str, orderType: str, qty: float, price: float) -> None:
    """ open a long position
    Args:
        session (HTTP): _description_
        symbol (str): _description_
        orderType (str): _description_
        qty (float): _description_
        price (float): _description_
    """
    long_position = session.place_order(
        category="linear",
        symbol=symbol,
        side="Buy",
        orderType=orderType,
        qty=qty,
        price=price,
        reduceOnly=False,
    )
    print(f"open long position @ {price}, qty: {qty}")
    # print(long_position)

def close_long_position(session: HTTP, symbol: str, orderType: str, qty: float, price: float) -> None:
    """ close a long position
    Args:
        session (HTTP): _description_
        symbol (str): _description_
        orderType (str): _description_
        qty (float): _description_
        price (float): _description_
    """
    long_position = session.place_order(
        category="linear",
        symbol=symbol,
        side="Sell",
        orderType=orderType,
        qty=qty,
        price=price,
        reduceOnly=True,
    )
    print(f"close long position @ {price}, qty: {qty}")
    # print(long_position)

def close_long_position_market(session: HTTP, symbol: str, qty: float) -> None:
    """ close a long position
    Args:
        session (HTTP): _description_
        symbol (str): _description_
        orderType (str): _description_
        qty (float): _description_
        price (float): _description_
    """
    long_position = session.place_order(
        category="linear",
        symbol=symbol,
        side="Sell",
        orderType="Market",
        qty=qty,
    )
    print(f"close long position @ market, qty: {qty}")
    # print(long_position)

def sell_spot_limit(session: HTTP, symbol: str, qty: float, price: float, price_decimals: int) -> None:
    spot_limit = session.place_order(
        category="spot",
        symbol=symbol,
        side="Sell",
        orderType="Limit",
        qty=qty,
        price=round(price, price_decimals),
        timeInForce="PostOnly",
    )
    print(f"sell spot limit @ {price}, qty: {qty}")

def sell_spot_market(session: HTTP, symbol: str, qty: float) -> None:
    spot_market = session.place_order(
        category="spot",
        symbol=symbol,
        side="Sell",
        orderType="Market",
        qty=qty,
    )
    print(f"sell spot market, qty: {qty}")

def cancel_all_orders(session: HTTP, category: str, symbol: str) -> None:
    """ cancel all orders
    Args:
        session (HTTP): _description_
        category (str): _description_
        symbol (str): _description_
    """
    session.cancel_all_orders(
        category=category,
        symbol=symbol,
    )
    print("Successfully cancelled all orders")

def get_coin_balance(session: HTTP, coin: str) -> float:
    """ get coin balance
    Args:
        session (HTTP): _description_
        symbol (str): _description_
    Returns:
        float: _description_
    """
    wallet = session.get_wallet_balance(
    accountType="UNIFIED",
    coin=coin,
    )
    
    # print(wallet['result']['list'][0]['coin'][0])
    
    coin_balance = round(float(wallet['result']['list'][0]['coin'][0]['walletBalance']), 2)
    coin_balance_left = round(float(wallet['result']['list'][0]['coin'][0]['availableToWithdraw']), 4)
    
    print(f"Coin Balance: {coin_balance} {coin}")
    print(f"Coin Balance Left: {coin_balance_left} {coin}")
    
    return coin_balance, coin_balance_left

def get_data(binance_client: Spot, symbol: str, interval: str, limit: int) -> pd.DataFrame:
   df = pd.DataFrame(binance_client.klines(symbol=symbol, interval=interval, limit=limit))
   df = df.iloc[:, :9]
   df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_av', 'Trades']

   # drop unnecessary columns
   df = df.drop(['Close_time', 'Quote_av', 'Trades'], axis=1)

   # convert to datetime
   df['Time'] = pd.to_datetime(df['Time'], unit='ms')

   # set index
   df = df.set_index('Time')
   # convert to float
   df = df.astype(float)

   return df

def calculate_atr(df, period):
 high_low = df['High'] - df['Low']
 high_close = abs(df['High'] - df['Close'].shift())
 low_close = abs(df['Low'] - df['Close'].shift())
 ranges = pd.concat([high_low, high_close, low_close], axis=1)
 true_range = ranges.max(axis=1)
 atr = true_range.ewm(span=period, adjust=False).mean()
 return atr

def calculate_keltner_channels(df, period, multiplier):
 ema = df['Close'].ewm(span=period, adjust=False).mean()
 atr = calculate_atr(df, period)
 upper_channel = ema + multiplier * atr
 lower_channel = ema - multiplier * atr
 return ema, upper_channel, lower_channel


def get_current_position(session: HTTP, symbol: str) -> tuple:
    """ get current position information
    Args:
        session (HTTP): _description_
        symbol (str): _description_
        
    Returns:
        current_position_symbol (str): _description_
        current_position_average_entry_price (float): _description_
        current_position_market_price (float): _description_
        current_position_qty (float): _description_
        current_position_side (str): _description_
        current_position_leverage (int): _description_
        current_position_liq_price (float): _description_
        current_position_unrealised_pnl (float): _description_
        current_position_created_time (str): _description_
        current_position_updated_time (str): _description_
    """
    position = session.get_positions(
        category="linear",
        symbol=symbol,
    )
    
    current_position_symbol = position['result']['list'][0]['symbol']
    current_position_average_entry_price = float(position['result']['list'][0]['avgPrice'])
    current_position_market_price = float(position['result']['list'][0]['markPrice'])
    current_position_qty = float(position['result']['list'][0]['size'])
    current_position_side = position['result']['list'][0]['side']
    current_position_leverage = int(position['result']['list'][0]['leverage'])
    current_position_liq_price = position['result']['list'][0]['liqPrice']
    current_position_unrealised_pnl = position['result']['list'][0]['unrealisedPnl']
    # we calculate time in utc-5 (new york time)
    current_position_created_time = (datetime.utcfromtimestamp(int(position['result']['list'][0]['createdTime']) / 1000) - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
    current_position_updated_time = (datetime.utcfromtimestamp(int(position['result']['list'][0]['updatedTime']) / 1000) - timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')
    
    
    # print(f"Current position symbol: {current_position_symbol}")
    # print(f"Current position average entry price: {current_position_average_entry_price}")
    # print(f"Current position market price: {current_position_market_price}")
    # print(f"Current position qty: {current_position_qty}")
    # print(f"Current position side: {current_position_side}")
    # print(f"Current position leverage: {current_position_leverage}")
    # print(f"Current position liq price: {current_position_liq_price}")
    # print(f"Current position unrealised pnl: {current_position_unrealised_pnl}")
    # print(f"Current position created time: {current_position_created_time}")
    # print(f"Current position updated time: {current_position_updated_time}")
    
    # print(position['result'])
    
    return current_position_symbol, current_position_average_entry_price, current_position_market_price, current_position_qty, current_position_side, current_position_leverage, current_position_liq_price, current_position_unrealised_pnl, current_position_created_time, current_position_updated_time