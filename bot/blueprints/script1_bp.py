# script1.py
from flask import Blueprint, redirect, url_for, request, session
import subprocess
import json
import os
import signal
from flask_login import login_required

script1_bp = Blueprint('script1_bp', __name__)

@script1_bp.route('/start', methods=['POST'])
@login_required
def start_script1():
    try:
        # Get the argument from the form
        script_timer = request.form.get('arg')
        
        # Store the argument in the session
        session['script1_arg'] = script_timer
        
        # Start script1 as a subprocess with the argument
        script1_process = subprocess.Popen(["python", "scripts/script1.py", script_timer])
        
        # Check if the JSON file is empty
        if os.stat('processes.json').st_size == 0:
            processes = {}
        else:
            with open('processes.json', 'r') as f:
                processes = json.load(f)
                
        # Store the subprocess in a JSON file
        processes['script1_process'] = script1_process.pid
        with open('processes.json', 'w') as f:
            json.dump(processes, f)
    except:
        print("Error starting script1")
        
    return redirect(url_for('home'))

@script1_bp.route('/stop', methods=['GET'])
@login_required
def stop_script1():    
    # Retrieve the subprocess from the JSON file
    with open('processes.json', 'r') as f:
        processes = json.load(f)

    try:
        # Terminate the subprocess
        if 'script1_process' in processes:
            print("Killing script1")
            os.kill(int(processes['script1_process']), signal.SIGTERM)
    except:
        print("script1_process not found")

    try:
        # Delete the subprocess from the JSON file
        del processes['script1_process']
        with open('processes.json', 'w') as f:
            json.dump(processes, f)
    except:
        print("script1_process not found")
        
    try:
        # Delete the argument from the session
        del session['script1_arg']
    except:
        print("script1_arg not found")
    
    return redirect(url_for('home'))