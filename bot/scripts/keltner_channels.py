from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
import sys
from pybit.unified_trading import HTTP
import os
import math
# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add the parent directory to the sys.path
sys.path.append(parent_dir)
# Now you can import the module
from config import bybit_session
from functions import ask_bid, buy_spot_limit, sell_spot_limit, sell_spot_market, cancel_all_orders, get_coin_balance, get_data, calculate_atr, calculate_keltner_channels, get_current_position, open_long_position, close_long_position_market
from binance.spot import Spot
import numpy as np

spot = Spot()

symbol = str(sys.argv[1]) # "BTC3LUSDT"
interval = str(sys.argv[2]) # "BTC3LUSDT"
limit = 1000
trading_timer = int(sys.argv[3]) # "BTC3LUSDT"
qty = int(sys.argv[4])

def job():

    frame = get_data(spot, symbol, interval, limit)
    frame['EMA'], frame['Upper_Channel'], frame['Lower_Channel'] = calculate_keltner_channels(frame, 20, 2)

    # Initialize buy and sell signals
    frame['Signal'] = 0.0

    # Create signals
    frame['Signal'][1:] = np.where(frame['Close'][1:] > frame['Upper_Channel'][1:], 1.0, 0.0) 
    frame['Signal'] = frame['Signal'].diff()

    # Create buy and sell signals
    frame['Buy_Signal'] = np.where(frame['Signal'] == 1.0, frame['Close'], np.nan)
    frame['Sell_Signal'] = np.where(frame['Signal'] == -1.0, frame['Close'], np.nan)

    signal = frame['Signal'].iloc[-1]
    ask, bid = ask_bid(bybit_session, symbol)
    current_position_qty = get_current_position(bybit_session, symbol)[3]
    
    # print(f"ask: {ask}, bid: {bid}, current_position_qty: {current_position_qty}, signal: {signal}")
    
    if current_position_qty == 0 and signal == 1.0:
        cancel_all_orders(bybit_session, "linear", symbol)
        print(f"open long position at {bid}")
        open_long_position(bybit_session, symbol, "Limit", qty, bid)
    elif current_position_qty == 1 and signal == -1.0:
        cancel_all_orders(bybit_session, "linear", symbol)
        print(f"close long position at {ask}")
        close_long_position_market(bybit_session, symbol, qty)
    else:
        cancel_all_orders(bybit_session, "linear", symbol)
        
    
    
# Create a BlockingScheduler instance
scheduler = BlockingScheduler()

# Add the job to the scheduler
scheduler.add_job(job, "interval", seconds=trading_timer)

# Modify the job to start immediately
for job in scheduler.get_jobs():
   job.modify(next_run_time=datetime.now())

print("script started")
# Start the scheduler
scheduler.start()