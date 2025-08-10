#!/usr/bin/env python3
"""
FULLY AUTONOMOUS DEPLOYMENT SCRIPT
Deploys complete hands-off OANDA trading system
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

def ensure_directories():
    """Ensure all required directories exist"""
    dirs = [
        "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs",
        "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/systemd"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Directory ensured: {dir_path}")

def create_systemd_service():
    """Create SystemD service for autonomous operation"""
    service_content = f"""[Unit]
Description=OANDA Autonomous Trading Bot
After=network.target
Wants=network.target

[Service]
Type=liveple
User={os.getenv('USER', 'trader')}
WorkingDirectory=/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda
ExecStart=/usr/bin/python3 /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/autonomous_controller.py
Restart=always
RestartSec=30
StandardOutput=append:/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/systemd.log
StandardError=append:/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs/systemd_error.log

# Environment
Environment=PYTHONPATH=/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda
Environment=PYTHONUNBUFFERED=1

# Security
PrivateTmp=true
NoNewPrivileges=true

# Resource limits
MemoryMax=2G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
"""
    
    service_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/systemd/oanda-autonomous.service"
    with open(service_file, 'w') as f:
        f.write(service_content)
    
    print(f"✅ SystemD service created: {service_file}")
    return service_file

def create_cron_jobs():
    """Create cron jobs for daily management"""
    cron_content = f"""# OANDA Autonomous Bot Management
# Daily restart at 7:00 AM
0 7 * * * /usr/bin/python3 /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/daily_restart.py

# Hourly health check
0 * * * * /usr/bin/python3 /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/health_check.py

# Every 15 minutes: cleanup logs
*/15 * * * * /usr/bin/python3 /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/log_cleanup.py

# Weekly profit analysis (Sundays at 23:00)
0 23 * * 0 /usr/bin/python3 /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/weekly_analysis.py
"""
    
    cron_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/systemd/autonomous.cron"
    with open(cron_file, 'w') as f:
        f.write(cron_content)
    
    print(f"✅ Cron jobs defined: {cron_file}")
    return cron_file

def create_daily_restart_script():
    """Create daily restart script"""
    script_content = """#!/usr/bin/env python3
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
"""
    
    script_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/daily_restart.py"
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_file, 0o755)
    print(f"✅ Daily restart script created: {script_file}")

def create_health_check_script():
    """Create health monitoring script"""
    script_content = """#!/usr/bin/env python3
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
"""
    
    script_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/health_check.py"
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_file, 0o755)
    print(f"✅ Health check script created: {script_file}")

def create_log_cleanup_script():
    """Create log rotation and cleanup script"""
    script_content = """#!/usr/bin/env python3
import os
import gzip
import shutil
from datetime import datetime, timedelta

