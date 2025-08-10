# generate_features.py
import os
import pandas as pd

DATA_DIR = "data/oanda"
FEATURED_SUFFIX = "_features.csv"

def add_indicators(df):
    df["returns"] = df["close"].pct_change()
    df["volatility"] = df["returns"].rolling(10).std()
    df["ma_fast"] = df["close"].rolling(window=5).mean()
    df["ma_slow"] = df["close"].rolling(window=20).mean()
    return df

for filename in os.listdir(DATA_DIR):
    if filename.endswith(FEATURED_SUFFIX):
        path = os.path.join(DATA_DIR, filename)
        try:
            df = pd.read_csv(path)
            if "close" not in df.columns:
                print(f"❌ Skipping {filename}: missing 'close'")
                continue

            df = add_indicators(df)
            df.dropna(inplace=True)
            df.to_csv(path, index=False)
            print(f"✅ Updated: {filename}")
        except Exception as e:
            print(f"⚠️ Failed on {filename}: {e}")
