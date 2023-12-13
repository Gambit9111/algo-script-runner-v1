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
from functions import ask_bid, buy_spot_limit, sell_spot_limit, sell_spot_market, cancel_all_orders, get_coin_balance

symbol = str(sys.argv[1]) # "BTC3LUSDT"
qty = int(sys.argv[2]) # 10
step_size_up = float(sys.argv[3]) # step size in $ to increase the price
step_size_down = float(sys.argv[4]) # step size in $ to decrease the price
max_entry_size = int(sys.argv[5]) # max entry size in qty
trading_timer = int(sys.argv[6]) # trading shuffle timer in seconds

trading_fee = 0.001
# symbol = "BTC3LUSDT"
coin = symbol[:-4]
# qty = 5
qty_with_fees = qty + (qty * trading_fee)
# step_size_up = 0.005
# step_size_down = 0.005
# max_entry_size = 25
# trading_timer = 300

# get_current_position(bybit_session, "spot", symbol)

# get_coin_balance(bybit_session, coin)

# print(get_coin_balance(bybit_session, coin)[1])

def job():
    cancel_all_orders(bybit_session, "spot", symbol)
    ask, bid = ask_bid(bybit_session, symbol)
    current_position_qty = get_coin_balance(bybit_session, coin)[0]

    print(f"ask: {ask}, bid: {bid}, current_position_qty: {current_position_qty}, trading_timer: {trading_timer} seconds")
    
    if current_position_qty < qty:
        print(f"1set {int(max_entry_size / qty)} limit buy orders bellow the price in steps of {step_size_down} dollar")
        for i in range(1, int(max_entry_size / qty) + 1):
            buy_spot_limit(bybit_session, symbol, qty_with_fees, bid - (i * step_size_down), 4)
    
    elif current_position_qty >= max_entry_size:
        print(f"2set {int(max_entry_size / qty)} limit sell orders above the price in steps of {step_size_up} dollar")
        for i in range(1, int(max_entry_size / qty) + 1):
            sell_spot_limit(bybit_session, symbol, qty, ask + (i * step_size_up), 4)
    
    elif current_position_qty >= qty and current_position_qty <= max_entry_size:
        position_size_left = max_entry_size - current_position_qty
        print(f"3set {math.ceil(position_size_left / qty)} limit buy orders bellow the price in steps of {step_size_down} dollar")
        for i in range(1, math.ceil(position_size_left / qty) + 1):
            buy_spot_limit(bybit_session, symbol, qty_with_fees, bid - (i * step_size_down), 4)
        
        print(f"4set {int(current_position_qty / qty)} limit sell orders above the price in steps of {step_size_up} dollar")
        for i in range(1, int(current_position_qty / qty) + 1):
            sell_spot_limit(bybit_session, symbol, qty, ask + (i * step_size_up), 4)
    
    else:
        print("error")
    
    # check if there are any balance left witch means some order was partially filled
    balance_left = get_coin_balance(bybit_session, coin)[1]
    if balance_left > qty / 2:
        # sell the partial position
        try:
            sell_spot_market(bybit_session, symbol, (balance_left - 0.01))
        except:
            print("error selling partial position")
    print("reshuffle trades done")

# Create a BlockingScheduler instance
scheduler = BlockingScheduler()

# Add the job to the scheduler
scheduler.add_job(job, "interval", seconds=trading_timer)

# Modify the job to start immediately
for job in scheduler.get_jobs():
   job.modify(next_run_time=datetime.now())

# Start the scheduler
scheduler.start()