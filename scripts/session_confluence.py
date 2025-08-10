# scripts/session_confluence.py
# 🕒 Time-of-Day Confidence Modulator

from datetime import datetime
import pytz

def get_session_multiplier():
    """Get confidence multiplier based on trading session"""
    try:
        # Get current UTC hour
        now = datetime.now(pytz.timezone("UTC")).hour

        # Trading session multipliers
        if 6 <= now < 12:
            return 1.15  # London Session (high liquidity)
        elif 12 <= now < 17:
            return 1.10  # NY Overlap (highest volume)
        elif 0 <= now < 5:
            return 0.95  # Asia Session (lower volume)
        else:
            return 1.00  # Off hours
            
    except Exception as e:
        print(f"⚠️ Session multiplier error: {e}")
        return 1.00  # Default multiplier

def get_session_name():
    """Get current trading session name"""
    try:
        now = datetime.now(pytz.timezone("UTC")).hour
        
        if 6 <= now < 12:
            return "London"
        elif 12 <= now < 17:
            return "NY Overlap"
        elif 0 <= now < 5:
            return "Asia"
        else:
            return "Off Hours"
            
    except Exception as e:
        print(f"⚠️ Session name error: {e}")
        return "Unknown"

def get_session_info():
    """Get complete session information"""
    return {
        "session": get_session_name(),
        "multiplier": get_session_multiplier(),
        "utc_hour": datetime.now(pytz.timezone("UTC")).hour
    }

# Usage
if __name__ == "__main__":
    info = get_session_info()
    print(f"📅 Current Session: {info['session']} (Multiplier: {info['multiplier']}x)")
    print(f"🕐 UTC Hour: {info['utc_hour']}")
