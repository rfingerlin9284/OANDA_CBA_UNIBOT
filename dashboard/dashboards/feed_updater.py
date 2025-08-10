"""
🎯 FVG DASHBOARD FEED UPDATER
Updates dashboard JSON feeds with live FVG detection data
LIVE TRADING ONLY - NO live_mode/PRACTICE MODE
"""
import json
import time
from datetime import datetime
import os

class FVGDashboardFeeder:
    def __init__(self):
        self.dashboard_dir = "/home/ing/FOUR_horsemen/ALPHA_FOUR/proto_oanda/wolfpack-lite/dashboards"
        self.oanda_feed = f"{self.dashboard_dir}/fvg_feed_oanda.json"
        self.coinbase_feed = f"{self.dashboard_dir}/fvg_feed_coinbase.json"
    
    def update_oanda_feed(self, pair, signal_data, active_trades=0):
        """Update OANDA FVG feed for dashboard"""
        try:
            # Load existing data
            if os.path.exists(self.oanda_feed):
                with open(self.oanda_feed, 'r') as f:
                    feed_data = json.load(f)
            else:
                feed_data = {"pairs": {}, "last_scan": "", "active_trades": 0}
            
            # Update with new signal
            feed_data["pairs"][pair] = {
                "direction": signal_data.get("direction", "N/A"),
                "confidence": signal_data.get("confidence", 0.0),
                "entry": signal_data.get("entry", 0.0),
                "sl": signal_data.get("sl", 0.0), 
                "tp": signal_data.get("tp", 0.0),
                "status": signal_data.get("status", "PENDING"),
                "time": datetime.now().strftime("%H:%M:%S"),
                "reason": signal_data.get("reason", "FVG Detection")
            }
            
            feed_data["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            feed_data["active_trades"] = active_trades
            feed_data["system_status"] = "LIVE OANDA TRADING"
            
            # Write back to file
            with open(self.oanda_feed, 'w') as f:
                json.dump(feed_data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"❌ Failed to update OANDA feed: {e}")
            return False
    
    def update_coinbase_feed(self, pair, signal_data, active_trades=0):
        """Update Coinbase FVG feed for dashboard"""
        try:
            # Load existing data
            if os.path.exists(self.coinbase_feed):
                with open(self.coinbase_feed, 'r') as f:
                    feed_data = json.load(f)
            else:
                feed_data = {"pairs": {}, "last_scan": "", "active_trades": 0}
            
            # Update with new signal
            feed_data["pairs"][pair] = {
                "direction": signal_data.get("direction", "N/A"),
                "confidence": signal_data.get("confidence", 0.0),
                "entry": signal_data.get("entry", 0.0),
                "sl": signal_data.get("sl", 0.0),
                "tp": signal_data.get("tp", 0.0),
                "status": signal_data.get("status", "PENDING"),
                "time": datetime.now().strftime("%H:%M:%S"),
                "reason": signal_data.get("reason", "FVG Detection")
            }
            
            feed_data["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            feed_data["active_trades"] = active_trades
            feed_data["system_status"] = "LIVE COINBASE SPOT TRADING"
            
            # Write back to file
            with open(self.coinbase_feed, 'w') as f:
                json.dump(feed_data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"❌ Failed to update Coinbase feed: {e}")
            return False
    
    def clear_pair_signal(self, pair, platform="oanda"):
        """Clear a specific pair's signal (when trade closes)"""
        try:
            feed_file = self.oanda_feed if platform == "oanda" else self.coinbase_feed
            
            if os.path.exists(feed_file):
                with open(feed_file, 'r') as f:
                    feed_data = json.load(f)
                
                # Remove the pair if it exists
                if pair in feed_data.get("pairs", {}):
                    del feed_data["pairs"][pair]
                    
                    # Update timestamp
                    feed_data["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Write back
                    with open(feed_file, 'w') as f:
                        json.dump(feed_data, f, indent=2)
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Failed to clear {pair} signal: {e}")
            return False
    
    def update_system_status(self, platform, status_message, active_trades=0):
        """Update system status without signal data"""
        try:
            feed_file = self.oanda_feed if platform == "oanda" else self.coinbase_feed
            
            if os.path.exists(feed_file):
                with open(feed_file, 'r') as f:
                    feed_data = json.load(f)
            else:
                feed_data = {"pairs": {}, "last_scan": "", "active_trades": 0}
            
            feed_data["last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            feed_data["active_trades"] = active_trades
            feed_data["system_status"] = status_message
            
            with open(feed_file, 'w') as f:
                json.dump(feed_data, f, indent=2)
                
            return True
            
        except Exception as e:
            print(f"❌ Failed to update {platform} status: {e}")
            return False

# Example usage for integration with your sniper bots
def example_usage():
    """Example of how to integrate with your sniper bots"""
    feeder = FVGDashboardFeeder()
    
    # Example: OANDA FVG signal detected
    oanda_signal = {
        "direction": "BUY",
        "confidence": 0.85,
        "entry": 1.10500,
        "sl": 1.10200,
        "tp": 1.11400,
        "status": "ACTIVE",
        "reason": "Bullish FVG + RSI Confluence"
    }
    
    feeder.update_oanda_feed("EUR/USD", oanda_signal, active_trades=1)
    
    # Example: Coinbase FVG signal detected
    coinbase_signal = {
        "direction": "SELL",
        "confidence": 0.82,
        "entry": 45250.00,
        "sl": 45800.00,
        "tp": 43600.00,
        "status": "PENDING",
        "reason": "Bearish FVG + EMA Break"
    }
    
    feeder.update_coinbase_feed("BTC-USD", coinbase_signal, active_trades=2)
    
    print("✅ Dashboard feeds updated with example data")

if __name__ == "__main__":
    example_usage()
