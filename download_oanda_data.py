#!/usr/bin/env python3
"""
Download 1 year of historical OHLCV data for the 12 most liquid OANDA forex pairs.
Saves each pair as CSV in data/oanda/ directory.
"""
import os
import pandas as pd
from datetime import datetime, timedelta
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from credentials import WolfpackCredentials

# 12 most liquid OANDA pairs
OANDA_PAIRS = [
    "EUR_USD", "USD_JPY", "GBP_USD", "AUD_USD", "USD_CAD", "USD_CHF",
    "NZD_USD", "EUR_JPY", "GBP_JPY", "EUR_GBP", "AUD_JPY", "USD_SGD"
]

def fetch_oanda_candles(api, pair, granularity, start_time):
    """Fetch OANDA candles using count-based approach (OANDA recommended)"""
    params = {
        "from": start_time.isoformat("T") + "Z",
        "granularity": granularity,
        "price": "M",
        "count": 5000  # Max allowed count
    }
    r = instruments.InstrumentsCandles(instrument=pair, params=params)
    api.request(r)
    candles = r.response['candles']
    data = []
    for c in candles:
        if not c['complete']:
            continue
        t = pd.to_datetime(c['time'])
        o = float(c['mid']['o'])
        h = float(c['mid']['h'])
        l = float(c['mid']['l'])
        cl = float(c['mid']['c'])
        v = c['volume']
        data.append([t, o, h, l, cl, v])
    return data

def main():
    # HARDCODED OANDA CREDENTIALS (user provided)
    OANDA_API_KEY = "9f82d69b67bba8def05c99dd9b982e70-699de766b489e14f9ad9649c1a2509f3"
    OANDA_ACCOUNT_ID = "001-001-13473069-001"
    OANDA_ENVIRONMENT = "live"
    api = API(access_token=OANDA_API_KEY, environment=OANDA_ENVIRONMENT)
    outdir = os.path.join("data", "oanda")
    os.makedirs(outdir, exist_ok=True)
    
    end = datetime.utcnow()
    start = end - timedelta(days=365)
    granularity = "M5"  # 5-minute candles
    
    for pair in OANDA_PAIRS:
        print(f"Downloading {pair}...")
        all_data = []
        current_time = start
        
        # Download in chunks using count-based approach
        while current_time < end and len(all_data) < 105120:  # ~1 year of 5m candles
            chunk_data = fetch_oanda_candles(api, pair, granularity, current_time)
            if not chunk_data:
                break
                
            # Filter data within our date range
            for row in chunk_data:
                if start <= row[0] <= end:
                    all_data.append(row)
            
            # Move to next chunk - advance by last candle time + 5 minutes
            if chunk_data:
                last_time = chunk_data[-1][0]
                current_time = last_time + timedelta(minutes=5)
            else:
                break
                
            # Avoid hitting rate limits
            import time
            time.sleep(0.1)
            
        df = pd.DataFrame(all_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        csv_path = os.path.join(outdir, f"{pair}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved {csv_path} ({len(df)} rows)")
    print("Done.")

if __name__ == "__main__":
    main()
