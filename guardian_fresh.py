#!/usr/bin/env python3
"""
Fresh Guardian Module - Live Mode Enforcer
Per deployment manual: PIN 841921
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def verify_live_mode():
    """Enforce live-only mode with constitutional PIN"""
    required_pin = "841921"
    user_pin = os.getenv("CONSTITUTIONAL_PIN", "")
    
    if user_pin != required_pin:
        print("❌ CONSTITUTIONAL PIN REQUIRED - LIVE MODE ONLY")
        sys.exit(1)
    
    env = os.getenv("OANDA_ENVIRONMENT", "").lower()
    if env != "live":
        print("❌ LIVE MODE ONLY - NO live_mode TRADING")
        sys.exit(1)
    
    print("✅ Live mode verified - Guardian active")
    return True

def validate_credentials():
    """Validate OANDA live credentials"""
    required_vars = [
        "OANDA_API_KEY",
        "OANDA_ACCOUNT_ID", 
        "OANDA_ENVIRONMENT"
    ]
    
    for var in required_vars:
        if not os.getenv(var):
            print(f"❌ Missing required variable: {var}")
            return False
    
    return True

if __name__ == "__main__":
    verify_live_mode()
    if validate_credentials():
        print("✅ Guardian verification complete")
