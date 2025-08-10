#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import joblib

MODEL_DIR = "models"
DATA_DIR = "data/historical"
LOG_DIR = "logs/replays"
os.makedirs(LOG_DIR, exist_ok=True)

def add_indicators(df):
    df["returns"] = df["close"].pct_change()
    df["rsi"] = ta.RSI(df["close"], timeperiod=14)
    df["macd"], _, _ = ta.MACD(df["close"])
    df["atr"] = ta.ATR(df["high"], df["low"], df["close"])
    df["volatility"] = df["returns"].rolling(10).std()
    df["ma_fast"] = df["close"].rolling(5).mean()
    df["ma_slow"] = df["close"].rolling(20).mean()
    df.dropna(inplace=True)
    return df

def load_model(symbol):
    model_path = os.path.join(MODEL_DIR, f"{symbol}_rf.pkl")
    return joblib.load(model_path)

def replay(symbol):
    print(f"\n🎬 SANDBOX REPLAY: {symbol}")
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    df = pd.read_csv(file_path)
    df = add_indicators(df)

    model = load_model(symbol)
    df['prediction'] = model.predict(df[['rsi', 'macd', 'atr', 'returns', 'volatility', 'ma_fast', 'ma_slow']])
    
    df['entry'] = df['prediction'].shift(1)
    df['pnl'] = df['returns'] * df['entry']
    df['cum_pnl'] = df['pnl'].cumsum()

    df[['cum_pnl']].plot(title=f"{symbol} Cumulative PnL")
    plt.savefig(os.path.join(LOG_DIR, f"{symbol}_pnl.png"))
    print(f"📊 Replay finished. Graph saved to {LOG_DIR}/{symbol}_pnl.png")

if __name__ == "__main__":
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".csv"):
            pair = filename.replace(".csv", "")
            replay(pair)
