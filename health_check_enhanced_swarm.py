#!/usr/bin/env python3
# Enhanced Swarm System Health Check

import json
import os
import sys
from datetime import datetime

def check_system_health():
    """Check enhanced swarm system health"""
    print("🔍 ENHANCED SWARM SYSTEM HEALTH CHECK")
    print("=" * 40)
    
    health_status = {"overall": True, "checks": []}
    
    # Check configuration
    if os.path.exists("config.json"):
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
            if "enhanced_swarm_config" in config:
                health_status["checks"].append({"config": "✅ Enhanced swarm config loaded"})
            else:
                health_status["checks"].append({"config": "❌ Enhanced swarm config missing"})
                health_status["overall"] = False
        except Exception as e:
            health_status["checks"].append({"config": f"❌ Config error: {e}"})
            health_status["overall"] = False
    else:
        health_status["checks"].append({"config": "❌ No config.json found"})
        health_status["overall"] = False
    
    # Check required files
    required_files = [
        "main_swarm_enhanced.py",
        "main_swarm_controller.py", 
        "ml_predictor.py",
        "credentials.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            health_status["checks"].append({file: f"✅ {file} present"})
        else:
            health_status["checks"].append({file: f"❌ {file} missing"})
            health_status["overall"] = False
    
    # Check directories
    required_dirs = ["logs", "missions", "models", "performance_reports"]
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            health_status["checks"].append({dir_name: f"✅ {dir_name}/ directory exists"})
        else:
            health_status["checks"].append({dir_name: f"❌ {dir_name}/ directory missing"})
            health_status["overall"] = False
    
    # Print results
    for check in health_status["checks"]:
        for key, value in check.items():
            print(f"   {value}")
    
    print("")
    if health_status["overall"]:
        print("✅ SYSTEM HEALTH: EXCELLENT - Ready for trading!")
    else:
        print("❌ SYSTEM HEALTH: ISSUES DETECTED - Please fix before trading")
    
    return health_status["overall"]

if __name__ == "__main__":
    healthy = check_system_health()
    sys.exit(0 if healthy else 1)
