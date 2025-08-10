# scripts/smart_volatility_filter.py
# 🚨 Volatility Guard for OANDA + Coinbase

import requests
import time
from datetime import datetime, timezone

# --- OANDA CONFIG ---
OANDA_API_KEY = "5f2cd72673e5c6214f94cc159e444a01-c229936202d1b6d0b4499086198da2b3"
OANDA_BASE_URL = "https://api-fxtrade.oanda.com/v3"
HEADERS = {"Authorization": f"Bearer {OANDA_API_KEY}"}

def fetch_volatility_oanda(pair="EUR_USD", granularity="M5", count=10):
    """Fetch OANDA volatility data"""
    try:
        url = f"{OANDA_BASE_URL}/instruments/{pair}/candles"
        params = {"granularity": granularity, "count": count, "price": "M"}
        res = requests.get(url, headers=HEADERS, params=params, timeout=5)
        
        if res.status_code != 200:
            return {"vol_spike": False, "last_range": 0.0}
            
        data = res.json()
        if "candles" not in data:
            return {"vol_spike": False, "last_range": 0.0}
            
        candles = data["candles"]
        ranges = []
        
        for c in candles:
            if "mid" in c and "h" in c["mid"] and "l" in c["mid"]:
                range_val = abs(float(c["mid"]["h"]) - float(c["mid"]["l"]))
                ranges.append(range_val)

        if len(ranges) < 2:
            return {"vol_spike": False, "last_range": 0.0}

        avg_range = sum(ranges[:-1]) / (len(ranges) - 1)
        last_range = ranges[-1]

        spike = last_range > 2 * avg_range if avg_range > 0 else False
        return {"vol_spike": spike, "last_range": round(last_range, 5)}
        
    except Exception as e:
        print(f"⚠️ OANDA volatility error: {e}")
        return {"vol_spike": False, "last_range": 0.0}

def fetch_volatility_coinbase(symbol="BTC-USD", interval="1m"):
    """Fetch Coinbase volatility data"""
    try:
        url = f"https://api.exchange.coinbase.com/products/{symbol}/candles?granularity=60"
        res = requests.get(url, timeout=5)
        
        if res.status_code != 200:
            return {"vol_spike": False, "last_range": 0.0}
            
        data = res.json()
        if not isinstance(data, list) or len(data) < 2:
            return {"vol_spike": False, "last_range": 0.0}

        ranges = []
        for c in data[:10]:  # Last 10 candles
            if len(c) >= 3:  # [time, low, high, open, close, volume]
                range_val = abs(float(c[2]) - float(c[1]))  # high - low
                ranges.append(range_val)

        if len(ranges) < 2:
            return {"vol_spike": False, "last_range": 0.0}

        avg_range = sum(ranges[:-1]) / (len(ranges) - 1)
        last_range = ranges[-1]
        spike = last_range > 2 * avg_range if avg_range > 0 else False
        
        return {"vol_spike": spike, "last_range": round(last_range, 2)}
        
    except Exception as e:
        print(f"⚠️ Coinbase volatility error: {e}")
        return {"vol_spike": False, "last_range": 0.0}

def is_market_safe():
    """Check if market conditions are safe for trading"""
    try:
        oanda = fetch_volatility_oanda()
        coinbase = fetch_volatility_coinbase()
        
        # Market is safe if neither platform shows volatility spikes
        safe = not oanda["vol_spike"] and not coinbase["vol_spike"]
        
        if not safe:
            print(f"🚨 Volatility spike detected - OANDA: {oanda['vol_spike']}, Coinbase: {coinbase['vol_spike']}")
        
        return safe
        
    except Exception as e:
        print(f"⚠️ Market safety check error: {e}")
        return True  # Default to safe if check fails

# Usage
if __name__ == "__main__":
    safe = is_market_safe()
    print(f"📊 Market Safety: {'✅ SAFE' if safe else '🚨 DANGEROUS'}")
