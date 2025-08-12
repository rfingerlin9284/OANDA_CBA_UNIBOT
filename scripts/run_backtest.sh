#!/usr/bin/env bash
set -euo pipefail
source .env.live
PAIRS_FX=("EURUSD" "GBPUSD" "USDJPY" "USDCHF" "AUDUSD" "USDCAD"
          "EURGBP" "EURJPY" "GBPJPY" "NZDUSD" "EURCHF" "AUDJPY"
          "CHFJPY" "EURAUD" "CADJPY" "GBPCAD" "AUDCAD" "NZDJPY")
PAIRS_CRYPTO=("BTC-USD" "ETH-USD" "SOL-USD" "ADA-USD" "AVAX-USD" "DOGE-USD"
              "LTC-USD" "LINK-USD" "MATIC-USD" "XRP-USD" "DOT-USD" "BNB-USD"
              "ATOM-USD" "UNI-USD" "AAVE-USD" "SUSHI-USD" "FIL-USD" "COMP-USD")
YEARS=10
echo "🏃 Running backtests for $YEARS years..."
python3 - <<'PY'
import yfinance as yf, pandas as pd, time, json, datetime
import numpy as np
pairs_fx = """EURUSD GBPUSD USDJPY USDCHF AUDUSD USDCAD
EURGBP EURJPY GBPJPY NZDUSD EURCHF AUDJPY
CHFJPY EURAUD CADJPY GBPCAD AUDCAD NZDJPY""".split()
pairs_crypto = """BTC-USD ETH-USD SOL-USD ADA-USD AVAX-USD DOGE-USD
LTC-USD LINK-USD MATIC-USD XRP-USD DOT-USD BNB-USD
ATOM-USD UNI-USD AAVE-USD SUSHI-USD FIL-USD COMP-USD""".split()
start = (datetime.date.today() - datetime.timedelta(days=3650)).isoformat()
end   = datetime.date.today().isoformat()
def backtest(symbol):
    df = yf.download(symbol,start=start,end=end,progress=False)
    df['ret'] = df['Adj Close'].pct_change()
    # simple MA cross strategy as placeholder
    df['ma20'] = df['Adj Close'].rolling(20).mean()
    df['ma50'] = df['Adj Close'].rolling(50).mean()
    df['signal'] = np.where(df['ma20'] > df['ma50'], 1, -1)
    df['strategy'] = df['signal'].shift(1) * df['ret']
    return df[['ret','strategy']].dropna().sum().strategy
results = {}
for p in pairs_fx + pairs_crypto:
    try:
        print(f"Backtesting {p}...")
        results[p] = backtest(p)
    except Exception as e:
        results[p] = str(e)
print(json.dumps(results, indent=2))
PY
