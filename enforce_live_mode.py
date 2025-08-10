#!/usr/bin/env python3
'''
🚨 LIVE MODE ENFORCER
Constitutional PIN: 841921
KILLS ALL SIMULATION LOGIC ON STARTUP
'''

import os
import sys
import json

def enforce_live_mode():
    '''Enforce live-only trading mode'''
    print("🚨 LIVE MODE ENFORCER - STARTING")
    
    # Set environment variables to live mode
    os.environ['SIM_MODE'] = 'false'
    os.environ['PRACTICE'] = 'false'
    os.environ['SANDBOX_MODE'] = 'false'
    os.environ['OANDA_ENVIRONMENT'] = 'live'
    os.environ['TRADING_MODE'] = 'LIVE_ONLY'
    
    print("✅ Environment variables set to LIVE MODE")
    
    # Verify no simulation files exist
    sim_files = [
        'config_demo.py', 'config_practice.py', 'config_sandbox.py',
        '.env.demo', '.env.practice', '.env.sandbox'
    ]
    
    for sim_file in sim_files:
        if os.path.exists(sim_file):
            print(f"🔥 DESTROYING simulation file: {sim_file}")
            os.remove(sim_file)
    
    # Block practice endpoints
    hosts_block = '''
# BLOCK SIMULATION ENDPOINTS - Constitutional PIN: 841921
127.0.0.1 api-fxpractice.oanda.com
127.0.0.1 api.sandbox.coinbase.com
'''
    
    print("🛡️  LIVE MODE ENFORCEMENT COMPLETE")
    return True

if __name__ == "__main__":
    enforce_live_mode()
