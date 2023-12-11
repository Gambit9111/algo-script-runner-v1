# script2.py
from flask import Blueprint, redirect, url_for, request, session
import subprocess
import json
import os
import signal
from flask_login import login_required

script2_bp = Blueprint('script2_bp', __name__)

@script2_bp.route('/start', methods=['POST'])
@login_required
def start_script2():
    try:
        # Get the argument from the form
        script_timer = request.form.get('arg')
        
        # Store the argument in the session
        session['script2_arg'] = script_timer
        
        # Start script2 as a subprocess with the argument
        script2_process = subprocess.Popen(["python", "scripts/script2.py", script_timer])
        
        # Check if the JSON file is empty
        if os.stat('processes.json').st_size == 0:
            processes = {}
        else:
            with open('processes.json', 'r') as f:
                processes = json.load(f)
                
        # Store the subprocess in a JSON file
        processes['script2_process'] = script2_process.pid
        with open('processes.json', 'w') as f:
            json.dump(processes, f)
    except:
        print("Error starting script2")
       
    return redirect(url_for('home'))

@script2_bp.route('/stop', methods=['GET'])
@login_required
def stop_script2():   
   # Retrieve the subprocess from the JSON file
   with open('processes.json', 'r') as f:
       processes = json.load(f)

   try:
       # Terminate the subprocess
       if 'script2_process' in processes:
           print("Killing script2")
           os.kill(int(processes['script2_process']), signal.SIGTERM)
   except:
       print("script2_process not found")

   try:
       # Delete the subprocess from the JSON file
       del processes['script2_process']
       with open('processes.json', 'w') as f:
           json.dump(processes, f)
   except:
       print("script2_process not found")
       
   try:
       # Delete the argument from the session
       del session['script2_arg']
   except:
       print("script2_arg not found")
   
   return redirect(url_for('home'))
