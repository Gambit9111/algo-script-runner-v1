from flask import Flask, render_template, session
import json
import os
from flask_login import login_required

from blueprints.script1_bp import script1_bp
from blueprints.script2_bp import script2_bp
from blueprints.login_bp import login_bp

from config import FLASK_SECRET_KEY


app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY # Replace 'your secret key' with a secret key


app.register_blueprint(script1_bp, url_prefix='/script1')
app.register_blueprint(script2_bp, url_prefix='/script2')
app.register_blueprint(login_bp, url_prefix='/auth')

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
  script2_status = 'Stopped' if 'script2_process' not in processes else 'Running'
  
  # get the arguments from session
  script1_arg = session.get('script1_arg')
  script2_arg = session.get('script2_arg')

  # Pass the status of each script to the template
  return render_template('control.html', script1_status=script1_status, script2_status=script2_status, script1_arg=script1_arg, script2_arg=script2_arg, title='Home')


if __name__ == "__main__":
 app.run()