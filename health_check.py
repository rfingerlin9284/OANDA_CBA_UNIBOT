#!/usr/bin/env python3
import os
import json
import psutil
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/health_check.log'),
        logging.StreamHandler()
    ]
)

def health_check():
    logging.info("💊 PERFORMING HEALTH CHECK")
    
    health_status = {
        "timestamp": datetime.now().isoformat(),
        "system": {},
        "bot": {},
        "trading": {}
    }
    
    # System health
    health_status["system"]["cpu_percent"] = psutil.cpu_percent(interval=1)
    health_status["system"]["memory_percent"] = psutil.virtual_memory().percent
    health_status["system"]["disk_percent"] = psutil.disk_usage('/').percent
    
    # Bot process health
    bot_running = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'autonomous_controller.py' in ' '.join(proc.info['cmdline'] or []):
            bot_running = True
            health_status["bot"]["pid"] = proc.info['pid']
            health_status["bot"]["cpu_percent"] = proc.cpu_percent()
            health_status["bot"]["memory_mb"] = proc.memory_info().rss / 1024 / 1024
            break
    
    health_status["bot"]["running"] = bot_running
    
    # Check for emergency conditions
    emergencies = []
    
    if health_status["system"]["cpu_percent"] > 90:
        emergencies.append("High CPU usage")
    
    if health_status["system"]["memory_percent"] > 90:
        emergencies.append("High memory usage")
    
    if not bot_running:
        emergencies.append("Bot not running")
    
    health_status["emergencies"] = emergencies
    
    # Save health report
    health_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/health_status.json"
    with open(health_file, 'w') as f:
        json.dump(health_status, f, indent=2)
    
    if emergencies:
        logging.warning(f"⚠️ HEALTH ISSUES: {', '.join(emergencies)}")
    else:
        logging.info("✅ SYSTEM HEALTHY")

if __name__ == "__main__":
    health_check()
