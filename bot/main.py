from flask import Flask, render_template, session
import json
import os
from flask_login import login_required

from blueprints.script1_bp import script1_bp
from blueprints.login_bp import login_bp
from blueprints.spot_crawler_bp import spot_crawler_bp
from blueprints.keltner_channels_bp import keltner_channels_bp

from config import FLASK_SECRET_KEY, bybit_session
from functions import ask_bid, get_wallet_balance


app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY # Replace 'your secret key' with a secret key


app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(script1_bp, url_prefix='/script1')
app.register_blueprint(spot_crawler_bp, url_prefix='/spot-crawler')
app.register_blueprint(keltner_channels_bp, url_prefix='/keltner-channels')


# ! home route
@app.route('/', methods=['GET'])
@login_required
def home():
  # Check if the JSON file is empty
  if os.stat('processes.json').st_size == 0:
      processes = {}
  else:
      with open('processes.json', 'r') as f:
          processes = json.load(f)

  # Check the status of each script
  script1_status = 'Stopped' if 'script1_process' not in processes else 'Running'
  spot_crawler_status = 'Stopped' if 'spot_crawler_process' not in processes else 'Running'
  keltner_channels_status = 'Stopped' if 'keltner_channels_process' not in processes else 'Running'
  # script2_status = 'Stopped' if 'script2_process' not in processes else 'Running'
  
  # get the arguments from session
  script1_arg = session.get('script1_arg')
  # script2_arg = session.get('script2_arg')
  
  # ! spot crawler
  spot_crawler_symbol = session.get('spot_crawler_symbol')
  spot_crawler_qty = session.get('spot_crawler_qty')
  spot_crawler_step_size_up = session.get('spot_crawler_step_size_up')
  spot_crawler_step_size_down = session.get('spot_crawler_step_size_down')
  spot_crawler_max_entry_size = session.get('spot_crawler_max_entry_size')
  spot_crawler_trading_timer = session.get('spot_crawler_trading_timer')
  
  #! keltner channels
  keltner_channels_symbol = session.get('keltner_channels_symbol')
  keltner_channels_interval = session.get('keltner_channels_interval')
  keltner_channels_trading_timer = session.get('keltner_channels_trading_timer')
  keltner_channels_qty = session.get('keltner_channels_qty')
  
  wallet_balance = get_wallet_balance(bybit_session)[0]
  

  # Pass the status of each script to the template
  return render_template('control.html',
                         title='Home',
                         wallet_balance=wallet_balance,
                         
                         script1_status=script1_status, 
                         script1_arg=script1_arg,
                                         
                         spot_crawler_status=spot_crawler_status,
                         spot_crawler_symbol=spot_crawler_symbol,
                         spot_crawler_qty=spot_crawler_qty,
                         spot_crawler_step_size_up=spot_crawler_step_size_up,
                         spot_crawler_step_size_down=spot_crawler_step_size_down,
                         spot_crawler_max_entry_size=spot_crawler_max_entry_size,
                         spot_crawler_trading_timer=spot_crawler_trading_timer,
                         
                         keltner_channels_symbol=keltner_channels_symbol,
                         keltner_channels_interval=keltner_channels_interval,
                         keltner_channels_trading_timer=keltner_channels_trading_timer,
                         keltner_channels_qty=keltner_channels_qty,
                        )


if __name__ == "__main__":
 app.run(debug=True)