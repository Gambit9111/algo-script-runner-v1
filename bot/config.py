from pybit.unified_trading import HTTP

import os
from dotenv import load_dotenv
load_dotenv()


FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
BYBIT_API_SECRET = os.getenv('BYBIT_API_SECRET')

if FLASK_SECRET_KEY is None:
    raise ValueError('FLASK_SECRET_KEY is not set')
elif ADMIN_USERNAME is None:
    raise ValueError('ADMIN_USERNAME is not set')
elif ADMIN_PASSWORD is None:
    raise ValueError('ADMIN_PASSWORD is not set')
elif BYBIT_API_KEY is None:
    raise ValueError('BYBIT_API_KEY is not set')
elif BYBIT_API_SECRET is None:
    raise ValueError('BYBIT_API_SECRET is not set')
else:
    print("Config loaded successfully")
    

# Bybit session
bybit_session = HTTP(
    testnet=False,
    api_key=BYBIT_API_KEY,
    api_secret=BYBIT_API_SECRET,
)