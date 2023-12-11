import os
from dotenv import load_dotenv
load_dotenv()

FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

if FLASK_SECRET_KEY is None:
    raise ValueError('FLASK_SECRET_KEY is not set')
elif ADMIN_USERNAME is None:
    raise ValueError('ADMIN_USERNAME is not set')
elif ADMIN_PASSWORD is None:
    raise ValueError('ADMIN_PASSWORD is not set')
else:
    print("Config loaded successfully")