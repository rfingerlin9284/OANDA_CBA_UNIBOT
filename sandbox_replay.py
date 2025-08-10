# ✅ Full Python script starts here (safe to paste in Bash)
import os
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

MODEL_DIR = "models"
DATA_DIR = "data/historical" 

def add_indicators(df):
    df["returns"] = df["close"].pct_change()
    df["volatility"] = df["returns"].rolling(10).std()
    df["ma_fast"] = df["close"].rolling(window=5).mean() 
    df["ma_slow"] = df["close"].rolling(window=20).mean()

    # RSI
    delta = df["close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()
    rs = avg_gain / (avg_loss + 1e-6)
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26

    # ATR
    df["H-L"] = df["high"] - df["low"]
    df["H-C"] = np.abs(df["high"] - df["close"].shift())
    df["L-C"] = np.abs(df["low"] - df["close"].shift())
    tr = df[["H-L", "H-C", "L-C"]].max(axis=1)
    df["atr"] = tr.rolling(window=14).mean()

    df.dropna(inplace=True)
    return df

def load_model(symbol):
    model_path = os.path.join(MODEL_DIR, f"{symbol}_rf.pkl")
    return joblib.load(model_path)

def replay(symbol):
    csv_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    if not os.path.exists(csv_path):
        print(f"❌ Data file not found: {csv_path}")
        return

    print(f"\n🎬 REPLAYING: {symbol}")
    df = pd.read_csv(csv_path)
    df.columns = [col.lower() for col in df.columns]
    df = add_indicators(df)

    model = load_model(symbol)
    features = ['rsi', 'returns', 'volatility', 'ma_fast', 'ma_slow', 'macd', 'atr']
    df['prediction'] = model.predict(df[features])
    df['confidence'] = model.predict_proba(df[features]).max(axis=1)

    hits = df[df['prediction'] == 1]
    accuracy = len(hits) / len(df)
    avg_conf = df['confidence'].mean()

    print(f"✅ {symbol} predictions complete.")
    print(f"📊 Accuracy (raw match %): {accuracy:.2%}")
    print(f"📈 Avg. Confidence: {avg_conf:.2%}")
    print(df[['time', 'close', 'prediction', 'confidence']].tail(10).to_string(index=False))

if __name__ == "__main__":
    symbol_list = ["ETH_USD", "BTC_USD", "LTC_USD", "MATIC_USD", "XRP_USD", "SOL_USD", "ADA_USD", "BCH_USD", "AVAX_USD", "DOT_USD"]
    for pair in symbol_list:
        try:
            replay(pair)
        except Exception as e:
            print(f"⚠️  {pair} failed: {e}")
