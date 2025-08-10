#!/usr/bin/env python3
"""
Train ML models (RandomForest) for OANDA and Coinbase pairs using historical CSVs.
Features: RSI, MACD, ATR, returns, etc. Labels: 1 (up), 0 (down).
Saves models as .pkl in models/ directory.
"""
import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# ========== CONFIG ==========
DATA_DIR = 'data/historical'
MODEL_DIR = 'models'
FEATURES = ['rsi', 'macd', 'atr', 'returns', 'volatility', 'ma_fast', 'ma_slow']
RSI_PERIOD = 14
ATR_PERIOD = 14
MA_FAST = 10
MA_SLOW = 50

os.makedirs(MODEL_DIR, exist_ok=True)

def compute_features(df):
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(RSI_PERIOD).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(RSI_PERIOD).mean()
    rs = gain / (loss + 1e-9)
    df['rsi'] = 100 - (100 / (1 + rs))
    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    # ATR
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    df['atr'] = ranges.max(axis=1).rolling(ATR_PERIOD).mean()
    # Returns
    df['returns'] = df['close'].pct_change()
    # Volatility
    df['volatility'] = df['returns'].rolling(20).std()
    # Moving averages
    df['ma_fast'] = df['close'].rolling(MA_FAST).mean()
    df['ma_slow'] = df['close'].rolling(MA_SLOW).mean()
    return df

def generate_labels(df, horizon=5, threshold=0.002):
    # Label: 1 if price increases by threshold in next N days, else 0
    df['future_return'] = df['close'].shift(-horizon) / df['close'] - 1
    df['label'] = (df['future_return'] > threshold).astype(int)
    return df

def train_and_save_model(df, pair, model_dir=MODEL_DIR):
    df = df.dropna().reset_index(drop=True)
    X = df[FEATURES]
    y = df['label']
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    print(f"\n=== {pair} ===")
    
    # Save model
    model_path = os.path.join(model_dir, f"{pair}_rf.pkl")
    print("💾 Saving trained model...")
    joblib.dump(clf, model_path)
    print(f"[SAVED] {model_path}")

def process_all_pairs():
    print("🕰️ Starting full historical training...")
    csv_files = glob.glob(f"{DATA_DIR}/*.csv")
    for csv_file in csv_files:
        pair = os.path.basename(csv_file).replace('.csv', '')
        print(f"\n[PROCESSING] {pair}")
        df = pd.read_csv(csv_file)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = compute_features(df)
        df = generate_labels(df)
        train_and_save_model(df, pair)

if __name__ == "__main__":
    print("=== MODEL TRAINING START ===")
    process_all_pairs()
    print("=== MODEL TRAINING COMPLETE ===")
