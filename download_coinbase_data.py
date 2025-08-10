#!/usr/bin/env python3
"""
Download 1 year of historical OHLCV data for the 12 most liquid Coinbase spot crypto pairs.
Saves each pair as CSV in data/coinbase/ directory.
"""
import os
import pandas as pd
from datetime import datetime, timedelta
import ccxt

# 12 most liquid Coinbase spot pairs
COINBASE_PAIRS = [
    "BTC/USD", "ETH/USD", "USDT/USD", "SOL/USD", "XRP/USD", "ADA/USD",
    "DOGE/USD", "AVAX/USD", "LINK/USD", "LTC/USD", "BCH/USD", "MATIC/USD"
]

def fetch_coinbase_candles(exchange, symbol, timeframe, since, end):
    all_data = []
    ms_per_candle = 5 * 60 * 1000  # 5m
    while since < end:
        candles = exchange.fetch_ohlcv(symbol, timeframe, since, limit=500)
        if not candles:
            break
        for c in candles:
            if c[0] >= end:
                break
            all_data.append(c)
        since = candles[-1][0] + ms_per_candle
        if len(candles) < 500:
            break
    return all_data

def main():
    outdir = os.path.join("data", "coinbase")
    os.makedirs(outdir, exist_ok=True)
    exchange = ccxt.coinbase({'rateLimit': 1000, 'enableRateLimit': True})
    end = int(datetime.utcnow().timestamp() * 1000)
    since = int((datetime.utcnow() - timedelta(days=365)).timestamp() * 1000)
    timeframe = "5m"
    for symbol in COINBASE_PAIRS:
        print(f"Downloading {symbol}...")
        data = fetch_coinbase_candles(exchange, symbol, timeframe, since, end)
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        csv_path = os.path.join(outdir, f"{symbol.replace('/', '_')}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved {csv_path} ({len(df)} rows)")
    print("Done.")

if __name__ == "__main__":
    main()
