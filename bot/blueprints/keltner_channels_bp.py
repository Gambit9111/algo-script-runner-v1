# spot_crawler.py
from flask import Blueprint, redirect, url_for, request, session
import subprocess
import json
import os
import signal
from flask_login import login_required

keltner_channels_bp = Blueprint('keltner_channels_bp', __name__)

@keltner_channels_bp.route('/start', methods=['POST'])
@login_required
def start_keltner_channels():
    try:
        # Get the argument from the form
        keltner_channels_symbol = request.form.get('symbol')
        keltner_channels_interval = request.form.get('interval')
        keltner_channels_trading_timer = request.form.get('trading_timer')
        keltner_channels_qty = request.form.get('qty')
        
        # Store the argument in the session
        session['keltner_channels_symbol'] = keltner_channels_symbol
        session['keltner_channels_interval'] = keltner_channels_interval
        session['keltner_channels_trading_timer'] = keltner_channels_trading_timer
        session['keltner_channels_qty'] = keltner_channels_qty
        
        # # Start script1 as a subprocess with the argument
        keltner_channels_process = subprocess.Popen(["python", "scripts/keltner_channels.py", keltner_channels_symbol, keltner_channels_interval, keltner_channels_trading_timer, keltner_channels_qty])
        
        # # Check if the JSON file is empty amd load it
        if os.stat('processes.json').st_size == 0:
            processes = {}
        else:
            with open('processes.json', 'r') as f:
                processes = json.load(f)
                
        # # Store the subprocess in a JSON file
        processes['keltner_channels_process'] = keltner_channels_process.pid
        with open('processes.json', 'w') as f:
            json.dump(processes, f)
    except:
        print("Error starting spot crawler")
        
    return redirect(url_for('home'))

@keltner_channels_bp.route('/stop', methods=['GET'])
@login_required
def stop_keltner_channels():    
    # Retrieve the subprocess from the JSON file
    with open('processes.json', 'r') as f:
        processes = json.load(f)

    try:
        # Terminate the subprocess
        if 'keltner_channels_process' in processes:
            print("Killing keltner_channels")
            os.kill(int(processes['keltner_channels_process']), signal.SIGTERM)
    except:
        print("keltner_channels_process not found")

    try:
        # Delete the subprocess from the JSON file
        del processes['keltner_channels_process']
        with open('processes.json', 'w') as f:
            json.dump(processes, f)
    except:
        print("keltner_channels_process not found")
        
    try:
        # Delete the argument from the session
        del session['keltner_channels_symbol']
        del session['keltner_channels_interval']
        del session['keltner_channels_trading_timer']
        del session['keltner_channels_qty']
        
    except:
        print("arguments not found")
    
    return redirect(url_for('home'))