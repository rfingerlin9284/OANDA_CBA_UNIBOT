#!/usr/bin/env python3
import os
import signal
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/daily_restart.log'),
        logging.StreamHandler()
    ]
)

def daily_restart():
    logging.info("🌅 STARTING DAILY RESTART SEQUENCE")
    
    # 1. Signal autonomous controller to restart
    restart_flag = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.DAILY_RESTART"
    with open(restart_flag, 'w') as f:
        f.write(str(datetime.now().timestamp()))
    
    # 2. Archive yesterday's logs
    yesterday = datetime.now().strftime('%Y%m%d')
    log_archive = f"/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/archive_{yesterday}"
    os.makedirs(log_archive, exist_ok=True)
    
    # 3. Clear temporary files
    temp_files = [".RESTART_REQUESTED", ".EMERGENCY_STOP"]
    for temp_file in temp_files:
        path = f"/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/{temp_file}"
        if os.path.exists(path):
            os.remove(path)
    
    logging.info("✅ DAILY RESTART SEQUENCE COMPLETE")

if __name__ == "__main__":
    daily_restart()
