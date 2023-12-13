# spot_crawler.py
from flask import Blueprint, redirect, url_for, request, session
import subprocess
import json
import os
import signal
from flask_login import login_required

spot_crawler_bp = Blueprint('spot_crawler_bp', __name__)

@spot_crawler_bp.route('/start', methods=['POST'])
@login_required
def start_spot_crawler():
    try:
        # Get the argument from the form
        spot_crawler_symbol = request.form.get('symbol')
        spot_crawler_qty = request.form.get('qty')
        spot_crawler_step_size_up = request.form.get('step_size_up')
        spot_crawler_step_size_down = request.form.get('step_size_down')
        spot_crawler_max_entry_size = request.form.get('max_entry_size')
        spot_crawler_trading_timer = request.form.get('trading_timer')
        
        # Store the argument in the session
        session['spot_crawler_symbol'] = spot_crawler_symbol
        session['spot_crawler_qty'] = spot_crawler_qty
        session['spot_crawler_step_size_up'] = spot_crawler_step_size_up
        session['spot_crawler_step_size_down'] = spot_crawler_step_size_down
        session['spot_crawler_max_entry_size'] = spot_crawler_max_entry_size
        session['spot_crawler_trading_timer'] = spot_crawler_trading_timer
        
        # # Start script1 as a subprocess with the argument
        spot_crawler_process = subprocess.Popen(["python", "scripts/spot_crawler.py", spot_crawler_symbol, spot_crawler_qty, spot_crawler_step_size_up, spot_crawler_step_size_down, spot_crawler_max_entry_size, spot_crawler_trading_timer])
        
        # # Check if the JSON file is empty amd load it
        if os.stat('processes.json').st_size == 0:
            processes = {}
        else:
            with open('processes.json', 'r') as f:
                processes = json.load(f)
                
        # # Store the subprocess in a JSON file
        processes['spot_crawler_process'] = spot_crawler_process.pid
        with open('processes.json', 'w') as f:
            json.dump(processes, f)
    except:
        print("Error starting spot crawler")
        
    return redirect(url_for('home'))

@spot_crawler_bp.route('/stop', methods=['GET'])
@login_required
def stop_spot_crawler():    
    # Retrieve the subprocess from the JSON file
    with open('processes.json', 'r') as f:
        processes = json.load(f)

    try:
        # Terminate the subprocess
        if 'spot_crawler_process' in processes:
            print("Killing spot_crawler")
            os.kill(int(processes['spot_crawler_process']), signal.SIGTERM)
    except:
        print("spot_crawler_process not found")

    try:
        # Delete the subprocess from the JSON file
        del processes['spot_crawler_process']
        with open('processes.json', 'w') as f:
            json.dump(processes, f)
    except:
        print("spot_crawler_process not found")
        
    try:
        # Delete the argument from the session
        del session['spot_crawler_symbol']
        del session['spot_crawler_qty']
        del session['spot_crawler_step_size_up']
        del session['spot_crawler_step_size_down']
        del session['spot_crawler_max_entry_size']
        del session['spot_crawler_trading_timer']
    except:
        print("arguments not found")
    
    return redirect(url_for('home'))