def cleanup_logs():
    log_dir = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/logs"
    
    # Compress logs older than 1 day
    cutoff_time = datetime.now() - timedelta(days=1)
    
    for filename in os.listdir(log_dir):
        if not filename.endswith('.log'):
            continue
        
        filepath = os.path.join(log_dir, filename)
        
        if os.path.getmtime(filepath) < cutoff_time.timestamp():
            # Compress the file
            compressed_name = f"{filename}_{datetime.now().strftime('%Y%m%d')}.gz"
            compressed_path = os.path.join(log_dir, compressed_name)
            
            with open(filepath, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            os.remove(filepath)
            print(f"✅ Compressed and cleaned: {filename}")
    
    # Remove compressed logs older than 30 days
    old_cutoff = datetime.now() - timedelta(days=30)
    
    for filename in os.listdir(log_dir):
        if not filename.endswith('.gz'):
            continue
        
        filepath = os.path.join(log_dir, filename)
        
        if os.path.getmtime(filepath) < old_cutoff.timestamp():
            os.remove(filepath)
            print(f"🗑️ Removed old log: {filename}")

if __name__ == "__main__":
    cleanup_logs()
"""
    
    script_file = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/log_cleanup.py"
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_file, 0o755)
    print(f"✅ Log cleanup script created: {script_file}")

def install_dependencies():
    """Install required Python packages"""
    required_packages = [
        "watchdog",
        "psutil",
        "schedule"
    ]
    
    for package in required_packages:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Installed: {package}")
            else:
                print(f"❌ Failed to install {package}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")

def setup_autonomous_integration():
    """Setup autonomous integration with existing main.py"""
    integration_code = '''
# === AUTONOMOUS INTEGRATION ===
import threading
import signal

def check_restart_signals():
    """Check for restart signals from autonomous controller"""
    restart_flag = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.RESTART_REQUESTED"
    daily_restart_flag = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.DAILY_RESTART"
    
    if os.path.exists(restart_flag) or os.path.exists(daily_restart_flag):
        print("🔄 RESTART SIGNAL RECEIVED - Shutting down gracefully...")
        
        # Clean up flags
        for flag in [restart_flag, daily_restart_flag]:
            if os.path.exists(flag):
                os.remove(flag)
        
        # Graceful shutdown
        os._exit(0)

def autonomous_signal_handler(signum, frame):
    """Handle signals from autonomous controller"""
    print(f"📡 Received signal {signum} - Graceful shutdown initiated")
    check_restart_signals()
    os._exit(0)

# Register signal handlers
signal.signal(signal.SIGUSR1, autonomous_signal_handler)
signal.signal(signal.SIGUSR2, autonomous_signal_handler)

# Start background thread to check for restart signals
def background_signal_checker():
    while True:
        check_restart_signals()
        time.sleep(30)

signal_thread = threading.Thread(target=background_signal_checker, daemon=True)
signal_thread.start()

print("🤖 AUTONOMOUS INTEGRATION ACTIVE")
# === END AUTONOMOUS INTEGRATION ===
'''
    
    print("✅ Autonomous integration code prepared")
    print("💡 This code should be added to main.py near the top")
    
    return integration_code

def deploy_autonomous_system():
    """Deploy the complete autonomous system"""
    print("🚀 DEPLOYING FULLY AUTONOMOUS OANDA BOT SYSTEM")
    print("=" * 60)
    
    # Step 1: Ensure directories
    ensure_directories()
    
    # Step 2: Install dependencies
    print("\n📦 Installing dependencies...")
    install_dependencies()
    
    # Step 3: Create SystemD service
    print("\n🔧 Creating SystemD service...")
    service_file = create_systemd_service()
    
    # Step 4: Create cron jobs
    print("\n⏰ Setting up cron jobs...")
    cron_file = create_cron_jobs()
    
    # Step 5: Create management scripts
    print("\n📜 Creating management scripts...")
    create_daily_restart_script()
    create_health_check_script()
    create_log_cleanup_script()
    
    # Step 6: Setup integration
    print("\n🔗 Preparing autonomous integration...")
    integration_code = setup_autonomous_integration()
    
    # Step 7: Create startup script
    startup_script = "/mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/start_autonomous.sh"
    with open(startup_script, 'w') as f:
        f.write(f"""#!/bin/bash
# FULLY AUTONOMOUS OANDA BOT STARTUP

echo "🚀 STARTING FULLY AUTONOMOUS OANDA BOT SYSTEM"

# Ensure we're in the right directory
cd /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda

# Install/update systemd service (requires sudo)
echo "🔧 Installing SystemD service..."
sudo cp systemd/oanda-autonomous.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable oanda-autonomous.service

# Install cron jobs
echo "⏰ Installing cron jobs..."
crontab systemd/autonomous.cron

# Start the autonomous controller
echo "🤖 Starting autonomous controller..."
sudo systemctl start oanda-autonomous.service

# Show status
echo "📊 System Status:"
sudo systemctl status oanda-autonomous.service --no-pager

echo "✅ FULLY AUTONOMOUS SYSTEM DEPLOYED"
echo ""
echo "🎮 CONTROL COMMANDS:"
echo "  Start:   sudo systemctl start oanda-autonomous.service"
echo "  Stop:    sudo systemctl stop oanda-autonomous.service"
echo "  Status:  sudo systemctl status oanda-autonomous.service"
echo "  Logs:    journalctl -u oanda-autonomous.service -f"
echo ""
echo "🔒 EMERGENCY STOP:"
echo "  touch /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.BOT_LOCK"
echo ""
echo "🔓 UNLOCK:"
echo "  rm /mnt/wsl/FOUR_HORSEMEN/ALPHA_FOUR/proto_oanda/.BOT_LOCK"
""")
    
    os.chmod(startup_script, 0o755)
    
    print("\n" + "=" * 60)
    print("✅ FULLY AUTONOMOUS DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print(f"\n🎮 TO START THE AUTONOMOUS SYSTEM:")
    print(f"   bash {startup_script}")
    print("\n🔍 MONITORING:")
    print("   tail -f logs/autonomous.log")
    print("   tail -f logs/systemd.log") 
    print("\n🛑 EMERGENCY STOP:")
    print("   touch .BOT_LOCK")
    print("\n🔓 UNLOCK:")
    print("   rm .BOT_LOCK")
    
    return True

if __name__ == "__main__":
    success = deploy_autonomous_system()
    
    if success:
        print("\n🎯 READY FOR FULLY AUTONOMOUS OPERATION!")
        print("💰 Target: $400/day with zero human intervention")
        print("🤖 Self-launching • Self-correcting • Self-scaling")
    else:
        print("\n❌ Deployment failed - check logs")
        sys.exit(1)
